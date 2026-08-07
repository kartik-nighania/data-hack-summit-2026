# Monitoring & Evaluating Agentic AI in Production with Langfuse

A hands-on workshop: build a multi-agent support desk with **LangGraph**, then wrap the full
production loop around it with **Langfuse** — tracing → prompt management → user feedback →
evaluation (rules, LLM-as-a-Judge, **DeepEval**) → online evals → dashboards →
monitoring/alerting → a CI/CD quality gate that blocks bad merges.

The running example is the **Meridian Housing Finance support agent**: a supervisor routing
between account, policy, and service specialists over a mock loan-servicing world.

## Notebooks

Run them in order — 03 must run before 04/05 (it seeds the dataset and ships v2).

| Notebook | What happens | Open |
| --- | --- | --- |
| `00_setup_and_agent` | keys & connection check; the mock world, the specialists' tools, prompts v1, the graph; first traces; PII masking | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/00_setup_and_agent.ipynb) |
| `01_prompt_versioning` | labels, staging → promote → rollback, fallbacks | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/01_prompt_versioning.ipynb) |
| `02_tracing_and_feedback` | trace anatomy, sessions, timeout/retry demo, tags; user feedback as scores | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/02_tracing_and_feedback.ipynb) |
| `03_evaluation` | golden dataset (frozen), baseline run, rule evaluators, hand-built judges + bias checks, DeepEval, managed evaluator, annotation, ship v2 & prove it | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/03_evaluation.ipynb) |
| `04_production_online_eval` | simulated production traffic, online scoring (trace/observation/session level), promote failures, dashboards & Metrics API | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/04_production_online_eval.ipynb) |
| `05_incident_alerting_ci` | baseline → v3 incident → alert → rollback; the CI gate live; wrap-up | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kartik-nighania/data-hack-summit-2026/blob/main/workshop/05_incident_alerting_ci.ipynb) |

## Getting started

1. Get an [OpenAI API key](https://platform.openai.com/api-keys) and a free
   [Langfuse Cloud](https://cloud.langfuse.com) project (public + secret key).
2. **Colab** (recommended): hit a Colab badge above and paste your keys into the keys cell.
   **Local**: copy `.env.example` to `.env` at the repo root, `pip install -r requirements.txt`,
   open the notebook.

Trainee cost ≈ **$1–1.5 OpenAI** + a few thousand of the 50k free Langfuse units.

## Repo layout

| Path | What |
| --- | --- |
| `workshop/` | The six module notebooks (each bootstraps itself) |
| `app/` | The reusable package the notebooks import (agent, tools, prompts, evaluators, …) |
| `data/` | Mock world, policy knowledge base, golden test items |
| `tests/run_evals.py` | The CI quality gate (thresholds in `tests/quality_threshold.json`) |
| `.github/workflows/eval-gate.yml` | Runs the gate on every PR via `langfuse/experiment-action` |

## The CI/CD quality gate

Every pull request re-runs the frozen golden dataset (`meridian-golden-v1`, 22 items) against
the agent and compares run-level scores to the bar in `tests/quality_threshold.json` — a
regression fails the check, with the score table posted as a PR comment.

Setup: add `OPENAI_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` as GitHub Actions
secrets and `LANGFUSE_HOST` as a variable (run notebooks 00 + 03 in that Langfuse project
first). Run it locally with:

```bash
python tests/run_evals.py   # exit 1 on regression
```
