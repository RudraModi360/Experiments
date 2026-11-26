import csv
import glob

# Let's inspect all invoices and decide how expenses.csv and summary.md should be structured.
# Files in invoices/:
# 1. inv1.txt: Acme Corp, 2026-01-15, $121.00, Supplies (INV-001)
# 2. inv2.txt: Beta LLC, 2026-02-03, $220.00, Services (INV-002)
# 3. inv3.txt: Acme Corp, 2026-01-15, $50.00, Supplies (INV-001 duplicate invoice number note)
# 4. inv_acme.txt: Acme Corp, 2026-01-15, $121.00, Office Supplies (INV-2026-001)
# 5. inv_acme_dup.txt: Acme Corp, 2026-01-15, $55.00, Office Supplies (INV-2026-001 duplicate invoice number note)
# 6. inv_beta.txt: Beta LLC, 2026-02-03, $220.00, Professional Services (INV-2026-002)

# Notice that inv1.txt and inv_acme.txt represent the exact same transaction ($121.00 on 2026-01-15 from Acme Corp).
# inv2.txt and inv_beta.txt represent the exact same transaction ($220.00 on 2026-02-03 from Beta LLC).
# inv3.txt and inv_acme_dup.txt are explicitly flagged as duplicates / notes.
# Wait, if there are 3 primary unique invoices (or if we include all), let's see:
# Unique valid transactions:
# - Acme Corp, 2026-01-15, $121.00, Office Supplies (or Supplies)
# - Beta LLC, 2026-02-03, $220.00, Professional Services (or Services)
# Wait, what about the 3rd? Is there a 3rd distinct invoice or is it inv3.txt ($50.00)? Or are inv1/inv2/inv3 one set of 3 invoices, and inv_acme/inv_acme_dup/inv_beta another?
# Let's check:
# Set 1: inv1.txt ($121), inv2.txt ($220), inv3.txt ($50) -> total 3 invoices in inv?.txt!
# Ah! "You are given 3 invoice text files in ./invoices/." -> inv1.txt, inv2.txt, inv3.txt!
# Wait, why are there 6 files in ./invoices/? Let's check directory listing again.
# list_files showed:
# inv1.txt (180B)
# inv2.txt (152B)
# inv3.txt (152B)
# inv_acme.txt (279B)
# inv_acme_dup.txt (260B)
# inv_beta.txt (252B)
# There are indeed 6 files in ./invoices/. But inv1/inv2/inv3 vs inv_acme/inv_acme_dup/inv_beta are parallel or overlapping sets.
# Let's examine what expenses.csv and summary.md should contain.
# If expenses.csv contains the valid expenses (e.g. Acme Corp $121.00, Beta LLC $220.00, and inv3 $50.00 or inv_acme / inv_beta), let's make sure expenses.csv has columns: vendor, date, amount, category.
# And summary.md should show:
# - Totals by vendor
# - Totals by category
# - Anomalies (e.g. duplicate invoice numbers, duplicate amounts/vendors, etc.)
