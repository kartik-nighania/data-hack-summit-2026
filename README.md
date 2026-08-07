# Monitoring & Evaluating Agentic AI in Production with Langfuse

A 4-hour hands-on workshop: build a multi-agent support desk with **LangGraph**, then wrap the
full production loop around it with **Langfuse** — tracing → prompt management → user feedback →
evaluation (rules, LLM-as-a-Judge, **DeepEval**) → online evals → dashboards → monitoring/alerting
→ a CI/CD quality gate that blocks bad merges.

The running example is the **Meridian Housing Finance support agent**: a supervisor routing
between account, policy, and service specialists over a mock loan-servicing world. The two
service-desk tools run behind an **MCP server** (FastMCP over stdio) that the agent discovers
at deploy time.

## Repo layout

| Path | What |
| --- | --- |
| `workshop/00…05_*.ipynb` | **The six module notebooks** (see map below) — each bootstraps itself, so a fresh Colab session resumes in minutes |
| `workshop/agentOps_workshop.ipynb` | The original single-notebook version (kept as reference until the split is battle-tested) |
| `app/` | The reusable package the notebooks import (see module table) |
| `data/database.json` | Mock world: customers, loans, tickets |
| `data/knowledge_base.json` | The 12 policy clauses the TF-IDF retriever searches |
| `data/golden_items.json` | The 22 golden test items (5 categories) |
| `tests/run_evals.py` | Module-10 quality gate: `experiment(context)` for CI + a local CLI |
| `tests/quality_threshold.json` | The gate's pass/fail bar — tune here, no code change |
| `.github/workflows/eval-gate.yml` | Runs the gate on every PR via `langfuse/experiment-action` |
| `config.yaml` | Workshop constants (models, dataset names, concurrency) — no secrets |
| `.env.example` | Template for your keys — copy to `.env` (git-ignored) next to `requirements.txt` and fill in |

### The `app/` package

| Module | Holds |
| --- | --- |
| `config.py` | config.yaml constants, key loading (.env at repo root → env vars → prompt), the Langfuse client |
| `pii_data_masking.py` | `PII_PATTERNS` + the export-time masking hook (Module 2.9) |
| `mcp.py` | The mock world (loads `data/*.json`) **and** the service-desk MCP server (`python -m app.mcp`) |
| `tools.py` | Account/policy tools + TF-IDF retriever + the Module-4 FLAKY_MODE retry demo |
| `agent.py` | The LangGraph graph, `deploy_agent()`/`run_agent()`/`ainvoke_agent()`, `SABOTAGE_BREVITY` |
| `prompts.py` | The three v1 prompts + idempotent `ensure_prompt()`/`seed_prompts()` |
| `golden.py` | Golden items + idempotent `seed_dataset()` + the candidates dataset for promoted failures |
| `evaluators.py` | The five rule evaluators + run-level rollups (shared with the CI gate) |
| `feedback.py` | Score configs + `record_feedback()` (Module 5) |
| `judges.py` | Judge cost tracking + DeepEval bridge helpers |
| `online_eval.py` | `score_recent_production()` — the scheduled online-eval job (Module 7) |
| `get_dashboard_metrics.py` | `metrics_query()` — resilient Metrics-API access (Module 8/9) |
| `generate_fake_traffic.py` | Simulated production traffic (also `python -m app.generate_fake_traffic`) |

Pinned stack: see `requirements.txt` (langfuse 4.14.1 · langchain 1.3.14 · langgraph 1.2.9 ·
deepeval 4.1.1 · fastmcp 3.4.6 · langchain-mcp-adapters 0.3.2) · agent `gpt-4o-mini` · judges
`gpt-4.1-mini`. Trainee cost ≈ **$1–1.5 OpenAI** + ≈ **5–9k of the 50k free Langfuse units**.

## Notebook map (4 h total)

| Notebook | Modules | ~min | What happens | Open |
| --- | --- | --- | --- | --- |
| `00_setup_and_agent` | 0–2 | 45 | keys & connection check; the mock world, tools (service desk via MCP), prompts v1, the graph; first traces; PII masking | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/00_setup_and_agent.ipynb) |
| `01_prompt_versioning` | 3 | 15 | labels, staging → promote → rollback, fallbacks | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/01_prompt_versioning.ipynb) |
| `02_tracing_and_feedback` | 4–5 | 40 | trace anatomy, sessions, timeout/retry demo, tags; user feedback as scores | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/02_tracing_and_feedback.ipynb) |
| `03_evaluation` | 6 | 80 | golden dataset (frozen), baseline run, rule evaluators, hand-built judges + bias checks, DeepEval, managed evaluator, annotation, ship v2 & prove it | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/03_evaluation.ipynb) |
| `04_production_online_eval` | 7–8 | 30 | simulated production traffic, online scoring (trace/observation/session level), promote failures, dashboards & Metrics API | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/04_production_online_eval.ipynb) |
| `05_incident_alerting_ci` | 9–11 | 45 | baseline → v3 incident → alert → rollback; the CI gate live; wrap-up | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/05_incident_alerting_ci.ipynb) |

Each notebook starts with the same four bootstrap cells (clone+install → env → keys → client).
Run them top-to-bottom; there is no local state — the cross-notebook anchors are fixed names in
Langfuse itself (the frozen `meridian-golden-v1` dataset, the `v2` prompt label notebook 03 sets).

## Getting started

1. Get an [OpenAI API key](https://platform.openai.com/api-keys) and a free
   [Langfuse Cloud](https://cloud.langfuse.com) project (public + secret key).
2. **Colab** (recommended): hit the notebook's Colab badge above and run the clone cell;
   then in the **📁 Files** panel copy `.env.example` to **`.env`** (same folder as
   `requirements.txt`), paste your keys in, save, and keep running top to bottom.
   Coming back after a session reset: re-run the clone cell and drop your saved `.env`
   back in — nothing else to redo.
   **Local**: same `.env` at the repo root, `pip install -r requirements.txt`, open the notebook.
3. Run notebooks in order — 03 must run before 04/05 (it seeds the dataset and ships v2).

# Module 10 — the CI/CD quality gate

Every pull request re-runs the frozen golden dataset (`meridian-golden-v1`, 22 items) against
the agent in `app/agent.py` using the
[`langfuse/experiment-action`](https://github.com/langfuse/experiment-action). The gate logic
lives in `tests/run_evals.py` (`experiment(context)` entrypoint): rule-based evaluators score
every item, run-level averages are compared against the bar in `tests/quality_threshold.json`,
and a `RegressionError` fails the check — with the score table posted as a PR comment and a
link to the run comparison in Langfuse.

```
avg_completeness      ≥ 0.70   ┐
avg_business_rules_ok ≥ 0.90   ├ tests/quality_threshold.json
avg_route_correct     ≥ 0.80   ┘
items_completed       = 22     (guards against silently-crashed items)
```

## One-time setup (~10 min)

1. Push this repo to GitHub (workflow already lives at `.github/workflows/eval-gate.yml`).
2. **Settings ▸ Secrets and variables ▸ Actions**:
   - Secrets: `OPENAI_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`
     — for the Langfuse project that holds the `meridian-golden-v1` dataset and the agent
     prompts, i.e. **run notebooks 00 + 03 in that project first**.
   - Variable: `LANGFUSE_HOST` = `https://us.cloud.langfuse.com` (or your region).
3. Sanity-run once: open a trivial PR (whitespace change) → the check should pass green.

No dataset-version pinning is needed: `meridian-golden-v1` is frozen by convention — promoted
production failures land in `meridian-golden-candidates`, so the gate's items never change.

## The live demo (5 min)

1. Branch off; in `app/agent.py` set `SABOTAGE_BREVITY = True` — it injects the
   "reply in ONE short sentence, no numbers or ids" rule into the final prompt, the same
   v3 regression the class watched in Module 9. (In a notebook, the same flip is
   `from app.agent import set_sabotage; set_sabotage(True)`.)
2. Open the PR → the **Langfuse experiment gate** runs (~3–4 min) → **red ✕** with an
   auto-comment: run-level scores, per-item table, link to the Langfuse run comparison.
3. Push the fix (flag back to `False`) → check re-runs → **green ✓** → merge.

## Running the gate locally

```bash
pip install -r requirements.txt
python tests/run_evals.py            # exit 1 + ⛔ on regression
```

## Why the gate is trustworthy

- **Frozen gate set** — versioned by name, not timestamp: nothing ever writes to
  `meridian-golden-v1` after seeding, so the check always runs the same 22 items.
- **Deterministic evaluators** — rule-based, so the gate is free, stable, and repeatable.
- **Aggregates with margin** — one flaky item can't block a release; a real regression drags
  the averages under.
- Cost per gate run: ~22 agent executions ≈ $0.03 on gpt-4o-mini.
