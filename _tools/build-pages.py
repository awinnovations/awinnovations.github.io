#!/usr/bin/env python3
"""Regenerates guide.html, privacy.html, accessibility.html and 404.html.
Optional helper only: the site is plain static files and needs no build step.
Run from the site folder:  python3 _tools/build-pages.py [path/to/voice-cloning-guide.md]
"""
import re, sys, pathlib, markdown, html

SITE = pathlib.Path(__file__).resolve().parent.parent
GUIDE_MD = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else SITE.parent / "drafts" / "voice-cloning-guide.md"
PDF = "downloads/agewell-voice-cloning-guide.pdf"

def head(title, desc, canonical):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- PREVIEW: remove the next line at launch, once every [CONFIRM] item is resolved. -->
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'self' https://*.sibforms.com; form-action 'self' https://*.sibforms.com; base-uri 'self'; object-src 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="theme-color" content="#15324F">
<link rel="canonical" href="https://awinnovations.org/{canonical}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/AtkinsonHyperlegibleNext-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css">
<script src="assets/js/config.js" defer></script>
<script src="assets/js/site.js" defer></script>
</head>
<body>
<svg width="0" height="0" class="sprite" aria-hidden="true" focusable="false">
  <symbol id="mae-face" viewBox="0 0 120 120">
    <path d="M22 60a38 38 0 0 1 76 0" fill="none" stroke="#D97732" stroke-width="7" stroke-linecap="round"/>
    <rect x="20" y="28" width="80" height="70" rx="33" fill="#FBF7EE" stroke="#E2D8C6" stroke-width="2"/>
    <rect x="28" y="37" width="64" height="52" rx="24" fill="#15324F"/>
    <ellipse cx="48" cy="60" rx="6" ry="8" fill="#D97732"/><ellipse cx="72" cy="60" rx="6" ry="8" fill="#D97732"/>
    <path d="M53 74q7 6 14 0" fill="none" stroke="#FBF7EE" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="19" cy="63" r="10" fill="#D97732"/><circle cx="19" cy="63" r="4.5" fill="#15324F"/>
    <circle cx="101" cy="63" r="10" fill="#D97732"/><circle cx="101" cy="63" r="4.5" fill="#15324F"/>
  </symbol>
</svg>
<a class="skip-link" href="#main">Skip to main content</a>
<aside class="preview-bar" aria-label="Preview notice"><p><strong>Preview for review.</strong> Not public yet. Items marked <mark class="confirm">[CONFIRM]</mark> need a decision before launch.</p></aside>
<header class="site-header" id="top">
  <div class="wrap header-inner">
    <a class="brand" href="index.html" aria-label="AgeWell Innovations home">
      <svg class="brand-mark" aria-hidden="true" focusable="false"><use href="#mae-face"/></svg>
      <span class="brand-text" aria-hidden="true"><span class="brand-name">AgeWell</span><span class="brand-sub">Innovations</span></span>
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
      <span class="menu-icon" aria-hidden="true"><span></span><span></span><span></span></span>
      <span class="menu-label">Menu</span>
    </button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>
        <li><a href="index.html#programs">Programs</a></li>
        <li><a href="index.html#learn">Learn</a></li>
        <li><a href="index.html#mable-and-mae">Mable &amp; Mae</a></li>
        <li><a href="index.html#newsletter">Newsletter</a></li>
        <li><a href="index.html#events">Events</a></li>
        <li><a href="index.html#about">About</a></li>
        <li class="nav-cta"><a class="btn btn-primary btn-small" href="index.html#newsletter">Get the AgeWell Update</a></li>
      </ul>
    </nav>
  </div>
</header>
"""

FOOT = """
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <p class="footer-name"><svg class="brand-mark" aria-hidden="true" focusable="false"><use href="#mae-face"/></svg> AgeWell Innovations</p>
      <p class="footer-tag">Technology with care.</p>
      <p>Helping older adults and caregivers across the US understand technology, recognize scams and build confidence.</p>
    </div>
    <nav aria-label="Footer">
      <ul class="footer-links">
        <li><a href="index.html#programs">Programs</a></li>
        <li><a href="index.html#learn">Learn</a></li>
        <li><a href="index.html#mable-and-mae">Mable &amp; Mae</a></li>
        <li><a href="index.html#newsletter">Newsletter</a></li>
        <li><a href="index.html#events">Events</a></li>
        <li><a href="index.html#about">About</a></li>
        <li><a href="index.html#contact">Contact</a></li>
        <li><a href="privacy.html">Privacy notice</a></li>
        <li><a href="accessibility.html">Accessibility</a></li>
      </ul>
    </nav>
    <div>
      <p class="footer-head">Follow along</p>
      <ul class="footer-links">
        <li><a href="https://x.com/AW_Innovations" rel="noopener">X: @AW_Innovations</a></li>
        <li><a href="https://www.facebook.com/agewellinnovations" rel="noopener">Facebook: AgeWell Innovations</a></li>
        <li><a href="https://www.instagram.com/aw_innovations_/" rel="noopener">Instagram: @aw_innovations_</a></li>
        <li><a href="https://www.youtube.com/@AW_Innovations" rel="noopener">YouTube: @AW_Innovations</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-legal">
    <p>United States · <mark class="confirm confirm-dark">[CONFIRM LEGAL LINE: Alabama-registered organization; mailing address PO box TBD]</mark></p>
    <p>AgeWell Innovations is not yet recognized by the IRS as a 501(c)(3) organization. Our content is general education, not legal or financial advice.</p>
    <p>Mable &amp; Mae artwork created with AI assistance and reviewed by AgeWell Innovations.</p>
    <p>© 2026 AgeWell Innovations <mark class="confirm confirm-dark">[CONFIRM EXACT LEGAL NAME]</mark></p>
    <p><a href="#top">Back to top</a></p>
  </div>
</footer>
</body>
</html>
"""

def confirm_marks(s):
    # Turn [CONFIRM ...] / [CONFIRM: ...] placeholders into visible marks.
    return re.sub(r"\[(CONFIRM[^\]]*)\]", r'<mark class="confirm">[\1]</mark>', s)

def build_guide():
    md = GUIDE_MD.read_text(encoding="utf-8")
    md = re.sub(r"^>\s*\*\*DRAFT FOR REVIEW\*\*.*\n", "", md, flags=re.M)      # draft banner
    md = re.split(r"^### Reviewer notes", md, flags=re.M)[0]                  # reviewer notes
    md = md.rstrip().rstrip("-").rstrip()
    # Split title block (H1 + H2 subtitle + byline) from the body.
    m = re.search(r"^# ([^\n]+)\n+## ([^\n]+)\n+(.*?)\n---", md, flags=re.S | re.M)
    title, subtitle, byline = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
    body = md[m.end():]
    # The final block after the last --- is the footer/legal block; render it smaller.
    parts = body.rsplit("\n---\n", 1)
    main_md, foot_md = (parts[0], parts[1]) if len(parts) == 2 else (body, "")
    main_md = re.sub(r"\n---\n", "\n", main_md)
    conv = markdown.Markdown(extensions=["toc", "sane_lists", "smarty"], extension_configs={"toc": {"permalink": False}})
    main_html = conv.convert(main_md)
    main_html = re.sub(r"(https?://[^\s<]+)", lambda mm: f'<a href="{mm.group(1)}" rel="noopener">{mm.group(1)}</a>', main_html)
    main_html = main_html.replace('<h2 id="sources-checked-october-7-2026">', '<h2 id="sources">')
    main_html = re.sub(r'(<h2 id="sources">.*?</h2>\s*)<ol>', r'\1<ol class="sources">', main_html, flags=re.S)
    main_html = re.sub(r'(<h2 id="the-short-version">.*?)(?=<h2 )', r'<section class="short-version">\1</section>\n', main_html, count=1, flags=re.S)
    foot_html = markdown.markdown(foot_md, extensions=["sane_lists", "smarty"]) if foot_md else ""
    byline_html = markdown.markdown(byline, extensions=["smarty"])
    page = head(f"{html.escape(title)} | AgeWell Innovations",
                "A plain-language guide to checking a surprise call for help: pause, hang up and call back on a number you already know.",
                "guide.html")
    page += f"""<main id="main" tabindex="-1">
<div class="page-hero"><div class="wrap narrow">
  <p class="crumb"><a href="index.html#learn">← Back to Learn</a></p>
  <p class="kicker">Guide 1 · A familiar voice is not proof of identity</p>
  <h1>{html.escape(title)}</h1>
  <p class="subhead">{html.escape(subtitle)}</p>
  {byline_html}
  <div class="page-actions">
    <a class="btn btn-primary" href="{PDF}" download>Download the printable guide (PDF, large type)</a>
    <a class="btn btn-secondary" href="index.html#practice">Try the practice exercise</a>
  </div>
</div></div>
<article class="prose wrap narrow">
{confirm_marks(main_html)}
<div class="callout">{confirm_marks(foot_html)}</div>
</article>
</main>
"""
    page += FOOT
    (SITE / "guide.html").write_text(page, encoding="utf-8")

def simple(name, title, desc, inner):
    page = head(f"{title} | AgeWell Innovations", desc, name)
    page += f"""<main id="main" tabindex="-1">
<div class="page-hero"><div class="wrap narrow"><p class="crumb"><a href="index.html">← AgeWell Innovations home</a></p><h1>{title}</h1></div></div>
<article class="prose wrap narrow">
{inner}
</article>
</main>
"""
    page += FOOT
    (SITE / name).write_text(page, encoding="utf-8")

PRIVACY = """
<p class="small"><mark class="confirm">[CONFIRM: effective date and privacy notice owner/review before launch]</mark></p>
<p>We ask only for what we need, and we use it only for what you asked us to do.</p>
<h2>What we collect</h2>
<ul>
<li><strong>Newsletter signup:</strong> your email address and, if you choose, your first name. If you check the box for safety alerts, we record that choice separately. We also keep a record of when and where you agreed, so we can show you asked to hear from us.</li>
<li><strong>Interest list:</strong> your email address, and if you choose, your name, organization, the items you checked and a short message.</li>
<li><strong>Nothing else on purpose.</strong> Please don’t send birth dates, health details or details about money lost to a scam.</li>
</ul>
<h2>What this website does not do</h2>
<ul>
<li>No advertising or tracking cookies, and no analytics scripts.</li>
<li>No requests for your microphone, camera or location.</li>
<li>The practice exercise is fictional and saves nothing.</li>
<li>Fonts and images are served from this website, not from outside services.</li>
</ul>
<p>Like most websites, our web host may keep short-term technical logs (such as IP addresses) to run and protect the site. <mark class="confirm">[CONFIRM: hosting provider name and its log policy]</mark></p>
<h2>How we use it</h2>
<p>To send the emails you asked for and to reply about the items you checked. We use Brevo to store contacts and send our emails. You can unsubscribe any time with the link in every email. We don’t sell your information. <mark class="confirm">[CONFIRM]</mark></p>
<h2>Your choices</h2>
<ul>
<li>Unsubscribe with the link at the bottom of any email.</li>
<li>Ask us to see, correct or delete your information at <mark class="confirm">[CONFIRM INBOX]</mark>.</li>
</ul>
<h2>Questions</h2>
<p>Write to us at <mark class="confirm">[CONFIRM INBOX]</mark>.</p>
"""

ACCESS = """
<p>We want this site to be easy for everyone to use, including people who use screen readers, keyboards, magnifiers or larger text.</p>
<h2>What we’ve done</h2>
<ul>
<li>Large, readable text in Atkinson Hyperlegible Next, a typeface designed for low-vision readers.</li>
<li>Color combinations checked for contrast. Copper is used for decoration, not for important text.</li>
<li>Every control works with a keyboard, with a visible focus outline.</li>
<li>Animations are short and gentle. They switch off if your device asks for reduced motion, and Mae’s greeting has a pause button.</li>
<li>The comic is set as real text, with a full transcript. Images have text descriptions.</li>
<li>The guide is available as a web page and as a large-type PDF.</li>
<li>Forms have clear labels, and error messages are written out in words, not shown by color alone.</li>
</ul>
<h2>Known gaps</h2>
<ul>
<li>Finished comic artwork is still in production. The script and transcript are complete.</li>
<li>We haven’t yet tested this site with older adult readers. We plan to, and we’ll fix what we learn.</li>
</ul>
<h2>Tell us what’s hard to use</h2>
<p>If anything on this site is hard to use, tell us at <mark class="confirm">[CONFIRM INBOX]</mark> and we’ll help you get the information another way.</p>
<p class="small">Last reviewed October 2026.</p>
"""

NOTFOUND = """
<p>We couldn’t find that page. It may have moved.</p>
<ul>
<li><a href="index.html">Go to the AgeWell Innovations home page</a></li>
<li><a href="guide.html">Read the guide: A familiar voice is not proof of identity</a></li>
<li><a href="index.html#newsletter">Get the AgeWell Update</a></li>
</ul>
"""

if __name__ == "__main__":
    build_guide()
    simple("privacy.html", "Privacy notice", "How AgeWell Innovations handles the little information we collect.", PRIVACY)
    simple("accessibility.html", "Accessibility", "How AgeWell Innovations makes this site easy to use, and how to tell us what isn’t.", ACCESS)
    simple("404.html", "Page not found", "This page could not be found.", NOTFOUND)
    print("built guide.html, privacy.html, accessibility.html, 404.html from", GUIDE_MD)
