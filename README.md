# Moaz Ahmed | Data Analyst Portfolio

Static site (HTML, CSS, JS). No build step.

```
index.html
assets/css/style.css        glass theme and 3D styles
assets/css/enhance.css      intro, chessboard floor, cursor
assets/js/enhance.js        Opera Game move list, intro, cursor, result badges
assets/js/enhance3d.js      3D chess world (Three.js r128): reflective ivory and obsidian pieces, environment lighting, sculpted knight; scroll plays the Opera Game
assets/css/premium.css      design layer: SF-style system type, champagne palette, refined glass, window bars, reveal
assets/css/projects.css     project cards and case-study pages
assets/js/premium.js        scroll reveal, magnetic buttons, hero depth
assets/js/main.js           tilt, Three.js hero, chessboard, charts, form
assets/certificates/        IBM Data Fundamentals (PDF and preview)
projects/01..04-*/          analysis.ipynb, analysis.html (case study), data.csv, README.md
assets/img/projects/<slug>/ WebP charts used by the cards and case studies
tools/                      dev only, not needed to run the site (see below)
```

## Before publishing
LinkedIn and email are set. Add your GitHub URL to `GH` at the top of `assets/js/main.js` to show the GitHub links.

## Run locally
`python -m http.server 8000` then open http://localhost:8000

## Deploy on GitHub Pages
Push the folder to a repo, then Settings > Pages > Deploy from branch > `main` / root.

## Sharing preview
`assets/img/og.png` is the link-preview image. After deploying, change the `og:image` URL in `index.html` to the full address (for example https://your-name.github.io/repo/assets/img/og.png) so LinkedIn shows it.

## 3D background
Loaded from cdnjs (Three.js r128). If WebGL or the CDN is unavailable the page falls back to the normal 2D layout.

## Rebuilding the project numbers, charts and pages
The site itself has no build step. The `tools/` folder is only for regenerating the project content:

```
pip install pandas numpy scipy matplotlib pillow
python3 tools/build_project_assets.py   # recomputes every number from projects/*/data.csv, writes tools/numbers.json and the WebP charts
python3 tools/build_pages.py            # rewrites the Featured projects section, the four analysis.html pages and the project READMEs
```

Every figure on the cards and case studies comes from `tools/numbers.json`. Search the case studies for `TODO` to find any facts that still need an answer.
