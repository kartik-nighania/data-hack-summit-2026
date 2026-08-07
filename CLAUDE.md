# Monitoring & Evaluating Agentic AI in Production with Langfuse

A 4-hour hands-on workshop repo. Trainees run the six module notebooks in `workshop/`
top to bottom; all reusable code lives in the `app/` package, and the repo carries the
Module-10 CI/CD quality gate as real code so a pull request against this repo is itself
the live demo.

The running example is the **Meridian Housing Finance support agent**: a LangGraph
supervisor routing between account / policy / service specialist agents over a mock
loan-servicing world, fully instrumented with Langfuse. The two service-desk tools run
behind an MCP server (FastMCP, stdio) that the agent discovers at deploy time.

## Repo map

| Path | Role |
| --- | --- |
| `workshop/00…05_*.ipynb` | The six module notebooks (00: M0–2 · 01: M3 · 02: M4–5 · 03: M6 · 04: M7–8 · 05: M9–11). Generated from the monolith; every notebook starts with the same 4 bootstrap cells |
| `workshop/agentOps_workshop.ipynb` | The original 91-cell monolith — kept as the teaching-content reference until the split notebooks are battle-tested |
| `app/config.py` | config.yaml constants + `load_keys()` (notebook paste-cell/env vars → .env → getpass; "..." placeholders ignored) + `get_lf()` (client with masking hook). **No network at import anywhere in app/** |
| `app/pii_data_masking.py` | `PII_PATTERNS` list + export-time masking hook; empty list = no-op |
| `app/mcp.py` | Mock world (loads `data/*.json`) + the service-desk MCP server. Run as `python -m app.mcp` — never `python app/mcp.py` (would shadow the real `mcp` package) |
| `app/tools.py` | Account/policy tools, TF-IDF retriever, `FLAKY_MODE` retry demo (Module 4) |
| `app/agent.py` | Graph + `deploy_agent()`/`get_agent()`/`redeploy_agent()`, async `ainvoke_agent()`/`run_agent()`, `SABOTAGE_BREVITY` + `set_sabotage()`. **Agent is async-only** (MCP tools); notebooks use top-level `await` |
| `app/prompts.py` | v1 prompt texts + idempotent `ensure_prompt()`/`seed_prompts()` |
| `app/golden.py` | `GOLDEN_ITEMS` (from `data/golden_items.json`) + idempotent `seed_dataset()` + `ensure_candidates_dataset()` |
| `app/evaluators.py` | The 5 rule evaluators + `make_run_evaluator()` — shared by notebook 03 and the CI gate |
| `app/feedback.py`, `app/judges.py`, `app/online_eval.py`, `app/get_dashboard_metrics.py`, `app/generate_fake_traffic.py` | Module 5 / 6 / 7 / 8 helpers, traffic simulator (`python -m app.generate_fake_traffic`) |
| `data/` | `database.json` (world), `knowledge_base.json` (policy KB), `golden_items.json` (22 items, ids `gd-*`) |
| `tests/run_evals.py` + `tests/quality_threshold.json` | Module-10 gate: `experiment(context)` for `langfuse/experiment-action` + local CLI; thresholds in the JSON |
| `.github/workflows/eval-gate.yml` | Runs the gate on every PR; `should_skip_sdk_installation: true` keeps the pinned langfuse |
| `docs/` (git-ignored, local) | Langfuse + DeepEval doc mirror backing the `agentops-docs` skill |

## Conventions

- **Langfuse/DeepEval questions: use the `agentops-docs` skill** and answer from the `docs/`
  mirror, not memory — the repo pins specific versions and both products move fast.
- **Pinned stack — do not bump casually.** Pins live only in `requirements.txt` now
  (notebooks install from it). Core: `langfuse==4.14.1 · langchain==1.3.14 · langgraph==1.2.9 ·
  langchain-openai==1.3.5 · deepeval==4.1.1 · openai==2.46.0 · fastmcp==3.4.6 ·
  langchain-mcp-adapters==0.3.2`. Models: agent `gpt-4o-mini`, judges `gpt-4.1-mini`.
- **Sync rule:** notebook 00/03 cells teach by importing from `app/` with the original header
  comments; the monolith still has everything inline. If you change agent/evaluator/prompt
  behaviour, update `app/` (the source of truth) and check the corresponding notebook
  markdown still tells the truth.
- Langfuse assets the notebooks create (gate depends on them): dataset `meridian-golden-v1`,
  prompts `support-supervisor`, `policy-agent`, `final-response`, `judge-goal-accuracy`,
  score configs `csat`, `goal_accuracy_human`. All seeding is **get-or-create idempotent** —
  keep it that way (`create_prompt` makes a new version on every call).
- **No timestamps, no local state — anchors are fixed names in Langfuse:** the gate set is
  frozen by NAME (`meridian-golden-v1` is never written after seeding; Module 7.5 promotes
  into `meridian-golden-candidates`), and notebook 05's rollback target is the `v2` prompt
  **label** notebook 03 stamps on `final-response`. Never add a version-pin or state file back.
- Env vars: `OPENAI_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`,
  `LANGFUSE_HOST`/`LANGFUSE_BASE_URL` (config sets both). Trainees paste keys into each
  notebook's keys cell (their Colab copy saves to Drive); local runs use `.env` at the repo
  root (from `.env.example`; git-ignored — never commit or print). CI: GitHub secrets +
  `LANGFUSE_HOST` variable.
- The monolith notebook stores cell `source` as single strings (not line lists); the six
  generated notebooks use plain strings too — account for that when editing programmatically.
- The notebooks are regenerable: the builder script lives in the session scratchpad
  (`build_notebooks.py`); prefer editing `app/` or the builder over hand-editing six ipynb files.

## Commands

```bash
.venv/bin/python -m pip install -r requirements.txt        # full pinned stack
python -m py_compile app/*.py tests/run_evals.py           # quick syntax check
python -m app.mcp                                          # run the MCP server standalone (stdio)
python -m app.generate_fake_traffic --sessions 6 --version v2   # simulated prod traffic
python tests/run_evals.py [run_name]                       # the merge gate, locally (exit 1 on regression)
```

Running the gate, the traffic generator, or the notebooks costs real OpenAI money
(~$0.03/gate run, ~$1–1.5 for the full workshop) and writes to the configured Langfuse
project — don't run them speculatively.

## Course structure (six notebooks · 4 h)

- **00 · Setup & the agent (M0–2, 45 m)** — keys/connection check; mock world, tools (service
  desk via MCP), v1 prompts, the graph; first traces; PII masking at export time
- **01 · Prompt versioning (M3, 15 m)** — labels, staging→promote→rollback, fallbacks
- **02 · Tracing & feedback (M4–5, 40 m)** — trace anatomy, sessions/users/tags, the
  FLAKY_MODE timeout-retry demo; user feedback as scores (trace id derived from request id)
- **03 · Evaluation deep dive (M6, 80 m)** — golden dataset (pinned), baseline experiment,
  rule evaluators, hand-built judges with bias measurement, DeepEval metrics, managed
  evaluator, human annotation (κ), ship v2 + prove it run-vs-run
- **04 · Production & online evals (M7–8, 30 m)** — simulated traffic, online scoring at
  trace/observation/session level, promote failures to the dataset; dashboards & Metrics API
- **05 · Incident, alerting & CI (M9–11, 45 m)** — baseline drift job, the v3 brevity
  incident, Monitors, rollback (via the `v2` prompt label); the CI gate live; wrap-up
