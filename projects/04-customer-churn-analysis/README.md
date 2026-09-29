# Customer Churn Analysis

**Dataset:** 10,300 rows x 10 columns, 10,000 after removing 300 duplicates.

**Key results:** Churn 76.34% (7,634 of 10,000 customers). Cleaning fixed inconsistent region and plan spellings, 700 missing payment methods, 995 missing and 44 invalid ages, 500 missing, 48 negative and 11 outlier spend values, and 50 negative service call counts. The notebook has no significance tests; the case study adds them.

**Case study:** `analysis.html` (problem, data, method, findings, recommendation, next steps).

**Files**
- `analysis.ipynb`: the Jupyter notebook. It reads `customer churn.csv`; the site's Dataset link downloads `data.csv` under that name.
- `analysis.html`: the case study page
- `data.csv`: the dataset

**Stack:** Python, Pandas, NumPy, Matplotlib, Jupyter
