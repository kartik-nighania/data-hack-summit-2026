# Langfuse doc index

All paths relative to `docs/langfuse/`. Filenames mirror the upstream URL path, so the
prefix `langfuse.com_docs_<section>_` is a reliable section filter for `ls | grep`.

## Observability — core

| Page | File |
|---|---|
| Overview: what tracing gives you | `langfuse.com_docs_observability_overview.md` |
| Get started (install, first trace, keys) | `langfuse.com_docs_observability_get-started.md` |
| Concepts: trace / observation / span / generation | `langfuse.com_docs_observability_data-model.md` |
| What a *good* trace looks like | `langfuse.com_docs_observability_best-practices.md` |
| Observation types reference | `langfuse.com_docs_observability_features_observation-types.md` |
| Troubleshooting & FAQ | `langfuse.com_docs_observability_troubleshooting-and-faq.md` |

## Observability — SDK

| Page | File |
|---|---|
| SDK overview (Python + JS) | `langfuse.com_docs_observability_sdk_overview.md` |
| Instrumentation: `@observe`, spans, context | `langfuse.com_docs_observability_sdk_instrumentation.md` |
| Advanced features | `langfuse.com_docs_observability_sdk_advanced-features.md` |
| SDK troubleshooting & FAQ | `langfuse.com_docs_observability_sdk_troubleshooting-and-faq.md` |
| Upgrade paths (index) | `langfuse.com_docs_observability_sdk_upgrade-path.md` |
| Python v2 → v3 | `langfuse.com_docs_observability_sdk_upgrade-path_python-v2-to-v3.md` |
| Python v3 → v4 | `langfuse.com_docs_observability_sdk_upgrade-path_python-v3-to-v4.md` |
| JS/TS v3 → v4 | `langfuse.com_docs_observability_sdk_upgrade-path_js-v3-to-v4.md` |
| JS/TS v4 → v5 | `langfuse.com_docs_observability_sdk_upgrade-path_js-v4-to-v5.md` |

## Observability — features

| Page | File |
|---|---|
| Sessions (multi-turn conversations) | `langfuse.com_docs_observability_features_sessions.md` |
| Tags | `langfuse.com_docs_observability_features_tags.md` |
| Metadata | `langfuse.com_docs_observability_features_metadata.md` |
| User tracking | `langfuse.com_docs_observability_features_users.md` |
| User feedback capture | `langfuse.com_docs_observability_features_user-feedback.md` |
| Masking / redacting sensitive fields | `langfuse.com_docs_observability_features_masking.md` |
| Token & cost tracking | `langfuse.com_docs_observability_features_token-and-cost-tracking.md` |
| Log levels | `langfuse.com_docs_observability_features_log-levels.md` |
| Agent graphs (LangGraph etc.) | `langfuse.com_docs_observability_features_agent-graphs.md` |
| MCP tracing | `langfuse.com_docs_observability_features_mcp-tracing.md` |
| Environments (dev/staging/prod split) | `langfuse.com_docs_observability_features_environments.md` |
| Releases & versioning | `langfuse.com_docs_observability_features_releases-and-versioning.md` |
| Sampling | `langfuse.com_docs_observability_features_sampling.md` |
| Event queuing / batching / flush | `langfuse.com_docs_observability_features_queuing-batching.md` |
| Trace IDs & distributed tracing | `langfuse.com_docs_observability_features_trace-ids-and-distributed-tracing.md` |
| Trace URLs | `langfuse.com_docs_observability_features_url.md` |
| Filter search bar syntax | `langfuse.com_docs_observability_features_filter-search-bar.md` |
| Full-text search | `langfuse.com_docs_observability_features_full-text-search.md` |
| Comments | `langfuse.com_docs_observability_features_comments.md` |
| Corrections | `langfuse.com_docs_observability_features_corrections.md` |
| Multi-modality (images, audio) | `langfuse.com_docs_observability_features_multi-modality.md` |
| Web callouts | `langfuse.com_docs_observability_features_web-callouts.md` |

## Prompt management

| Page | File |
|---|---|
| Overview | `langfuse.com_docs_prompt-management_overview.md` |
| Get started (create, fetch, compile) | `langfuse.com_docs_prompt-management_get-started.md` |
| Concepts / data model | `langfuse.com_docs_prompt-management_data-model.md` |
| Version control, labels, rollback | `langfuse.com_docs_prompt-management_features_prompt-version-control.md` |
| Variables | `langfuse.com_docs_prompt-management_features_variables.md` |
| Message placeholders (chat prompts) | `langfuse.com_docs_prompt-management_features_message-placeholders.md` |
| Config (model params on the prompt) | `langfuse.com_docs_prompt-management_features_config.md` |
| Composability (prompts referencing prompts) | `langfuse.com_docs_prompt-management_features_composability.md` |
| Link prompt → traces | `langfuse.com_docs_prompt-management_features_link-to-traces.md` |
| Caching & latency | `langfuse.com_docs_prompt-management_features_caching.md` |
| Guaranteed availability / fallbacks | `langfuse.com_docs_prompt-management_features_guaranteed-availability.md` |
| A/B testing prompt versions | `langfuse.com_docs_prompt-management_features_a-b-testing.md` |
| Playground | `langfuse.com_docs_prompt-management_features_playground.md` |
| Folders | `langfuse.com_docs_prompt-management_features_folders.md` |
| GitHub integration | `langfuse.com_docs_prompt-management_features_github-integration.md` |
| Webhooks / Slack on prompt change | `langfuse.com_docs_prompt-management_features_webhooks-slack-integrations.md` |
| Manage prompts via MCP | `langfuse.com_docs_prompt-management_features_mcp-server.md` |
| n8n node | `langfuse.com_docs_prompt-management_features_n8n-node.md` |
| Troubleshooting & FAQ | `langfuse.com_docs_prompt-management_troubleshooting-and-faq.md` |

## Evaluation

| Page | File |
|---|---|
| Overview | `langfuse.com_docs_evaluation_overview.md` |
| Core concepts (online vs offline, levels) | `langfuse.com_docs_evaluation_core-concepts.md` |
| Code evaluators (custom / rule-based) | `langfuse.com_docs_evaluation_evaluation-methods_code-evaluators.md` |
| Managed LLM-as-a-Judge | `langfuse.com_docs_evaluation_evaluation-methods_llm-as-a-judge.md` |
| Annotation queues (human review) | `langfuse.com_docs_evaluation_evaluation-methods_annotation-queues.md` |
| Scores via API/SDK | `langfuse.com_docs_evaluation_evaluation-methods_scores-via-sdk.md` |
| Scores via UI | `langfuse.com_docs_evaluation_evaluation-methods_scores-via-ui.md` |
| Scores overview | `langfuse.com_docs_evaluation_scores_overview.md` |
| Scores data model (numeric/categorical/boolean) | `langfuse.com_docs_evaluation_scores_data-model.md` |
| Score analytics | `langfuse.com_docs_evaluation_scores_score-analytics.md` |
| Datasets (goldens, versioning) | `langfuse.com_docs_evaluation_experiments_datasets.md` |
| Experiments data model | `langfuse.com_docs_evaluation_experiments_data-model.md` |
| Experiments via SDK (`run_experiment`) | `langfuse.com_docs_evaluation_experiments_experiments-via-sdk.md` |
| Experiments via UI | `langfuse.com_docs_evaluation_experiments_experiments-via-ui.md` |
| Experiments in CI/CD (quality gates) | `langfuse.com_docs_evaluation_experiments_experiments-ci-cd.md` |
| Troubleshooting & FAQ | `langfuse.com_docs_evaluation_troubleshooting-and-faq.md` |

## Metrics, dashboards, alerting

| Page | File |
|---|---|
| Overview | `langfuse.com_docs_metrics_overview.md` |
| Custom dashboards & custom metrics | `langfuse.com_docs_metrics_features_custom-dashboards.md` |
| Metrics API | `langfuse.com_docs_metrics_features_metrics-api.md` |
| Monitors and alerts | `langfuse.com_docs_metrics_features_monitors.md` |

## API & data platform

| Page | File |
|---|---|
| Overview | `langfuse.com_docs_api-and-data-platform_overview.md` |
| Public API | `langfuse.com_docs_api-and-data-platform_features_public-api.md` |
| Observations API | `langfuse.com_docs_api-and-data-platform_features_observations-api.md` |
| Query via SDKs | `langfuse.com_docs_api-and-data-platform_features_query-via-sdk.md` |
| CLI | `langfuse.com_docs_api-and-data-platform_features_cli.md` |
| MCP server | `langfuse.com_docs_api-and-data-platform_features_mcp-server.md` |
| Agent skill | `langfuse.com_docs_api-and-data-platform_features_agent-skill.md` |
| Export from UI | `langfuse.com_docs_api-and-data-platform_features_export-from-ui.md` |
| Export to blob storage | `langfuse.com_docs_api-and-data-platform_features_export-to-blob-storage.md` |
| Blob export field reference | `langfuse.com_docs_api-and-data-platform_features_blob-storage-export-fields.md` |

## Administration & platform

| Page | File |
|---|---|
| RBAC / access control | `langfuse.com_docs_administration_rbac.md` |
| Authentication & SSO | `langfuse.com_docs_administration_authentication-and-sso.md` |
| SCIM and Org API | `langfuse.com_docs_administration_scim-and-org-api.md` |
| LLM connections (judge model config) | `langfuse.com_docs_administration_llm-connection.md` |
| Spend alerts | `langfuse.com_docs_administration_spend-alerts.md` |
| Billable units | `langfuse.com_docs_administration_billable-units.md` |
| Data retention | `langfuse.com_docs_administration_data-retention.md` |
| Data deletion | `langfuse.com_docs_administration_data-deletion.md` |
| Audit logs | `langfuse.com_docs_administration_audit-logs.md` |
| Troubleshooting & FAQ | `langfuse.com_docs_administration_troubleshooting-and-faq.md` |
| Security & guardrails | `langfuse.com_docs_security-and-guardrails.md` |
| Self-hosting | `langfuse.com_self-hosting.md` |
| Glossary | `langfuse.com_docs_glossary.md` |
| v4 / Fast Preview release notes | `langfuse.com_docs_v4.md` |
| Roadmap | `langfuse.com_docs_roadmap.md` |
| Demo project | `langfuse.com_docs_demo.md` |
| Ask AI / Langfuse Assistant / Docs MCP | `langfuse.com_docs_ask-ai.md`, `langfuse.com_docs_langfuse-assistant.md`, `langfuse.com_docs_docs-mcp.md` |

## Integrations & cookbooks

| Page | File |
|---|---|
| Integrations overview | `langfuse.com_integrations.md` |
| OpenTelemetry (native) | `langfuse.com_integrations_native_opentelemetry.md` |
| OpenAI SDK — Python | `langfuse.com_integrations_model-providers_openai-py.md` |
| OpenAI SDK — JS/TS | `langfuse.com_integrations_model-providers_openai-js.md` |
| Flowise (no-code) | `langfuse.com_integrations_no-code_flowise.md` |
| Cookbook: JS/TS SDK | `langfuse.com_guides_cookbook_js_langfuse_sdk.md` |
| Cookbook: OpenAI structured outputs | `langfuse.com_guides_cookbook_integration_openai_structured_output.md` |
| Cookbook: synthetic datasets | `langfuse.com_guides_cookbook_example_synthetic_datasets.md` |
| Cookbook: LLM security monitoring | `langfuse.com_guides_cookbook_example_llm_security_monitoring.md` |
| Cookbook: OTel via OpenLIT / OpenLLMetry / MLflow / Arize | `langfuse.com_guides_cookbook_otel_integration_openlit.md`, `..._openllmetry.md`, `..._mlflow.md`, `..._arize.md` |
