#!/usr/bin/env python3
"""Generates the static pages for stonebloom.studio.

Edit the page content below, then run:  python3 build.py
Output: index.html, clay-art/, about/, contact/, 404.html
"""
from pathlib import Path

ROOT = Path(__file__).parent
SITE_URL = "https://www.stonebloom.studio"
INSTAGRAM = "https://www.instagram.com/stone.bloom.art"
EMAIL = "vweidenbaum@gmail.com"
FORM_ENDPOINT = f"https://formsubmit.co/ajax/{EMAIL}"

NAV = [("clay-art", "Clay art"), ("about", "About"), ("contact", "Contact")]

INSTAGRAM_ICON = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
    '<rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/><circle cx="12" cy="12" r="4"/>'
    '<circle cx="17" cy="7" r=".9" fill="currentColor" stroke="none"/></svg>'
)


def img(name, alt, sizes, focal=None, eager=False):
    style = f' style="object-position:{focal}"' if focal else ""
    loading = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return (
        f'<img src="{{r}}images/{name}-1600.jpg" '
        f'srcset="{{r}}images/{name}-800.jpg 800w, {{r}}images/{name}-1600.jpg 1600w" '
        f'sizes="{sizes}" alt="{alt}"{style}{loading} decoding="async">'
    )


def block(m, d, z, html, cls=""):
    cls = f" {cls}" if cls else ""
    return f'<div class="fe-block{cls}" style="--m:{m};--d:{d};--z:{z}">{html}</div>'


def gallery(items, columns, gutter, ratio, sizes):
    figures = "\n".join(
        f'        <figure class="fade">{img(name, alt, sizes, focal)}</figure>' for name, alt, focal in items
    )
    return (
        f'<div class="gallery" style="--columns:{columns};--gallery-gutter:{gutter};--ratio:{ratio}">\n'
        f"{figures}\n      </div>"
    )


def header(current, theme):
    links = "".join(
        f'<a href="{{r}}{slug}/"{" aria-current=page" if slug == current else ""}>{label}</a>'
        for slug, label in NAV
    )
    dark = " menu--dark" if theme == "dark" else ""
    return f"""  <a class="skip-link" href="#page">Skip to Content</a>
  <header class="header header--{theme}">
    <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
    <div class="header-social fade"><a class="icon-link" href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{INSTAGRAM_ICON}</a></div>
    <div class="header-center">
      <a class="site-title fade" href="{{r}}">Stone Bloom</a>
      <nav class="header-nav fade" aria-label="Main">{links}</nav>
    </div>
  </header>
  <div class="menu{dark}" id="menu">
    <nav aria-label="Mobile">{links}</nav>
    <a class="icon-link" href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{INSTAGRAM_ICON}</a>
  </div>"""


def footer():
    links = "<br>".join(f'<a href="{{r}}{slug}/">{label}</a>' for slug, label in NAV)
    blocks = "\n        ".join([
        block("1/3/2/6", "1/4/3/8", 1, '<div class="text fade"><h4>Stone bloom</h4></div>'),
        block("1/2/3/3", "1/2/3/3", 0, '<div class="text fade"><h3>*</h3></div>'),
        block("3/2/6/6", "1/20/3/22", 2, f'<div class="text fade"><p>{links}</p></div>'),
        block("6/2/10/10", "1/22/2/26", 4,
              f'<div class="text fade"><p><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></p></div>'),
    ])
    return f"""  <footer class="footer section section--bright section--small section--top">
      <div class="fe" style="--rows-m:10;--rows-d:2">
        {blocks}
      </div>
  </footer>"""


def page(path, title, description, theme, current, sections):
    # 404.html is served from any URL, so it needs root-absolute paths
    r = "/" if path == "404.html" else ("../" if path else "")
    canonical = f"{SITE_URL}/{path}" if path and path != "404.html" else SITE_URL
    body = "\n".join(sections)
    html = f"""<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:site_name" content="Stone Bloom">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE_URL}/images/dsc00825-1-1600.jpg">
  <link rel="icon" type="image/png" href="{{r}}images/favicon.png">
  <link rel="apple-touch-icon" href="{{r}}images/apple-touch-icon.png">
  <link rel="stylesheet" href="{{r}}css/fonts.css">
  <link rel="stylesheet" href="{{r}}css/style.css">
  <script>document.documentElement.classList.add('js')</script>
</head>
<body>
{header(current, theme)}
  <main id="page">
{body}
  </main>
{footer()}
  <script src="{{r}}js/main.js" defer></script>
</body>
</html>
"""
    html = html.replace("{r}", r)
    out = ROOT / path if path.endswith(".html") else ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("wrote", out.relative_to(ROOT))


DESCRIPTION = (
    "Stone Bloom is home to unique clay art and jewelry by designer and artist Victoria Weidenbaum."
)

# ---------------------------------------------------------------- Home

home = [
    f"""    <section class="section section--first section--white section--small">
      <div class="fe" style="--rows-m:16;--rows-d:16">
        {block("1/2/3/10", "5/2/9/9", 3, '<div class="text fade"><h1>Art to ground you</h1></div>')}
        {block("3/2/5/10", "10/2/12/9", 4, '<a class="btn fade" href="{r}clay-art/">View available pieces</a>', "fe-block--middle")}
        {block("6/4/17/10", "1/16/17/26", 0, '<div class="fe-image fe-image--rounded fade">' + img("dsc00825-1", "Terracotta marbled clay wall hanging with gold hexagon accents, hung from a wooden branch", "(min-width: 768px) 42vw, 66vw", eager=True) + "</div>")}
        {block("9/2/14/7", "4/12/14/19", 2, '<div class="fe-image fe-image--rounded fade">' + img("260603-vika-2385676", "Woman wearing a black and white marbled clay necklace with a heart pendant", "(min-width: 768px) 29vw, 54vw", "75.2% 42.4%", eager=True) + "</div>")}
      </div>
    </section>""",
    f"""    <section class="section section--light section--small section--top">
      <div class="fe" style="--rows-m:5;--rows-d:4">
        {block("1/2/4/10", "1/8/3/20", 0, '<div class="text center fade"><p>Stone Bloom is home to unique clay art and jewelry, founded by designer and artist Victoria Weidenbaum. The name captures the essence of her technique: by mixing clays of different colors, she creates marbled tiles that make the stone appear to bloom.</p></div>')}
        {block("4/4/6/8", "3/12/5/16", 1, '<a class="btn btn--small fade" href="{r}clay-art/">View available art</a>', "fe-block--middle")}
      </div>
    </section>""",
    f"""    <section class="section section--bright section--flush">
      {gallery([
          ("dsc00707", "Close-up of black and white marbled clay discs tied with leather cord", None),
          ("260603-vika-1673431", "Hands assembling a wall hanging of clay squiggles, discs and textured diamonds", None),
      ], 2, 50, "3/4", "(min-width: 768px) 44vw, 43vw")}
    </section>""",
    f"""    <section class="section section--bright section--10vh">
      <div class="fe" style="--rows-m:11;--rows-d:5">
        {block("2/2/5/10", "2/2/5/11", 0, '<div class="text fade"><h4>Newsletter</h4><p>We send updates about new available pieces once a month.</p></div>')}
        {block("5/2/12/10", "2/14/5/26", 1, f'''<form class="newsletter fade" action="https://formsubmit.co/{EMAIL}" method="POST" data-ajax="{FORM_ENDPOINT}" data-success="Thank you!">
            <input type="hidden" name="_subject" value="Stone Bloom newsletter signup">
            <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
            <input type="email" name="email" placeholder="Email Address" aria-label="Email Address" autocomplete="email" required>
            <button class="btn" type="submit">Sign Up</button>
          </form>''')}
        {block("11/2/12/10", "5/2/6/26", 2, "<hr>", "fe-block--middle")}
      </div>
    </section>""",
    f"""    <section class="section section--bright section--flush">
      {gallery([
          ("img-3740", "Hand holding black, white and grey marbled clay squiggles", None),
          ("img-6146-2", "Terracotta clay wall hanging above a reading nook with rust-colored pillows", None),
          ("img-3624", "Close-up of overlapping terracotta and white marbled clay petals", None),
          ("dsc00733", "Black, grey and white clay wall hanging on a driftwood branch above a bench", "51% 2%"),
          ("dsc00730", "Narrow blue and green clay tile wall hanging in a dining room", "37% 0%"),
          ("dsc00712", "Black and white clay squiggles laid out on a wooden table", "48% 94%"),
      ], 3, 53, "1", "(min-width: 768px) 29vw, 43vw")}
    </section>""",
]

# ---------------------------------------------------------------- Clay art

clay_items = [
    ("img-3503", "Wall hanging of three terracotta marbled clay ovals with gold hexagons and beaded strands"),
    ("dsc00716", "Wide wall hanging of marbled clay discs fading from white to black"),
    ("img-3623", "Shield-shaped wall hanging of overlapping terracotta marbled clay petals"),
    ("img-3738", "Wall hanging of black, white and grey clay squiggles on a curved branch"),
    ("dsc00759", "Oval terracotta marbled clay wall hanging with gold hexagon accents"),
    ("dsc00739", "Mobile-style wall hanging of grey, white and black clay squiggles with gold accents"),
    ("dsc00718", "Wall hanging of terracotta and white marbled clay triangles in a zigzag pattern"),
    ("img-6138-2", "Wide wall hanging of terracotta marbled clay discs on a wavy branch"),
    ("dsc00717", "Narrow wall hanging of clay tiles fading from deep blue to terracotta"),
    ("img-1029", "Wall hanging of layered terracotta marbled clay rectangles"),
    ("img-3022", "Triangular wall hanging of terracotta marbled clay triangles"),
]

clay = [
    f"""    <section class="section section--first section--white section--flush">
      {gallery([(n, a, None) for n, a in clay_items], 3, 20, "1", "(min-width: 768px) 30vw, 44vw")}
    </section>""",
    f"""    <section class="section section--white section--small">
      <div class="fe" style="--rows-m:5;--rows-d:2">
        {block("1/2/3/10", "1/2/3/14", 2, '<div class="text fade"><h3>Contact us about available pieces</h3></div>')}
        {block("4/2/6/10", "1/20/3/26", 5, f'<a class="btn fade" href="mailto:{EMAIL}?subject=Available%20art">Contact</a>', "fe-block--middle")}
      </div>
    </section>""",
]

# ---------------------------------------------------------------- About

about = [
    f"""    <section class="section section--first section--dark section--small section--bottom">
      <div class="fe" style="--rows-m:21;--rows-d:11">
        {block("1/1/10/11", "1/7/10/13", 2, '<div class="fe-image fe-image--circle fade">' + img("img-0337-2", "Victoria Weidenbaum, founder of Stone Bloom", "(min-width: 768px) 22vw, 80vw", eager=True) + "</div>")}
        {block("10/2/11/10", "1/14/3/26", 0, '<div class="text fade"><h4>Inspired by nature</h4></div>', "fe-block--middle-m")}
        {block("11/2/22/10", "3/14/11/24", 1, '''<div class="text fade">
            <p>I'm Victoria, a Russian-Ukrainian designer and artist who moved to San Francisco eleven years ago. For over a decade, I built a career in tech, but when I discovered clay, something clicked into place.</p>
            <p>I've always been drawn to the quiet beauty around me: the intricate designs and patterns in architecture, the timeless elegance of marble, the way light catches on leaves, the patterns in tree bark, the colors that shift across the ocean. My marbling technique is my way of translating those fleeting moments into something tangible, something that lasts.</p>
            <p>After years of creating for screens, I'm now creating with my hands. Stone Bloom is my leap into the life I've been working toward, one where I can show others what I see: that beauty exists in unexpected places, and that even stones can bloom.</p>
          </div>''')}
      </div>
    </section>""",
]

# ---------------------------------------------------------------- Contact

contact = [
    f"""    <section class="section section--first section--light section--medium">
      <div class="fe" style="--rows-m:29;--rows-d:13">
        {block("1/2/2/10", "1/2/3/7", 1, '<div class="text fade"><h4>Get in Touch</h4></div>')}
        {block("2/2/4/10", "2/2/4/8", 4, f'<div class="text fade"><p>For all inquiries, please contact {EMAIL} or use the form.</p></div>')}
        {block("4/2/28/10", "1/12/12/26", 3, f'''<form class="form fade" action="https://formsubmit.co/{EMAIL}" method="POST" data-ajax="{FORM_ENDPOINT}" data-success="Thank you!">
            <input type="hidden" name="_subject" value="New message from stonebloom.studio">
            <input type="hidden" name="_template" value="table">
            <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
            <fieldset>
              <legend>Name</legend>
              <div class="row">
                <div class="field"><label class="caption" for="first-name">First Name<span class="req">(required)</span></label><input id="first-name" type="text" name="First Name" autocomplete="given-name" required></div>
                <div class="field"><label class="caption" for="last-name">Last Name</label><input id="last-name" type="text" name="Last Name" autocomplete="family-name"></div>
              </div>
            </fieldset>
            <div class="field"><label class="title" for="email">Email<span class="req">(required)</span></label><input id="email" type="email" name="email" autocomplete="email" required></div>
            <div class="field"><label class="title" for="message">Message<span class="req">(required)</span></label><textarea id="message" name="Message" required></textarea></div>
            <button class="btn btn--large" type="submit">Submit</button>
          </form>''')}
      </div>
    </section>""",
]

not_found = [
    """    <section class="section section--first section--white section--medium">
      <div class="fe" style="--rows-m:6;--rows-d:6">
        <div class="fe-block" style="--m:1/2/7/10;--d:1/2/7/26;--z:0"><div class="text center"><h3>Page not found</h3><p><a href="/">Back to Stone Bloom</a></p></div></div>
      </div>
    </section>""",
]

page("", "Stone Bloom", DESCRIPTION, "white", None, home)
page("clay-art", "Clay art — Stone Bloom", "Available clay wall art by Stone Bloom.", "white", "clay-art", clay)
page("about", "About — Stone Bloom", "About Victoria Weidenbaum, the designer and artist behind Stone Bloom.", "dark", "about", about)
page("contact", "Contact — Stone Bloom", "Get in touch with Stone Bloom.", "light", "contact", contact)
page("404.html", "Page not found — Stone Bloom", DESCRIPTION, "white", None, not_found)
