# Retail Sales Performance Analysis

**Dataset:** 6,120 rows x 10 columns, 6,000 after removing 120 duplicates.

**Key results:** Total sales 2,367,685.40, total profit 737,857.60, 6,000 orders, average order value 394.61, average margin 30.94% (mean of per-order margins; total profit over total sales is 31.16%). Welch t-test on profit per order, discounted vs full price: p = 0.0015 (significant, small effect).

**Case study:** `analysis.html` (problem, data, method, findings, recommendation, next steps).

**Files**
- `analysis.ipynb`: the Jupyter notebook. It reads `retail_sales_data.csv`; the site's Dataset link downloads `data.csv` under that name.
- `analysis.html`: the case study page
- `data.csv`: the dataset

**Stack:** Python, Pandas, NumPy, Matplotlib, Seaborn, SciPy, Jupyter
