# Changelog

## v12: Featured projects rebuilt from the four notebooks

**Numbers corrected** (checked against the notebooks and data.csv)
- Retail card: category shares were wrong (Electronics 58.3%, Home 14.3%, Sports 11.5%, Clothing 8.9%). Correct: 57.2%, 14.4%, 11.4%, 9.1%, plus 0.9% with no category. The card said the t-test compared sales; it compares profit per order, discounted vs full price.
- Churn card: "6 data-quality fixes" had no source and is gone. The old README said "995 missing or invalid ages"; 995 are missing and 44 more are invalid.
- Attrition and marketing cards: the department and channel rankings were shown as findings. Chi-square tests say they are within noise (p = 0.70 and p = 0.40), so the cards now say so. The t-test named on each card is on salary (attrition) and ad spend (marketing).
- Verified and kept: 2.37M sales, 6,000 orders, 394.61 order value, 30.9% margin, p = 0.0015; 25.8% attrition, 7,000 employees, 7.5 years, p < 0.0001; 19.4% conversion, 6,500 leads, 1,259 conversions, 1,034 per conversion, p = 0.28; 76.3% churn, 10,000 customers, 300 duplicates. "30K+ records" matches 30,120 raw rows.

**Added**
- Project cards: one-line problem, recommendation, three headline numbers, one chart, tools, links.
- Case studies (analysis.html) with Problem, Data, Method, What I found, Recommendation, What I would do next; window bars, back link, previous/next links.
- 11 WebP charts in `assets/img/projects/<slug>/` (1200px wide, 18 to 34 KB) with alt text.
- Honest notes on weak or non-significant results, and 13 `TODO for Moaz` markers.
- `assets/css/projects.css`, `tools/` (number and chart generators), project READMEs regenerated.

**Changed**
- `windows.js`: a panel can set its own window title with `data-title`.
- `main.js`: removed the hard-coded chart data (it held the wrong retail numbers).
- `enhance.js`: removed the hard-coded "Best move" lines that repeated those numbers.
- Dataset links download under the file name each notebook reads (for example `customer churn.csv`).
- Churn card no longer lists Seaborn or SciPy: that notebook imports them but never uses them.
- Old nbconvert exports of analysis.html were replaced by the case studies (still in the v11 zip).

## v13: Subtle polish pass

**Toned down**
- Noise overlay opacity: .07 → .035
- Orbs: .10/.08 → .06/.04; spotlight: .08 → .04
- Holo rainbow on cert cards: .18 → .10
- Glass card shadow: softer spread (70px → 50px)
- Card tilt: max angle from 14° to 6°, scale from 1.03 to 1.01, perspective from 900 to 1200

**Improved readability**
- `Data Analyst` subtitle opacity: .50 → .65
- Muted text (--mut) opacity: .62 → .70
- Section bottom padding: 24px → 64px for better breathing room

**Cleaned up**
- Removed chess knight icon (♞) from the progress bar
- Removed unused Google Fonts (Inter) load — system font stack covers it
- Fixed conflicting .lead margin-bottom (36px vs 44px → 44px)
- Fixed skills chessboard info card height shift on hover (min-height)

- Removed custom cursor logic and HTML to restore default pointer

- Removed smoothing interpolation on custom cursor so it tracks 1:1 with zero lag

- Added scrolling Typewriter effect to all section titles and lead paragraphs
