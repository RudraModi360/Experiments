# Eval run `round-5`

- deepeval: `4.3.4`
- judge chain: `google/gemini-3.1-flash-lite` via fallback chain google/gemini-3.1-flash-lite
- generated: 2026-11-26T15:51:45

| Case | Status | Checks | Metrics | Steps | Time | Model |
|---|---|---|---|---|---|---|
| budget-forecast-045 | fail | fail | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.25, Correctness=0.10, CodeChangeQuality=0.05 | 20 | 82.22s | gemini-3.5-flash-lite |
| clinical-trial-summary-056 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=1.00 | 7 | 22.04s | gemini-3.5-flash-lite |
| contract-risk-review-046 | pass | pass | ConversationCompletenessMetric=—, TurnRelevancyMetric=—, ConversationalCorrectness=— | 7 | 12.67s | gemini-3.5-flash-lite |
| course-outline-066 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=1.00 | 6 | 15.84s | gemini-3.5-flash-lite |
| email-triage-reply-044 | fail | pass | ConversationCompletenessMetric=—, TurnRelevancyMetric=—, ConversationalCorrectness=— | 9 | 27.45s | gemini-3.5-flash-lite |
| expense-audit-051 | fail | fail | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, CodeChangeQuality=0.50 | 8 | 26.78s | gemini-3.5-flash-lite |
| grade-calculator-057 | fail | fail | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, CodeChangeQuality=0.10 | 8 | 28.07s | gemini-3.5-flash-lite |
| hr-onboarding-checklist-060 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.25, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=1.00 | 8 | 23.67s | gemini-3.5-flash-lite |
| incident-postmortem-062 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.25, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=1.00 | 4 | 14.25s | gemini-3.5-flash-lite |
| invoice-expense-synthesis-041 | fail | pass | TaskCompletionMetric=0.90, StepEfficiencyMetric=0.25, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=0.87 | 16 | 64.36s | gemini-3.5-flash-lite |
| knowledge-base-faq-063 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, FaithfulnessMetric=0.83, ContextualRelevancyMetric=1.00 | 4 | 7.4s | gemini-3.5-flash-lite |
| lead-gen-outreach-071 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=0.75 | 8 | 36.36s | gemini-3.5-flash-lite |
| lead-gen-pipeline-073 | pass | pass | ConversationCompletenessMetric=—, TurnRelevancyMetric=—, ConversationalCorrectness=— | 17 | 53.39s | gemini-3.5-flash-lite |
| lead-gen-quotation-072 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=0.83 | 5 | 15.71s | gemini-3.5-flash-lite |
| lesson-plan-generator-053 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=1.00 | 6 | 26.65s | gemini-3.5-flash-lite |
| medical-visit-summary-042 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.25, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=0.92 | 8 | 47.47s | gemini-3.5-flash-lite |
| meeting-minutes-047 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=0.50, FaithfulnessMetric=1.00, ContextualRelevancyMetric=1.00 | 3 | 8.93s | gemini-3.5-flash-lite |
| patient-appointment-scheduler-065 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.25, Correctness=1.00, CodeChangeQuality=1.00 | 15 | 45.34s | gemini-3.5-flash-lite |
| personal-finance-advisor-070 | pass | pass | ConversationCompletenessMetric=—, TurnRelevancyMetric=—, ConversationalCorrectness=— | 9 | 27.28s | gemini-3.5-flash-lite |
| policy-compliance-check-059 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=0.50 | 3 | 6.68s | gemini-3.5-flash-lite |
| product-review-sentiment-061 | fail | fail | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, CodeChangeQuality=0.10 | 9 | 29.93s | gemini-3.5-flash-lite |
| report-refine-session-050 | pass | pass | ConversationCompletenessMetric=—, TurnRelevancyMetric=—, ConversationalCorrectness=— | 17 | 61.38s | gemini-3.5-flash-lite |
| resume-cv-builder-048 | pass | pass | ConversationCompletenessMetric=—, TurnRelevancyMetric=—, ConversationalCorrectness=— | 8 | 32.81s | gemini-3.5-flash-lite |
| sales-forecast-058 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, CodeChangeQuality=1.00 | 11 | 27.68s | gemini-3.5-flash-lite |
| study-schedule-043 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=0.88 | 13 | 52.25s | gemini-3.5-flash-lite |
| tax-deduction-finder-055 | fail | fail | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.25, Correctness=1.00, CodeChangeQuality=0.05 | 8 | 16.82s | gemini-3.5-flash-lite |
| travel-expense-claim-064 | fail | fail | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, CodeChangeQuality=0.10 | 9 | 18.92s | gemini-3.5-flash-lite |
| travel-itinerary-049 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=1.00 | 7 | 33.0s | gemini-3.5-flash-lite |
| weekly-status-report-069 | fail | pass | TaskCompletionMetric=1.00, StepEfficiencyMetric=0.50, Correctness=1.00, FaithfulnessMetric=1.00, ContextualRelevancyMetric=1.00 | 4 | 12.78s | gemini-3.5-flash-lite |
