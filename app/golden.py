"""The golden test set (Module 6.1): 22 items across 5 categories, loaded from
data/golden_items.json.

Versioning by fixed names, not timestamps: `meridian-golden-v1` is the FROZEN gate
set — seeding is idempotent (fixed item ids) and nothing else ever writes to it, so
fetching it "latest" always returns the same 22 items. Production failures are
promoted into the separate candidates dataset (Module 7.5) instead.
"""
import json

from app.config import CANDIDATES_DATASET_NAME, DATA_DIR, DATASET_NAME, get_lf

GOLDEN_ITEMS = json.loads((DATA_DIR / "golden_items.json").read_text())


def seed_dataset():
    """Ensure the dataset + its 22 items exist (get-or-create — re-running never duplicates)."""
    lf = get_lf()
    try:
        dataset = lf.get_dataset(DATASET_NAME)
        existing = {i.id for i in dataset.items}
    except Exception:
        lf.create_dataset(
            name=DATASET_NAME,
            description="Golden test set for the Meridian support agent (22 items, 5 categories) — FROZEN",
            metadata={"owner": "workshop", "schema": "input:{question,customer_id} / expected:{reference,must_mention}"},
        )
        existing = set()

    for g in [g for g in GOLDEN_ITEMS if g["id"] not in existing]:
        lf.create_dataset_item(
            dataset_name=DATASET_NAME,
            id=g["id"],                                   # fixed id → re-running upserts, never duplicates
            input={"question": g["question"], "customer_id": g["customer_id"]},
            expected_output={"reference": g["reference"], "must_mention": g["must_mention"],
                             "expected_route": g["expected_route"], "expected_tools": g["expected_tools"]},
            metadata={"category": g["category"], "difficulty": g["difficulty"],
                      "policy_refs": g.get("policy_refs", [])},
        )
    lf.flush()
    return lf.get_dataset(DATASET_NAME)


def ensure_candidates_dataset():
    """Get-or-create the staging dataset where production failures are promoted —
    keeps the frozen v1 gate set untouched until items are reviewed and authored."""
    lf = get_lf()
    try:
        lf.get_dataset(CANDIDATES_DATASET_NAME)
    except Exception:
        lf.create_dataset(
            name=CANDIDATES_DATASET_NAME,
            description="Promoted production failures awaiting review → the future golden-v2",
            metadata={"owner": "workshop"},
        )
    return CANDIDATES_DATASET_NAME
