"""The online-evaluation job (Module 7.3): reference-free scoring of live production
traffic — trace-level resolution confidence, a BOOLEAN escalation flag, and a
component-level retrieval score attached to the retriever observation.

Notebook 04 teaches this inline; notebook 05 (the incident) imports it from here.
In real life this function runs on a schedule (cron / GitHub Actions / Cloud Function).
"""
import asyncio
from datetime import datetime, timedelta, timezone

from deepeval.metrics import ContextualRelevancyMetric
from deepeval.test_case import LLMTestCase
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from app.config import JUDGE_MODEL, get_lf
from app.judges import _measure, _mk, _track_judge


class ResolutionVerdict(BaseModel):
    resolved: float = Field(ge=0, le=1, description="1.0 = fully resolved, professional, safe")
    reasoning: str


_RES_SYS = ("You review a housing-finance support reply WITHOUT knowing the correct answer. "
            "Score how well it RESOLVES the question. Anchors: 1.0 = contains the specific facts the "
            "question needs (amounts, dates, charges, document names, ticket ids) plus a clear next step; "
            "0.5 = addresses the topic but is missing some specifics; 0.3 or BELOW = vague reassurance "
            "with NO concrete figures, ids or steps ('it is all sorted, do not worry') - however friendly. "
            "Also penalize to 0.2 any rate promises or other customers' data. Judge substance, not length.")


async def score_recent_production(minutes_back=30, sample=12, since=None):
    """The 'online evaluation job' you would run on a schedule: pull recent prod traces,
    attach reference-free scores at TRACE level and component scores at OBSERVATION level."""
    lf = get_lf()
    since = since or (datetime.now(timezone.utc) - timedelta(minutes=minutes_back))  # SDK expects datetimes
    page = lf.api.trace.list(environment=["production"], from_timestamp=since, limit=50, page=1)
    traces = [t for t in page.data if t.name == "meridian-support-agent"][:sample]
    llm = ChatOpenAI(model=JUDGE_MODEL, temperature=0)
    scored = 0
    for t in traces:
        q = (t.input or {}).get("question", "") if isinstance(t.input, dict) else str(t.input)
        a = (t.output or {}).get("answer", "") if isinstance(t.output, dict) else str(t.output)
        out = await llm.with_structured_output(ResolutionVerdict, include_raw=True).ainvoke(
            [("system", _RES_SYS), ("user", f"QUESTION:\n{q}\n\nREPLY:\n{a}")])
        _track_judge(out["raw"]); v = out["parsed"]
        lf.create_score(trace_id=t.id, name="resolution_conf", value=round(v.resolved, 3),
                        comment=v.reasoning, environment="production")   # trace-level, reference-FREE
        obs = lf.api.observations.get_many(trace_id=t.id, limit=100)
        # Ticket found score
        ticket = any(o.name == "create_ticket" for o in obs.data)
        lf.create_score(trace_id=t.id, name="escalated", value=ticket, data_type="BOOLEAN",
                        comment="a service ticket was created in this conversation",
                        environment="production")
        retr = next((o for o in obs.data if o.name == "policy-kb-retriever"), None)
        if retr and a:
            rq = (retr.input or {}).get("query") if isinstance(retr.input, dict) else str(retr.input)
            chunks = (retr.output or {}).get("chunks") if isinstance(retr.output, dict) else None
            if rq and chunks:
                m = await asyncio.to_thread(_measure, _mk(ContextualRelevancyMetric),
                                            LLMTestCase(input=rq, actual_output=a, retrieval_context=chunks))
                lf.create_score(trace_id=t.id, observation_id=retr.id,          # ← OBSERVATION-level
                                name="retrieval_relevancy", value=round(m.score, 3),
                                comment=str(m.reason)[:300], environment="production")
        scored += 1
    lf.flush()
    return scored
