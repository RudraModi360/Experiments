import csv
import glob
import re

# Let's parse all invoice files
# Files:
# inv1.txt: INV-001, Acme Corp, 2026-01-15, Total 121.00, Supplies
# inv2.txt: INV-002, Beta LLC, 2026-02-03, Total 220.00, Services
# inv3.txt: INV-001, Acme Corp, 2026-01-15, Total 50.00, Supplies, NOTE: duplicate invoice number
# inv_acme.txt: INV-2026-001, Acme Corp, 2026-01-15, Total 121.00, Office Supplies
# inv_acme_dup.txt: INV-2026-001, Acme Corp, 2026-01-15, Total 55.00, Office Supplies, NOTE: DUPLICATE
# inv_beta.txt: INV-2026-002, Beta LLC, 2026-02-03, Total 220.00, Professional Services

# Wait, the user prompt states: "You are given 3 invoice text files in ./invoices/. Consolidate them into expenses.csv (vendor, date, amount, category) and summary.md (totals by vendor/category, anomalies)."
# Wait, why are there 6 files in ./invoices/? Let's check pairs or duplicates or sets of invoices.
# Notice inv1.txt / inv2.txt / inv3.txt vs inv_acme.txt / inv_acme_dup.txt / inv_beta.txt.
# Let's analyze all 6 files carefully.
# inv1.txt: Invoice #INV-001, Vendor: Acme Corp, Date: 2026-01-15, Total: 121.00, Category: Supplies
# inv2.txt: Invoice #INV-002, Vendor: Beta LLC, Date: 2026-02-03, Total: 220.00, Category: Services
# inv3.txt: Invoice #INV-001, Vendor: Acme Corp, Date: 2026-01-15, Total: 50.00, Category: Supplies, NOTE: duplicate invoice number
# inv_acme.txt: INVOICE #INV-2026-001, Vendor: Acme Corp, Date: 2026-01-15, Total: $121.00, Category: Office Supplies
# inv_acme_dup.txt: INVOICE #INV-2026-001, Vendor: Acme Corp, Date: 2026-01-15, Total: $55.00, Category: Office Supplies, NOTE: DUPLICATE invoice number (same as INV-2026-001)
# inv_beta.txt: INVOICE #INV-2026-002, Vendor: Beta LLC, Date: 2026-02-03, Total: $220.00, Category: Professional Services

# Notice that inv1.txt and inv_acme.txt are identical content (Acme Corp, 2026-01-15, $121.00), except inv_acme.txt has invoice number INV-2026-001 and category Office Supplies, while inv1.txt has INV-001 and category Supplies.
# Wait! Let's check if there are 3 distinct valid invoices or if the prompt mentions "3 invoice text files" referring to a specific set or if there are duplicates / multiple versions.
# Let's inspect what files are present and how they relate.
