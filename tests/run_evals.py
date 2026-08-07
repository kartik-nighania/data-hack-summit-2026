"""Module 10 — CI/CD quality gate for the Meridian support agent.

Re-runs the golden dataset (`meridian-golden-v1`) against the agent in app/agent.py
and blocks the merge (RegressionError) when any run-level aggregate falls below its
threshold. Same logic as notebook cell 10.1, packaged for two entry points:

1. GitHub Actions — `langfuse/experiment-action` calls `experiment(context)`
   (wired up in .github/workflows/eval-gate.yml). The action loads the dataset,
   stamps commit/branch metadata, posts the score table on the PR, and fails the
   check on RegressionError.

2. Local sanity run — `python tests/run_evals.py [run_name]`
   reads keys from .env / environment.

The gate set is versioned by NAME, not timestamp: `meridian-golden-v1` is frozen —
nothing writes to it after seeding (promoted production failures land in the
candidates dataset), so fetching it latest always returns the same 22 items.

Thresholds live in tests/quality_threshold.json so PMs can tune the bar without
touching code (and the gate itself re-runs when they do, since it's still a PR).

Prerequisite either way: the Langfuse project holds the `meridian-golden-v1` dataset
and the three agent prompts — seed them with app.prompts.seed_prompts() and
app.golden.seed_dataset() (or by running the notebooks through Module 6).
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from langfuse import Evaluation, RegressionError

from app.config import DATASET_NAME, EXPERIMENT_CONCURRENCY, get_lf
from app.agent import ainvoke_agent
from app.evaluators import RULE_EVALUATORS, make_run_evaluator

MAX_CONCURRENCY = EXPERIMENT_CONCURRENCY

# Gate on aggregates with margin: deterministic rules only, so the gate is cheap and
# stable. A single flaky item can't block a release; a real regression (e.g. the
# SABOTAGE_BREVITY prompt tweak) drags the averages under and fails the check.
_GATE_CONFIG = json.loads(Path(__file__).with_name("quality_threshold.json").read_text())
GATE_THRESHOLDS = _GATE_CONFIG["thresholds"]
MIN_ITEMS = _GATE_CONFIG["min_items_completed"]   # fewer completed items means task errors, not quality


# ── task: one dataset item -> one agent execution ────────────────────────────
async def golden_task(*, item, **kwargs):
    """Runs inside the experiment's trace context, so all LangGraph spans nest
    under the item's trace automatically."""
    return await ainvoke_agent(item.input["question"], item.input["customer_id"])


def run_items_completed(*, item_results, **kw):
    return Evaluation(name="items_completed", value=len(item_results),
                      comment=f"{len(item_results)}/{MIN_ITEMS} items executed without task errors")


RUN_EVALUATORS = [make_run_evaluator(m.replace("avg_", "")) for m in GATE_THRESHOLDS]
RUN_EVALUATORS.append(run_items_completed)


# ── the gate ─────────────────────────────────────────────────────────────────
def enforce_thresholds(result, thresholds=GATE_THRESHOLDS):
    """Raise RegressionError on the first aggregate below its threshold."""
    completed = len(result.item_results)
    if completed < MIN_ITEMS:
        raise RegressionError(result=result, metric="items_completed",
                              value=float(completed), threshold=float(MIN_ITEMS))
    aggregates = {e.name: e.value for e in result.run_evaluations if e.value is not None}
    print("gate aggregates:", {k: round(v, 3) for k, v in aggregates.items()
                               if isinstance(v, (int, float))})
    for metric, threshold in thresholds.items():
        value = aggregates.get(metric)
        if not isinstance(value, (int, float)) or value < threshold:
            raise RegressionError(result=result, metric=metric,
                                  value=float(value) if isinstance(value, (int, float)) else 0.0,
                                  threshold=threshold)
    return result


def experiment(context):
    """Entrypoint for langfuse/experiment-action: the action supplies the dataset
    (name + pinned version from the workflow inputs) and CI metadata via context."""
    result = context.run_experiment(
        name="ci-quality-gate",
        description="PR merge gate: rule-based evaluators on the pinned golden dataset",
        task=golden_task,
        evaluators=RULE_EVALUATORS,
        run_evaluators=RUN_EVALUATORS,
        max_concurrency=MAX_CONCURRENCY,
    )
    return enforce_thresholds(result)


# ── local runner ─────────────────────────────────────────────────────────────
def main():
    from datetime import datetime, timezone

    lf = get_lf()
    dataset = lf.get_dataset(DATASET_NAME)          # frozen by convention → latest == the 22-item v1 set

    run_name = sys.argv[1] if len(sys.argv) > 1 else \
        f"local-gate-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}"
    result = dataset.run_experiment(
        name="ci-quality-gate",
        run_name=run_name,
        description="local quality-gate run on the frozen v1 set",
        task=golden_task,
        evaluators=RULE_EVALUATORS,
        run_evaluators=RUN_EVALUATORS,
        max_concurrency=MAX_CONCURRENCY,
    )
    lf.flush()
    try:
        enforce_thresholds(result)
    except RegressionError as e:
        print(f"⛔ MERGE BLOCKED — RegressionError: {e.metric} = {e.value:.3f} < threshold {e.threshold}")
        sys.exit(1)
    print(f"✅ GATE PASSED — '{run_name}' may merge.")
    print("🔗 run in the UI:", result.dataset_run_url)


if __name__ == "__main__":
    main()
