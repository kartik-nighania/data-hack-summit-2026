---
name: agentops-docs
description: Answer questions and write code for Langfuse (tracing, prompt management, evaluation, scores, datasets, experiments, dashboards, monitors, alerts, self-hosting) and DeepEval (metrics, G-Eval, DAG, test cases, goldens, synthesizer, benchmarks, conversation simulator, CI/CD, prompt optimization). Use whenever the task mentions Langfuse or DeepEval by name, or involves LLM/agent observability, tracing, LLM-as-a-judge, eval metrics, golden datasets, or eval-based quality gates — including all workshop modules in this repo.
---

# Langfuse & DeepEval docs

A local, cleaned mirror of the full Langfuse and DeepEval documentation lives in this
repo. **Answer from these files, not from memory** — both products move fast and your
priors are likely stale (Langfuse v4 SDK, DeepEval 4.0).

**Docs root:** `docs/` at the repo root (`docs/langfuse/`, `docs/deepeval/`).
118 Langfuse pages, 119 DeepEval pages. Every file starts with frontmatter carrying
its upstream `source:` URL — cite that URL when you quote a page.

## Workflow

1. **Route.** Find the topic in the routing table below, or open the matching index:
   - `references/langfuse-index.md` — every Langfuse page, grouped by area
   - `references/deepeval-index.md` — every DeepEval page, grouped by area
2. **Read the whole file.** These pages are 10–40 KB; read the file end-to-end rather
   than grepping a fragment out of it. Partial reads are how you miss the caveat that
   makes the code wrong.
3. **Widen if the first file doesn't answer it.** Grep across the mirror:
   ```bash
   grep -rli "run_experiment" docs/langfuse/
   grep -rn "class BaseMetric" docs/deepeval/ | head -20
   ```
   Filenames are the URL path (`docs/langfuse/langfuse.com_docs_<section>_<page>.md`),
   so `ls docs/langfuse/ | grep evaluation` is an effective topic filter.
4. **Read adjacent pages before answering a design question.** "Which metric should I
   use?" or "how do I structure this eval?" needs the concepts page plus two or three
   candidate pages, not one.
5. **Ground the answer.** Prefer code copied from the docs over code you compose from
   memory. Name the file you used and its `source:` URL.

For broad questions that would mean reading many files (e.g. "compare every RAG metric",
"audit our tracing setup against the docs"), dispatch an `Explore` or `general-purpose`
subagent per area and synthesize — don't serially read 20 pages into your own context.

## Routing table — most common tasks

| Task | File |
|---|---|
| **Langfuse** | |
| First trace / SDK install | `langfuse/langfuse.com_docs_observability_get-started.md` |
| Traces, spans, generations — what the objects are | `langfuse/langfuse.com_docs_observability_data-model.md` |
| `@observe`, context managers, manual spans | `langfuse/langfuse.com_docs_observability_sdk_instrumentation.md` |
| Redacting PII before it leaves the app | `langfuse/langfuse.com_docs_observability_features_masking.md` |
| Sessions (multi-turn) / tags / metadata / users | `..._features_sessions.md`, `..._features_tags.md`, `..._features_metadata.md`, `..._features_users.md` |
| Token counts & cost | `langfuse/langfuse.com_docs_observability_features_token-and-cost-tracking.md` |
| Agent graph view for LangGraph | `langfuse/langfuse.com_docs_observability_features_agent-graphs.md` |
| Prompt versioning, labels, rollback | `langfuse/langfuse.com_docs_prompt-management_features_prompt-version-control.md` |
| Fetch & compile a prompt in code | `langfuse/langfuse.com_docs_prompt-management_get-started.md` |
| Tie a prompt version to its traces | `langfuse/langfuse.com_docs_prompt-management_features_link-to-traces.md` |
| Eval concepts (online/offline, levels) | `langfuse/langfuse.com_docs_evaluation_core-concepts.md` |
| Scores: types, ranges, data model | `langfuse/langfuse.com_docs_evaluation_scores_data-model.md` |
| Send a score / user feedback from your app | `langfuse/langfuse.com_docs_evaluation_evaluation-methods_scores-via-sdk.md` |
| Golden datasets | `langfuse/langfuse.com_docs_evaluation_experiments_datasets.md` |
| Run a dataset experiment in code | `langfuse/langfuse.com_docs_evaluation_experiments_experiments-via-sdk.md` |
| Custom / rule-based evaluators | `langfuse/langfuse.com_docs_evaluation_evaluation-methods_code-evaluators.md` |
| Managed LLM-as-a-Judge (no-code, online evals) | `langfuse/langfuse.com_docs_evaluation_evaluation-methods_llm-as-a-judge.md` |
| Human annotation / review queues | `langfuse/langfuse.com_docs_evaluation_evaluation-methods_annotation-queues.md` |
| Eval in CI, blocking a merge | `langfuse/langfuse.com_docs_evaluation_experiments_experiments-ci-cd.md` |
| Custom dashboards & custom metrics | `langfuse/langfuse.com_docs_metrics_features_custom-dashboards.md` |
| Pull metrics out programmatically | `langfuse/langfuse.com_docs_metrics_features_metrics-api.md` |
| Threshold alerting on live metrics | `langfuse/langfuse.com_docs_metrics_features_monitors.md` |
| Query traces/scores via SDK | `langfuse/langfuse.com_docs_api-and-data-platform_features_query-via-sdk.md` |
| Something isn't showing up in the UI | `langfuse/langfuse.com_docs_observability_troubleshooting-and-faq.md` |
| **DeepEval** | |
| Install & first eval | `deepeval/deepeval.com_docs_getting-started.md` |
| Which metric to pick | `deepeval/deepeval.com_docs_metrics-introduction.md` |
| `LLMTestCase` fields | `deepeval/deepeval.com_docs_evaluation-test-cases.md` |
| Custom rubric metric (G-Eval) | `deepeval/deepeval.com_docs_metrics-llm-evals.md` |
| Deterministic decision-tree metric (DAG) | `deepeval/deepeval.com_docs_metrics-dag.md` |
| Write a metric from scratch | `deepeval/deepeval.com_docs_metrics-custom.md` |
| Did the agent call the right tools | `deepeval/deepeval.com_docs_metrics-tool-correctness.md` |
| Right args to those tools | `deepeval/deepeval.com_docs_metrics-argument-correctness.md` |
| Did the agent achieve the goal | `deepeval/deepeval.com_docs_metrics-goal-accuracy.md`, `..._metrics-task-completion.md` |
| RAG grounding — output vs *retrieved* context | `deepeval/deepeval.com_docs_metrics-faithfulness.md` (higher = better) |
| Hallucination — output vs *ground-truth* context | `deepeval/deepeval.com_docs_metrics-hallucination.md` (lower = better) |
| Schema validity of output | `deepeval/deepeval.com_docs_metrics-json-correctness.md` |
| Score one step, not the whole run | `deepeval/deepeval.com_docs_evaluation-component-level-llm-evals.md` |
| Datasets & goldens | `deepeval/deepeval.com_docs_evaluation-datasets.md` |
| Generate synthetic test cases | `deepeval/deepeval.com_docs_synthetic-data-generation-introduction.md` |
| `deepeval test run` in CI | `deepeval/deepeval.com_docs_evaluation-unit-testing-in-ci-cd.md` |
| Pick the judge model / set API keys | `deepeval/deepeval.com_docs_environment-variables.md` |
| Errors, rate limits, flaky scores | `deepeval/deepeval.com_docs_troubleshooting.md`, `..._docs_faq.md` |

## Reading these files correctly

The mirror is scraped HTML that has been cleaned, but two artifacts remain and both
can produce a *wrong answer* rather than a missing one:

- **Language tabs are flattened.** A line like
  `> **Tabs:** Python SDK | JS/TS SDK | Langchain (Python) — the code blocks below follow this order.`
  marks a tab group: the untagged code fences that follow are those languages, **in that
  order**. No fence in this mirror carries a language tag, and Python and JS blocks sit
  directly adjacent. Count the fences against the tab list before quoting one — handing a
  user JS when they asked for Python is the most likely failure mode here.
- **Known-bad upstream values.** DeepEval metric pages state a default judge model of
  `gpt-5.4`, which does not exist. Don't repeat model ids from the docs as fact; point the
  user at `deepeval.com_docs_environment-variables.md` to set the judge model explicitly.
  DeepEval pages also carry a few miscounts ("EIGHT optional parameters" over a list of
  nine) and at least one snippet with a missing comma — read code before pasting it.

## Things worth knowing before you answer

- **Langfuse Python SDK is v3/v4.** v2 patterns (`langfuse.trace(...)`, `StatefulTraceClient`)
  are gone. If code in the repo or in your head looks v2, check
  `langfuse/langfuse.com_docs_observability_sdk_upgrade-path_python-v2-to-v3.md` and
  `..._python-v3-to-v4.md` before "fixing" anything.
- **Langfuse "evaluators" are three different things** — code evaluators run in your
  process, managed LLM-as-a-Judge runs server-side on live traffic, and experiment
  evaluators run against a dataset. Establish which one the user means before writing code.
- **DeepEval metric names are load-bearing.** Faithfulness ≠ Hallucination (retrieved
  context vs. ground-truth context); Turn-prefixed metrics are the multi-turn variants.
  Check the metric page, don't infer from the name.
- **The two tools compose.** DeepEval metrics can be wrapped as Langfuse evaluators and
  their results pushed back as Langfuse scores — that's how this workshop's Module 6
  wires them. Read both sides before designing that integration.
- The docs are a point-in-time mirror. If a page contradicts observed behaviour, say so
  rather than insisting the doc is right.
