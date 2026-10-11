# AgeWell Innovations website (awinnovations.org)

Plain HTML/CSS/JS. No build step and no server code. Serve the folder as-is.

- `index.html`: homepage (all main sections)
- `guide.html`, `privacy.html`, `accessibility.html`, `404.html`, `notes.html`: supporting pages (`notes.html` = AI & Safety Notes archive)
- `assets/data/notes.json`: the single source for AI & Safety Notes (homepage cards, archive, Ask Mae). Publication is manual: a person writes and checks each note against its official source, sets `reviewed`, then runs `python3 _tools/build-pages.py`.
- `assets/js/ask-mae.js` + `assets/data/mae-knowledge.json`: Ask Mae **demo** (prewritten answers, no AI service, no network calls, nothing stored). Edit answers in `_tools/mae-knowledge.src.py`, then run `python3 _tools/mae-knowledge.src.py`. Live AI plan: `../site-evidence/ask-mae-live-ai-plan.md`.
- `downloads/agewell-voice-cloning-guide.pdf`: printable guide (generated from `guide.html` print styles)
- `assets/js/config.js`: **the only file to edit to connect the Brevo forms** (paste each Brevo form's public `action` URL) **and the donation checkout** (`donateUrl`; empty = Donate hidden everywhere; `reviewShowDonate` is review-only and must stay `false`). Never put an API key in this repo. See `../site-evidence/brevo-setup-checklist.md` and `../site-evidence/donation-options.md`.
- `assets/fonts/`: Fraunces and Atkinson Hyperlegible Next, SIL Open Font License 1.1 (license files included)
- `_tools/build-pages.py`: regenerates guide/privacy/accessibility/404/notes pages and the `<!-- GEN:… -->` blocks in `index.html` (nav, notes cards, Ask Mae dialog, footer). Idempotent. Edit the templates there, not the generated blocks.
- PDF: after rebuilding, `google-chrome --headless=new --no-pdf-header-footer --print-to-pdf=downloads/agewell-voice-cloning-guide.pdf http://127.0.0.1:8765/guide.html`
- `_headers`: security headers for Netlify / Cloudflare Pages (ignored by GitHub Pages)
- `CNAME`: intentionally absent during the GitHub Pages preview (https://awinnovations.github.io/). Re-add it (single line `awinnovations.org`) at cutover, after the domain is verified and DNS points to GitHub. See launch-plan.md.
- `robots.txt`: preview blocks all crawling (`Disallow: /`). At launch replace with `Allow: /` plus `Sitemap: https://awinnovations.org/sitemap.xml`.

Preview state: every page carries `<meta name="robots" content="noindex, nofollow">` and a "Preview for review" bar. Remove both at launch once every `[CONFIRM]` mark is resolved (`grep -rn "CONFIRM\|noindex\|preview-bar" *.html _tools`).

Local preview: `python3 -m http.server 8765` then open http://127.0.0.1:8765/

Rollback: `git revert <commit>` (or redeploy the previous commit/deploy on the host).
