"""Judge bookkeeping + the DeepEval bridge helpers (Modules 6.4/6.5).

Notebook 03 teaches these inline; notebook 04 and app/online_eval.py import them
from here. JUDGE_USAGE tracks token spend across every judge call in the process
so eval economics stay visible.
"""
from app.config import JUDGE_MODEL

JUDGE_USAGE = {"input_tokens": 0, "output_tokens": 0, "calls": 0}
_PRICE_PER_M = {"gpt-4.1-mini": (0.40, 1.60), "gpt-4o-mini": (0.15, 0.60)}


def _track_judge(raw_msg):
    u = getattr(raw_msg, "usage_metadata", None) or {}
    JUDGE_USAGE["input_tokens"] += u.get("input_tokens", 0)
    JUDGE_USAGE["output_tokens"] += u.get("output_tokens", 0)
    JUDGE_USAGE["calls"] += 1


def judge_cost_usd():
    pin, pout = _PRICE_PER_M.get(JUDGE_MODEL, (0.40, 1.60))
    return JUDGE_USAGE["input_tokens"] / 1e6 * pin + JUDGE_USAGE["output_tokens"] / 1e6 * pout


# ── DeepEval bridge: LangGraph run → LLMTestCase, metric → measured metric ───
def _mk(metric_cls, **kwargs):
    return metric_cls(model=JUDGE_MODEL, async_mode=False, verbose_mode=False, **kwargs)


def _measure(metric, tc):
    try:
        metric.measure(tc, _show_indicator=False)
    except TypeError:
        metric.measure(tc)
    return metric
