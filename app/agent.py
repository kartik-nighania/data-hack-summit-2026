"""Meridian support agent — the LangGraph supervisor + specialists (Module 2).

The CI gate re-runs the golden dataset against THIS code on every PR.
SABOTAGE_BREVITY simulates the Module-9 "v3" regression arriving via a pull request.

Account and policy tools are in-process (app/tools.py); the two service-desk tools
come from the MCP server in app/mcp.py, discovered over stdio at graph-build time.
The graph builds lazily on the first ainvoke_agent() call — importing this module
does no network I/O.
"""
import logging
import operator
import sys
import time
from typing import Annotated, Literal

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langfuse import propagate_attributes
from langgraph.graph import END, START, MessagesState, StateGraph
from pydantic import BaseModel, Field

from app.config import AGENT_MODEL, REPO_ROOT, get_lf, trace_url
from app.prompts import FINAL_V1, POLICY_V1, SUPERVISOR_V1

SABOTAGE_BREVITY = False   # ← the PR under review flips this to True


def set_sabotage(on: bool):
    """Flip the brevity sabotage at runtime — the notebook demo path (a PR edits the
    constant above instead). Applies on the very next request; no redeploy needed.
    NOTE: `from app.agent import SABOTAGE_BREVITY` then assigning would only rebind
    your local name — use this helper (or `app.agent.SABOTAGE_BREVITY = True`)."""
    global SABOTAGE_BREVITY
    SABOTAGE_BREVITY = on
    return SABOTAGE_BREVITY


# Our chat prompts keep a {"type": "placeholder"} message that LangChain resolves at invoke
# time (MessagesPlaceholder); mute the SDK's false-alarm warning for exactly that case.
class _MutePlaceholderFalseAlarm(logging.Filter):
    def filter(self, record):
        return "have not been resolved" not in record.getMessage()


logging.getLogger("langfuse").addFilter(_MutePlaceholderFalseAlarm())

# ── the service-desk tools live behind MCP (stdio) ───────────────────────────
SERVICE_MCP_SERVERS = {
    "meridian_service_desk": {
        "command": sys.executable,
        "args": ["-m", "app.mcp"],   # -m keeps app/mcp.py from shadowing the real `mcp` package
        "cwd": str(REPO_ROOT),
        "transport": "stdio",
    }
}


async def load_service_tools():
    """Discover create_ticket / get_ticket_status from the MCP server. The returned
    tools open a fresh stdio session per call, so they are event-loop agnostic."""
    client = MultiServerMCPClient(SERVICE_MCP_SERVERS)
    return await client.get_tools()


# ── graph ────────────────────────────────────────────────────────────────────
class SupportState(MessagesState):
    customer_id: str
    route: str
    visited: Annotated[list, operator.add]


class Route(BaseModel):
    """The supervisor's routing decision."""
    next: Literal["account", "policy", "service", "FINISH"]
    reasoning: str = Field(description="One sentence on why this route")


MAX_HOPS = 4


def _lc_chat_prompt(langfuse_prompt):
    """Langfuse chat prompt -> LangChain ChatPromptTemplate, LINKED so every generation
    made with it is tied to the exact prompt version in the trace (→ per-version metrics)."""
    tpl = ChatPromptTemplate.from_messages(langfuse_prompt.get_langchain_prompt())
    tpl.metadata = {"langfuse_prompt": langfuse_prompt}
    return tpl


def supervisor_node(state: SupportState):
    # live-fetch by label: a label move in Langfuse changes behaviour with NO redeploy
    lf = get_lf()
    p = lf.get_prompt("support-supervisor", cache_ttl_seconds=0, type="chat",
                      fallback=SUPERVISOR_V1)
    if len(state["visited"]) >= MAX_HOPS:
        return {"route": "FINISH", "visited": ["FINISH(forced)"]}
    llm = ChatOpenAI(model=p.config.get("model", AGENT_MODEL),
                     temperature=p.config.get("temperature", 0))
    chain = _lc_chat_prompt(p) | llm.with_structured_output(Route)
    decision = chain.invoke({"conversation": state["messages"]})
    return {"route": decision.next, "visited": [decision.next]}


def finalize_node(state: SupportState):
    lf = get_lf()
    p = lf.get_prompt("final-response", cache_ttl_seconds=0, type="chat", fallback=FINAL_V1)
    tpl = _lc_chat_prompt(p)
    if SABOTAGE_BREVITY:  # ← the "innocent" PR change the gate must catch (the Module-9 v3 prompt)
        tpl = ChatPromptTemplate.from_messages(
            [("system", "You write the final reply to the customer for Meridian Housing Finance.\n"
                        "CRITICAL STYLE RULE: reply in ONE short friendly sentence (maximum ~20 words). "
                        "Do not include long numbers, ids, or lists - keep it brief, warm and reassuring. "
                        "Customers love short answers.")]
            + p.get_langchain_prompt()[1:-1]
            + [("user", "Now write the single final reply to the customer.")]
        )
    llm = ChatOpenAI(model=p.config.get("model", AGENT_MODEL),
                     temperature=p.config.get("temperature", 0.3))
    return {"messages": [(tpl | llm).invoke({"conversation": state["messages"]})]}


async def deploy_agent():
    """Build the compiled graph, baking in the CURRENT production prompts for the specialists
    (like a service deploy). The supervisor & finalize prompts are live-fetched per request.
    Async because the service tools are discovered from the MCP server at deploy time."""
    from app.tools import ACCOUNT_TOOLS, POLICY_TOOLS

    lf = get_lf()
    policy_prompt = lf.get_prompt("policy-agent", cache_ttl_seconds=0, fallback=POLICY_V1)
    service_tools = await load_service_tools()
    account = create_agent(model=AGENT_MODEL, tools=ACCOUNT_TOOLS, name="account_agent",
                           system_prompt=("You are Meridian's loan-account specialist. Use your tools to fetch "
                                          "facts for the customer id given in the conversation. Report numbers exactly."))
    policy = create_agent(model=AGENT_MODEL, tools=POLICY_TOOLS, name="policy_agent",
                          system_prompt=policy_prompt.prompt)
    service = create_agent(model=AGENT_MODEL, tools=service_tools, name="service_agent",
                           system_prompt=("You are Meridian's service-request specialist. Raise tickets and check "
                                          "their status using your tools for the customer id in the conversation."))
    g = StateGraph(SupportState)
    g.add_node("supervisor", supervisor_node)
    g.add_node("account_agent", account)
    g.add_node("policy_agent", policy)
    g.add_node("service_agent", service)
    g.add_node("finalize", finalize_node)
    g.add_edge(START, "supervisor")
    g.add_conditional_edges("supervisor", lambda s: s["route"],
                            {"account": "account_agent", "policy": "policy_agent",
                             "service": "service_agent", "FINISH": "finalize"})
    for worker in ["account_agent", "policy_agent", "service_agent"]:
        g.add_edge(worker, "supervisor")
    g.add_edge("finalize", END)
    return g.compile()


_AGENT_GRAPH = None


async def get_agent():
    """The cached compiled graph — deployed on first use."""
    global _AGENT_GRAPH
    if _AGENT_GRAPH is None:
        _AGENT_GRAPH = await deploy_agent()
    return _AGENT_GRAPH


async def redeploy_agent():
    """Rebuild the cached graph — call after promoting a new specialist prompt (a 'deploy')."""
    global _AGENT_GRAPH
    _AGENT_GRAPH = await deploy_agent()
    return _AGENT_GRAPH


# ── Invocation layer + extraction of tool calls / retrievals / route ─────────
def _package(result: dict, question: str, customer_id: str) -> dict:
    """Turn the raw graph result into the structure every evaluator will consume."""
    msgs = result["messages"]
    tool_calls, outputs_by_id = [], {}
    for m in msgs:
        if isinstance(m, ToolMessage):
            outputs_by_id[m.tool_call_id] = str(m.content)
    for m in msgs:
        if isinstance(m, AIMessage) and m.tool_calls:
            for tc in m.tool_calls:
                tool_calls.append({"name": tc["name"], "args": tc.get("args", {}),
                                   "output": outputs_by_id.get(tc.get("id"), "")[:600]})
    retrieved = []
    for tc in tool_calls:
        if tc["name"] == "search_policy_kb" and tc["output"]:
            retrieved.extend([c.strip() for c in tc["output"].split("\n---\n") if c.strip()])
    return {
        "question": question,
        "customer_id": customer_id,
        "answer": msgs[-1].content if msgs else "",
        "route": [v for v in result.get("visited", []) if v not in ("FINISH", "FINISH(forced)")],
        "tool_calls": tool_calls,
        "retrieved": retrieved,
        "n_messages": len(msgs),
    }


def _graph_input(question: str, customer_id: str, history=None):
    msgs = list(history or [])
    msgs.append(HumanMessage(content=f"{question}\n\n(authenticated customer_id: {customer_id})"))
    return {"messages": msgs, "customer_id": customer_id, "route": "", "visited": []}


async def ainvoke_agent(question: str, customer_id: str, history=None, callbacks=None) -> dict:
    from langfuse.langchain import CallbackHandler
    graph = await get_agent()
    result = await graph.ainvoke(
        _graph_input(question, customer_id, history),
        config={"callbacks": callbacks or [CallbackHandler()], "recursion_limit": 25},
    )
    return _package(result, question, customer_id)


async def run_agent(question: str, customer_id: str, *, user_id=None, session_id=None,
                    tags=None, environment=None, version=None, trace_seed=None, history=None) -> dict:
    """The production entry point (async port of notebook cell 4.x run_agent):
       root 'agent' span (trace input/output) + propagate_attributes (user/session/tags/env/version)
       + LangChain CallbackHandler + a predictable trace_id we can attach scores to later."""
    lf = get_lf()
    trace_context = None
    if trace_seed:
        trace_context = {"trace_id": lf.create_trace_id(seed=trace_seed)}
    t0 = time.time()
    with lf.start_as_current_observation(as_type="agent", name="meridian-support-agent",
                                         input={"question": question, "customer_id": customer_id},
                                         trace_context=trace_context) as root:
        trace_id = lf.get_current_trace_id()
        with propagate_attributes(
            trace_name="meridian-support-agent",
            user_id=user_id or customer_id,                  # user-level views key off this
            session_id=session_id,                           # = the conversation / LangGraph thread id
            tags=tags or [],
            environment=environment,                         # None → client default ('development')
            version=version,
            metadata={"thread_id": session_id or "", "app": "meridian-support"},
        ):
            pkg = await ainvoke_agent(question, customer_id, history=history)
        root.update(output={"answer": pkg["answer"], "route": pkg["route"]})
    pkg.update({"trace_id": trace_id, "latency_s": round(time.time() - t0, 2),
                "url": trace_url(trace_id)})
    return pkg
