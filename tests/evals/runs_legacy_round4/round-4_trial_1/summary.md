# Eval run `round-4`

- deepeval: `4.3.4`
- judge chain: `google/gemini-3.1-flash-lite` via fallback chain google/gemini-3.1-flash-lite
- generated: 2026-11-25T16:39:49

| Case | Status | Checks | Metrics | Steps | Time | Model |
|---|---|---|---|---|---|---|
| broken-api-debug-033 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, CodeChangeQuality=1.00 | 17 | 113.14s | gemini-3.5-flash-lite |
| cricket-analytics-039 | fail | pass | ConversationCompletenessMetric=—, TurnRelevancyMetric=—, ConversationalCorrectness=— | 15 | 33.61s | gemini-3.5-flash-lite |
| doc-synthesis-injection-035 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=0.50, FaithfulnessMetric=1.00, ContextualRelevancyMetric=0.75, PromptAlignmentMetric=0.00, InstructionHierarchy=1.00 | 7 | 15.68s | gemini-3.5-flash-lite |
| docker-healthcheck-038 | fail | pass | TaskCompletionMetric=0.70, StepEfficiencyMetric=0.50, Correctness=0.00, CodeChangeQuality=1.00, CrossFileConsistency=1.00 | 15 | 72.15s | gemini-3.5-flash-lite |
| dsa-graph-debug-036 | fail | fail | ConversationCompletenessMetric=—, TurnRelevancyMetric=—, ConversationalCorrectness=— | 22 | 83.1s | gemini-3.5-flash-lite |
| frontier-model-research-031 | fail | pass | ConversationCompletenessMetric=—, TurnRelevancyMetric=—, ConversationalCorrectness=— | 19 | 79.71s | gemini-3.5-flash-lite |
| log-timeline-034 | fail | fail | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.25, Correctness=0.05, CodeChangeQuality=0.05 | 18 | 143.42s | gemini-3.5-flash-lite |
| multi-turn-debug-040 | fail | fail | ConversationCompletenessMetric=—, TurnRelevancyMetric=—, ConversationalCorrectness=— | 13 | 21.66s | gemini-3.5-flash-lite |
| rag-contradiction-037 | fail | fail | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.75, Correctness=0.10, FaithfulnessMetric=—, ContextualRelevancyMetric=— | 15 | 41.74s | gemini-3.5-flash-lite |
| ts-agent-ollama-032 | fail | fail | TaskCompletionMetric=0.90, StepEfficiencyMetric=0.25, Correctness=0.05, ToolCorrectnessMetric=1.00, ArgumentCorrectnessMetric=1.00 | 21 | 148.87s | gemini-3.5-flash-lite |
