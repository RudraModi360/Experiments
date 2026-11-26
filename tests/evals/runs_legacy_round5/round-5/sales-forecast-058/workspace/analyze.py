import csv

with open('sales.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for r in rows:
    print(r)

sales = [float(r['sales']) for r in rows]
diffs = [sales[i] - sales[i-1] for i in range(1, len(sales))]
print("Differences (month over month):", diffs)
print("Unique diffs:", set(diffs))
