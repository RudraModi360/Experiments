import csv

with open('expenses.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

for col in ['rent', 'food', 'transport']:
    vals = [float(row[col]) for row in data]
    print(f"=== {col} monthly values ===")
    for i, v in enumerate(vals):
        m_num = i + 1
        print(f"Month {m_num:2d} ({data[i]['month']}): {v:6.1f}")
