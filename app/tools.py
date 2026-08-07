"""In-process tools (the specialists' hands): the account specialist's lookups and
the policy retriever.

The two service-desk tools (create_ticket / get_ticket_status) are NOT here —
they run behind the MCP server in app/mcp.py and the agent discovers them over
stdio at deploy time (see app/agent.py).
"""
import json
import math
import random
import re
import time
from collections import Counter
from datetime import datetime, timedelta

from langchain.tools import tool

from app.config import get_lf
from app.mcp import CUSTOMERS, LOANS, POLICY_KB

FLAKY_MODE = {"on": False, "fail_rate": 0.6}   # module 4 flips this on for the timeout/retry demo
_flaky_rng = random.Random(7)


class TfidfRetriever:
    def __init__(self, docs: dict):
        self.ids = list(docs)
        self.tokenized = {i: self._tok(docs[i]) for i in self.ids}
        self.df = Counter(t for toks in self.tokenized.values() for t in set(toks))
        self.n = len(self.ids)

    @staticmethod
    def _tok(text):
        return re.findall(r"[a-z0-9%]+", text.lower())

    def _vec(self, toks):
        tf = Counter(toks)
        return {t: (1 + math.log(c)) * math.log(1 + self.n / (1 + self.df.get(t, 0))) for t, c in tf.items()}

    def search(self, query: str, k: int = 3):
        qv = self._vec(self._tok(query))
        scores = {}
        for i in self.ids:
            dv = self._vec(self.tokenized[i])
            dot = sum(qv[t] * dv.get(t, 0) for t in qv)
            norm = math.sqrt(sum(v * v for v in qv.values())) * math.sqrt(sum(v * v for v in dv.values()))
            scores[i] = dot / norm if norm else 0.0
        top = sorted(scores, key=scores.get, reverse=True)[:k]
        return [(i, round(scores[i], 3), POLICY_KB[i]) for i in top]


retriever = TfidfRetriever(POLICY_KB)


@tool
def get_customer(customer_id: str) -> str:
    """Look up a customer's profile (name, contact details, PAN, loan accounts) by customer id."""
    c = CUSTOMERS.get(customer_id)
    if not c:
        return f"ERROR: no customer with id {customer_id}"
    return json.dumps({"customer_id": customer_id, **c})


@tool
def get_loan_summary(loan_id: str) -> str:
    """Get a loan's summary: outstanding balance, interest rate and type, EMI amount, due day, remaining tenure."""
    l = LOANS.get(loan_id)
    if not l:
        return f"ERROR: no loan with id {loan_id}"
    return json.dumps({"loan_id": loan_id, **l})


def _fetch_emi_schedule(loan_id: str) -> str:
    """Simulated core-banking call - times out sometimes when FLAKY_MODE is on (module 4)."""
    l = LOANS.get(loan_id)
    if not l or l["status"] != "active":
        return f"ERROR: no active loan with id {loan_id}"
    if FLAKY_MODE["on"] and _flaky_rng.random() < FLAKY_MODE["fail_rate"]:
        time.sleep(1.0)
        raise TimeoutError("core-banking EMI service timed out after 1000ms")
    rows, outstanding = [], l["outstanding"]
    base = datetime(2026, 8, l["due_day"])
    for m in range(3):
        interest = round(outstanding * l["rate_pct"] / 100 / 12)
        principal = l["emi"] - interest
        rows.append({"due_date": (base + timedelta(days=31 * m)).strftime("%Y-%m-%d"),
                     "emi": l["emi"], "interest_part": interest, "principal_part": principal})
        outstanding -= principal
    return json.dumps({"loan_id": loan_id, "next_installments": rows})


@tool
def get_emi_schedule(loan_id: str) -> str:
    """Get the next 3 EMI installments for a loan with the principal/interest split of each."""
    # Timeout-and-retry made VISIBLE: each attempt is its own span; failures carry level=ERROR.
    lf = get_lf()
    for attempt in (1, 2, 3):
        with lf.start_as_current_observation(as_type="span", name=f"emi-fetch-attempt-{attempt}",
                                             input={"loan_id": loan_id}) as sp:
            try:
                data = _fetch_emi_schedule(loan_id)
                sp.update(output="ok")
                return data
            except TimeoutError as e:
                sp.update(level="ERROR", status_message=str(e), output={"error": str(e)})
                if attempt == 3:
                    return "ERROR: EMI service unavailable after 3 attempts - please try again later"
                time.sleep(0.4 * attempt)   # backoff before retrying


@tool
def search_policy_kb(query: str) -> str:
    """Search Meridian's policy knowledge base. Returns the top-3 policy clauses for the query."""
    # We wrap the retrieval in a dedicated 'retriever' observation so retrievals are
    # first-class citizens in the trace - filterable, chartable, and scorable on their own.
    lf = get_lf()
    with lf.start_as_current_observation(as_type="retriever", name="policy-kb-retriever",
                                         input={"query": query, "top_k": 3}) as ret:
        hits = retriever.search(query, k=3)
        chunks = [f"[{pid}] {text}" for pid, _score, text in hits]
        ret.update(output={"chunks": chunks, "scores": {pid: s for pid, s, _ in hits}})
    return "\n---\n".join(chunks)


ACCOUNT_TOOLS = [get_customer, get_loan_summary, get_emi_schedule]
POLICY_TOOLS = [search_policy_kb]
