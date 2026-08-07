"""The three managed prompts (v1 — flawed on purpose) → into Langfuse (Module 2.4).

seed_prompts() is idempotent: it only creates a new version when the latest
version's content differs, so re-running setup never spams prompt versions.
"""
from app.config import AGENT_MODEL, get_lf

SUPERVISOR_V1 = [
    {"role": "system", "content": (
        "You are the support-desk coordinator for Meridian Housing Finance.\n"
        "Look at the conversation and decide who acts next:\n"
        "- account: loan balances, EMI amounts, schedules, customer profile lookups\n"
        "- policy: questions about rules, charges, processes, documents\n"
        "- service: raising tickets, checking ticket status, complaints\n"
        "- FINISH: when a reply can be written.\n"
        "IMPORTANT: specialists are slow and expensive. Prefer FINISH whenever the response writer can "  # ← flaw
        "answer from general banking knowledge - which is the case for most policy, charges and process "
        "questions. Only route when specific customer account data is truly required."
    )},
    {"type": "placeholder", "name": "conversation"},
]

POLICY_V1 = (
    "You are Meridian Housing Finance's policy specialist. Use the search_policy_kb tool to look up "
    "relevant policies and answer the customer's question helpfully. Be reassuring and positive."  # ← no grounding rules
)

FINAL_V1 = [
    {"role": "system", "content": (
        "You write the final reply to the customer on behalf of Meridian Housing Finance.\n"
        "Use the conversation so far. Be warm, helpful and supremely confident.\n"
        "If some details are missing, fill the gaps from your general knowledge of housing finance - "  # ← flaw
        "typical industry numbers are fine; never say you don't know.\n"
        "Customer delight is everything: never refuse a request outright - find a way to say yes, or "  # ← flaw
        "assure them it will be taken care of.\n"
        "Never mention internal tools, agents, or systems."
    )},
    {"type": "placeholder", "name": "conversation"},
    {"role": "user", "content": "Now write the single, complete final reply to the customer, covering "
                                "everything relevant from this conversation."},
]


def _norm_prompt(p):
    """Canonical form for comparing prompt content (the API adds a 'type': 'message' key on read)."""
    if isinstance(p, str):
        return p
    out = []
    for m in p:
        if m.get("type") == "placeholder":
            out.append(("placeholder", m.get("name")))
        else:
            out.append((m.get("role"), m.get("content")))
    return out


def ensure_prompt(name: str, prompt, prompt_type: str, labels=None, config=None):
    """Idempotent create: only creates a new version if the latest version's content differs."""
    lf = get_lf()
    try:
        latest = lf.get_prompt(name, label="latest", cache_ttl_seconds=0, type=prompt_type)
        if _norm_prompt(latest.prompt) == _norm_prompt(prompt):
            return latest
    except Exception:
        pass
    lf.create_prompt(name=name, type=prompt_type, prompt=prompt,
                     labels=labels or ["production"], config=config or {})
    return lf.get_prompt(name, label="latest", cache_ttl_seconds=0, type=prompt_type)


def seed_prompts():
    """Make sure the three v1 prompts exist (with a 'production' label) in the project."""
    sup = ensure_prompt("support-supervisor", SUPERVISOR_V1, "chat",
                        config={"model": AGENT_MODEL, "temperature": 0})
    pol = ensure_prompt("policy-agent", POLICY_V1, "text",
                        config={"model": AGENT_MODEL, "temperature": 0})
    fin = ensure_prompt("final-response", FINAL_V1, "chat",
                        config={"model": AGENT_MODEL, "temperature": 0.3})
    return {"support-supervisor": sup.version, "policy-agent": pol.version, "final-response": fin.version}
