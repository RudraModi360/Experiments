# Expense Forecast Report (Jan-Mar 2027)

## Executive Summary
This report provides a 3-month expense forecast for **January, February, and March 2027**, based on 12 months of historical data from **January to December 2026** (`expenses.csv`). Using a combination of ordinary least squares (OLS) linear regression for trend analysis and historical residual analysis for seasonal/cyclical adjustments, the forecast projects expected outlays across three core categories: **Rent**, **Food**, and **Transport**.

---

## Historical Data Overview & Trend Analysis
An analysis of the 2026 monthly expense data reveals consistent upward linear trends across all categories, paired with distinct recurring monthly fluctuations.

### 1. Rent
- **Historical Trend:** Upward linear trend with an average monthly growth rate (slope) of approximately **+$47.90 per month**. Starting at $1,200.00 in January 2026, rent grew steadily to reach $1,727.27 by December 2026 (baseline trend).
- **Seasonality & Patterns:** Rent exhibits a strong, regular alternating monthly fluctuation pattern. Compared to the baseline trend line, even-numbered months (e.g., Feb, Apr, Jun) consistently dip by ~$50, while odd-numbered months (e.g., Mar, May, Jul) peak by ~$150. This creates a cyclical wave on top of the upward trend.

### 2. Food
- **Historical Trend:** Upward linear trend with an average monthly growth rate of approximately **+$4.51 per month**. 
- **Seasonality & Patterns:** Food expenses fluctuate moderately around the trend line (ranging roughly between $300 and $380), driven by monthly variations in grocery shopping frequency and dining habits.

### 3. Transport
- **Historical Trend:** Upward linear trend with an average monthly growth rate of approximately **+$4.95 per month**.
- **Seasonality & Patterns:** Transport expenses show recurring month-to-month patterns reflecting seasonal commuting and fuel price fluctuations.

---

## Methodology & Forecasting Approach
To project expenses for **Jan–Mar 2027** (Months 13, 14, and 15):
1. **Trend Projection:** Linear regression equations ($y = \text{slope} \times x + \text{intercept}$) were fitted to the 2026 historical monthly data for each category to capture baseline growth.
2. **Seasonal Adjustment:** Residuals (actual historical value minus trend value) were calculated for each month. The residual from the corresponding month in 2026 (Month 1 for January, Month 2 for February, Month 3 for March) was added to the projected trend value to account for recurring seasonal effects.

---

## 3-Month Forecast Summary (Jan–Mar 2027)

The resulting forecasts saved in `forecast.csv` are summarized below:

| Month | Rent ($) | Food ($) | Transport ($) | Total Expenses ($) |
| :--- | :---: | :---: | :---: | :---: |
| **2027-01** (Month 13) | 1,774.83 | 354.13 | 209.37 | **2,338.33** |
| **2027-02** (Month 14) | 1,724.83 | 374.13 | 199.37 | **2,298.33** |
| **2027-03** (Month 15) | 1,874.83 | 344.13 | 219.37 | **2,438.33** |

---

## Underlying Assumptions
1. **Continuation of Macro Trends:** The linear growth rates observed across 2026 (rent increases, inflationary pressures on food and transport) will continue at similar average rates through the first quarter of 2027.
2. **Repeating Seasonality:** The cyclical variations observed in 2026 (such as rent adjustments and monthly transport/food spending habits) repeat predictably in the corresponding months of 2027.
3. **External Stability:** No extraordinary one-time events (such as sudden major relocation, fuel shocks, or unexpected regulatory rent freezes) occur during Q1 2027.
