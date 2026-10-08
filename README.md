# AgeWell Innovations website (awinnovations.org)

Plain HTML/CSS/JS. No build step and no server code. Serve the folder as-is.

- `index.html`: homepage (all main sections)
- `guide.html`, `privacy.html`, `accessibility.html`, `404.html`: supporting pages
- `downloads/agewell-voice-cloning-guide.pdf`: printable guide (generated from `guide.html` print styles)
- `assets/js/config.js`: **the only file to edit to connect the Brevo forms** (paste each Brevo form's public `action` URL). Never put an API key in this repo.
- `assets/fonts/`: Fraunces and Atkinson Hyperlegible Next, SIL Open Font License 1.1 (license files included)
- `_tools/build-pages.py`: optional helper that regenerates the guide/privacy/accessibility/404 pages from `../drafts/voice-cloning-guide.md`
- `_headers`: security headers for Netlify / Cloudflare Pages (ignored by GitHub Pages)
- `CNAME`: custom domain for GitHub Pages branch publishing (ignored elsewhere)

Preview state: every page carries `<meta name="robots" content="noindex, nofollow">` and a "Preview for review" bar. Remove both at launch once every `[CONFIRM]` mark is resolved (`grep -rn "CONFIRM\|noindex\|preview-bar" *.html _tools`).

Local preview: `python3 -m http.server 8765` then open http://127.0.0.1:8765/

Rollback: `git revert <commit>` (or redeploy the previous commit/deploy on the host).
