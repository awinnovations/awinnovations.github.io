#!/usr/bin/env python3
"""Regenerates guide.html, privacy.html, accessibility.html, 404.html and notes.html,
and refreshes the generated blocks inside index.html (nav, AI & Safety Notes cards,
Ask Mae dialog, footer) from shared templates and assets/data/notes.json.
Optional helper only: the site is plain static files and needs no build step.
Run from the site folder:  python3 _tools/build-pages.py [path/to/voice-cloning-guide.md]
"""
import re, sys, json, pathlib, markdown, html

SITE = pathlib.Path(__file__).resolve().parent.parent
GUIDE_MD = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else SITE.parent / "drafts" / "voice-cloning-guide.md"
PDF = "downloads/agewell-voice-cloning-guide.pdf"

def head(title, desc, canonical, scripts=("assets/js/config.js", "assets/js/site.js")):
    script_tags = "\n".join(f'<script src="{x}" defer></script>' for x in scripts)
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
{script_tags}
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
{nav("index.html")}
  </div>
</header>
"""


def nav(prefix=""):
    """Main navigation. prefix="" on the homepage (same-page anchors), "index.html" elsewhere."""
    items = [("programs", "Programs"), ("learn", "Learn"), ("mable-and-mae", "Mable &amp; Mae"), ("newsletter", "Newsletter"),
             ("events", "Events"), ("about", "About"), ("support", "Donate")]
    # Donate stays hidden until donateUrl is set in assets/js/config.js (site.js reveals it).
    lis = "\n".join((f'        <li data-donate-show hidden><a href="{prefix}#{a}">{t}</a></li>' if a == "support"
                      else f'        <li><a href="{prefix}#{a}">{t}</a></li>') for a, t in items)
    return f"""    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>
{lis}
        <li class="nav-cta"><a class="btn btn-primary btn-small" href="{prefix}#signup">Get the AgeWell Update</a></li>
      </ul>
    </nav>"""

def footer(prefix=""):
    return f"""
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <p class="footer-name"><svg class="brand-mark" aria-hidden="true" focusable="false"><use href="#mae-face"/></svg> AgeWell Innovations</p>
      <p class="footer-tag">Technology with care.</p>
      <p>Helping older adults and caregivers across the US understand technology, recognize scams and build confidence.</p>
    </div>
    <nav aria-label="Footer">
      <ul class="footer-links">
        <li><a href="{prefix}#programs">Programs</a></li>
        <li><a href="{prefix}#learn">Learn</a></li>
        <li><a href="notes.html">AI &amp; Safety Notes</a></li>
        <li><a href="{prefix}#ask-mae-section">Ask Mae (demo)</a></li>
        <li><a href="{prefix}#mable-and-mae">Mable &amp; Mae</a></li>
        <li><a href="{prefix}#newsletter">Newsletter</a></li>
        <li><a href="{prefix}#events">Events</a></li>
        <li><a href="{prefix}#about">About</a></li>
        <li data-donate-show hidden><a href="{prefix}#support">Donate</a></li>
        <li><a href="{prefix}#contact">Contact</a></li>
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
      <p class="footer-head footer-head-gap">Contact</p>
      <p><a href="mailto:hello@awinnovations.org">hello@awinnovations.org</a></p>
    </div>
  </div>
  <div class="wrap footer-legal">
    <!-- INTERNAL TODO (not shown on site): confirmed mailing address. Do not publish a placeholder or a home address. Required before the Brevo welcome email can be finalized. See site-evidence/brevo-setup-checklist.md. -->
    <p>United States · <mark class="confirm confirm-dark">[CONFIRM LEGAL LINE: exact registered legal name and legal-status wording]</mark></p>
    <p>AgeWell Innovations is not yet recognized by the IRS as a 501(c)(3) organization. <mark class="confirm confirm-dark">[CONFIRM LEGAL-STATUS WORDING]</mark> Our content is general education, not legal or financial advice.</p>
    <p>Artwork created with AI assistance and reviewed by AgeWell Innovations.</p>
    <p>© 2026 AgeWell Innovations.</p>
    <p><a href="#top">Back to top</a></p>
  </div>
</footer>
"""

FOOT = footer("index.html") + "</body>\n</html>\n"


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
<p>We ask only for what we need, and we use it only for what you asked us to do. This notice was last checked on October 11, 2026.</p>
<h2>What this website collects today</h2>
<ul>
<li><strong>Newsletter signup (preview):</strong> the signup form is not connected yet. Right now it only checks what you typed, on your own device, and shows a message. Nothing is sent or saved.</li>
<li><strong>Interest list (preview):</strong> also not connected yet. Nothing is sent or saved.</li>
<li><strong>Ask Mae (demo):</strong> see the next section.</li>
<li><strong>Email:</strong> if you write to <a href="mailto:hello@awinnovations.org">hello@awinnovations.org</a>, we receive your message and email address so we can reply.</li>
</ul>
<h2 id="ask-mae">Ask Mae (demo)</h2>
<ul>
<li>Ask Mae is a demonstration. Its answers are prewritten by AgeWell and are part of this website.</li>
<li>It runs in your web browser. What you type or tap in Ask Mae is not sent to AgeWell or to any AI company, and AgeWell does not store it.</li>
<li>The chat is not saved on your device, and it is gone when you close or reload the page. Ask Mae uses no cookies.</li>
<li>Even so, please don’t type passwords, verification codes or account details into Ask Mae, or anywhere you aren’t sure about.</li>
<li>If we ever connect Ask Mae to a live AI service, we will update this notice first. We will name the company that processes the messages and explain what it keeps, for how long, and whether it uses messages to improve its products.</li>
</ul>
<h2>When signup opens</h2>
<ul>
<li><strong>Newsletter:</strong> we will ask for your email address and, if you choose, your first name. The separate safety alerts box stays unchecked unless you check it. We will keep a record of when you agreed, so we can show you asked to hear from us.</li>
<li><strong>Interest list:</strong> your email address and, if you choose, your name, organization, the items you checked and a short message. Joining the interest list does not sign you up for the newsletter.</li>
<li>We plan to use Brevo to store contacts and send our emails. You will be able to unsubscribe at any time with the link in every email. We don’t sell your information. <mark class="confirm">[CONFIRM]</mark></li>
<li><strong>Donations:</strong> online giving isn’t open yet. When it opens, payments will be handled on a secure page run by our payment provider. This website will never ask for card details. <mark class="confirm">[CONFIRM CHECKOUT PROVIDER AND ITS PRIVACY TERMS]</mark></li>
<li>Please don’t send birth dates, health details or details about money lost to a scam.</li>
</ul>
<h2>What this website does not do</h2>
<ul>
<li>No advertising or tracking cookies, and no analytics scripts.</li>
<li>No requests for your microphone, camera or location.</li>
<li>The practice exercise is fictional and saves nothing.</li>
<li>Fonts, images and Ask Mae’s answers are served from this website, not from outside services.</li>
</ul>
<h2 id="hosting">Our web host</h2>
<p>This website is hosted on GitHub Pages, a service of GitHub. GitHub says: “When a GitHub Pages site is visited, the visitor’s IP address is logged and stored for security purposes, regardless of whether the visitor has signed into GitHub or not.” An IP address is the number that identifies your internet connection. AgeWell does not receive these logs.</p>
<p class="small">Sources: <a href="https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection" rel="noopener">GitHub Docs, “What is GitHub Pages?” (Data collection)</a> and the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub General Privacy Statement</a>. Checked October 11, 2026.</p>
<h2>Your choices</h2>
<ul>
<li>Once our emails start, unsubscribe with the link at the bottom of any email.</li>
<li>Ask us to see, correct or delete your information at <a href="mailto:hello@awinnovations.org">hello@awinnovations.org</a>.</li>
</ul>
<h2>Questions</h2>
<p>Write to us at <a href="mailto:hello@awinnovations.org">hello@awinnovations.org</a>. Email is not emergency support. If someone is in danger, call 911.</p>
"""

ACCESS = """
<p>We want this site to be easy for everyone to use, including people who use screen readers, keyboards, magnifiers or larger text.</p>
<h2>What we’ve done</h2>
<ul>
<li>Large, readable text in Atkinson Hyperlegible Next, a typeface designed for low-vision readers.</li>
<li>Color combinations checked for contrast. Copper is used for decoration, not for important text.</li>
<li>Every control works with a keyboard, with a visible focus outline.</li>
<li>Animations are short and gentle. They switch off if your device asks for reduced motion, and Mae’s greeting has a pause button.</li>
<li>Ask Mae (demo) opens in a window with large text and buttons. Close it with the Close button or the Escape key, and you return to where you were. New answers are announced to screen readers.</li>
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
<p>If anything on this site is hard to use, tell us at <a href="mailto:hello@awinnovations.org">hello@awinnovations.org</a> and we’ll help you get the information another way.</p>
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


NOTES_JSON = SITE / "assets" / "data" / "notes.json"
MAE_SCRIPTS = ("assets/js/config.js", "assets/js/site.js", "assets/js/ask-mae.js")

def esc(x): return html.escape(x, quote=True)

def note_card(n, prefix=""):
    """Short homepage card. Every required field: date, status, who, step, limits, source, reviewed."""
    return f"""      <article class="note-card reveal" aria-labelledby="card-{n['id']}">
        <p class="note-date">{esc(n['dateLabel'])}</p>
        <h3 id="card-{n['id']}">{esc(n['title'])}</h3>
        <dl class="note-facts">
          <div><dt>Status</dt><dd>{esc(n['status'])}</dd></div>
          <div><dt>Who it affects</dt><dd>{esc(n['affects'])}</dd></div>
          <div><dt>Practical step</dt><dd>{esc(n['step'])}</dd></div>
          <div><dt>Limitations</dt><dd>{esc(n['limitations'])}</dd></div>
        </dl>
        <p class="note-source"><strong>Official source:</strong> <a href="{esc(n['source']['url'])}" rel="noopener">{esc(n['source']['publisher'])}, {esc(n['source']['dateLabel'])}</a></p>
        <p class="note-reviewed">Reviewed: {esc(n['reviewedLabel'])}</p>
        <a class="note-more" href="notes.html#{n['id']}">Read the full note<span class="sr-only">: {esc(n['title'])}</span></a>
      </article>"""

def note_full(n):
    g = f"<p>{esc(n['guidance'])}</p>" if n.get("guidance") else ""
    return f"""<article class="note-full" id="{n['id']}" aria-labelledby="h-{n['id']}">
  <p class="note-date">{esc(n['dateLabel'])}</p>
  <h2 id="h-{n['id']}">{esc(n['title'])}</h2>
  <div class="note-company">
    <p class="note-label">Company announcement ({esc(n['company']['name'])}, {esc(n['source']['dateLabel'])})</p>
    <p>{esc(n['company']['summary'])}</p>
  </div>
  <div class="note-guide">
    <p class="note-label">AgeWell guidance</p>
    <dl class="note-facts">
      <div><dt>Availability or rollout status</dt><dd>{esc(n['status'])}</dd></div>
      <div><dt>Who it affects</dt><dd>{esc(n['affects'])}</dd></div>
      <div><dt>Practical step</dt><dd>{esc(n['step'])}</dd></div>
      <div><dt>Limitations</dt><dd>{esc(n['limitations'])}</dd></div>
    </dl>
    {g}
    <p class="note-teach"><strong>{esc(n['teachingLabel'])}:</strong> “{esc(n['teaching'])}”</p>
  </div>
  <p class="note-source"><strong>Official source:</strong> <a href="{esc(n['source']['url'])}" rel="noopener">{esc(n['source']['title'])}</a> ({esc(n['source']['publisher'])}, {esc(n['source']['dateLabel'])})</p>
  <p class="note-reviewed">Reviewed by AgeWell: {esc(n['reviewedLabel'])}</p>
</article>"""

def mae_dialog():
    return """<dialog class="mae-dialog" id="ask-mae" aria-labelledby="ask-mae-title" aria-describedby="ask-mae-demo">
  <div class="mae-shell">
    <div class="mae-head">
      <svg class="mae-head-face" aria-hidden="true" focusable="false"><use href="#mae-face"/></svg>
      <div class="mae-head-text">
        <h2 id="ask-mae-title" tabindex="-1">Ask Mae</h2>
        <p class="mae-demo" id="ask-mae-demo"><strong>Demo:</strong> Mae’s answers here are prewritten, not live AI.</p>
      </div>
      <button type="button" class="mae-close" data-mae-close><span aria-hidden="true">✕</span> Close</button>
    </div>
    <div class="mae-scroll">
      <div class="mae-log" data-mae-log role="log" aria-live="polite" aria-label="Conversation with Mae"></div>
      <div class="mae-starters" data-mae-starters role="group" aria-label="Pick a topic">
        <button type="button" class="mae-chip" data-topic="scam">Something feels like a scam</button>
        <button type="button" class="mae-chip" data-topic="device">Help with my phone or computer</button>
        <button type="button" class="mae-chip" data-topic="ai">Explain AI to me</button>
        <button type="button" class="mae-chip" data-topic="agewell">Ask about AgeWell</button>
      </div>
    </div>
    <form class="mae-form" data-mae-form autocomplete="off">
      <label for="mae-input">Or type a short question</label>
      <div class="mae-input-row">
        <input id="mae-input" data-mae-input type="text" autocomplete="off" maxlength="300" aria-describedby="mae-input-hint">
        <button type="submit" class="btn btn-primary">Ask</button>
      </div>
      <p class="mae-hint" id="mae-input-hint">Please don’t share passwords, verification codes or private account details. Nothing you type is saved or sent anywhere.</p>
    </form>
    <div class="mae-foot">
      <p><a href="mailto:hello@awinnovations.org?subject=Question%20for%20AgeWell">Ask a person: hello@awinnovations.org</a><br>Email is not emergency support. If someone is in danger, call 911.</p>
      <button type="button" class="mae-reset" data-mae-reset>Start over</button>
    </div>
  </div>
</dialog>"""

def inject(text, name, block):
    a, b = f"<!-- GEN:{name}:START -->", f"<!-- GEN:{name}:END -->"
    i0 = text.index(a) + len(a); i1 = text.index(b)
    return text[:i0] + "\n" + block + "\n" + text[i1:]

def build_notes():
    notes = json.loads(NOTES_JSON.read_text(encoding="utf-8"))["notes"]
    inner = """<p class="lede-sm">Short, dated notes about AI and safety news. Each note keeps what a company announced separate from AgeWell’s practical guidance, and links to the official source.</p>
<div class="callout"><p><strong>How we publish these notes:</strong> a person at AgeWell writes each note by hand and checks it against the official source before it goes up. Nothing here is posted automatically. Each note shows the date we last reviewed it.</p></div>
""" + "\n".join(note_full(n) for n in notes) + """
<h2 id="update">Get notes like these by email</h2>
<p>Reviewed notes will also appear in <a href="index.html#newsletter">The AgeWell Update</a>, our monthly email newsletter (upcoming). <a href="index.html#signup">Get the AgeWell Update</a>.</p>
<h2 id="ask">Questions about a note?</h2>
<p><button type="button" class="btn btn-secondary" data-ask-mae hidden>Ask Mae about these notes (demo)</button></p>
<p>Or ask a person at <a href="mailto:hello@awinnovations.org">hello@awinnovations.org</a>. Email is not emergency support.</p>
"""
    page = head("AI &amp; Safety Notes | AgeWell Innovations", "Short, reviewed, dated notes about AI and safety news, with practical steps for older adults and caregivers.", "notes.html", MAE_SCRIPTS)
    page += f"""<main id="main" tabindex="-1">
<div class="page-hero"><div class="wrap narrow"><p class="crumb"><a href="index.html#safety-notes">← Back to AgeWell Innovations home</a></p><p class="kicker">Reviewed by a person</p><h1>AI &amp; Safety Notes</h1></div></div>
<div class="prose wrap narrow notes-archive">
{inner}
</div>
</main>
{mae_dialog()}
"""
    page += FOOT
    (SITE / "notes.html").write_text(page, encoding="utf-8")
    idx = SITE / "index.html"
    t = idx.read_text(encoding="utf-8")
    t = inject(t, "NAV", nav(""))
    t = inject(t, "NOTES", "\n".join(note_card(n) for n in notes[:3]))
    t = inject(t, "MAE", mae_dialog())
    t = inject(t, "FOOTER", footer("").strip())
    idx.write_text(t, encoding="utf-8")

if __name__ == "__main__":
    build_guide()
    simple("privacy.html", "Privacy notice", "How AgeWell Innovations handles the little information we collect.", PRIVACY)
    simple("accessibility.html", "Accessibility", "How AgeWell Innovations makes this site easy to use, and how to tell us what isn’t.", ACCESS)
    simple("404.html", "Page not found", "This page could not be found.", NOTFOUND)
    build_notes()
    print("built guide.html, privacy.html, accessibility.html, 404.html, notes.html and index.html blocks from", GUIDE_MD, "and", NOTES_JSON)
