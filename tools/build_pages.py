#!/usr/bin/env python3
"""
Build the Featured projects section (index.html) and the four case-study pages.

Every number comes from tools/numbers.json, which tools/build_project_assets.py
computes from projects/*/data.csv. Run that script first, then this one:

    python3 tools/build_project_assets.py && python3 tools/build_pages.py

Anything the files cannot tell us is written as a TODO (class "todo") and listed
at the end of the run.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
N = json.loads((ROOT / "tools" / "numbers.json").read_text())
R, A, M, C = N["retail"], N["attrition"], N["marketing"], N["churn"]
TODOS = []


# ------------------------------------------------------------------ helpers
def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def n2(x): return f"{x:,.2f}"
def sg(x): return n2(x).replace("-", "\u2212")
def pc(x, d=1): return f"{x:.{d}f}%"


def pv(p):
    if p < 0.0001: return "p < 0.0001"
    if p < 0.01: return f"p = {p:.4f}"
    return f"p = {p:.2f}"


def esc(s): return html.escape(s, quote=True)


def todo(text, slug):
    TODOS.append((slug, text))
    return f'<span class="todo">TODO for Moaz: {esc(text)}</span>'


def v_word(v):
    return "weak" if v < 0.10 else "moderate"


def d_word(d):
    d = abs(d)
    return "small" if d < 0.2 else ("small to medium" if d < 0.5 else "medium or larger")


def badge(ok, text):
    return f'<span class="badge {"ok" if ok else "no"}">{esc(text)}</span>'


def tests_table(rows, caption):
    """rows: (question, result, test, source, p, sig_bool, effect_text)"""
    body = ""
    for q, res, test, src, p, sig, eff in rows:
        verdict = badge(sig, "Significant" if sig else "Not significant")
        body += (f"<tr><td>{q}</td><td>{res}</td><td>{test} <span class='badge'>{src}</span></td>"
                 f"<td class='n'>{pv(p)}</td><td>{verdict} {eff}</td></tr>")
    return (f'<div class="tw"><table><caption>{caption}</caption><thead><tr><th>Question</th><th>Result</th>'
            f'<th>Test</th><th class="n">p-value</th><th>Verdict</th></tr></thead><tbody>{body}</tbody></table></div>')


def table(head, rows, caption, num_cols=()):
    th = "".join(f'<th class="{"n" if i in num_cols else ""}">{h}</th>' for i, h in enumerate(head))
    tr = "".join("<tr>" + "".join(f'<td class="{"n" if i in num_cols else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tw"><table><caption>{caption}</caption><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def facts(pairs):
    return "<dl class='facts'>" + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in pairs) + "</dl>"


def fig(prefix, chart, alt, caption=None):
    c = chart
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure class="shot"><img src="{prefix}{c["file"]}" width="{c["width"]}" height="{c["height"]}" '
            f'alt="{esc(alt)}" loading="lazy">{cap}</figure>')


def pills(items):
    return '<div class="pills tools">' + "".join(f'<span class="pill">{esc(i)}</span>' for i in items) + "</div>"


def stats3(items):
    return '<div class="stats3">' + "".join(f"<div><b>{b}</b><span>{esc(s)}</span></div>" for b, s in items) + "</div>"


def callout(label, inner):
    return f'<div class="callout"><span class="lab">{label}</span>{inner}</div>'


def ol(items): return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"
def ul(items): return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def panel(title, body):
    return (f'<section class="cs"><div class="glass cs-panel" data-title="{esc(title)}">'
            f'<h2>{esc(title)}</h2>{body}</div></section>')


TOOLS_FULL = ["Python", "Pandas", "NumPy", "Matplotlib", "Seaborn", "SciPy", "Jupyter"]
# The churn notebook imports seaborn and scipy but never calls them, so they are not listed.
TOOLS_CHURN = ["Python", "Pandas", "NumPy", "Matplotlib", "Jupyter"]

ORDER = ["retail", "attrition", "marketing", "churn"]
META = {
    "retail": dict(dir="01-retail-sales-performance-analysis", title="Retail Sales Performance Analysis", match="Game 1",
                   csv_name="retail_sales_data.csv", tools=TOOLS_FULL),
    "attrition": dict(dir="02-employee-attrition-analysis", title="Employee Attrition Analysis", match="Game 2",
                      csv_name="employee_attrition_data.csv", tools=TOOLS_FULL),
    "marketing": dict(dir="03-marketing-campaign-performance-analysis", title="Marketing Campaign Performance Analysis",
                      match="Game 3", csv_name="marketing_campaign_data.csv", tools=TOOLS_FULL),
    "churn": dict(dir="04-customer-churn-analysis", title="Customer Churn Analysis", match="Game 4",
                  csv_name="customer churn.csv", tools=TOOLS_CHURN),
}

# ------------------------------------------------------------------ derived numbers
rd = R["by_discount"]
ret = dict(
    sales=R["total_sales"], orders=R["orders"], el=R["electronics"], pt=R["profit_test"], mt=R["margin_test_added"],
    imp=R["imputation_check_added"],
)
ot = A["by_overtime"]
ot_leaver_share = ot["Yes"]["left"] / A["left"] * 100
sat = A["by_satisfaction"]
dept = A["by_department"]
named_dept = {k: v for k, v in dept.items() if k != "Unknown"}
d_lo = min(named_dept.values(), key=lambda v: v["rate"])["rate"]
d_hi = max(named_dept.values(), key=lambda v: v["rate"])["rate"]
ch = M["by_channel"]
named_ch = {k: v for k, v in ch.items() if k != "Unknown"}
dv = M["by_device"]
named_dv = {k: v for k, v in dv.items() if k != "Unknown"}
eg = M["by_engagement"]
cd = C["by_days"]
cc = C["by_calls"]
cp = C["by_plan"]
nt = C["num_tests"]

# ------------------------------------------------------------------ card + page content
CARDS = {}
PAGES = {}

# ---------------- retail
CARDS["retail"] = dict(
    problem="Where does the money come from, and do discounts pay for themselves?",
    decision=(f"Keep Electronics at the centre, since it brings {pc(ret['el']['sales_share'])} of sales from "
              f"{pc(ret['el']['order_share'])} of orders. Review discounts before extending them: discounted orders earn "
              f"{n2(ret['pt']['diff'])} less profit each, though margin stays flat."),
    stats=[(f"{R['total_sales'] / 1e6:.2f}M", f"Total sales from {n0(R['orders'])} orders"),
           (pc(ret["el"]["sales_share"]), "Of sales come from Electronics"),
           (n2(ret["pt"]["diff"]), f"Less profit per discounted order ({pv(ret['pt']['p'])})")],
    chart=R["charts"]["sales-by-category"],
    alt=("Horizontal bar chart of share of total sales by category: Electronics "
         f"{pc(R['category_share']['Electronics'])}, Home {pc(R['category_share']['Home'])}, Sports "
         f"{pc(R['category_share']['Sports'])}, Clothing {pc(R['category_share']['Clothing'])}, Beauty "
         f"{pc(R['category_share']['Beauty'])}, no category recorded {pc(R['category_share']['Unknown'])}."),
)

bd_rows = [[("No discount" if k == "0" else f"{k}% off"), n0(v["n"]), n2(v["qty"]), n2(v["cost"]), n2(v["profit"]), pc(v["margin"], 2)]
           for k, v in rd.items()]
margins = [v["margin"] for v in rd.values()]
qtys = [v["qty"] for v in rd.values()]
prices = [v["price"] for v in rd.values()]
PAGES["retail"] = dict(
    lede="I checked where a retail business earns its money and whether its discounts pay for themselves.",
    summary_rec=("Keep Electronics at the centre of the plan and review discounts before extending them. "
                 "Confirm how Cost is defined first."),
    sections=[
        ("Problem", f"""
<p>The dataset covers five product categories across four regions. Two questions decide where a retailer puts its effort: which categories and regions carry the profit, and whether discounting pays for itself.</p>
<p>The files contain no client brief, so these questions come from the notebook's own list of business insights: the strongest categories and regions, sales trends, and how discount levels relate to profit.</p>"""),
        ("Data", facts([
            ("Source", todo("say where this dataset comes from and how it was collected; the notebook does not say", "retail")),
            ("Size", f"{n0(R['raw_rows'])} rows and {R['raw_cols']} columns. {n0(R['orders'])} unique orders remain after removing {R['duplicates']} duplicate rows."),
            ("Period", f"1 Jan 2024 to 30 Jun 2025 ({R['months']} months)."),
            ("Columns", "Order_ID, Order_Date, Region, Category, Product, Quantity, Unit_Price, Discount, Sales, Cost"),
            ("Quality problems", f"Before cleaning: {R['missing']['Region']} missing regions, {R['missing']['Category']} missing categories, {R['missing']['Unit_Price']} missing unit prices and {R['missing']['Sales']} missing sales values. {R['qty_le0_raw']} orders have a quantity of zero or below, and {R['sales_le0_raw']} have sales of zero or below."),
            ("Discounts", "Five levels: 0%, 5%, 10%, 15% and 20%."),
            ("Currency", todo("state the currency of Sales, Cost and Unit_Price; the files give none", "retail")),
        ])),
        ("Method", ol([
            f"Removed {R['duplicates']} duplicate rows, then trimmed and standardised the text in Region, Category and Product.",
            f"Filled missing regions and categories with \"Unknown\" ({R['unknown_region_orders']} and {R['unknown_category_orders']} orders).",
            f"Replaced invalid or missing values with the column median: {R['qty_le0_after_dedup']} quantities, {R['unit_price_replaced']} unit prices and {R['sales_replaced']} sales values.",
            "Added Profit (Sales minus Cost), Profit_Margin (profit as a percentage of sales), and month and quarter columns.",
            "Compared sales by category, profit by region, monthly sales, and margin by discount level.",
            "Tested whether discounted orders earn a different profit per order than full-price orders, using Welch's t-test, which does not assume equal variances.",
            "Added two checks the notebook does not contain: the same test on margin percentage, and a check of how median-filling affects the results.",
        ])),
        ("What I found", f"""
<h3>Electronics carries the business</h3>
<p>Electronics brings <strong>{pc(ret['el']['sales_share'])} of sales</strong> ({R['category_sales']['Electronics'] / 1e6:.2f}M) from {pc(ret['el']['order_share'])} of orders. An average Electronics order is worth {n2(ret['el']['avg_order'])}, against {n2(ret['el']['others_avg_order'])} for every other category. Its share of profit ({pc(ret['el']['profit_share'])}) is close to its share of sales, so the advantage comes from order size, not margin.</p>
{fig('../../', R['charts']['sales-by-category'], CARDS['retail']['alt'], f"Electronics dominates sales. The {pc(R['category_share']['Unknown'])} bar for no category comes from {R['unknown_category_orders']} orders with a missing category.")}
<h3>Discounts lower profit per order, but not the margin</h3>
<p>Most orders carry a discount: {n0(R['discount_orders'])} of {n0(R['orders'])} ({pc(R['discount_share_orders'])}). Discounted orders earn {n2(ret['pt']['mean_b'])} profit on average, against {n2(ret['pt']['mean_a'])} for full-price orders. That is <strong>{n2(ret['pt']['diff'])} less per order</strong> (95% confidence interval {n2(ret['pt']['ci_low'])} to {n2(ret['pt']['ci_high'])}; Welch's t-test, {pv(ret['pt']['p'])}). The effect is small: the gap is about {ret['pt']['diff'] / ret['pt']['mean_a'] * 100:.0f}% of full-price profit, and Cohen's d is {abs(ret['pt']['cohens_d']):.2f}.</p>
<p>Margin tells a different story. Average margin stays near 31% at every discount level ({pc(min(margins))} to {pc(max(margins))}). The gap between discounted and full-price orders is {abs(ret['mt']['diff']):.2f} points ({pv(ret['mt']['p'])}), so I found no margin effect. Discounts also do not lift order size: average quantity stays between {n2(min(qtys))} and {n2(max(qtys))} items at every level.</p>
{fig('../../', R['charts']['margin-by-discount'], f"Bar chart of average profit margin by discount level, all close to 31%: no discount {pc(rd['0']['margin'])}, 5% off {pc(rd['5']['margin'])}, 10% off {pc(rd['10']['margin'])}, 15% off {pc(rd['15']['margin'])}, 20% off {pc(rd['20']['margin'])}.", "Margin percentage does not move with the discount level.")}
{table(["Discount", "Orders", "Avg quantity", "Avg cost", "Avg profit", "Avg margin"], bd_rows, "Orders by discount level (averages per order)", num_cols=(1, 2, 3, 4, 5))}
{callout("Check before you trust this", f"<p>Average cost per order falls from {n2(rd['0']['cost'])} with no discount to {n2(rd['20']['cost'])} at 20% off, although average unit price stays between {n2(min(prices))} and {n2(max(prices))}. A discount changes the selling price, not what the item cost, so this pattern suggests Cost may be calculated from the discounted sales value. The files cannot confirm that, and it would explain why margin never moves.</p><p>{todo('explain how the Cost column was calculated', 'retail')}</p>")}
<h3>Regions are close, and sales are flat</h3>
<p>Profit by region ranges from {n0(R['region']['West']['profit'])} (West) to {n0(R['region']['North']['profit'])} (North). I did not test whether that gap is real, so I would not act on it. Monthly sales range from {n0(R['month_min']['sales'])} (Feb 2025) to {n0(R['month_max']['sales'])} (Apr 2025). The first half of 2025 ({n0(R['h1_2025_sales'])}) is level with the first half of 2024 ({n0(R['h1_2024_sales'])}), a change of {R['h1_change_pct']:+.1f}%. With {R['months']} months of data I cannot separate seasonality from noise.</p>
{fig('../../', R['charts']['monthly-sales'], f"Line chart of monthly sales from January 2024 to June 2025. Sales move between {n0(R['month_min']['sales'])} in February 2025 and {n0(R['month_max']['sales'])} in April 2025, with no steady upward or downward trend.", "Monthly sales move within a band and show no clear trend.")}
{callout("Where this analysis is weak", f"<p><strong>Filled sales values.</strong> The notebook replaced {ret['imp']['rows_imputed']} sales values ({pc(ret['imp']['share_pct'])} of orders) with the median, {n2(ret['imp']['median_used'])}. All {ret['imp']['negative_profit_rows']} orders that show a negative profit come from these filled values. Without them, average margin is {pc(ret['imp']['avg_margin_not_imputed'], 2)} instead of {pc(ret['imp']['avg_margin_all'], 2)}, and Electronics margin is {pc(ret['imp']['electronics_margin_not_imputed'], 2)} instead of {pc(ret['imp']['electronics_margin_all'], 2)}. The margin shown on the projects page, {pc(R['avg_margin'])}, is the notebook's figure as written.</p><p><strong>A better fill exists.</strong> In the {n0(ret['imp']['sales_formula_rows'])} orders where quantity, unit price and discount are all valid, Sales equals quantity × unit price × (1 − discount) every time. A formula would fill the gaps better than the median.</p><p><strong>Small effect.</strong> The discount result is statistically significant but small, and the sample covers only {R['months']} months.</p>")}
{tests_table([
    ("Profit per order, discounted vs full price", f"{n2(ret['pt']['mean_b'])} vs {n2(ret['pt']['mean_a'])}", "Welch t-test", "Notebook", ret['pt']['p'], True, f"Small effect (d = {abs(ret['pt']['cohens_d']):.2f})"),
    ("Margin percentage, discounted vs full price", f"{pc(ret['mt']['mean_b'], 2)} vs {pc(ret['mt']['mean_a'], 2)}", "Welch t-test", "Added", ret['mt']['p'], False, ""),
], "Statistical tests. \"Notebook\" means the test is in the notebook; \"Added\" means I added it.")}"""),
        ("Recommendation", ol([
            f"<strong>Treat Electronics as the core line.</strong> It brings {pc(ret['el']['sales_share'])} of sales, so track its monthly sales and stock first.",
            f"<strong>Do not extend discounts on this evidence.</strong> Discounted orders earn about {ret['pt']['diff'] / ret['pt']['mean_a'] * 100:.0f}% less profit per order and do not bring bigger baskets. Test a smaller discount on a few products before changing anything.",
            "<strong>Confirm how Cost is defined</strong> before drawing any conclusion about discount margins.",
        ])),
        ("What I would do next", ul([
            "Recompute Sales from quantity, unit price and discount instead of using the median, then rerun every figure.",
            "Split the discount test by category to see whether Electronics behaves differently.",
            "Test the regional profit gap, for example with a one-way ANOVA on profit per order.",
            "Look at profit by product; the file lists 20 products.",
            "Repeat the analysis on more than 18 months of data to check for seasonality.",
        ])),
    ],
    summary=[(f"{R['total_sales'] / 1e6:.2f}M", f"Total sales from {n0(R['orders'])} orders"),
             (pc(ret["el"]["sales_share"]), f"Of sales from Electronics, on {pc(ret['el']['order_share'])} of orders"),
             (n2(ret["pt"]["diff"]), f"Less profit per discounted order ({pv(ret['pt']['p'])}, small effect)")],
)

# ---------------- attrition
CARDS["attrition"] = dict(
    problem="Who leaves, and which factors can HR change?",
    decision=(f"Start with overtime and low satisfaction. {pc(ot['Yes']['rate'])} of people who work overtime left, "
              f"against {pc(ot['No']['rate'])} of those who do not. Department and remote work show no difference."),
    stats=[(pc(A["attrition_rate"]), f"Left the company: {n0(A['left'])} of {n0(A['employees'])} employees"),
           (f"+{A['overtime_gap_pp']:.1f} pts", "Higher attrition with overtime"),
           (pc(A["salary_test"]["diff_pct_of_stayed"]), "Lower pay for leavers (small effect)")],
    chart=A["charts"]["attrition-by-overtime"],
    alt=(f"Bar chart of attrition rate by overtime: {pc(ot['Yes']['rate'])} for employees who work overtime "
         f"({n0(ot['Yes']['n'])} people) and {pc(ot['No']['rate'])} for those who do not ({n0(ot['No']['n'])} people), "
         f"with a dashed line at the company rate of {pc(A['attrition_rate'])}."),
)
st = A["salary_test"]
ca = A["chi_added"]
lo, hi = A["sat_low_vs_high_added"], None
PAGES["attrition"] = dict(
    lede="I looked for what separates employees who leave from those who stay, and which of those factors an HR team could change.",
    summary_rec="Start with overtime and low satisfaction. Department, remote work and job level show no difference.",
    sections=[
        ("Problem", f"""
<p>The dataset covers {n0(A['employees'])} employees, and {pc(A['attrition_rate'])} of them left. The question: who leaves, and which factors could HR change?</p>
<p>The files contain no brief, so the questions come from the notebook's own insight list: compare attrition across departments, examine overtime and job satisfaction as possible indicators, and compare the salaries of employees who left and stayed.</p>"""),
        ("Data", facts([
            ("Source", todo("say where this dataset comes from; the notebook does not say", "attrition")),
            ("Size", f"{n0(A['raw_rows'])} rows and {A['raw_cols']} columns. {n0(A['employees'])} unique employees remain after removing {A['duplicates']} duplicate rows."),
            ("Columns", "Employee_ID, Department, Job_Level, Age, Years_At_Company, Monthly_Salary, Overtime, Job_Satisfaction (1 to 5), Training_Hours, Remote_Work, Attrition (1 = left, 0 = stayed)"),
            ("Quality problems", f"Before cleaning: {A['missing']['Department']} missing departments, {A['missing']['Monthly_Salary']} missing salaries and {A['missing']['Job_Satisfaction']} missing satisfaction scores. {A['invalid_age_raw']} ages fall outside 18 to 100, and the lowest is −7."),
            ("Definitions", todo("explain what Overtime and Attrition measure, and over what period employees left; the files do not say", "attrition")),
            ("Currency", todo("state the currency of Monthly_Salary; the files give none", "attrition")),
        ])),
        ("Method", ol([
            f"Removed {A['duplicates']} duplicate rows and standardised the text in Department, Job_Level, Overtime and Remote_Work.",
            f"Filled {A['missing_dept_after_dedup']} missing departments with \"Unknown\". Replaced {A['invalid_age_after_dedup']} invalid ages, {A['missing_salary_after_dedup']} missing salaries and {A['missing_sat_after_dedup']} missing satisfaction scores with the column median.",
            "Added age, tenure and salary bands.",
            "Compared attrition by department, overtime and satisfaction score, and salary by outcome.",
            "Tested the salary gap between leavers and stayers with Welch's t-test, the notebook's test.",
            "Added checks the notebook does not contain: chi-square tests for each category, effect sizes, and 95% confidence ranges for each department.",
        ])),
        ("What I found", f"""
<h3>Overtime shows the clearest gap</h3>
<p><strong>{pc(ot['Yes']['rate'])} of employees who work overtime left</strong> ({n0(ot['Yes']['left'])} of {n0(ot['Yes']['n'])}), against {pc(ot['No']['rate'])} of those who do not ({n0(ot['No']['left'])} of {n0(ot['No']['n'])}). That is {A['overtime_gap_pp']:.1f} percentage points more. Overtime staff make up {pc(A['overtime_share_pct'])} of employees but {pc(ot_leaver_share)} of leavers. Chi-square test: {pv(ca['Overtime']['p'])}, Cramér's V = {ca['Overtime']['cramers_v']:.2f}, a {v_word(ca['Overtime']['cramers_v'])} link.</p>
{fig('../../', A['charts']['attrition-by-overtime'], CARDS['attrition']['alt'])}
<h3>Low satisfaction adds a weaker signal</h3>
<p>Attrition is {pc(sat['1.0']['rate'])} at satisfaction score 1 and {pc(sat['2.0']['rate'])} at score 2, then drops to {pc(sat['3.0']['rate'])}, {pc(sat['4.0']['rate'])} and {pc(sat['5.0']['rate'])} for scores 3 to 5. Scores 1 and 2 together give {pc(lo['low_rate'])} ({n0(lo['low_n'])} employees), against {pc(lo['high_rate'])} for scores 3 to 5 ({n0(lo['high_n'])}). The link is real ({pv(ca['Job_Satisfaction']['p'])}) but weak (V = {ca['Job_Satisfaction']['cramers_v']:.2f}), and it looks like a step at score 3, not a smooth slope.</p>
{fig('../../', A['charts']['attrition-by-satisfaction'], f"Bar chart of attrition rate by job satisfaction score from 1 (lowest) to 5 (highest): {pc(sat['1.0']['rate'])}, {pc(sat['2.0']['rate'])}, {pc(sat['3.0']['rate'])}, {pc(sat['4.0']['rate'])} and {pc(sat['5.0']['rate'])}. Scores 1 and 2 are above the company rate of {pc(A['attrition_rate'])}.")}
<h3>Pay differs, but only a little</h3>
<p>Employees who left earned {n2(st['mean_b'])} a month on average, against {n2(st['mean_a'])} for those who stayed. That is {n2(st['diff'])} less, or {pc(st['diff_pct_of_stayed'])} (95% confidence interval {n2(st['ci_low'])} to {n2(st['ci_high'])}; Welch's t-test, {pv(st['p'])}). Cohen's d is {st['cohens_d']:.2f}, a {d_word(st['cohens_d'])} effect, so pay explains little on its own.</p>
<h3>Department, remote work and job level make no difference</h3>
<p>Across the six named departments, attrition ranges from {pc(d_lo)} to {pc(d_hi)}. The 95% confidence ranges overlap, and the chi-square test finds no difference ({pv(ca['Department']['p'])}). Remote work shows none either: {pc(A['by_remote']['No']['rate'])} for on-site staff and {pc(A['by_remote']['Yes']['rate'])} for remote staff ({pv(ca['Remote_Work']['p'])}). Job level ranges from {pc(min(v['rate'] for v in A['by_level'].values()))} to {pc(max(v['rate'] for v in A['by_level'].values()))} ({pv(ca['Job_Level']['p'])}); Engineers are highest, but the gap is not significant. Tenure ({A['other_tests_added']['Years_At_Company']['stayed']:.2f} vs {A['other_tests_added']['Years_At_Company']['left']:.2f} years, {pv(A['other_tests_added']['Years_At_Company']['p'])}), age ({pv(A['other_tests_added']['Age']['p'])}) and training hours ({pv(A['other_tests_added']['Training_Hours']['p'])}) do not separate leavers either.</p>
{fig('../../', A['charts']['attrition-by-department'], "Horizontal bar chart of attrition rate by department with 95% confidence ranges: " + ", ".join(f"{k if k not in ('Hr','It') else k.upper()} {pc(v['rate'])}" for k, v in sorted(dept.items(), key=lambda kv: -kv[1]['rate'])) + f". All ranges overlap the company rate of {pc(A['attrition_rate'])}.", "Every department's range overlaps the company rate, so the ranking is not reliable.")}
{tests_table([
    ("Salary, stayed vs left", f"{n2(st['mean_a'])} vs {n2(st['mean_b'])}", "Welch t-test", "Notebook", st['p'], True, f"Small effect (d = {st['cohens_d']:.2f})"),
    ("Overtime", f"{pc(ot['Yes']['rate'])} vs {pc(ot['No']['rate'])}", "Chi-square", "Added", ca['Overtime']['p'], True, f"{v_word(ca['Overtime']['cramers_v']).capitalize()} (V = {ca['Overtime']['cramers_v']:.2f})"),
    ("Job satisfaction, scores 1 to 5", f"{pc(min(v['rate'] for v in sat.values()))} to {pc(max(v['rate'] for v in sat.values()))}", "Chi-square", "Added", ca['Job_Satisfaction']['p'], True, f"{v_word(ca['Job_Satisfaction']['cramers_v']).capitalize()} (V = {ca['Job_Satisfaction']['cramers_v']:.2f})"),
    ("Department", f"{pc(d_lo)} to {pc(d_hi)}", "Chi-square", "Added", ca['Department']['p'], False, ""),
    ("Job level", f"{pc(min(v['rate'] for v in A['by_level'].values()))} to {pc(max(v['rate'] for v in A['by_level'].values()))}", "Chi-square", "Added", ca['Job_Level']['p'], False, ""),
    ("Remote work", f"{pc(A['by_remote']['No']['rate'])} vs {pc(A['by_remote']['Yes']['rate'])}", "Chi-square", "Added", ca['Remote_Work']['p'], False, ""),
], "Statistical tests. Effect size: Cramér's V under 0.10 is weak and 0.10 to 0.30 is moderate; Cohen's d under 0.2 is small.")}
{callout("Where this analysis is weak", f"<p><strong>No cause.</strong> The data is a single snapshot with no dates. Overtime, low satisfaction and leaving may all move together for other reasons. Nothing here shows that overtime makes people leave.</p><p><strong>Overlap.</strong> I did not check whether the employees who work overtime are also the unhappy ones, so the two effects may partly be one.</p><p><strong>Big sample, small gaps.</strong> With {n0(A['employees'])} employees, even a {pc(st['diff_pct_of_stayed'])} pay gap is significant. I report the effect size next to every p-value for that reason.</p><p><strong>Filled values.</strong> {A['missing_dept_after_dedup']} employees have no department, and {A['invalid_age_after_dedup']} ages were replaced with the median.</p>")}"""),
        ("Recommendation", ol([
            f"<strong>Review overtime first.</strong> Overtime staff are {pc(A['overtime_share_pct'])} of employees but {pc(ot_leaver_share)} of leavers. Find out which teams and roles carry the most overtime, and whether it is required or voluntary.",
            f"<strong>Add a satisfaction check-in</strong> for employees who score 1 or 2. Their attrition is {pc(lo['low_rate'])}.",
            "<strong>Do not build a department-specific retention plan on this data.</strong> Department gaps are within noise.",
            f"<strong>Treat pay as a secondary lever.</strong> The gap is significant, but leavers earn only {pc(st['diff_pct_of_stayed'])} less.",
        ])),
        ("What I would do next", ul([
            "Fit a logistic regression with overtime, satisfaction, salary and job level together, to see which effects hold once the others are controlled.",
            "Check whether the employees who work overtime are the same ones who report low satisfaction.",
            "Get exit dates, so I can test whether overtime comes before leaving.",
            "Ask HR what counts as overtime and over what period attrition was measured.",
        ])),
    ],
    summary=[(pc(A["attrition_rate"]), f"Left the company: {n0(A['left'])} of {n0(A['employees'])} employees"),
             (f"+{A['overtime_gap_pp']:.1f} pts", f"Higher attrition with overtime ({pc(ot['Yes']['rate'])} vs {pc(ot['No']['rate'])})"),
             (pc(st["diff_pct_of_stayed"]), "Lower monthly pay for leavers (small effect)")],
)

# ---------------- marketing
h4 = M["clicks_4plus_added"]
h01 = M["clicks_0to1_added"]
CARDS["marketing"] = dict(
    problem="Which channels and devices convert best, and does more ad spend buy results?",
    decision=(f"Do not move budget between channels on this data: channel and device gaps sit within noise. Work on engagement "
              f"instead. Leads with 4 or more ad clicks convert at {pc(h4['rate'])}, against {pc(h01['rate'])} for 0 to 1 clicks."),
    stats=[(pc(M["conversion_rate"]), f"Conversion: {n0(M['conversions'])} of {n0(M['leads'])} leads"),
           (n0(M["cost_per_conversion"]), "Ad spend per conversion"),
           (pc(h4["rate"]), f"Conversion with 4+ ad clicks ({pc(h01['rate'])} with 0 to 1)")],
    chart=M["charts"]["conversion-by-engagement"],
    alt=(f"Bar chart of conversion rate by ad-click engagement: low (0 to 1 clicks) {pc(eg['Low']['rate'])}, medium (2 to 3) "
         f"{pc(eg['Medium']['rate'])}, high (4 to 6) {pc(eg['High']['rate'])}, very high (7 or more) {pc(eg['Very High']['rate'])}, "
         f"with a dashed line at the overall rate of {pc(M['conversion_rate'])}."),
)
sp = M["spend_test"]
cm = M["chi_added"]
pp = M["by_prev_purchases_added"]
ch_lo = min(named_ch.values(), key=lambda v: v["rate"])
ch_hi = max(named_ch.values(), key=lambda v: v["rate"])
PAGES["marketing"] = dict(
    lede="I compared conversion by channel, device and ad engagement, and checked whether spending more on a lead buys more conversions.",
    summary_rec="Do not move budget between channels on this data. Work on ad engagement instead.",
    sections=[
        ("Problem", f"""
<p>The dataset covers {n0(M['leads'])} leads, {M['total_spend'] / 1e6:.2f}M of ad spend, five channels and three device types. {pc(M['conversion_rate'])} of leads converted. Which channels and devices convert best, and is more ad spend linked to more conversions?</p>
<p>The files contain no brief, so the questions come from the notebook's own insight list: compare channel conversion before reallocating budget, find high-engagement segments, compare devices, and track cost per conversion.</p>"""),
        ("Data", facts([
            ("Source", todo("say where this dataset comes from; the notebook does not say", "marketing")),
            ("Size", f"{n0(M['raw_rows'])} rows and {M['raw_cols']} columns. {n0(M['leads'])} unique leads remain after removing {M['duplicates']} duplicate rows."),
            ("Columns", "Lead_ID, Channel, Age, Monthly_Income, Website_Visits, Ad_Clicks, Ad_Spend, Previous_Purchases, Device, Converted (1 = converted, 0 = did not)"),
            ("Quality problems", f"Before cleaning: {M['missing']['Channel']} missing channels, {M['missing']['Monthly_Income']} missing incomes and {M['missing']['Device']} missing devices. {M['invalid_age_raw']} ages fall outside 18 to 100 (from −5 to 120), and {M['negative_spend_raw']} ad spend values are negative."),
            ("Definitions", todo("explain what Ad_Spend measures (per lead or per campaign) and what counts as a conversion, over what period; the files do not say", "marketing")),
            ("Currency", todo("state the currency of Ad_Spend and Monthly_Income; the files give none", "marketing")),
        ])),
        ("Method", ol([
            f"Removed {M['duplicates']} duplicate rows, standardised the text in Channel and Device, and filled missing values with \"Unknown\" ({n0(ch['Unknown']['n'])} channels and {n0(dv['Unknown']['n'])} devices).",
            f"Replaced {M['invalid_age_after_dedup']} invalid ages, {M['missing']['Monthly_Income']} missing incomes and {M['negative_spend_after_dedup']} negative spend values with the column median.",
            "Grouped leads by ad clicks into four engagement levels: low (0 to 1 clicks), medium (2 to 3), high (4 to 6) and very high (7 or more).",
            "Compared conversion by channel, device and engagement. Calculated conversion rate, total spend, and cost per conversion (total spend divided by conversions).",
            "Tested whether leads that converted received different ad spend, using Welch's t-test, the notebook's test.",
            "Added checks the notebook does not contain: chi-square tests for channel, device, engagement and previous purchases, and 95% confidence ranges for each channel.",
        ])),
        ("What I found", f"""
<h3>Channels and devices sit within noise</h3>
<p>Referral converts best ({pc(ch['Referral']['rate'])}) and Search worst ({pc(ch['Search']['rate'])}), a gap of {ch['Referral']['rate'] - ch['Search']['rate']:.1f} points. But each channel's 95% confidence range overlaps the others, and the chi-square test cannot separate them ({pv(cm['Channel']['p'])}). Devices are closer still: {pc(dv['Mobile']['rate'])} on mobile to {pc(dv['Desktop']['rate'])} on desktop ({pv(cm['Device']['p'])}). Cost per conversion follows the same pattern, from {n2(ch['Referral']['cost_per_conv'])} (Referral) to {n2(ch['Search']['cost_per_conv'])} (Search), so I would not act on it.</p>
{fig('../../', M['charts']['conversion-by-channel'], "Horizontal bar chart of conversion rate by channel with 95% confidence ranges: " + ", ".join(f"{('no channel recorded' if k == 'Unknown' else k)} {pc(v['rate'])}" for k, v in sorted(ch.items(), key=lambda kv: -kv[1]['rate'])) + ". The ranges overlap, so the ranking is not reliable.", "The confidence ranges overlap. The channel ranking could change with a new sample.")}
<h3>More spend per lead does not buy conversions</h3>
<p>Leads that converted received {n2(sp['mean_a'])} of ad spend on average, against {n2(sp['mean_b'])} for leads that did not. The difference is {sg(sp['diff'])} (95% confidence interval {sg(sp['ci_low'])} to {sg(sp['ci_high'])}; Welch's t-test, {pv(sp['p'])}). There is no evidence that spend per lead changes the outcome. Spend does not buy clicks either: their correlation is {M['corr_spend_clicks_added']:.3f}.</p>
<h3>Engagement is the signal</h3>
<p>Conversion climbs with ad clicks: <strong>{pc(eg['Low']['rate'])}</strong> for 0 to 1 clicks ({n0(eg['Low']['n'])} leads), {pc(eg['Medium']['rate'])} for 2 to 3, {pc(eg['High']['rate'])} for 4 to 6, and <strong>{pc(eg['Very High']['rate'])}</strong> for 7 or more ({n0(eg['Very High']['n'])} leads). Chi-square {pv(cm['Engagement_Level']['p'])}, V = {cm['Engagement_Level']['cramers_v']:.2f}, a {v_word(cm['Engagement_Level']['cramers_v'])} link. Cost per conversion falls from {n2(eg['Low']['cost_per_conv'])} at low engagement to {n2(eg['High']['cost_per_conv'])} (high) and {n2(eg['Very High']['cost_per_conv'])} (very high).</p>
<p>Average spend per lead is almost the same at every level ({n2(min(M['avg_spend_by_engagement'].values()))} to {n2(max(M['avg_spend_by_engagement'].values()))}), so {pc(M['spend_share_low_engagement_pct'])} of all spend goes to leads who barely click. Previous purchases also link to conversion, but weakly: {pc(pp['0']['rate'])} for none to {pc(pp['6']['rate'])} for six ({pv(cm['Previous_Purchases']['p'])}, V = {cm['Previous_Purchases']['cramers_v']:.2f}).</p>
{fig('../../', M['charts']['conversion-by-engagement'], CARDS['marketing']['alt'])}
{tests_table([
    ("Ad spend, converted vs not", f"{n2(sp['mean_a'])} vs {n2(sp['mean_b'])}", "Welch t-test", "Notebook", sp['p'], False, ""),
    ("Channel", f"{pc(ch_lo['rate'])} to {pc(ch_hi['rate'])}", "Chi-square", "Added", cm['Channel']['p'], False, ""),
    ("Device", f"{pc(min(v['rate'] for v in named_dv.values()))} to {pc(max(v['rate'] for v in named_dv.values()))}", "Chi-square", "Added", cm['Device']['p'], False, ""),
    ("Ad-click engagement", f"{pc(eg['Low']['rate'])} to {pc(eg['Very High']['rate'])}", "Chi-square", "Added", cm['Engagement_Level']['p'], True, f"{v_word(cm['Engagement_Level']['cramers_v']).capitalize()} (V = {cm['Engagement_Level']['cramers_v']:.2f})"),
    ("Previous purchases, 0 to 6", f"{pc(pp['0']['rate'])} to {pc(pp['6']['rate'])}", "Chi-square", "Added", cm['Previous_Purchases']['p'], True, f"{v_word(cm['Previous_Purchases']['cramers_v']).capitalize()} (V = {cm['Previous_Purchases']['cramers_v']:.2f})"),
], "Statistical tests. The notebook's own test found no difference, and so do my added tests for channel and device.")}
{callout("Where this analysis is weak", f"<p><strong>Engagement is not proof.</strong> Clicks come from the lead, not from the budget. Leads who were already interested may click more and also convert more. The data shows the link. It does not show that raising clicks would raise conversion.</p><p><strong>Small top group.</strong> Only {n0(eg['Very High']['n'])} leads fall in the 7-or-more group, so {pc(eg['Very High']['rate'])} is a rough figure.</p><p><strong>No-channel leads.</strong> {n0(ch['Unknown']['n'])} leads have no channel. Their {pc(ch['Unknown']['rate'])} conversion has a wide 95% range ({pc(ch['Unknown']['ci'][0])} to {pc(ch['Unknown']['ci'][1])}), so it says little.</p><p><strong>A null result is a result.</strong> The notebook's one test found nothing. That is worth reporting, and it is why I do not recommend moving budget.</p>")}"""),
        ("Recommendation", ol([
            "<strong>Do not reallocate budget between channels or devices on this data.</strong> The gaps are within noise.",
            f"<strong>Test ways to raise engagement.</strong> {pc(M['spend_share_low_engagement_pct'])} of spend reaches the {n0(h01['n'])} leads with 0 to 1 clicks, and they cost {n2(h01['cost_per_conv'])} per conversion against {n2(h4['cost_per_conv'])} for leads with 4 or more clicks. Try creative or targeting changes as a controlled experiment.",
            "<strong>Track cost per conversion by engagement level</strong>, not only by channel.",
        ])),
        ("What I would do next", ul([
            "Run an A/B test on ad creative or targeting for low-engagement leads, to see whether raising clicks raises conversion.",
            "Fit a logistic regression with clicks, visits, previous purchases, channel and device together.",
            "Get dates, so I can look at trends and the lag between clicks and conversion.",
            "Split cost per conversion by channel and engagement together, once each group has enough leads.",
        ])),
    ],
    summary=[(pc(M["conversion_rate"]), f"Conversion: {n0(M['conversions'])} of {n0(M['leads'])} leads"),
             (n0(M["cost_per_conversion"]), f"Ad spend per conversion ({M['total_spend'] / 1e6:.2f}M in total)"),
             (pc(h4["rate"]), f"Conversion with 4+ ad clicks ({pc(h01['rate'])} with 0 to 1)")],
)

# ---------------- churn
c3 = C["calls_3plus"]
c02 = C["calls_0to2"]
pa = C["plan_by_activity_added"]
ce = C["chi_added"]
ag = C["by_activity"]
CARDS["churn"] = dict(
    problem="Which customers leave, and what warns us first?",
    decision=(f"Watch login recency and service calls. Churn rises steadily from {pc(cd['0-30']['rate'])} for customers who logged in "
              f"within 30 days to {pc(cd['151+']['rate'])} after 150 days, with no sharp cliff. Gender, age and payment method show no link."),
    stats=[(pc(C["churn_rate"]), f"Churned: {n0(C['churned'])} of {n0(C['clean_rows'])} customers"),
           (pc(cd["151+"]["rate"]), f"Churn after 150+ days without login ({pc(cd['0-30']['rate'])} within 30)"),
           (pc(cp["Basic"]["rate"]), f"Churn on the Basic plan (Plus: {pc(cp['Plus']['rate'])})")],
    chart=C["charts"]["churn-by-login-recency"],
    alt=("Line chart of churn rate by days since last login: " +
         ", ".join(f"{k} days {pc(cd[k]['rate'])}" for k in ["0-30", "31-60", "61-90", "91-120", "121-150"]) +
         f", 151 or more days {pc(cd['151+']['rate'])}. The line rises steadily and stays above the overall rate of {pc(C['churn_rate'])} after 61 days."),
)
PAGES["churn"] = dict(
    lede="I looked for early warning signs of customer churn, and cleaned a messy customer file to get there.",
    summary_rec="Flag customers early by login recency and service calls. Gender, age and payment method show no link.",
    sections=[
        ("Problem", f"""
<p>In this dataset, {pc(C['churn_rate'])} of {n0(C['clean_rows'])} customers have churned. Which customers leave, and what warns us first?</p>
<p>The files contain no brief. The questions are the notebook's own headings: does activity level affect churn, is time since last login a cliff, and do plan, payment method, region, age, gender, service calls and spend matter?</p>"""),
        ("Data", facts([
            ("Source", todo("say where this dataset comes from; the notebook does not say", "churn")),
            ("Size", f"{n0(C['raw_rows'])} rows and {C['raw_cols']} columns. {n0(C['clean_rows'])} unique customers remain after removing {C['duplicates']} duplicate rows."),
            ("Columns", "Customer_ID, Gender, Region, Subscription_Plan, Payment_Method, Age, Days_Since_Last_Login, Customer_Service_Calls, Monthly_Spend, Churn (1 = churned, 0 = retained)"),
            ("Quality problems", f"{C['region_labels_raw']} spellings of 4 regions and {C['plan_labels_raw']} spellings of 3 plans. After removing duplicates: {C['missing_after_dedup']['Payment_Method']} missing payment methods, {C['missing_after_dedup']['Age']} missing ages and {C['missing_after_dedup']['Monthly_Spend']} missing spend values. Invalid values: {C['age_invalid_total']} ages (below 5 or above 100, including {C['age_150']} of exactly 150), {C['spend_negative']} negative spend values, {C['spend_99999']} spend values of 99,999.99, and {C['calls_negative']} negative service call counts."),
            ("Definitions", todo("explain what Churn means and over what period customers were counted; the files do not say", "churn")),
            ("Currency", todo("state the currency of Monthly_Spend; the files give none", "churn")),
        ])),
        ("Method", ol([
            f"Removed {C['duplicates']} duplicate rows.",
            f"Standardised capitalisation: region from {C['region_labels_raw']} spellings to 4, and plan from {C['plan_labels_raw']} spellings to 3.",
            f"Filled {C['missing_after_dedup']['Payment_Method']} missing payment methods with \"Unknown\".",
            f"Replaced {C['missing_after_dedup']['Age']} missing and {C['age_invalid_total']} invalid ages with the median age, 33.",
            f"Replaced {C['missing_after_dedup']['Monthly_Spend']} missing, {C['spend_negative']} negative and {C['spend_99999']} outlier (99,999.99) spend values with the median, and {C['calls_negative']} negative service call counts with the median.",
            "Grouped customers by login recency: Active (0 to 30 days), At Risk (31 to 90) and Inactive (91 or more), and in 30-day buckets.",
            "Compared churn across plan, region, gender, payment method, service calls, spend and age, with one chart per question.",
            "The notebook has no significance tests. I added chi-square tests and t-tests to check whether each gap is real.",
        ])),
        ("What I found", f"""
<h3>Login recency is the strongest warning</h3>
<p>Churn rises steadily from <strong>{pc(cd['0-30']['rate'])}</strong> for customers who logged in within 30 days to <strong>{pc(cd['151+']['rate'])}</strong> for those away 151 days or more. There is no cliff: each 30-day step adds 4 to 9 points, and the climb slows after 120 days. Half of customers ({n0(ag['Inactive']['n'])} of {n0(C['clean_rows'])}) are Inactive (91 or more days), and {pc(ag['Inactive']['rate'])} of them churned. Churned customers last logged in {nt['Days_Since_Last_Login']['mean_churned']:.1f} days ago on average, against {nt['Days_Since_Last_Login']['mean_retained']:.1f} for retained ones (Cohen's d = {nt['Days_Since_Last_Login']['cohens_d']:.2f}, the largest effect I found).</p>
{fig('../../', C['charts']['churn-by-login-recency'], CARDS['churn']['alt'], "Churn climbs with every extra month of inactivity. Numbers under each label show how many customers fall in the group.")}
<h3>Many service calls go with churn</h3>
<p>Churn goes from {pc(cc['0']['rate'])} for customers with no calls to {pc(cc['6+']['rate'])} for six or more ({n0(cc['6+']['n'])} customers). Customers with 3 or more calls ({n0(c3['n'])}) churn at {pc(c3['rate'])}, against {pc(c02['rate'])} for those with 0 to 2 ({n0(c02['n'])}). Churned customers made {nt['Customer_Service_Calls']['mean_churned']:.2f} calls on average, against {nt['Customer_Service_Calls']['mean_retained']:.2f} (d = {nt['Customer_Service_Calls']['cohens_d']:.2f}).</p>
{fig('../../', C['charts']['churn-by-service-calls'], "Line chart of churn rate by number of customer service calls: " + ", ".join(f"{k} calls {pc(cc[k]['rate'])}" for k in ['0', '1', '2', '3', '4', '5']) + f", six or more {pc(cc['6+']['rate'])}. The line rises with every extra call.")}
<h3>Basic plan customers leave most</h3>
<p>Churn is {pc(cp['Basic']['rate'])} on Basic, {pc(cp['Pro']['rate'])} on Pro and {pc(cp['Plus']['rate'])} on Plus (chi-square {pv(ce['Subscription_Plan']['p'])}, V = {ce['Subscription_Plan']['cramers_v']:.2f}). Average monthly spend follows the plan: {n2(C['avg_spend_by_plan']['Basic'])} on Basic, {n2(C['avg_spend_by_plan']['Pro'])} on Pro and {n2(C['avg_spend_by_plan']['Plus'])} on Plus. Churned customers spend less overall ({n2(nt['Monthly_Spend']['mean_churned'])} against {n2(nt['Monthly_Spend']['mean_retained'])}, d = {abs(nt['Monthly_Spend']['cohens_d']):.2f}). The plan gap holds at every activity level: among Inactive customers, churn is {pc(pa['Basic']['Inactive'])} on Basic and {pc(pa['Plus']['Inactive'])} on Plus.</p>
{fig('../../', C['charts']['churn-by-plan'], f"Bar chart of churn rate by subscription plan: Basic {pc(cp['Basic']['rate'])} ({n0(cp['Basic']['n'])} customers), Pro {pc(cp['Pro']['rate'])} ({n0(cp['Pro']['n'])}), Plus {pc(cp['Plus']['rate'])} ({n0(cp['Plus']['n'])}), with a dashed line at the overall rate of {pc(C['churn_rate'])}.")}
<h3>What does not matter</h3>
<p>Gender ({pc(min(v['rate'] for v in C['by_gender'].values()))} to {pc(max(v['rate'] for v in C['by_gender'].values()))}, {pv(ce['Gender']['p'])}), payment method ({pc(min(v['rate'] for v in C['by_payment'].values()))} to {pc(max(v['rate'] for v in C['by_payment'].values()))}, {pv(ce['Payment_Method']['p'])}) and age ({nt['Age']['mean_churned']:.2f} vs {nt['Age']['mean_retained']:.2f} years, {pv(nt['Age']['p'])}) show no link with churn. Region is statistically significant ({pc(C['by_region']['East']['rate'])} in the East to {pc(C['by_region']['South']['rate'])} in the South, {pv(ce['Region']['p'])}) but weak (V = {ce['Region']['cramers_v']:.2f}).</p>
{tests_table([
    ("Days since last login, churned vs retained", f"{nt['Days_Since_Last_Login']['mean_churned']:.1f} vs {nt['Days_Since_Last_Login']['mean_retained']:.1f}", "Welch t-test", "Added", nt['Days_Since_Last_Login']['p'], True, f"{d_word(nt['Days_Since_Last_Login']['cohens_d']).capitalize()} (d = {nt['Days_Since_Last_Login']['cohens_d']:.2f})"),
    ("Service calls, churned vs retained", f"{nt['Customer_Service_Calls']['mean_churned']:.2f} vs {nt['Customer_Service_Calls']['mean_retained']:.2f}", "Welch t-test", "Added", nt['Customer_Service_Calls']['p'], True, f"{d_word(nt['Customer_Service_Calls']['cohens_d']).capitalize()} (d = {nt['Customer_Service_Calls']['cohens_d']:.2f})"),
    ("Monthly spend, churned vs retained", f"{n2(nt['Monthly_Spend']['mean_churned'])} vs {n2(nt['Monthly_Spend']['mean_retained'])}", "Welch t-test", "Added", nt['Monthly_Spend']['p'], True, f"{d_word(nt['Monthly_Spend']['cohens_d']).capitalize()} (d = {abs(nt['Monthly_Spend']['cohens_d']):.2f})"),
    ("Subscription plan", f"{pc(cp['Plus']['rate'])} to {pc(cp['Basic']['rate'])}", "Chi-square", "Added", ce['Subscription_Plan']['p'], True, f"{v_word(ce['Subscription_Plan']['cramers_v']).capitalize()} (V = {ce['Subscription_Plan']['cramers_v']:.2f})"),
    ("Region", f"{pc(C['by_region']['East']['rate'])} to {pc(C['by_region']['South']['rate'])}", "Chi-square", "Added", ce['Region']['p'], True, f"{v_word(ce['Region']['cramers_v']).capitalize()} (V = {ce['Region']['cramers_v']:.2f})"),
    ("Gender", f"{pc(min(v['rate'] for v in C['by_gender'].values()))} to {pc(max(v['rate'] for v in C['by_gender'].values()))}", "Chi-square", "Added", ce['Gender']['p'], False, ""),
    ("Payment method", f"{pc(min(v['rate'] for v in C['by_payment'].values()))} to {pc(max(v['rate'] for v in C['by_payment'].values()))}", "Chi-square", "Added", ce['Payment_Method']['p'], False, ""),
    ("Age, churned vs retained", f"{nt['Age']['mean_churned']:.2f} vs {nt['Age']['mean_retained']:.2f}", "Welch t-test", "Added", nt['Age']['p'], False, ""),
], "Statistical tests. The notebook compares groups with charts and written notes; every test here is one I added.")}
{callout("Where this analysis is weak", f"<p><strong>The base rate is very high.</strong> {pc(C['churn_rate'])} of customers churned, and even customers who logged in within 30 days churn at {pc(cd['0-30']['rate'])}. I do not know how churn is defined or over what period, so I would not quote these rates as a benchmark.</p><p><strong>Recency may be a result, not a cause.</strong> Customers who have already left stop logging in. Without dates I cannot tell which comes first.</p><p><strong>Ages 5 to 17.</strong> {n0(C['age_under_18_remaining'])} customers aged 5 to 17 remain after cleaning. The notebook's comment says ages were limited to 18 to 100, but the code only removes ages below 5. I would check whether these ages are real.</p><p><strong>Filled ages.</strong> About {n0(C['missing_after_dedup']['Age'] + C['age_invalid_total'])} ages ({pc((C['missing_after_dedup']['Age'] + C['age_invalid_total']) / C['clean_rows'] * 100, 0)} of customers) were replaced with the median. Age does not relate to churn, so this changes little, but it should be stated.</p><p><strong>Small print.</strong> The notebook's written note gives the churned service-call average as 1.90. The data gives {nt['Customer_Service_Calls']['mean_churned']:.2f}, which the chart label rounds to 1.9. I use {nt['Customer_Service_Calls']['mean_churned']:.2f}.</p><p>{todo('add the payment-methods.jpg image that the notebook loads (it is missing from the files, so the payment donut chart cell fails)', 'churn')}</p>")}"""),
        ("Recommendation", ol([
            f"<strong>Build an early-warning list from login recency.</strong> Start outreach when a customer passes 30 days without a login, and give priority to those past 90 days. Churn climbs steadily, so the exact threshold is a judgement call to test, not a value from the data.",
            f"<strong>Flag customers with 3 or more service calls</strong> for a follow-up from the support team. They churn at {pc(c3['rate'])}.",
            f"<strong>Review the Basic plan experience.</strong> It has {pc(cp['Basic']['rate'])} churn across {n0(cp['Basic']['n'])} customers.",
            "<strong>Do not target by gender or payment method.</strong> Neither relates to churn.",
        ])),
        ("What I would do next", ul([
            "Confirm the churn definition and get dates, then check whether low logins come before churn.",
            "Fit a logistic regression on recency, service calls, plan and spend to rank the drivers, and test how well it predicts churn on customers held out of the fit.",
            "Check the 470 customers aged 5 to 17.",
            f"Look at plan and recency together to pick a first target group; Basic customers who are Inactive churn at {pc(pa['Basic']['Inactive'])}.",
        ])),
    ],
    summary=[(pc(C["churn_rate"]), f"Churned: {n0(C['churned'])} of {n0(C['clean_rows'])} customers"),
             (pc(cd["151+"]["rate"]), f"Churn after 150+ days without login ({pc(cd['0-30']['rate'])} within 30)"),
             (pc(c3["rate"]), f"Churn with 3+ service calls ({pc(c02['rate'])} with 0 to 2)")],
)

# ------------------------------------------------------------------ page shell
NAV = ('<nav class="glass" aria-label="Sections"><a href="../../index.html#top">Home</a><a href="../../index.html#about">About</a>'
       '<a href="../../index.html#game">Game</a><a href="../../index.html#certs">Certs</a>'
       '<a class="on" href="../../index.html#projects">Projects</a><a href="../../index.html#skills">Skills</a>'
       '<a href="../../index.html#contact">Contact</a></nav>')
V = "12"


def links_html(key, prefix="", case=True):
    m = META[key]
    base = f"{prefix}projects/{m['dir']}/"
    first = f'<a href="{base}analysis.html">Case study</a>' if case else ""
    return (f'<div class="links">{first}<a href="{base}analysis.ipynb" download>Notebook</a>'
            f'<a href="{base}data.csv" download="{esc(m["csv_name"])}">Dataset</a></div>')


def page(key):
    m, P, i = META[key], PAGES[key], ORDER.index(key)
    prev_k = ORDER[i - 1] if i > 0 else None
    next_k = ORDER[i + 1] if i < len(ORDER) - 1 else None
    pn = ""
    if prev_k:
        pn += f'<a href="../{META[prev_k]["dir"]}/analysis.html"><small>Previous project</small><b>{esc(META[prev_k]["title"])}</b></a>'
    if next_k:
        pn += f'<a class="next{"" if prev_k else " solo"}" href="../{META[next_k]["dir"]}/analysis.html"><small>Next project</small><b>{esc(META[next_k]["title"])}</b></a>'
    if not next_k:
        pn = pn.replace('<a href=', '<a class="solo" href=', 1)
    desc = f"Case study: {m['title']}. {P['lede']}"
    body = f'''<section class="cs cs-head">
<a class="back" href="../../index.html#projects">← All projects</a>
<span class="mv">{m["match"]} · Case study</span>
<h1>{esc(m["title"])}</h1>
<p class="lede">{esc(P["lede"])}</p>
{pills(m["tools"])}
{links_html(key, "../../".replace("../../", "../../")[:0] or "", case=False).replace('projects/' + m['dir'] + '/', '')}
</section>
'''
    body += panel("Summary", stats3(P["summary"]) + f'<div class="callout"><span class="lab">Recommendation</span><p>{P["summary_rec"]}</p></div>')
    for title, content in P["sections"]:
        body += panel(title, content)
    body += (f'<section class="cs"><div class="glass cs-panel" data-title="More projects"><h2>More projects</h2>'
             f'<div class="pn">{pn}</div><p class="pn-all"><a href="../../index.html#projects">Back to all projects</a></p></div></section>')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(m["title"])} | Moaz Ahmed</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#000000">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>♚</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/css/style.css?v={V}"><link rel="stylesheet" href="../../assets/css/enhance.css?v={V}"><link rel="stylesheet" href="../../assets/css/premium.css?v={V}"><link rel="stylesheet" href="../../assets/css/projects.css?v={V}">
</head>
<body class="cs-page">
<a class="skip" href="#main">Skip to content</a>
<div class="orb o1"></div><div class="orb o2"></div>
{NAV}
<main id="main">
{body}</main>
<footer><span>© 2026 Moaz Ahmed</span><a href="../../index.html#projects">All projects</a></footer>
<script src="../../assets/js/premium.js?v={V}"></script>
<script src="../../assets/js/windows.js?v={V}"></script>
</body>
</html>
'''


def card(key):
    m, c = META[key], CARDS[key]
    ch = c["chart"]
    return f'''<article class="glass tilt card pcard" data-tilt><span class="mv">{m["match"]}</span><h3>{esc(m["title"])}</h3>
<p class="prob">{esc(c["problem"])}</p>
<div class="dec"><b>Recommendation</b>{esc(c["decision"])}</div>
{stats3(c["stats"])}
<figure class="shot"><img src="{ch["file"]}" width="{ch["width"]}" height="{ch["height"]}" alt="{esc(c["alt"])}" loading="lazy"></figure>
{pills(m["tools"])}
{links_html(key)}</article>'''


def build_index():
    p = ROOT / "index.html"
    s = p.read_text()
    section = ('<section id="projects"><h2 class="gold">Featured projects</h2>'
               '<p class="lead">Four end-to-end analyses. Each one states the problem, the recommendation it leads to, and the numbers behind it, with a case study, the notebook and the dataset.</p>'
               '<div class="grid pj">' + "".join(card(k) for k in ORDER) + '</div></section>')
    s2, n = re.subn(r'<section id="projects">.*?</section>', lambda _m: section, s, flags=re.S)
    assert n == 1
    s2 = s2.replace('?v=11', f'?v={V}')
    if "projects.css" not in s2:
        s2 = s2.replace(f'<link rel="stylesheet" href="assets/css/premium.css?v={V}">',
                        f'<link rel="stylesheet" href="assets/css/premium.css?v={V}"><link rel="stylesheet" href="assets/css/projects.css?v={V}">')
    p.write_text(s2)


def readme(key):
    m = META[key]
    if key == "retail":
        res = (f"Total sales {n2(R['total_sales'])}, total profit {n2(R['total_profit'])}, {n0(R['orders'])} orders, average order value {n2(R['aov'])}, "
               f"average margin {n2(R['avg_margin'])}% (mean of per-order margins; total profit over total sales is {n2(R['pooled_margin'])}%). "
               f"Welch t-test on profit per order, discounted vs full price: {pv(R['profit_test']['p'])} (significant, small effect).")
        ds = f"{n0(R['raw_rows'])} rows x {R['raw_cols']} columns, {n0(R['orders'])} after removing {R['duplicates']} duplicates."
    elif key == "attrition":
        res = (f"{n0(A['employees'])} employees, attrition {n2(A['attrition_rate'])}%, average monthly salary {n2(A['avg_salary'])}, average tenure {n2(A['avg_tenure'])} years. "
               f"Welch t-test on salary, stayed vs left: {pv(A['salary_test']['p'])} (significant, small effect).")
        ds = f"{n0(A['raw_rows'])} rows x {A['raw_cols']} columns, {n0(A['employees'])} after removing {A['duplicates']} duplicates."
    elif key == "marketing":
        res = (f"{n0(M['leads'])} leads, {n0(M['conversions'])} conversions, conversion rate {n2(M['conversion_rate'])}%, total ad spend {n2(M['total_spend'])}, "
               f"cost per conversion {n2(M['cost_per_conversion'])}. Welch t-test on ad spend, converted vs not: {pv(M['spend_test']['p'])} (not significant).")
        ds = f"{n0(M['raw_rows'])} rows x {M['raw_cols']} columns, {n0(M['leads'])} after removing {M['duplicates']} duplicates."
    else:
        res = (f"Churn {n2(C['churn_rate'])}% ({n0(C['churned'])} of {n0(C['clean_rows'])} customers). Cleaning fixed inconsistent region and plan spellings, "
               f"{C['missing_after_dedup']['Payment_Method']} missing payment methods, {C['missing_after_dedup']['Age']} missing and {C['age_invalid_total']} invalid ages, "
               f"{C['missing_after_dedup']['Monthly_Spend']} missing, {C['spend_negative']} negative and {C['spend_99999']} outlier spend values, and {C['calls_negative']} negative service call counts. "
               f"The notebook has no significance tests; the case study adds them.")
        ds = f"{n0(C['raw_rows'])} rows x {C['raw_cols']} columns, {n0(C['clean_rows'])} after removing {C['duplicates']} duplicates."
    txt = f"""# {m['title']}

**Dataset:** {ds}

**Key results:** {res}

**Case study:** `analysis.html` (problem, data, method, findings, recommendation, next steps).

**Files**
- `analysis.ipynb`: the Jupyter notebook. It reads `{m['csv_name']}`; the site's Dataset link downloads `data.csv` under that name.
- `analysis.html`: the case study page
- `data.csv`: the dataset

**Stack:** {', '.join(m['tools'])}
"""
    (ROOT / "projects" / m["dir"] / "README.md").write_text(txt)


if __name__ == "__main__":
    for k in ORDER:
        (ROOT / "projects" / META[k]["dir"] / "analysis.html").write_text(page(k))
        readme(k)
    build_index()
    print(f"Built index.html projects section, 4 case studies, 4 READMEs. {len(TODOS)} TODO markers:")
    for slug, t in TODOS:
        print(f"  [{slug}] {t}")
