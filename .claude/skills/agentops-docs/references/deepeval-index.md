# DeepEval doc index

All paths relative to `docs/deepeval/`. Filenames mirror the upstream URL path — every
metric page is `deepeval.com_docs_metrics-<name>.md`, so `ls | grep metrics-` lists them all.

## Start here

| Page | File |
|---|---|
| Introduction to DeepEval | `deepeval.com_docs_introduction.md` |
| Design philosophy | `deepeval.com_docs_introduction-design-philosophy.md` |
| Comparisons vs other frameworks | `deepeval.com_docs_introduction-comparisons.md` |
| 5-min quickstart | `deepeval.com_docs_getting-started.md` |
| Quickstart: RAG | `deepeval.com_docs_getting-started-rag.md` |
| Quickstart: agents | `deepeval.com_docs_getting-started-agents.md` |
| Quickstart: chatbots | `deepeval.com_docs_getting-started-chatbots.md` |
| Quickstart: MCP | `deepeval.com_docs_getting-started-mcp.md` |
| Quickstart: LLM arena | `deepeval.com_docs_getting-started-llm-arena.md` |
| Quickstart: vibe coding | `deepeval.com_docs_vibe-coder-quickstart.md`, `deepeval.com_docs_vibe-coding.md` |

## Evaluation mechanics

| Page | File |
|---|---|
| Introduction to LLM evals | `deepeval.com_docs_evaluation-introduction.md` |
| Single-turn test case (`LLMTestCase`) | `deepeval.com_docs_evaluation-test-cases.md` |
| Multi-turn test case | `deepeval.com_docs_evaluation-multiturn-test-cases.md` |
| Arena test case | `deepeval.com_docs_evaluation-arena-test-cases.md` |
| End-to-end evaluation | `deepeval.com_docs_evaluation-end-to-end-llm-evals.md` |
| End-to-end, single-turn | `deepeval.com_docs_evaluation-end-to-end-single-turn.md` |
| End-to-end, multi-turn | `deepeval.com_docs_evaluation-end-to-end-multi-turn.md` |
| Component-level evaluation (score one step) | `deepeval.com_docs_evaluation-component-level-llm-evals.md` |
| LLM tracing | `deepeval.com_docs_evaluation-llm-tracing.md` |
| Datasets & goldens | `deepeval.com_docs_evaluation-datasets.md` |
| Prompts | `deepeval.com_docs_evaluation-prompts.md` |
| Flags and configs (`evaluate()` options) | `deepeval.com_docs_evaluation-flags-and-configs.md` |
| Unit testing in CI/CD (`deepeval test run`) | `deepeval.com_docs_evaluation-unit-testing-in-ci-cd.md` |
| MCP evaluation | `deepeval.com_docs_evaluation-mcp.md` |

## Metrics — general

| Page | File |
|---|---|
| Introduction: how to choose a metric | `deepeval.com_docs_metrics-introduction.md` |
| G-Eval (custom rubric, LLM judge) | `deepeval.com_docs_metrics-llm-evals.md` |
| DAG (deterministic decision tree) | `deepeval.com_docs_metrics-dag.md` |
| Custom / DIY metrics (`BaseMetric`) | `deepeval.com_docs_metrics-custom.md` |
| Community metrics | `deepeval.com_docs_community-metrics-overview.md` |
| RAGAS wrapper | `deepeval.com_docs_metrics-ragas.md` |

## Metrics — RAG

| Metric | File |
|---|---|
| Answer Relevancy | `deepeval.com_docs_metrics-answer-relevancy.md` |
| Faithfulness (vs retrieval context) | `deepeval.com_docs_metrics-faithfulness.md` |
| Hallucination (vs ground-truth context) | `deepeval.com_docs_metrics-hallucination.md` |
| Citation Faithfulness | `deepeval.com_docs_metrics-citation-faithfulness.md` |
| Contextual Precision | `deepeval.com_docs_metrics-contextual-precision.md` |
| Contextual Recall | `deepeval.com_docs_metrics-contextual-recall.md` |
| Contextual Relevancy | `deepeval.com_docs_metrics-contextual-relevancy.md` |
| Summarization | `deepeval.com_docs_metrics-summarization.md` |

## Metrics — agents & tools

| Metric | File |
|---|---|
| Tool Correctness (right tools called) | `deepeval.com_docs_metrics-tool-correctness.md` |
| Argument Correctness (right args) | `deepeval.com_docs_metrics-argument-correctness.md` |
| Tool Use | `deepeval.com_docs_metrics-tool-use.md` |
| Tool Permission | `deepeval.com_docs_metrics-tool-permission.md` |
| Task Completion | `deepeval.com_docs_metrics-task-completion.md` |
| Goal Accuracy | `deepeval.com_docs_metrics-goal-accuracy.md` |
| Plan Adherence | `deepeval.com_docs_metrics-plan-adherence.md` |
| Plan Quality | `deepeval.com_docs_metrics-plan-quality.md` |
| Step Efficiency | `deepeval.com_docs_metrics-step-efficiency.md` |
| Agent Loop Detection | `deepeval.com_docs_metrics-agent-loop-detection.md` |
| MCP Task Completion | `deepeval.com_docs_metrics-mcp-task-completion.md` |
| MCP-Use | `deepeval.com_docs_metrics-mcp-use.md` |
| Multi-Turn MCP-Use | `deepeval.com_docs_metrics-multi-turn-mcp-use.md` |

## Metrics — conversational / multi-turn

| Metric | File |
|---|---|
| Conversational G-Eval | `deepeval.com_docs_metrics-conversational-g-eval.md` |
| Conversational DAG | `deepeval.com_docs_metrics-conversational-dag.md` |
| Conversation Completeness | `deepeval.com_docs_metrics-conversation-completeness.md` |
| Knowledge Retention | `deepeval.com_docs_metrics-knowledge-retention.md` |
| Role Adherence | `deepeval.com_docs_metrics-role-adherence.md` |
| Topic Adherence | `deepeval.com_docs_metrics-topic-adherence.md` |
| Turn Relevancy | `deepeval.com_docs_metrics-turn-relevancy.md` |
| Turn Faithfulness | `deepeval.com_docs_metrics-turn-faithfulness.md` |
| Turn Contextual Precision / Recall / Relevancy | `deepeval.com_docs_metrics-turn-contextual-precision.md`, `..._metrics-turn-contextual-recall.md`, `..._metrics-turn-contextual-relevancy.md` |

## Metrics — safety, format, deterministic

| Metric | File |
|---|---|
| Bias | `deepeval.com_docs_metrics-bias.md` |
| Toxicity | `deepeval.com_docs_metrics-toxicity.md` |
| PII Leakage | `deepeval.com_docs_metrics-pii-leakage.md` |
| Misuse | `deepeval.com_docs_metrics-misuse.md` |
| Non-Advice | `deepeval.com_docs_metrics-non-advice.md` |
| Role Violation | `deepeval.com_docs_metrics-role-violation.md` |
| Prompt Alignment | `deepeval.com_docs_metrics-prompt-alignment.md` |
| Json Correctness (schema validity) | `deepeval.com_docs_metrics-json-correctness.md` |
| Exact Match | `deepeval.com_docs_metrics-exact-match.md` |
| Pattern Match | `deepeval.com_docs_metrics-pattern-match.md` |
| Arena G-Eval | `deepeval.com_docs_metrics-arena-g-eval.md` |

## Metrics — multimodal

| Metric | File |
|---|---|
| Text to Image | `deepeval.com_docs_multimodal-metrics-text-to-image.md` |
| Image Editing | `deepeval.com_docs_multimodal-metrics-image-editing.md` |
| Image Coherence | `deepeval.com_docs_multimodal-metrics-image-coherence.md` |
| Image Helpfulness | `deepeval.com_docs_multimodal-metrics-image-helpfulness.md` |
| Image Reference | `deepeval.com_docs_multimodal-metrics-image-reference.md` |

## Synthetic data generation

| Page | File |
|---|---|
| Introduction | `deepeval.com_docs_synthetic-data-generation-introduction.md` |
| Golden Synthesizer | `deepeval.com_docs_golden-synthesizer.md` |
| From documents | `deepeval.com_docs_synthesizer-generate-from-docs.md` |
| From contexts | `deepeval.com_docs_synthesizer-generate-from-contexts.md` |
| From existing goldens | `deepeval.com_docs_synthesizer-generate-from-goldens.md` |
| From scratch | `deepeval.com_docs_synthesizer-generate-from-scratch.md` |

## Conversation simulator

| Page | File |
|---|---|
| Overview | `deepeval.com_docs_conversation-simulator.md` |
| Model callback | `deepeval.com_docs_conversation-simulator-model-callback.md` |
| Simulation graph | `deepeval.com_docs_conversation-simulator-simulation-graph.md` |
| Stopping logic | `deepeval.com_docs_conversation-simulator-stopping-logic.md` |
| Lifecycle hooks | `deepeval.com_docs_conversation-simulator-lifecycle-hooks.md` |
| Custom templates | `deepeval.com_docs_conversation-simulator-custom-templates.md` |

## Prompt optimization

| Page | File |
|---|---|
| Introduction | `deepeval.com_docs_prompt-optimization-introduction.md` |
| COPRO | `deepeval.com_docs_prompt-optimization-copro.md` |
| MIPROv2 | `deepeval.com_docs_prompt-optimization-miprov2.md` |
| GEPA | `deepeval.com_docs_prompt-optimization-gepa.md` |
| SIMBA | `deepeval.com_docs_prompt-optimization-simba.md` |

## Benchmarks

Introduction: `deepeval.com_docs_benchmarks-introduction.md`. Individual benchmarks follow
`deepeval.com_docs_benchmarks-<name>.md` — ARC, BBQ, BIG-Bench Hard, BoolQ, DROP, GSM8K,
HellaSwag, HumanEval, IFEval, LAMBADA, LogiQA, MathQA, MMLU, SQuAD, TruthfulQA, Winogrande.

## Configuration & operations

| Page | File |
|---|---|
| Environment variables (judge model, keys) | `deepeval.com_docs_environment-variables.md` |
| CLI settings | `deepeval.com_docs_command-line-interface.md` |
| Data privacy | `deepeval.com_docs_data-privacy.md` |
| Troubleshooting | `deepeval.com_docs_troubleshooting.md` |
| FAQ | `deepeval.com_docs_faq.md` |
| Miscellaneous | `deepeval.com_docs_miscellaneous.md` |
