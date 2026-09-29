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

- Fused new About Me text with the chess metaphor (kept "read a position before I move") and updated Contact section.
- Built interactive Window Manager for glass panels:
  - Red dot: closes window with scale-down animation
  - Yellow dot: maximizes window (overrides tilt, locks scroll)
  - Green dot: minimizes window to a new macOS-style Taskbar (Dock) on the right
  - Dock: highly styled glassy dock that expands as windows are minimized. Clicking a dock item restores the window.
- Fixed z-index conflict with custom cursor when windows are maximized.
- Enforced !important on window animations to prevent override by the continuous tilt requestAnimationFrame.

- Precision Genie Effect: Minimized windows now calculate their exact trajectory to fly perfectly into their corresponding Taskbar circle, and grow back out of it.
- Title bar stability: Disabled 3D tilt effect when hovering the top bar of a window, allowing stable interaction with the red/yellow/green buttons.
- Maximize animation: Added a pop-up grow animation instead of instant snap when maximizing.

- Fixed window minimize/maximize/close flying to the dock with no transform animation on tilt cards: `.win.win-animating` had `!important` inside a comma list (invalid, dropped) and `.js .rv2` transition overrode `.win`. Rule is valid now.
- Window manager: minimize/restore now lock the tilt, flatten the card with an inline `transition:none !important`, force a reflow, then add `.win-minimized` in the next frame. Flight path is measured after flattening and re-measured on restore.
- main.js: the animation lock is checked before the title-bar branch.

## v14: Skill title chips on the skills board

- Each piece on the skills chessboard now shows a small rectangle that rises from it with the skill title only (no description). Hover, focus or tap a piece to bring it up; the detail text stays in the side card.
- Same look as the rest of the site: dark glass, hairline border, 10px radius, a 2px left accent in the piece colour (pawns grey, knights and bishops ice blue, rooks and queen pale gold, king gold), and a thin stem down to the piece.
- The chip follows the piece when the board tilts with the pointer, and is clamped to the board area so it never leaves the screen (checked at 1440px and 390px).
- `main.js`: chip logic next to the piece data. `premium.css`: `.sklab` styles at the end. Cache version bumped to v=26 for both files.

## v15: Contact form sends to email

- The contact form now posts to FormSubmit (`formsubmit.co/ajax/<EMAIL>`), so each message lands in mezoahme136@gmail.com as a formatted "box" email with the subject "New portfolio message from <name>". A copy goes to elorex909@gmail.com through FormSubmit's `_cc` field. The sender's address is set as reply-to, so Reply goes straight to them.
- Button shows "Sending…", then a status line under it says sent or failed. If the request fails, the status offers a mailto link (with the second address in cc) and the message pre-filled.
- Hidden honeypot field (`_honey`) blocks simple spam bots.
- `index.html`: name attributes on the fields, honeypot, status line. `main.js`: `EMAIL_CC` constant and new submit handler. `premium.css`: `.fs` and `.hp` styles at the end. Cache version bumped to v=27 for main.js and premium.css.
- Setup step: the first message triggers an activation email from FormSubmit to mezoahme136@gmail.com. Click the activate link once, from the deployed site.
