"""User-feedback capture (Module 5): a standardized rating schema (score config)
+ the helper your app's feedback endpoint would call."""
from app.config import get_lf

_CSAT_CONFIG = None


def ensure_score_config(name, **kwargs):
    """Score configs pin the schema (type, range/categories) so every producer stays consistent."""
    lf = get_lf()
    existing = lf.api.score_configs.get(page=1, limit=100)
    for c in existing.data:
        if c.name == name:
            return c
    return lf.api.score_configs.create(name=name, **kwargs)


def csat_config():
    global _CSAT_CONFIG
    if _CSAT_CONFIG is None:
        _CSAT_CONFIG = ensure_score_config(
            "csat", data_type="CATEGORICAL",
            categories=[{"label": "1-very-bad", "value": 1}, {"label": "2-bad", "value": 2},
                        {"label": "3-neutral", "value": 3}, {"label": "4-good", "value": 4},
                        {"label": "5-excellent", "value": 5}],
            description="Post-chat customer satisfaction rating (1-5)",
        )
    return _CSAT_CONFIG


def record_feedback(request_id: str, thumbs_up: bool, comment: str = "", csat: str | None = None,
                    environment: str | None = None):
    """What YOUR app's feedback endpoint would do. Note: no trace object needed —
    the trace id is re-derived from the request id. Pass environment so the score
    lands in the same environment as its trace (dev scores ≠ prod scores!)."""
    lf = get_lf()
    trace_id = lf.create_trace_id(seed=request_id)
    lf.create_score(trace_id=trace_id, name="user-feedback", value=1 if thumbs_up else 0,
                    data_type="BOOLEAN", comment=comment, environment=environment,
                    score_id=f"user-feedback-{trace_id}")          # idempotent: re-votes overwrite
    if csat:
        lf.create_score(trace_id=trace_id, name="csat", value=csat,
                        data_type="CATEGORICAL", config_id=csat_config().id,
                        environment=environment, score_id=f"csat-{trace_id}")
    lf.flush()
    return trace_id
