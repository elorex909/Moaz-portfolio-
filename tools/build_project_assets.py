#!/usr/bin/env python3
"""
Recompute every number shown in the Featured projects section and case studies,
and export the charts as WebP.

Why this exists: each figure on the site must trace back to the data. This script
repeats the cleaning steps from each notebook (same order, same rules) on
projects/*/data.csv, writes tools/numbers.json, and draws the charts.

Run from the site folder:   python3 tools/build_project_assets.py
Needs: pandas, numpy, scipy, matplotlib, pillow (with WebP support).

Notes
- Cleaning matches the notebooks. Where this script adds a check the notebooks do
  not contain (chi-square tests, confidence intervals, imputation check), the
  key ends in "_added" or the case study labels it as an added check.
- Charts are re-drawn with the site's dark theme from the same grouped data as the
  notebook charts. They are not screenshots of the notebook output.
"""
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PROJ = ROOT / "projects"
IMG = ROOT / "assets" / "img" / "projects"

BG, FG, MUT, LINE = "#0d0f13", "#f5f5f7", "#9aa0aa", "#262b34"
GOLD, CYAN, SLATE = "#dcb972", "#a9d6e5", "#4a5361"
plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 22,
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.labelcolor": MUT, "xtick.color": MUT, "ytick.color": MUT,
    "axes.edgecolor": LINE, "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 1.4, "axes.grid": False,
})
W, H = 12, 6.6  # inches at dpi 100 -> 1200 x 660 px

def f(x):
    return float(x)

def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return f((c - h) * 100), f((c + h) * 100)

def chi2(df, col, target):
    ct = pd.crosstab(df[col], df[target])
    c2, p, dof, _ = stats.chi2_contingency(ct)
    n = ct.values.sum()
    v = np.sqrt(c2 / (n * (min(ct.shape) - 1)))
    return {"chi2": f(c2), "p": f(p), "dof": int(dof), "cramers_v": f(v)}

def welch(a, b):
    t, p = stats.ttest_ind(a, b, equal_var=False)
    diff = a.mean() - b.mean()
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return {"t": f(t), "p": f(p), "diff": f(diff), "ci_low": f(diff - 1.96 * se),
            "ci_high": f(diff + 1.96 * se), "cohens_d": f(diff / sp),
            "mean_a": f(a.mean()), "mean_b": f(b.mean()), "n_a": int(len(a)), "n_b": int(len(b))}

def save_webp(fig, folder, name):
    out = IMG / folder
    out.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100)
    plt.close(fig)
    buf.seek(0)
    im = Image.open(buf).convert("RGB")
    assert im.width <= 1200
    path = out / f"{name}.webp"
    im.save(path, "WEBP", quality=84, method=6)
    return {"file": f"assets/img/projects/{folder}/{name}.webp", "width": im.width,
            "height": im.height, "bytes": path.stat().st_size}

def style_axes(ax, ymax=None, pct=True, ylabel=None):
    ax.tick_params(axis="both", length=0, pad=10)
    ax.yaxis.grid(True, color=LINE, linewidth=1.2)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    if ymax:
        ax.set_ylim(0, ymax)
    if pct:
        ax.set_yticks(np.arange(0, (ymax or 100) + 1, 10 if (ymax or 100) <= 50 else 20))
        ax.set_yticklabels([f"{int(t)}%" for t in ax.get_yticks()])
    if ylabel:
        ax.set_ylabel(ylabel, labelpad=12)

def ref_legend(fig, label):
    """Dashed-line key at the top right, sized from the measured text so it never overlaps the label."""
    from matplotlib.lines import Line2D
    t = fig.text(0.975, 0.925, label, color=CYAN, fontsize=20, ha="right", va="center")
    fig.canvas.draw()
    bb = t.get_window_extent()
    fw = fig.get_figwidth() * fig.dpi
    x1 = bb.x0 / fw - 0.012
    fig.add_artist(Line2D([x1 - 0.045, x1], [0.925, 0.925], transform=fig.transFigure, color=CYAN,
                          linewidth=2.4, linestyle=(0, (4, 3))))

def whisker_note(fig):
    fig.text(0.975, 0.02, "Whiskers show the 95% confidence range", color=MUT, fontsize=18, ha="right", va="bottom")

VAL = dict(fontsize=26, color=FG, fontweight="bold", zorder=6,
           bbox=dict(facecolor=BG, edgecolor="none", pad=3))

def title(fig, text):
    fig.text(0.045, 0.94, text, fontsize=25, color=FG, ha="left", va="top", fontweight="bold")

def vbars(folder, name, labels, values, colors, ttl, ymax, fmt="{:.1f}%", sub=None,
          hline=None, hline_label=None, err=None):
    fig, ax = plt.subplots(figsize=(W, H))
    fig.subplots_adjust(left=0.10, right=0.975, top=0.83, bottom=0.22 if sub else 0.14)
    x = np.arange(len(values))
    ax.bar(x, values, color=colors, width=0.58, zorder=3)
    if err is not None:
        lo = [v - e[0] for v, e in zip(values, err)]
        hi = [e[1] - v for v, e in zip(values, err)]
        ax.errorbar(x, values, yerr=[lo, hi], fmt="none", ecolor=FG, elinewidth=2.2, capsize=8, zorder=4)
    style_axes(ax, ymax)
    for xi, v in zip(x, values):
        top = v if err is None else err[xi][1]
        ax.text(xi, top + ymax * 0.025, fmt.format(v), ha="center", va="bottom", **VAL)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{l}\n{s}" if sub else l for l, s in zip(labels, sub or labels)] if sub else labels, fontsize=21)
    if hline is not None:
        ax.axhline(hline, color=CYAN, linewidth=2, linestyle=(0, (5, 4)), zorder=2)
        ref_legend(fig, hline_label)
    title(fig, ttl)
    return save_webp(fig, folder, name)

def hbars(folder, name, labels, values, colors, ttl, xmax, fmt="{:.1f}%", err=None, vline=None,
          vline_label=None, extra=None):
    fig, ax = plt.subplots(figsize=(W, H))
    fig.subplots_adjust(left=0.30, right=0.94, top=0.83, bottom=0.14)
    y = np.arange(len(values))[::-1]
    ax.barh(y, values, color=colors, height=0.6, zorder=3)
    if err is not None:
        lo = [v - e[0] for v, e in zip(values, err)]
        hi = [e[1] - v for v, e in zip(values, err)]
        ax.errorbar(values, y, xerr=[lo, hi], fmt="none", ecolor=FG, elinewidth=2.2, capsize=7, zorder=4)
    ax.set_xlim(0, xmax)
    ax.xaxis.grid(True, color=LINE, linewidth=1.2)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.set_xticks(np.arange(0, xmax + 1, 10 if xmax <= 50 else 20))
    ax.set_xticklabels([f"{int(t)}%" if extra != "money" else "" for t in ax.get_xticks()])
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=22, color=FG)
    ax.tick_params(axis="both", length=0, pad=10)
    for yi, v, i in zip(y, values, range(len(values))):
        right = v if err is None else err[i][1]
        ax.text(right + xmax * 0.015, yi, fmt.format(v) if not isinstance(fmt, list) else fmt[i],
                va="center", ha="left", fontsize=24, color=FG, fontweight="bold", zorder=6)
    if vline is not None:
        ax.axvline(vline, color=CYAN, linewidth=2, linestyle=(0, (5, 4)), zorder=2)
        ref_legend(fig, vline_label)
    if err is not None:
        whisker_note(fig)
    title(fig, ttl)
    return save_webp(fig, folder, name)

def lineplot(folder, name, labels, values, ttl, ymax, fmt="{:.1f}%", hline=None, hline_label=None,
             sub=None, color=GOLD, label_every=1, ylab_fmt=None):
    fig, ax = plt.subplots(figsize=(W, H))
    fig.subplots_adjust(left=0.10, right=0.965, top=0.83, bottom=0.22 if sub else 0.15)
    x = np.arange(len(values))
    ax.plot(x, values, color=color, linewidth=4, marker="o", markersize=13, markerfacecolor=BG,
            markeredgewidth=3.4, zorder=3)
    ax.fill_between(x, values, color=color, alpha=0.10, zorder=2)
    style_axes(ax, ymax, pct=ylab_fmt is None)
    if ylab_fmt:
        ax.set_yticks(np.arange(0, ymax + 1, ymax / 4))
        ax.set_yticklabels([ylab_fmt(t) for t in ax.get_yticks()])
    for xi, v in zip(x, values):
        if xi % label_every == 0:
            ax.text(xi, v + ymax * 0.04, fmt.format(v), ha="center", va="bottom", **VAL)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{l}\n{s}" for l, s in zip(labels, sub)] if sub else labels, fontsize=21)
    ax.set_xlim(-0.4, len(values) - 0.6)
    if hline is not None:
        ax.axhline(hline, color=CYAN, linewidth=2, linestyle=(0, (5, 4)), zorder=1)
        ref_legend(fig, hline_label)
    title(fig, ttl)
    return save_webp(fig, folder, name)

def retail():
    raw = pd.read_csv(PROJ / "01-retail-sales-performance-analysis" / "data.csv")
    N = {"raw_rows": len(raw), "raw_cols": raw.shape[1], "duplicates": int(raw.duplicated().sum()),
         "missing": {k: int(v) for k, v in raw.isnull().sum().items() if v}}
    N["qty_le0_raw"], N["sales_le0_raw"] = int((raw.Quantity <= 0).sum()), int((raw.Sales <= 0).sum())
    df = raw.drop_duplicates().reset_index(drop=True)
    for c in ["Region", "Category", "Product"]:
        df[c] = df[c].astype("string").str.strip().str.title()
    df["Region"] = df["Region"].fillna("Unknown")
    df["Category"] = df["Category"].fillna("Unknown")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    N["qty_le0_after_dedup"] = int((df.Quantity <= 0).sum())
    sales_bad = ((df.Sales <= 0) | df.Sales.isna())
    N["sales_replaced"] = int(sales_bad.sum())
    N["unit_price_replaced"] = int(((df.Unit_Price <= 0) | df.Unit_Price.isna()).sum())
    df["sales_imputed"] = sales_bad
    df.loc[df.Quantity <= 0, "Quantity"] = np.nan
    df.loc[df.Unit_Price <= 0, "Unit_Price"] = np.nan
    df.loc[df.Sales <= 0, "Sales"] = np.nan
    for c in ["Quantity", "Unit_Price", "Sales"]:
        df[c] = df[c].fillna(df[c].median())
    df["Profit"] = df.Sales - df.Cost
    df["Profit_Margin"] = (df.Profit / df.Sales * 100).round(2)
    df["Month"] = df.Order_Date.dt.to_period("M").astype(str)

    N["unknown_region_orders"] = int((df.Region == "Unknown").sum())
    N["unknown_category_orders"] = int((df.Category == "Unknown").sum())
    N["clean_rows"] = len(df)
    N["date_min"], N["date_max"] = str(df.Order_Date.min().date()), str(df.Order_Date.max().date())
    N["months"] = int(df.Month.nunique())
    N["total_sales"], N["total_profit"] = f(df.Sales.sum()), f(df.Profit.sum())
    N["aov"], N["avg_margin"] = f(df.Sales.mean()), f(df.Profit_Margin.mean())
    N["pooled_margin"] = f(df.Profit.sum() / df.Sales.sum() * 100)
    N["orders"] = int(df.Order_ID.nunique())

    cs = df.groupby("Category").Sales.sum().sort_values(ascending=False)
    N["category_sales"] = {k: f(v) for k, v in cs.items()}
    N["category_share"] = {k: f(v / cs.sum() * 100) for k, v in cs.items()}
    el = df[df.Category == "Electronics"]
    N["electronics"] = {"sales_share": f(el.Sales.sum() / df.Sales.sum() * 100),
                        "profit_share": f(el.Profit.sum() / df.Profit.sum() * 100),
                        "order_share": f(len(el) / len(df) * 100), "orders": int(len(el)),
                        "avg_order": f(el.Sales.mean()), "others_avg_order": f(df[df.Category != "Electronics"].Sales.mean())}
    rp = df.groupby("Region").agg(orders=("Order_ID", "size"), sales=("Sales", "sum"), profit=("Profit", "sum"))
    N["region"] = {k: {"orders": int(v.orders), "sales": f(v.sales), "profit": f(v.profit)} for k, v in rp.iterrows()}

    d0, d1 = df[df.Discount == 0], df[df.Discount > 0]
    N["discount_share_orders"] = f((df.Discount > 0).mean() * 100)
    N["discount_orders"], N["no_discount_orders"] = int(len(d1)), int(len(d0))
    N["profit_test"] = welch(d0.Profit, d1.Profit)          # notebook test (Profit, no discount vs discounted)
    N["margin_test_added"] = welch(d0.Profit_Margin, d1.Profit_Margin)
    N["avg_sales_no_discount"], N["avg_sales_discounted"] = f(d0.Sales.mean()), f(d1.Sales.mean())
    bd = df.groupby("Discount").agg(n=("Profit", "size"), margin=("Profit_Margin", "mean"),
                                    profit=("Profit", "mean"), cost=("Cost", "mean"), sales=("Sales", "mean"),
                                    qty=("Quantity", "mean"), price=("Unit_Price", "mean"))
    N["by_discount"] = {f"{int(round(k * 100))}": {c: f(v[c]) for c in ["margin", "profit", "cost", "sales", "qty", "price"]} | {"n": int(v.n)} for k, v in bd.iterrows()}

    h24 = df[(df.Order_Date >= "2024-01-01") & (df.Order_Date <= "2024-06-30")].Sales.sum()
    h25 = df[(df.Order_Date >= "2025-01-01") & (df.Order_Date <= "2025-06-30")].Sales.sum()
    N["h1_2024_sales"], N["h1_2025_sales"], N["h1_change_pct"] = f(h24), f(h25), f((h25 / h24 - 1) * 100)
    ms = df.groupby("Month").Sales.sum()
    N["month_max"] = {"month": ms.idxmax(), "sales": f(ms.max())}
    N["month_min"] = {"month": ms.idxmin(), "sales": f(ms.min())}

    ok = df[~df.sales_imputed]
    N["imputation_check_added"] = {
        "rows_imputed": int(df.sales_imputed.sum()), "share_pct": f(df.sales_imputed.mean() * 100),
        "median_used": f(df.loc[~df.sales_imputed, "Sales"].median()),
        "negative_profit_rows": int((df.Profit < 0).sum()),
        "negative_profit_rows_imputed": int(((df.Profit < 0) & df.sales_imputed).sum()),
        "avg_margin_all": f(df.Profit_Margin.mean()), "avg_margin_not_imputed": f(ok.Profit_Margin.mean()),
        "electronics_margin_all": f(el.Profit_Margin.mean()),
        "electronics_margin_not_imputed": f(el[~el.sales_imputed].Profit_Margin.mean())}
    rr = raw.drop_duplicates()
    clean = rr[(rr.Sales > 0) & (rr.Unit_Price > 0) & (rr.Quantity > 0)]
    calc = clean.Quantity * clean.Unit_Price * (1 - clean.Discount)
    N["imputation_check_added"]["sales_formula_match_pct"] = f((abs(calc - clean.Sales) < 0.05).mean() * 100)
    N["imputation_check_added"]["sales_formula_rows"] = int(len(clean))

    ch = {}
    order = list(cs.index)
    labels = [("No category recorded" if c == "Unknown" else c) for c in order]
    vals = [N["category_share"][c] for c in order]
    ch["sales-by-category"] = hbars("retail-sales", "sales-by-category", labels, vals,
                                    [GOLD if c == "Electronics" else SLATE for c in order],
                                    "Share of total sales by category", 100,
                                    fmt=[f"{N['category_share'][c]:.1f}%  ·  {N['category_sales'][c] / 1e6:.2f}M" for c in order])
    ch["margin-by-discount"] = vbars("retail-sales", "margin-by-discount",
                                     ["No discount" if k == "0" else f"{k}% off" for k in N["by_discount"]], [N["by_discount"][k]["margin"] for k in N["by_discount"]],
                                     [CYAN] * 5, "Average profit margin by discount level", 50,
                                     sub=[f"{N['by_discount'][k]['n']:,} orders" for k in N["by_discount"]])
    ml = [pd.Period(m).strftime("%b %y") for m in ms.index]
    fig, ax = plt.subplots(figsize=(W, H))
    fig.subplots_adjust(left=0.115, right=0.965, top=0.83, bottom=0.15)
    x = np.arange(len(ms))
    ax.plot(x, ms.values, color=GOLD, linewidth=4, marker="o", markersize=10, markerfacecolor=BG, markeredgewidth=3, zorder=3)
    ax.fill_between(x, ms.values, color=GOLD, alpha=0.10, zorder=2)
    style_axes(ax, 200000, pct=False)
    ax.set_yticks(range(0, 200001, 50000))
    ax.set_yticklabels(["0", "50K", "100K", "150K", "200K"])
    ax.set_xticks(x[::3])
    ax.set_xticklabels(ml[::3], fontsize=21)
    ax.set_xlim(-0.5, len(ms) - 0.5)
    imax, imin = int(np.argmax(ms.values)), int(np.argmin(ms.values))
    ax.text(imax, ms.values[imax] + 7000, f"{ms.values[imax]:,.0f}", ha="center", fontsize=23, fontweight="bold")
    ax.text(imin, ms.values[imin] - 9000, f"{ms.values[imin]:,.0f}", ha="center", va="top", fontsize=23, fontweight="bold")
    title(fig, "Monthly sales, Jan 2024 to Jun 2025")
    ch["monthly-sales"] = save_webp(fig, "retail-sales", "monthly-sales")
    N["charts"] = ch
    return N

def attrition():
    raw = pd.read_csv(PROJ / "02-employee-attrition-analysis" / "data.csv")
    N = {"raw_rows": len(raw), "raw_cols": raw.shape[1], "duplicates": int(raw.duplicated().sum()),
         "missing": {k: int(v) for k, v in raw.isnull().sum().items() if v}}
    N["invalid_age_raw"] = int(((raw.Age < 18) | (raw.Age > 100)).sum())
    df = raw.drop_duplicates().reset_index(drop=True)
    N["invalid_age_after_dedup"] = int(((df.Age < 18) | (df.Age > 100)).sum())
    N["missing_dept_after_dedup"] = int(df.Department.isna().sum())
    N["missing_salary_after_dedup"] = int(df.Monthly_Salary.isna().sum())
    N["missing_sat_after_dedup"] = int(df.Job_Satisfaction.isna().sum())
    for c in ["Department", "Job_Level", "Overtime", "Remote_Work"]:
        df[c] = df[c].astype("string").str.strip().str.title()
    df["Department"] = df.Department.fillna("Unknown")
    df.loc[(df.Age < 18) | (df.Age > 100), "Age"] = np.nan
    df["Age"] = df.Age.fillna(df.Age.median())
    df.loc[df.Monthly_Salary <= 0, "Monthly_Salary"] = np.nan
    df["Monthly_Salary"] = df.Monthly_Salary.fillna(df.Monthly_Salary.median())
    df["Job_Satisfaction"] = df.Job_Satisfaction.clip(1, 5)
    df["Job_Satisfaction"] = df.Job_Satisfaction.fillna(df.Job_Satisfaction.median())

    N["clean_rows"], N["employees"] = len(df), int(df.Employee_ID.nunique())
    N["attrition_rate"], N["left"] = f(df.Attrition.mean() * 100), int(df.Attrition.sum())
    N["avg_salary"], N["avg_tenure"], N["avg_sat"] = f(df.Monthly_Salary.mean()), f(df.Years_At_Company.mean()), f(df.Job_Satisfaction.mean())
    N["salary_test"] = welch(df.loc[df.Attrition == 0, "Monthly_Salary"], df.loc[df.Attrition == 1, "Monthly_Salary"])  # notebook test
    N["salary_test"]["diff_pct_of_stayed"] = f(N["salary_test"]["diff"] / N["salary_test"]["mean_a"] * 100)

    def grp(col):
        g = df.groupby(col).Attrition.agg(["size", "sum", "mean"])
        return {str(k): {"n": int(v["size"]), "left": int(v["sum"]), "rate": f(v["mean"] * 100),
                         "ci": wilson(int(v["sum"]), int(v["size"]))} for k, v in g.iterrows()}
    N["by_department"], N["by_overtime"] = grp("Department"), grp("Overtime")
    N["by_satisfaction"], N["by_remote"], N["by_level"] = grp("Job_Satisfaction"), grp("Remote_Work"), grp("Job_Level")
    N["overtime_share_pct"] = f((df.Overtime == "Yes").mean() * 100)
    N["overtime_gap_pp"] = N["by_overtime"]["Yes"]["rate"] - N["by_overtime"]["No"]["rate"]
    N["chi_added"] = {c: chi2(df, c, "Attrition") for c in ["Department", "Overtime", "Job_Satisfaction", "Remote_Work", "Job_Level"]}
    low = df[df.Job_Satisfaction <= 2].Attrition
    high = df[df.Job_Satisfaction >= 3].Attrition
    N["sat_low_vs_high_added"] = {"low_n": int(len(low)), "low_rate": f(low.mean() * 100),
                                  "high_n": int(len(high)), "high_rate": f(high.mean() * 100)}
    N["other_tests_added"] = {}
    for col in ["Years_At_Company", "Age", "Training_Hours"]:
        a, b = df.loc[df.Attrition == 0, col], df.loc[df.Attrition == 1, col]
        N["other_tests_added"][col] = {"stayed": f(a.mean()), "left": f(b.mean()), "p": f(stats.ttest_ind(a, b, equal_var=False)[1])}

    ch = {}
    ov = N["by_overtime"]
    ch["attrition-by-overtime"] = vbars("employee-attrition", "attrition-by-overtime",
                                        ["No overtime", "Overtime"], [ov["No"]["rate"], ov["Yes"]["rate"]],
                                        [SLATE, GOLD], "Attrition rate by overtime", 50,
                                        sub=[f"{ov['No']['n']:,} employees", f"{ov['Yes']['n']:,} employees"],
                                        hline=N["attrition_rate"], hline_label=f"All employees {N['attrition_rate']:.1f}%")
    sv = N["by_satisfaction"]
    keys = ["1.0", "2.0", "3.0", "4.0", "5.0"]
    ch["attrition-by-satisfaction"] = vbars("employee-attrition", "attrition-by-satisfaction",
                                            ["1", "2", "3", "4", "5"], [sv[k]["rate"] for k in keys],
                                            [GOLD, GOLD, SLATE, SLATE, SLATE], "Attrition rate by job satisfaction score", 50,
                                            sub=["lowest", "", "", "", "highest"],
                                            hline=N["attrition_rate"], hline_label=f"All employees {N['attrition_rate']:.1f}%")
    dp = N["by_department"]
    order = sorted(dp, key=lambda k: -dp[k]["rate"])
    ch["attrition-by-department"] = hbars("employee-attrition", "attrition-by-department",
                                          [f"{('IT' if k in ('It',) else 'HR' if k == 'Hr' else k)}  (n={dp[k]['n']:,})" for k in order],
                                          [dp[k]["rate"] for k in order], [SLATE] * len(order),
                                          "Attrition rate by department", 50,
                                          err=[dp[k]["ci"] for k in order], vline=N["attrition_rate"],
                                          vline_label=f"All {N['attrition_rate']:.1f}%")
    N["charts"] = ch
    return N

def marketing():
    raw = pd.read_csv(PROJ / "03-marketing-campaign-performance-analysis" / "data.csv")
    N = {"raw_rows": len(raw), "raw_cols": raw.shape[1], "duplicates": int(raw.duplicated().sum()),
         "missing": {k: int(v) for k, v in raw.isnull().sum().items() if v}}
    N["invalid_age_raw"] = int(((raw.Age < 18) | (raw.Age > 100)).sum())
    N["negative_spend_raw"] = int((raw.Ad_Spend < 0).sum())
    df = raw.drop_duplicates().reset_index(drop=True)
    N["invalid_age_after_dedup"] = int(((df.Age < 18) | (df.Age > 100)).sum())
    N["negative_spend_after_dedup"] = int((df.Ad_Spend < 0).sum())
    for c in ["Channel", "Device"]:
        df[c] = df[c].astype("string").str.strip().str.title()
    df["Channel"] = df.Channel.fillna("Unknown")
    df["Device"] = df.Device.fillna("Unknown")
    df.loc[(df.Age < 18) | (df.Age > 100), "Age"] = np.nan
    df["Age"] = df.Age.fillna(df.Age.median())
    for c in ["Monthly_Income", "Ad_Spend"]:
        df.loc[df[c] < 0, c] = np.nan
        df[c] = df[c].fillna(df[c].median())
    for c in ["Website_Visits", "Ad_Clicks", "Previous_Purchases"]:
        df[c] = df[c].clip(lower=0)
    df["Engagement_Level"] = pd.cut(df.Ad_Clicks, bins=[-1, 1, 3, 6, np.inf], labels=["Low", "Medium", "High", "Very High"])

    ts, cv = df.Ad_Spend.sum(), int(df.Converted.sum())
    N["clean_rows"], N["leads"], N["conversions"] = len(df), int(df.Lead_ID.nunique()), cv
    N["conversion_rate"], N["total_spend"], N["cost_per_conversion"] = f(df.Converted.mean() * 100), f(ts), f(ts / cv)
    sp = welch(df.loc[df.Converted == 1, "Ad_Spend"], df.loc[df.Converted == 0, "Ad_Spend"])   # notebook test
    N["spend_test"] = sp

    def grp(col):
        g = df.groupby(col, observed=True).agg(n=("Converted", "size"), conv=("Converted", "sum"), spend=("Ad_Spend", "sum"))
        return {str(k): {"n": int(v.n), "conv": int(v.conv), "rate": f(v.conv / v.n * 100), "spend": f(v.spend),
                         "cost_per_conv": f(v.spend / v.conv), "ci": wilson(int(v.conv), int(v.n))} for k, v in g.iterrows()}
    N["by_channel"], N["by_device"], N["by_engagement"] = grp("Channel"), grp("Device"), grp("Engagement_Level")
    N["chi_added"] = {c: chi2(df, c, "Converted") for c in ["Channel", "Device", "Engagement_Level"]}
    hi = df[df.Ad_Clicks >= 4]
    lo = df[df.Ad_Clicks <= 1]
    N["clicks_4plus_added"] = {"n": int(len(hi)), "conv": int(hi.Converted.sum()), "rate": f(hi.Converted.mean() * 100),
                               "cost_per_conv": f(hi.Ad_Spend.sum() / hi.Converted.sum())}
    N["clicks_0to1_added"] = {"n": int(len(lo)), "conv": int(lo.Converted.sum()), "rate": f(lo.Converted.mean() * 100),
                              "cost_per_conv": f(lo.Ad_Spend.sum() / lo.Converted.sum())}
    N["spend_share_low_engagement_pct"] = f(lo.Ad_Spend.sum() / ts * 100)
    N["corr_spend_clicks_added"] = f(df[["Ad_Spend", "Ad_Clicks"]].corr().iloc[0, 1])
    N["by_prev_purchases_added"] = {str(k): {"n": int(v["size"]), "rate": f(v["mean"] * 100)}
                                    for k, v in df.groupby("Previous_Purchases").Converted.agg(["size", "mean"]).iterrows()}
    N["chi_added"]["Previous_Purchases"] = chi2(df, "Previous_Purchases", "Converted")
    N["avg_spend_by_engagement"] = {str(k): f(v) for k, v in df.groupby("Engagement_Level", observed=True).Ad_Spend.mean().items()}

    ch = {}
    eg = N["by_engagement"]
    names = ["Low", "Medium", "High", "Very High"]
    rng = {"Low": "0-1 clicks", "Medium": "2-3 clicks", "High": "4-6 clicks", "Very High": "7+ clicks"}
    ch["conversion-by-engagement"] = vbars("marketing-campaign", "conversion-by-engagement",
                                           [n.replace("Very High", "Very high") for n in names], [eg[n]["rate"] for n in names],
                                           [SLATE, SLATE, GOLD, GOLD], "Conversion rate by ad-click engagement", 50,
                                           sub=[f"{rng[n]}\n{eg[n]['n']:,} leads" for n in names],
                                           hline=N["conversion_rate"], hline_label=f"All leads {N['conversion_rate']:.1f}%")
    cc = N["by_channel"]
    order = sorted(cc, key=lambda k: -cc[k]["rate"])
    ch["conversion-by-channel"] = hbars("marketing-campaign", "conversion-by-channel",
                                        [f"{('Not recorded' if k == 'Unknown' else k)}  (n={cc[k]['n']:,})" for k in order],
                                        [cc[k]["rate"] for k in order], [SLATE] * len(order),
                                        "Conversion rate by channel", 50,
                                        err=[cc[k]["ci"] for k in order], vline=N["conversion_rate"],
                                        vline_label=f"All {N['conversion_rate']:.1f}%")
    N["charts"] = ch
    return N

def churn():
    raw = pd.read_csv(PROJ / "04-customer-churn-analysis" / "data.csv")
    N = {"raw_rows": len(raw), "raw_cols": raw.shape[1], "duplicates": int(raw.duplicated().sum()),
         "raw_churn_rate": f(raw.Churn.mean() * 100)}
    df = raw.drop_duplicates().reset_index(drop=True)
    N["clean_rows"] = len(df)
    N["missing_after_dedup"] = {k: int(v) for k, v in df.isnull().sum().items() if v}
    N["age_lt5"], N["age_gt100"] = int((df.Age < 5).sum()), int((df.Age > 100).sum())
    N["age_150"] = int((df.Age == 150).sum())
    N["spend_negative"], N["spend_99999"] = int((df.Monthly_Spend < 0).sum()), int((df.Monthly_Spend == 99999.99).sum())
    N["calls_negative"] = int((df.Customer_Service_Calls < 0).sum())
    N["region_labels_raw"], N["plan_labels_raw"] = int(raw.Region.nunique()), int(raw.Subscription_Plan.nunique())
    df["Payment_Method"] = df.Payment_Method.fillna("Unknown")
    df.loc[(df.Age < 5) | (df.Age > 100), "Age"] = np.nan
    df["Age"] = df.Age.fillna(df.Age.median())
    df.loc[df.Age == 150, "Age"] = np.nan
    df["Age"] = df.Age.fillna(df.Age.median())
    df["Monthly_Spend"] = df.Monthly_Spend.fillna(df.Monthly_Spend.median())
    df.loc[df.Monthly_Spend < 0, "Monthly_Spend"] = np.nan
    df["Monthly_Spend"] = df.Monthly_Spend.fillna(df.Monthly_Spend.median())
    df.loc[df.Monthly_Spend == 99999.99, "Monthly_Spend"] = np.nan
    df["Monthly_Spend"] = df.Monthly_Spend.fillna(df.Monthly_Spend.median())
    df.loc[df.Customer_Service_Calls < 0, "Customer_Service_Calls"] = np.nan
    df["Customer_Service_Calls"] = df.Customer_Service_Calls.fillna(df.Customer_Service_Calls.median())
    df["Region"] = df.Region.str.title()
    df["Subscription_Plan"] = df.Subscription_Plan.str.title()
    N["age_under_18_remaining"] = int((df.Age < 18).sum())
    N["age_min_after"] = f(df.Age.min())
    N["churned"], N["churn_rate"] = int(df.Churn.sum()), f(df.Churn.mean() * 100)
    N["retained"] = int(len(df) - df.Churn.sum())
    df["Login_Activity"] = pd.cut(df.Days_Since_Last_Login, bins=[-1, 30, 90, float("inf")], labels=["Active", "At Risk", "Inactive"])
    df["days_bucket"] = pd.cut(df.Days_Since_Last_Login, bins=[-1, 30, 60, 90, 120, 150, 200],
                               labels=["0-30", "31-60", "61-90", "91-120", "121-150", "151+"])
    df["calls_bucket"] = df.Customer_Service_Calls.clip(upper=6).astype(int).astype(str).replace({"6": "6+"})

    def grp(col):
        g = df.groupby(col, observed=True).Churn.agg(["size", "sum", "mean"])
        return {str(k): {"n": int(v["size"]), "churned": int(v["sum"]), "rate": f(v["mean"] * 100),
                         "ci": wilson(int(v["sum"]), int(v["size"]))} for k, v in g.iterrows()}
    for key, col in [("by_plan", "Subscription_Plan"), ("by_activity", "Login_Activity"), ("by_days", "days_bucket"),
                     ("by_region", "Region"), ("by_gender", "Gender"), ("by_payment", "Payment_Method"), ("by_calls", "calls_bucket")]:
        N[key] = grp(col)
    N["chi_added"] = {c: chi2(df, c, "Churn") for c in ["Subscription_Plan", "Login_Activity", "days_bucket", "Region", "Gender", "Payment_Method", "Customer_Service_Calls"]}
    N["num_tests"] = {}
    for col in ["Customer_Service_Calls", "Monthly_Spend", "Age", "Days_Since_Last_Login"]:
        a, b = df.loc[df.Churn == 0, col], df.loc[df.Churn == 1, col]
        t = welch(b, a)   # churned minus retained
        t["mean_churned"], t["mean_retained"] = f(b.mean()), f(a.mean())
        N["num_tests"][col] = t
    N["avg_spend_by_plan"] = {k: f(v) for k, v in df.groupby("Subscription_Plan").Monthly_Spend.mean().items()}
    N["plan_by_activity_added"] = {p: {a: f(v) for a, v in row.items()} for p, row in
                                   df.pivot_table(index="Subscription_Plan", columns="Login_Activity", values="Churn", aggfunc="mean", observed=True).mul(100).iterrows()}
    c3 = df[df.Customer_Service_Calls >= 3]
    N["calls_3plus"] = {"n": int(len(c3)), "churned": int(c3.Churn.sum()), "rate": f(c3.Churn.mean() * 100)}
    c02 = df[df.Customer_Service_Calls <= 2]
    N["calls_0to2"] = {"n": int(len(c02)), "rate": f(c02.Churn.mean() * 100)}
    N["age_invalid_total"] = N["age_lt5"] + N["age_gt100"]
    N["gender_counts"] = {k: int(v) for k, v in df.Gender.value_counts().items()}

    ch = {}
    order = ["0-30", "31-60", "61-90", "91-120", "121-150", "151+"]
    dd = N["by_days"]
    ch["churn-by-login-recency"] = lineplot("customer-churn", "churn-by-login-recency", order, [dd[k]["rate"] for k in order],
                                            "Churn rate by days since last login", 110,
                                            hline=N["churn_rate"], hline_label=f"All customers {N['churn_rate']:.1f}%",
                                            sub=[f"{dd[k]['n']:,}" for k in order])
    pl = N["by_plan"]
    porder = ["Basic", "Pro", "Plus"]
    ch["churn-by-plan"] = vbars("customer-churn", "churn-by-plan", porder, [pl[k]["rate"] for k in porder],
                                [GOLD, SLATE, SLATE], "Churn rate by subscription plan", 100,
                                sub=[f"{pl[k]['n']:,} customers" for k in porder],
                                hline=N["churn_rate"], hline_label=f"All customers {N['churn_rate']:.1f}%")
    cl = N["by_calls"]
    corder = ["0", "1", "2", "3", "4", "5", "6+"]
    ch["churn-by-service-calls"] = lineplot("customer-churn", "churn-by-service-calls", corder, [cl[k]["rate"] for k in corder],
                                            "Churn rate by customer service calls", 110,
                                            hline=N["churn_rate"], hline_label=f"All customers {N['churn_rate']:.1f}%",
                                            sub=[f"{cl[k]['n']:,}" for k in corder])
    N["charts"] = ch
    return N

if __name__ == "__main__":
    out = {"retail": retail(), "attrition": attrition(), "marketing": marketing(), "churn": churn()}
    (ROOT / "tools" / "numbers.json").write_text(json.dumps(out, indent=1, default=float))
    for k, v in out.items():
        for name, c in v["charts"].items():
            print(f"{k:10s} {c['file']:75s} {c['width']}x{c['height']}  {c['bytes'] / 1024:.0f} KB")
