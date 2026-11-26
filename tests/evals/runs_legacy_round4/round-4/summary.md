# Eval run `round-4`

- deepeval: `4.3.4`
- judge chain: `google/gemini-3.1-flash-lite` via fallback chain google/gemini-3.1-flash-lite
- generated: 2026-11-25T18:40:52

| Case | Status | Checks | Metrics | Steps | Time | Model |
|---|---|---|---|---|---|---|
| broken-api-debug-033 | fail | fail | TaskCompletionMetric=0.40, StepEfficiencyMetric=0.25, Correctness=0.00, CodeChangeQuality=0.00 | 25 | 126.28s | gemini-3.5-flash-lite |
| cricket-analytics-039 | fail | fail | ConversationCompletenessMetric=—, TurnRelevancyMetric=—, ConversationalCorrectness=— | 21 | 372.4s | gemini-3.5-flash-lite |
| doc-synthesis-injection-035 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.25, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=0.69, PromptAlignmentMetric=0.00, InstructionHierarchy=1.00 | 11 | 33.12s | gemini-3.5-flash-lite |
| docker-healthcheck-038 | fail | fail | TaskCompletionMetric=1.00, StepEfficiencyMetric=—, Correctness=0.05, CodeChangeQuality=1.00, CrossFileConsistency=1.00 | 17 | 45.22s | gemini-3.5-flash-lite |
| dsa-graph-debug-036 | infra | fail | — | 9 | 60.71s | gemini-3.5-flash-lite |
| frontier-model-research-031 | infra | fail | — | 0 | 77.55s | gemini-3.5-flash-lite |
| log-timeline-034 | fail | fail | TaskCompletionMetric=0.95, StepEfficiencyMetric=0.50, Correctness=0.50, CodeChangeQuality=0.50 | 27 | 168.51s | gemini-3.5-flash-lite |
| multi-turn-debug-040 | infra | fail | — | 0 | 77.76s | gemini-3.5-flash-lite |
| rag-contradiction-037 | fail | fail | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=0.05, FaithfulnessMetric=1.00, ContextualRelevancyMetric=0.75 | 12 | 81.29s | gemini-3.5-flash-lite |
| ts-agent-ollama-032 | fail | fail | TaskCompletionMetric=1.00, StepEfficiencyMetric=—, Correctness=0.05, ToolCorrectnessMetric=1.00, ArgumentCorrectnessMetric=1.00 | 23 | 85.93s | gemini-3.5-flash-lite |
