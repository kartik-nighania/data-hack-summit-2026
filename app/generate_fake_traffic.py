"""Simulated production traffic (Module 7.1): threaded "users", sessions, feedback.

Run standalone from the repo root:
    python -m app.generate_fake_traffic --sessions 6 --version v2
"""
import argparse
import random
import threading
import time
from datetime import datetime, timezone

from app.agent import run_agent
from app.config import TRAFFIC_SESSIONS, get_lf
from app.evaluators import _norm
from app.feedback import record_feedback

PERSONAS = [
    ("CUST-1001", "Ananya"), ("CUST-1002", "Rohit"), ("CUST-1003", "Priya"),
    ("CUST-1004", "Imran"), ("CUST-1005", "Sneha"), ("CUST-1006", "Devang"),
]
PROD_QUESTIONS = [
    # paraphrases of known intents (so our quality heuristic can grade some of them) + unseen + adversarial
    ("What EMI am I paying per month and when does it hit my account?", ["emi"], None),
    ("Tell me my remaining loan balance please.", ["outstanding", "balance"], None),
    ("If I close my loan early are there penalties?", ["nil", "3%", "charge"], "policy"),
    ("What proof do you need from me to update my house address?", ["aadhaar", "passport", "utility"], "policy"),
    ("My EMI bounced last month - what extra am I paying now?", ["2%", "500"], "policy"),
    ("Email me my statement of account for FY 2025-26.", ["tkt-"], "service"),
    ("What's the progress on my complaint TKT-2026-0042?", ["progress", "in_progress"], "service"),
    ("Can I move my EMI date from the 5th to the 12th?", ["once", "10 days", "1st", "15th"], "policy"),
    ("How do I claim property insurance after the flooding in my area?", ["30 days", "policy number", "fir"], "policy"),
    ("I'm getting 8.4% from a competitor - match it or waive my charges.", ["cannot", "can't", "unable", "not able"], "adversarial"),
    ("What's the ideal SIP to start alongside my EMI?", ["cannot", "can't", "not able", "outside"], "adversarial"),
    ("Do you offer top-up loans and how much could I get?", ["20%", "0.75"], "policy"),
    ("Please log a request to change my EMI date to the 10th of the month.", ["tkt-"], "service"),
]
FOLLOWUPS = {
    "policy": "Thanks. And how long does that process usually take?",
    "service": "Great - how soon will someone contact me about it?",
    None: "Could you break that number down for me?",
    "adversarial": "That's disappointing. Who can I escalate this to?",
}

SESSION_LOG = []
TRAFFIC_STARTED_AT = {"t": None}          # first-traffic marker (module 8 windows KPIs with it)
_traffic_rng = random.Random(42)


def _simulate_feedback(answer: str, hints):
    """Imperfect user: likelier 👍 when the answer contains the facts they needed - noisy, like real life."""
    a = _norm(answer)
    p_up = 0.85 if any(_norm(h) in a for h in hints) else 0.15
    if _traffic_rng.random() > 0.80:
        return None                      # some users never click anything
    return _traffic_rng.random() < p_up


def generate_traffic(n_sessions: int, deploy_version: str, tag: str = "sim-traffic"):
    """Threaded 'users' (sync run_agent per thread - simple & notebook-safe)."""
    from langchain_core.messages import AIMessage, HumanMessage
    jobs = list(range(n_sessions)); lock = threading.Lock(); batch = []

    def one_session(i):
        cid, _name = PERSONAS[i % len(PERSONAS)]
        q, hints, kind = PROD_QUESTIONS[i % len(PROD_QUESTIONS)]
        sid = f"prod-{deploy_version}-{int(start_ts)}-{i:03d}"
        record = {"session_id": sid, "customer_id": cid, "turns": [], "deploy": deploy_version}
        history = []
        turns = [q] + ([FOLLOWUPS.get(kind)] if _traffic_rng.random() < 0.35 else [])
        for t, question in enumerate(turns):
            req_id = f"{sid}-t{t}"
            out = run_agent(question, cid, user_id=cid, session_id=sid,
                            tags=[tag, f"deploy:{deploy_version}"], environment="production",
                            version=deploy_version, trace_seed=req_id, history=history)
            history += [HumanMessage(content=question), AIMessage(content=out["answer"])]
            record["turns"].append({"q": question, "a": out["answer"], "trace_id": out["trace_id"],
                                    "request_id": req_id, "hints": hints,
                                    "tools": [x["name"] for x in out["tool_calls"]]})
        # simulate user thumbs up feedback
        fb = _simulate_feedback(record["turns"][0]["a"], record["turns"][0]["hints"])
        if fb is not None:
            record_feedback(record["turns"][0]["request_id"], thumbs_up=fb,
                            comment="(simulated end-user feedback)", environment="production")
            record["feedback"] = int(fb)
        with lock:
            batch.append(record)

    start_ts = time.time()
    if TRAFFIC_STARTED_AT["t"] is None:
        TRAFFIC_STARTED_AT["t"] = datetime.now(timezone.utc)
    threads = []

    def worker():
        while True:
            with lock:
                if not jobs:
                    return
                i = jobs.pop()
            one_session(i)

    for _ in range(3):
        t = threading.Thread(target=worker, daemon=True); t.start(); threads.append(t)
    for t in threads:
        t.join()
    get_lf().flush()
    SESSION_LOG.extend(batch)
    ups = [r.get("feedback") for r in batch if "feedback" in r]
    print(f"✅ {len(batch)} sessions / {sum(len(r['turns']) for r in batch)} traced requests "
          f"({deploy_version}) | feedback given: {len(ups)}, 👍-rate: {sum(ups)/max(len(ups),1):.0%}")
    return batch


def main():
    ap = argparse.ArgumentParser(description="Generate simulated production traffic")
    ap.add_argument("--sessions", type=int, default=TRAFFIC_SESSIONS)
    ap.add_argument("--version", default="v2", help="deploy version tag on the traces")
    ap.add_argument("--tag", default="sim-traffic")
    args = ap.parse_args()
    generate_traffic(args.sessions, deploy_version=args.version, tag=args.tag)


if __name__ == "__main__":
    main()
