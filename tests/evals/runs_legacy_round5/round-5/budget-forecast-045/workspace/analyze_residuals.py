import csv

with open('expenses.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Detailed analysis and seasonal indices calculation
results = {}
for col in ['rent', 'food', 'transport']:
    vals = [float(row[col]) for row in data]
    n = len(vals)
    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(vals) / n
    slope = sum((x[i] - x_mean) * (vals[i] - y_mean) for i in range(n)) / sum((x[i] - x_mean) ** 2 for i in range(n))
    intercept = y_mean - slope * x_mean
    
    # Trend values for each historical month
    trends = [slope * i + intercept for i in range(n)]
    # Ratio to trend (multiplicative seasonal factor)
    ratios = [vals[i] / trends[i] for i in range(n)]
    
    # Month-specific seasonal index (average ratio for month index % 12, i.e., Jan = index 0, Feb = index 1, Mar = index 2)
    jan_ratios = [ratios[0], ratios[12] if 12 < n else ratios[0]] # we only have 1 year of data, so Jan is ratios[0]
    # Since we have exactly 12 months (Jan 2026 - Dec 2026), each month appears once.
    # To capture seasonality:
    # Notice in rent: Jan=1200, Feb=1150 (-50), Mar=1300 (+150), Apr=1250 (-50), May=1400 (+150)...
    # This is a repeating pattern of -50 in even/odd pairs or specific month oscillation!
    # Let's check the exact sequence of diffs: [-50, 150, -50, 150, -50, 150, -50, 150, -50, 150, -50]
    # Month 1 (Jan): 1200
    # Month 2 (Feb): 1150 (trend-50)
    # Month 3 (Mar): 1300 (trend+150)
    # Month 4 (Apr): 1250 (trend-50)
    # Month 5 (May): 1400 (trend+150)
    # Month 6 (Jun): 1350 (trend-50)
    # Month 7 (Jul): 1500 (trend+150)
    # Month 8 (Aug): 1450 (trend-50)
    # Month 9 (Sep): 1600 (trend+150)
    # Month 10 (Oct): 1550 (trend-50)
    # Month 11 (Nov): 1700 (trend+150)
    # Month 12 (Dec): 1650 (trend-50)
    
    # Wait, let's look at the residuals (Actual - Trend) for rent:
    residuals = [vals[i] - trends[i] for i in range(n)]
    print(f"--- {col} Residuals (Actual - Trend) ---")
    for i, r in enumerate(residuals):
        print(f"Month {i+1} ({data[i]['month']}): {r:.2f}")

