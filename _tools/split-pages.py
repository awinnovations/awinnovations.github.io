#!/usr/bin/env python3
"""One-time split of the long homepage into linked pages (Oct 13, 2026)."""
import re, pathlib
S = pathlib.Path(__file__).resolve().parent.parent
idx = (S/"index.html").read_text()
sec = {m.group(1): m.group(0) for m in re.finditer(r'<!-- [^\n]*-->\n<section class="[^"]*" id="([^"]+)".*?\n</section>', idx, re.S)}
PAGES = [  # slug, title, nav label, sections, card blurb
 ("about", "About AgeWell Innovations", "About", ["about", "support"], "Who we are, our founder and how to get involved."),
 ("programs", "Our programs", "Workshops", ["programs"], "Our planned workshop programs."),
 ("learn", "Learn: voice scams and the callback", "Learn", ["learn", "practice"], "A familiar voice is not proof of identity. Practice the callback."),
 ("mable-and-mae", "Mable & Mae and Ask Mae", "Mable &amp; Mae", ["mable-and-mae", "ask-mae-section"], "Our comic and the Ask Mae demo."),
 ("newsletter", "The AgeWell Update", "Newsletter", ["newsletter"], "Our email newsletter."),
 ("events", "Events", "Events", ["events"], "Upcoming events."),
 ("faq", "Frequently asked questions", "FAQ", ["faq"], "Answers to common questions."),
 ("contact", "Contact us", "Contact", ["contact"], "Ask a person: hello@awinnovations.org"),
]
EXTRA = [("/notes.html", "AI &amp; Safety Notes", "Short, dated notes about AI and safety news."),
         ("/guide.html", "Free guide", "Our voice-cloning scam guide.")]
idmap = {}
for slug, _, _, secs, _ in PAGES:
    for s in secs:
        for i in re.findall(r'\sid="([^"]+)"', sec[s]): idmap[i] = f"/{slug}/#{i}"
        idmap[s] = f"/{slug}/"
idmap["signup"] = "/join/"; idmap["safety-notes"] = "/notes.html"
for i in re.findall(r'\sid="([^"]+)"', sec["safety-notes"]): idmap.setdefault(i, "/notes.html")

def fix_links(t, here=None):
    t = re.sub(r'(href|src|srcset)="(?!https?:|mailto:|tel:|#|/|data:)([^"]+)"', r'\1="/\2"', t)
    def anc(m):
        attr, page, a = m.group(1), m.group(2), m.group(3)
        tgt = idmap.get(a)
        if not tgt: return m.group(0) if page else f'{attr}="/#{a}"' if here == "home-gone" else m.group(0)
        if here and tgt.startswith(f"/{here}/"): return f'{attr}="#{a}"'
        return f'{attr}="{tgt}"'
    return re.sub(r'(href)="(/index\.html|/)?#([^"]+)"', anc, t)

def nav():
    lis = "\n".join(f'        <li><a href="/{s}/">{l}</a></li>' for s, _, l, _, _ in PAGES[:4]) + \
          '\n        <li><a href="/notes.html">AI &amp; Safety Notes</a></li>\n        <li><a href="/guide.html">Free guide</a></li>\n' + \
          "\n".join(f'        <li><a href="/{s}/">{l}</a></li>' for s, _, l, _, _ in PAGES[5:])
    return f'''    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>
        <li><a href="/">Home</a></li>
{lis}
        <li class="nav-cta"><a class="btn btn-primary btn-small" href="/join/">Join the newsletter</a></li>
      </ul>
    </nav>'''
def foot_nav():
    items = [("/", "Home")] + [(f"/{s}/", l) for s, _, l, _, _ in PAGES] + [("/notes.html", "AI &amp; Safety Notes"), ("/guide.html", "Free guide"), ("/join/", "Join the newsletter"), ("/privacy.html", "Privacy notice"), ("/accessibility.html", "Accessibility")]
    return '<nav aria-label="Footer">\n      <ul class="footer-links">\n' + "\n".join(f'        <li><a href="{h}">{l}</a></li>' for h, l in items) + '\n      </ul>\n    </nav>'

def shell(t):
    t = re.sub(r'    <nav class="site-nav" id="site-nav" aria-label="Main">.*?</nav>', lambda m: nav(), t, flags=re.S)
    t = re.sub(r'<nav aria-label="Footer">.*?</nav>', lambda m: foot_nav(), t, flags=re.S)
    return t

top = idx[:idx.index('<main id="main"')]
bottom = idx[idx.index('</main>'):]
mae_dialog = re.search(r'<!-- GEN:MAE:START -->.*?<!-- GEN:MAE:END -->', idx, re.S).group(0)
for slug, title, label, secs, _ in PAGES:
    t = top.replace("<title>", "<title>" + title.replace("&", "&amp;") + " | AgeWell Innovations</title><!--", 1).replace("</title>\n", "-->\n", 1) if False else re.sub(r"<title>.*?</title>", f"<title>{title.replace('&','&amp;')} | AgeWell Innovations</title>", top)
    t = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://awinnovations.org/{slug}/">', t)
    body = "\n\n".join(sec[s] for s in secs)
    main = f'<main id="main" tabindex="-1">\n<div class="page-hero page-hero-slim"><div class="wrap"><p class="crumb"><a class="back-home" href="/">← Back to home</a></p></div></div>\n\n{body}\n\n<div class="wrap back-bottom"><p><a class="btn btn-secondary" href="/">← Back to home</a></p></div>\n'
    out = shell(t + main + bottom)
    if "ask-mae-section" not in secs:
        out = out.replace(mae_dialog, "")
    p = S/slug; p.mkdir(exist_ok=True)
    (p/"index.html").write_text(fix_links(out, slug))

cards = "\n".join(f'    <li><a class="hub-card" href="/{s}/"><span class="hub-title">{l}</span><span class="hub-desc">{d}</span></a></li>' for s, _, l, _, d in PAGES if s != "newsletter")
cards += "\n" + "\n".join(f'    <li><a class="hub-card" href="{h}"><span class="hub-title">{l}</span><span class="hub-desc">{d}</span></a></li>' for h, l, d in EXTRA)
cards += '\n    <li><a class="hub-card hub-card-cta" href="/join/"><span class="hub-title">Join the newsletter</span><span class="hub-desc">Friendly tips by email. Unsubscribe anytime.</span></a></li>'
home_main = f'''<main id="main" tabindex="-1">

<section class="hero hero-short" aria-labelledby="hero-title">
  <div class="wrap hero-short-grid">
    <picture class="hero-mae">
      <source srcset="/assets/img/mae-head.webp" type="image/webp">
      <img src="/assets/img/mae-head.jpg" width="480" height="480" alt="Mae, AgeWell's friendly robot helper">
    </picture>
    <div>
      <h1 id="hero-title">Technology with care.</h1>
      <p class="lede">AgeWell Innovations helps older adults and caregivers understand technology, recognize scams and build confidence through practical education.</p>
      <p><a class="btn btn-primary" href="/join/">Join the newsletter</a></p>
    </div>
  </div>
</section>

<section class="section hub" aria-labelledby="hub-title">
  <div class="wrap">
    <h2 id="hub-title">Explore AgeWell</h2>
    <ul class="hub-grid">
{cards}
    </ul>
  </div>
</section>

'''
home = shell(top + home_main + bottom.replace(mae_dialog, ""))
(S/"index.html").write_text(fix_links(home, "home"))
for f in ["guide.html", "privacy.html", "notes.html", "accessibility.html", "404.html", "join/index.html"]:
    q = S/f; q.write_text(fix_links(shell(q.read_text())))
print("ok", sorted(idmap.items())[:5])
