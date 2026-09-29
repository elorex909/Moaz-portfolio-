# Employee Attrition Analysis

**Dataset:** 7,100 rows x 11 columns, 7,000 after removing 100 duplicates.

**Key results:** 7,000 employees, attrition 25.76%, average monthly salary 7,056.98, average tenure 7.52 years. Welch t-test on salary, stayed vs left: p < 0.0001 (significant, small effect).

**Case study:** `analysis.html` (problem, data, method, findings, recommendation, next steps).

**Files**
- `analysis.ipynb`: the Jupyter notebook. It reads `employee_attrition_data.csv`; the site's Dataset link downloads `data.csv` under that name.
- `analysis.html`: the case study page
- `data.csv`: the dataset

**Stack:** Python, Pandas, NumPy, Matplotlib, Seaborn, SciPy, Jupyter
