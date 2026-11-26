import csv

expenses = [
    {"vendor": "Acme Corp", "date": "2026-01-15", "amount": 121.00, "category": "Office Supplies"},
    {"vendor": "Beta LLC", "date": "2026-02-03", "amount": 220.00, "category": "Professional Services"},
]

with open("expenses.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["vendor", "date", "amount", "category"])
    writer.writeheader()
    for row in expenses:
        writer.writerow(row)

print("expenses.csv created successfully.")
