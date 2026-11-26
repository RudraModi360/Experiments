import csv

with open('expenses.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

for col in ['rent', 'food', 'transport']:
    vals = [float(row[col]) for row in data]
    months = [row['month'] for row in data]
    print(f"--- {col} ---")
    for m, v in zip(months, vals):
        print(f"{m}: {v}")
    
    # Simple linear regression on index
    n = len(vals)
    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(vals) / n
    num = sum((x[i] - x_mean) * (vals[i] - y_mean) for i in range(n))
    den = sum((x[i] - x_mean) ** 2 for i in range(n))
    slope = num / den if den != 0 else 0
    intercept = y_mean - slope * x_mean
    print(f"Trend: slope = {slope:.2f}, intercept = {intercept:.2f}")
    
    # Differences or seasonality
    diffs = [vals[i] - vals[i-1] for i in range(1, n)]
    print(f"Diffs: {diffs}")
    print(f"Avg diff: {sum(diffs)/len(diffs):.2f}")
    print()
