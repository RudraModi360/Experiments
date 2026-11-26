import csv

# Load historical data
with open('expenses.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

months_to_forecast = ['2027-01', '2027-02', '2027-03']
forecasts = {}

for col in ['rent', 'food', 'transport']:
    vals = [float(row[col]) for row in data]
    n = len(vals)
    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(vals) / n
    slope = sum((x[i] - x_mean) * (vals[i] - y_mean) for i in range(n)) / sum((x[i] - x_mean) ** 2 for i in range(n))
    intercept = y_mean - slope * x_mean
    
    trends = [slope * i + intercept for i in range(n)]
    residuals = [vals[i] - trends[i] for i in range(n)]
    
    col_forecasts = []
    for step_idx, m_str in enumerate(months_to_forecast):
        month_index_in_year = step_idx # 0 for Jan, 1 for Feb, 2 for Mar
        absolute_month_idx = n + step_idx # 12, 13, 14
        trend_val = slope * absolute_month_idx + intercept
        seasonal_adj = residuals[month_index_in_year]
        fc = trend_val + seasonal_adj
        col_forecasts.append(round(fc, 2))
    
    forecasts[col] = col_forecasts

print("Forecast results by category:")
for col, fc_list in forecasts.items():
    print(f"  {col}: {fc_list}")

# Write forecast.csv
with open('forecast.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['month', 'rent', 'food', 'transport'])
    for i, m_str in enumerate(months_to_forecast):
        writer.writerow([m_str, forecasts['rent'][i], forecasts['food'][i], forecasts['transport'][i]])

print("forecast.csv generated successfully.")
