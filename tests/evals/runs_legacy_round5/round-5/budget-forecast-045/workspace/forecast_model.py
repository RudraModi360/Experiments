import csv

with open('expenses.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Let's inspect year-over-year or month-matching patterns if available, or compute additive/multiplicative seasonality.
# Since we have Jan-Dec 2026, forecasting Jan-Mar 2027.
# Let's check historical Jan, Feb, Mar values in 2026:
# rent: Jan=1200, Feb=1150, Mar=1300
# food: Jan=300, Feb=320, Mar=290
# transport: Jan=150, Feb=140, Mar=160

# Let's check trend + seasonal decomposition or simple linear projection + seasonal adjustment factor.
# For each category, let's look at linear regression trend values for months 13, 14, 15 (2027-01, 2027-02, 2027-03).
import math

for col in ['rent', 'food', 'transport']:
    vals = [float(row[col]) for row in data]
    n = len(vals)
    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(vals) / n
    slope = sum((x[i] - x_mean) * (vals[i] - y_mean) for i in range(n)) / sum((x[i] - x_mean) ** 2 for i in range(n))
    intercept = y_mean - slope * x_mean
    
    print(f"=== {col} ===")
    print(f"Linear Trend formula: y = {slope:.4f} * x + {intercept:.4f}")
    
    # Forecast months 13, 14, 15 (indices 12, 13, 14)
    for step, m_str in enumerate(['2027-01', '2027-02', '2027-03'], start=13):
        trend_val = slope * (step - 1) + intercept
        # Seasonal factor: ratio or difference compared to trend
        print(f"  {m_str} (Month {step}): trend forecast = {trend_val:.2f}")

