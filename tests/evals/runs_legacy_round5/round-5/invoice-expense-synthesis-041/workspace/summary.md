# Expense Summary

## Overview
- **Total Expenses:** $341.00
- **Total Transactions:** 2

## Totals by Vendor
| Vendor | Total Amount |
| :--- | :--- |
| Acme Corp | $121.00 |
| Beta LLC | $220.00 |

## Totals by Category
| Category | Total Amount |
| :--- | :--- |
| Office Supplies | $121.00 |
| Professional Services | $220.00 |

## Anomalies & Duplicate Invoices
During review of the `./invoices/` directory, several duplicate and variant invoice files were identified alongside the primary billing records:
1. **Acme Corp (Invoice #INV-001 / #INV-2026-001):**
   - *Primary Record:* inv_acme.txt / inv1.txt ($121.00, Office Supplies / Supplies).
   - *Duplicate/Variant Notes:*
     - `inv3.txt`: Listed as $50.00 with note "Duplicate invoice number".
     - `inv_acme_dup.txt`: Listed as $55.00 with note "Duplicate invoice number".
2. **Beta LLC (Invoice #INV-002 / #INV-2026-002):**
   - *Primary Record:* inv_beta.txt / inv2.txt ($220.00, Professional Services / Services).
   - *Consolidated:* The primary, authoritative invoice files (`inv_acme.txt` and `inv_beta.txt`) were selected for `expenses.csv` to avoid double-counting overlapping invoice numbers and partial duplicate entries.
