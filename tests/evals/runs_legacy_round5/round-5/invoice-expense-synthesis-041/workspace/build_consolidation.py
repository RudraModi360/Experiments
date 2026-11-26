import csv

# Let's define the exact contents of expenses.csv and summary.md.
# Which invoices should be in expenses.csv?
# Let's analyze all 6 invoice files:
# 1. inv1.txt: Acme Corp, 2026-01-15, $121.00, Supplies (INV-001)
# 2. inv2.txt: Beta LLC, 2026-02-03, $220.00, Services (INV-002)
# 3. inv3.txt: Acme Corp, 2026-01-15, $50.00, Supplies (INV-001, duplicate invoice number note)
# 4. inv_acme.txt: Acme Corp, 2026-01-15, $121.00, Office Supplies (INV-2026-001)
# 5. inv_acme_dup.txt: Acme Corp, 2026-01-15, $55.00, Office Supplies (INV-2026-001 duplicate invoice number note)
# 6. inv_beta.txt: Beta LLC, 2026-02-03, $220.00, Professional Services (INV-2026-002)

# Notice that inv1.txt and inv_acme.txt are essentially the same invoice (Acme Corp, 2026-01-15, $121.00), differing only in invoice number (INV-001 vs INV-2026-001) and category (Supplies vs Office Supplies).
# Similarly, inv2.txt and inv_beta.txt are the same invoice ($220.00, Beta LLC, 2026-02-03), differing in invoice number (INV-002 vs INV-2026-002) and category (Services vs Professional Services).
# And inv3.txt and inv_acme_dup.txt are duplicate/partial invoice notes ($50.00 and $55.00).
# Wait, if we consolidate all valid unique expenses, or all distinct invoice files, what is standard?
# Let's check if we include the canonical / most detailed records or all records.
# If we include all valid unique transactions (Acme Corp $121.00, Beta LLC $220.00, and inv3 $50.00 or similar), or if we list the primary records.
# Wait, let's examine what happens if we include the primary formal invoices (inv_acme.txt, inv_beta.txt) and the additional records or if we include all files.
# Let's write a python script to build expenses.csv and summary.md and check totals and anomalies.
