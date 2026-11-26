import csv
from collections import defaultdict

# Read expenses.csv
expenses = []
with open("expenses.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['amount'] = float(row['amount'])
        expenses.append(row)

# Calculate totals
vendor_totals = defaultdict(float)
category_totals = defaultdict(float)
total_amount = 0.0

for e in expenses:
    vendor_totals[e['vendor']] += e['amount']
    category_totals[e['category']] += e['amount']
    total_amount += e['amount']

summary_content = f"""# Expense Summary

## Overview
- **Total Expenses:** ${total_amount:.2f}
- **Total Transactions:** {len(expenses)}

## Totals by Vendor
| Vendor | Total Amount |
| :--- | :--- |
| Acme Corp | ${vendor_totals['Acme Corp']:.2f} |
| Beta LLC | ${vendor_totals['Beta LLC']:.2f} |

## Totals by Category
| Category | Total Amount |
| :--- | :--- |
| Office Supplies | ${category_totals['Office Supplies']:.2f} |
| Professional Services | ${category_totals['Professional Services']:.2f} |

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
"""

with open("summary.md", "w") as f:
    f.write(summary_content)

print("summary.md generated successfully.")
