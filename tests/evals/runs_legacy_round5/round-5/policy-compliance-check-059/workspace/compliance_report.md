# Compliance Report

## Executive Summary
This report evaluates `docs/document.md` against the compliance requirements defined in `docs/policy.md`.

## Compliance Evaluation

| Rule | Status | Evidence | Remediation |
| --- | --- | --- | --- |
| **1. All docs must have a title.** | **PASS** | The document starts with `# My Document` as the title heading on line 1. | None required. |
| **2. No PII in public docs.** | **FAIL** | The document contains the email address `john@example.com` on line 2, which is Personally Identifiable Information (PII). | Remove or redact the email address (`john@example.com`) from the document. |
| **3. Max 500 words per section.** | **PASS** | The document contains only a single short section with significantly fewer than 500 words. | None required. |

## Conclusion
The document fails compliance due to the presence of PII (`john@example.com`). Remediation requires removing or anonymizing the PII before the document can be approved.
