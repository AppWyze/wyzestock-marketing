#!/usr/bin/env python3
"""Builds the Wyzestock marketing site (static HTML) from one shared layout.

Same look and feel as www.wyzesales.com (AppWyze/wyzesales-marketing): navy and amber, Inter and Space Grotesk,
the same sections, landing-page blocks, lightbox and contact form. Each page is written out as a self-contained
index.html (CSS inline), like the WyzeSales site, so the site needs no build step on Netlify.

Run:  python3 _build/build.py     (from the repo root; rewrites index.html and every */index.html)
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / '_build'
SITE = 'https://wyzestock.co.za'  # primary domain on Netlify since 2026-10-21; www redirects here
APP = 'https://app.wyzestock.co.za'
EMAIL = 'support@wyzestock.co.za'
WA_NUMBER = '27621847381'
WA_LABEL = '+27 62 184 7381'
CONTACT_FN = 'https://zaupomwvqpzmsrkoftlr.supabase.co/functions/v1/send-contact-email'

CSS = (B / 'site.css').read_text()
LIGHTBOX = (B / 'lightbox.js').read_text()
WA_SVG = (B / 'wa.svg').read_text()

PAGES = [
    ('/stock-optimisation/', 'Stock optimisation'),
    ('/replenishment/', 'Replenishment'),
    ('/distribution/', 'Distribution'),
    ('/demand-management/', 'Demand management'),
    ('/ai-insights/', 'AI Insights'),
]


def esc(t):
    return html.escape(t, quote=True)


def wa_link(text='Hi, I\'d like to find out more about Wyzestock.'):
    from urllib.parse import quote
    return (f'<a class="wa-logo-link" href="https://wa.me/{WA_NUMBER}?text={quote(text)}" target="_blank" rel="noopener" '
            f'aria-label="Chat with us on WhatsApp, {WA_LABEL} (opens in a new tab)">\n            {WA_SVG}\n'
            f'            <span class="wa-text"><strong>Chat with us on WhatsApp</strong><span>{WA_LABEL}</span></span>\n          </a>')


def head(title, desc, path, schema=None):
    url = SITE + path
    ld = f'<script type="application/ld+json">\n{json.dumps(schema, indent=2, ensure_ascii=False)}\n</script>\n' if schema else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">

<!-- Favicon -->
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/images/icon-192.png">

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wyzestock">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/images/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/images/og.png">

<meta name="theme-color" content="#0A1620">

{ld}<style>{CSS}
  /* ---------- Wyzestock additions ---------- */
  .flow-svg {{ width: 100%; height: auto; display: block; }}
  .stat-row {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: var(--line); border: 1px solid var(--line);
               border-radius: var(--radius); overflow: hidden; margin-top: 8px; }}
  .stat {{ background: var(--navy-mid); padding: 22px 20px; }}
  .stat b {{ display: block; font-family: 'Space Grotesk', sans-serif; font-size: 26px; color: var(--amber); line-height: 1.1; margin-bottom: 6px; }}
  .stat span {{ font-size: 13.5px; color: var(--text-2); }}
  @media (max-width: 760px) {{ .stat-row {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
'''


def nav(home=False):
    p = '' if home else '/'
    links = [('/stock-optimisation/', 'Stock optimisation'), ('/replenishment/', 'Replenishment'),
             ('/distribution/', 'Distribution'), ('/demand-management/', 'Demand management'), ('/ai-insights/', 'AI Insights'),
             ('/partners/', 'Partners')]
    brand_href = '#top' if home else '/'
    items = '\n'.join(f'      <a href="{h}">{t}</a>' for h, t in links)
    return f'''
<nav>
  <div class="nav-inner">
    <a href="{brand_href}" class="nav-brand">
      <img src="/images/icon-192.png" alt="Wyzestock logo">
      <span>Wyze<span class="accent">stock</span></span>
    </a>
    <div class="nav-links">
{items}
    </div>
    <div class="nav-cta">
      <a href="{APP}" class="btn btn-ghost">Sign in</a>
      <a href="{p}#contact" class="btn btn-primary">Get in touch</a>
    </div>
  </div>
</nav>
'''


def footer():
    links = ''.join(f'\n      <a href="{h}">{t}</a>' for h, t in PAGES)
    return f'''
<footer>
  <div class="wrap footer-inner">
    <div>&copy; 2026 Wyzestock, a product of CL Wyeth t/a Wyzelink.</div>
    <div class="footer-links">{links}
      <a href="/partners/">For ERP partners</a>
      <a href="{APP}">Sign in</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </div>
</footer>
'''


CONTACT_JS = f'''
<script>
  const form = document.getElementById('contact-form');
  if (form) {{
  const statusEl = document.getElementById('form-status');
  const submitBtn = document.getElementById('contact-submit-btn');

  form.addEventListener('submit', async function (e) {{
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();
    const website = document.getElementById('website').value; // honeypot

    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending…';
    statusEl.textContent = '';
    statusEl.className = 'form-status';

    try {{
      const res = await fetch('{CONTACT_FN}', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ name, email, message, website }})
      }});

      const data = await res.json();

      if (!res.ok || data.error) {{
        throw new Error(data.error || 'Something went wrong');
      }}

      statusEl.textContent = "Thanks, we've got your message and will be in touch soon.";
      statusEl.className = 'form-status success';
      form.reset();
    }} catch (err) {{
      statusEl.textContent = "Couldn't send that. Please try again, or email {EMAIL} directly.";
      statusEl.className = 'form-status error';
    }} finally {{
      submitBtn.disabled = false;
      submitBtn.textContent = 'Send message';
    }}
  }});
  }}
</script>
'''


def tail():
    return f'''{CONTACT_JS}
<script>{LIGHTBOX}</script>
</body>
</html>
'''


def frame(img, alt, w=None, h=None, cls='showcase-frame', eager=False):
    size = f' width="{w}" height="{h}"' if w and h else ''
    load = 'eager' if eager else 'lazy'
    return f'<div class="{cls}"><img src="/images/{img}"{size} alt="{esc(alt)}" loading="{load}"></div>'


def showcase(sid, label, title, intro, bullets, images, reverse=False, link=None):
    lis = '\n'.join(f'            <li>{b}</li>' for b in bullets)
    more = f'\n          <a class="learn-more" href="{link[0]}">{link[1]} &rarr;</a>' if link else ''
    imgs = '\n          '.join(frame(*i) for i in images)
    stack = ' showcase-image-stack' if len(images) > 1 else ''
    return f'''
  <section class="showcase-section" id="{sid}">
    <div class="wrap">
      <div class="showcase-row{' reverse' if reverse else ''} top-align">
        <div class="showcase-text">
          <div class="section-label">{label}</div>
          <h2>{title}</h2>
          <p>{intro}</p>
          <ul class="showcase-list">
{lis}
          </ul>{more}
        </div>
        <div class="showcase-image{stack}">
          {imgs}
        </div>
      </div>
    </div>
  </section>
'''


def contact_section(heading='Let\'s see if Wyzestock fits your business'):
    return f'''
  <section class="contact" id="contact">
    <div class="wrap">
      <div class="contact-inner">
        <div class="section-label">Get in touch</div>
        <h2 style="font-size: 26px; font-weight: 700; margin-bottom: 10px;">{heading}</h2>
        <p style="color: var(--text-2); font-size: 15px;">Tell us what you stock, where you hold it and which ERP you run, and we'll get back to you, usually within a business day.</p>

        <div class="wa-block">
          {wa_link()}
        </div>

        <div class="form-or" aria-hidden="true">or send a message</div>

        <form class="contact-form" id="contact-form" style="margin-top:22px;">
          <div class="form-row">
            <label for="name">Name</label>
            <input type="text" id="name" name="name" required autocomplete="name">
          </div>
          <div class="form-row">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" required autocomplete="email">
          </div>
          <div class="form-row">
            <label for="message">Message</label>
            <textarea id="message" name="message" required placeholder="Tell us about your business: what you stock, how many locations, and which ERP you use."></textarea>
          </div>
          <div class="form-row contact-honeypot">
            <label for="website">Website</label>
            <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
          </div>
          <div class="contact-submit">
            <button type="submit" class="btn btn-primary" id="contact-submit-btn">Send message</button>
          </div>
          <div class="form-status" id="form-status"></div>
        </form>

        <div class="contact-alt">
          Prefer email? Reach us directly at <a href="mailto:{EMAIL}">{EMAIL}</a><br>For ERP or accounting partners, <a href="/partners/">see how we work with you</a>. <a href="/Wyzestock-One-Pager.pdf">Download the one-page overview (PDF)</a>.
        </div>
      </div>
    </div>
  </section>
'''


def features(cards, label, title, sub, sid='features', cls='features'):
    cs = '\n'.join(f'''        <div class="feature-card">
          <div class="feature-icon">{i}</div>
          <h3>{t}</h3>
          <p>{d}</p>
        </div>''' for i, t, d in cards)
    return f'''
  <section class="{cls}" id="{sid}">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">{label}</div>
        <h2>{title}</h2>
        <p>{sub}</p>
      </div>
      <div class="feature-grid">
{cs}
      </div>
    </div>
  </section>
'''


# ───────────────────────────── Home ─────────────────────────────

HUB_SVG = '''
        <svg class="hub-svg" viewBox="0 0 1000 560" role="img" aria-labelledby="hub-title hub-desc" xmlns="http://www.w3.org/2000/svg">
          <title id="hub-title">How Wyzestock works</title>
          <desc id="hub-desc">The right stock at the centre, connected to six parts of Wyzestock: stock position, forecasting, replenishment, distribution, demand management and bills of material.</desc>

          <ellipse class="ring" cx="500" cy="280" rx="330" ry="205"/>
          <circle class="ring" cx="500" cy="280" r="130"/>

          <line class="spoke" x1="500" y1="280" x2="500" y2="75"/>
          <line class="spoke" x1="500" y1="280" x2="786" y2="177"/>
          <line class="spoke" x1="500" y1="280" x2="786" y2="383"/>
          <line class="spoke" x1="500" y1="280" x2="500" y2="485"/>
          <line class="spoke" x1="500" y1="280" x2="214" y2="383"/>
          <line class="spoke" x1="500" y1="280" x2="214" y2="177"/>

          <circle class="hub-halo" cx="500" cy="280" r="104"/>
          <circle class="hub-core" cx="500" cy="280" r="76"/>
          <text class="hub-num" x="500" y="282" text-anchor="middle" style="font-size:30px">Right</text>
          <text class="hub-cap" x="500" y="306" text-anchor="middle">stock, right place</text>

          <rect class="node" x="385" y="33" width="230" height="84" rx="12"/>
          <circle cx="407" cy="63" r="5" fill="#FFB23E"/>
          <text class="node-title" x="421" y="69">Stock position</text>
          <text class="node-sub" x="405" y="90">Model stock, excess and</text>
          <text class="node-sub" x="405" y="107">shortfall, item by location</text>

          <rect class="node" x="671" y="135" width="230" height="84" rx="12"/>
          <circle cx="693" cy="165" r="5" fill="#3B82F6"/>
          <text class="node-title" x="707" y="171">Replenishment</text>
          <text class="node-sub" x="691" y="192">What to order, from whom,</text>
          <text class="node-sub" x="691" y="209">rounded to how you buy</text>

          <rect class="node" x="671" y="341" width="230" height="84" rx="12"/>
          <circle cx="693" cy="371" r="5" fill="#10B981"/>
          <text class="node-title" x="707" y="377">Distribution</text>
          <text class="node-sub" x="691" y="398">What to move between</text>
          <text class="node-sub" x="691" y="415">locations before you buy</text>

          <rect class="node" x="385" y="443" width="230" height="84" rx="12"/>
          <circle cx="407" cy="473" r="5" fill="#8B5CF6"/>
          <text class="node-title" x="421" y="479">Demand management</text>
          <text class="node-sub" x="405" y="500">Sales against forecast and</text>
          <text class="node-sub" x="405" y="517">production, every morning</text>

          <rect class="node" x="99" y="341" width="230" height="84" rx="12"/>
          <circle cx="121" cy="371" r="5" fill="#06B6D4"/>
          <text class="node-title" x="135" y="377">Bills of material</text>
          <text class="node-sub" x="119" y="398">Components planned from</text>
          <text class="node-sub" x="119" y="415">finished-good demand</text>

          <rect class="node" x="99" y="135" width="230" height="84" rx="12"/>
          <circle cx="121" cy="165" r="5" fill="#F472B6"/>
          <text class="node-title" x="135" y="171">Forecasting</text>
          <text class="node-sub" x="119" y="192">Seasonal forecasts for every</text>
          <text class="node-sub" x="119" y="209">item at every location</text>
        </svg>'''

SYNC_SVG = '''
        <svg class="flow-svg" viewBox="0 0 620 300" role="img" aria-labelledby="sync-t" xmlns="http://www.w3.org/2000/svg">
          <title id="sync-t">Your ERP is read twice a day; Wyzestock recalculates and the screens and the morning report are ready</title>
          <rect x="10" y="95" width="170" height="110" rx="14" fill="#0E2230" stroke="rgba(255,255,255,0.12)"/>
          <text x="95" y="140" text-anchor="middle" fill="#EDF1F3" font-family="Space Grotesk, Inter, sans-serif" font-weight="600" font-size="18">Your ERP</text>
          <text x="95" y="165" text-anchor="middle" fill="#8DA1AC" font-family="Inter, sans-serif" font-size="13">stock, sales, orders,</text>
          <text x="95" y="183" text-anchor="middle" fill="#8DA1AC" font-family="Inter, sans-serif" font-size="13">POs, recipes</text>
          <line x1="185" y1="150" x2="255" y2="150" stroke="rgba(255,178,62,0.55)" stroke-width="2" stroke-dasharray="5 6"/>
          <polygon points="255,144 266,150 255,156" fill="#FFB23E"/>
          <text x="225" y="134" text-anchor="middle" fill="#FFB23E" font-family="Inter, sans-serif" font-size="12" font-weight="600">07:00 &amp; 14:00</text>
          <rect x="270" y="80" width="180" height="140" rx="16" fill="#FFB23E"/>
          <text x="360" y="135" text-anchor="middle" fill="#1A1206" font-family="Space Grotesk, Inter, sans-serif" font-weight="700" font-size="22">Wyzestock</text>
          <text x="360" y="160" text-anchor="middle" fill="#1A1206" font-family="Inter, sans-serif" font-size="13" font-weight="600">forecast, model stock,</text>
          <text x="360" y="178" text-anchor="middle" fill="#1A1206" font-family="Inter, sans-serif" font-size="13" font-weight="600">orders and transfers</text>
          <line x1="455" y1="110" x2="500" y2="80" stroke="rgba(255,178,62,0.55)" stroke-width="2" stroke-dasharray="5 6"/>
          <line x1="455" y1="190" x2="500" y2="220" stroke="rgba(255,178,62,0.55)" stroke-width="2" stroke-dasharray="5 6"/>
          <rect x="500" y="40" width="112" height="78" rx="12" fill="#0E2230" stroke="rgba(255,255,255,0.12)"/>
          <text x="556" y="75" text-anchor="middle" fill="#EDF1F3" font-family="Inter, sans-serif" font-weight="600" font-size="14">Screens</text>
          <text x="556" y="95" text-anchor="middle" fill="#8DA1AC" font-family="Inter, sans-serif" font-size="12">always current</text>
          <rect x="500" y="182" width="112" height="78" rx="12" fill="#0E2230" stroke="rgba(255,255,255,0.12)"/>
          <text x="556" y="217" text-anchor="middle" fill="#EDF1F3" font-family="Inter, sans-serif" font-weight="600" font-size="14">Morning</text>
          <text x="556" y="237" text-anchor="middle" fill="#8DA1AC" font-family="Inter, sans-serif" font-size="12">report by email</text>
        </svg>'''


def home():
    schema = {
        '@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': 'Wyzestock',
        'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Web',
        'description': 'Inventory optimisation, replenishment and distribution for manufacturers and distributors. Model stock, '
                       'reorder points and safety stock for every item at every location, seasonal forecasts, purchase and '
                       'transfer suggestions and a daily demand management report, synced from your ERP.',
        'featureList': ['Model stock, reorder point and safety stock per item and location', 'Excess, slow-moving and stock-out exceptions',
                        'Seasonal forecasting with manual overrides', 'Purchase suggestions rounded to minimum order and pack size',
                        'Transfers between locations', 'Demand management report emailed every morning', 'Bills of material and component planning',
                        'AI explanations checked against your figures', 'Automatic ERP sync twice a day', 'PDF and Excel export'],
        'url': SITE, 'publisher': {'@type': 'Organization', 'name': 'CL Wyeth t/a Wyzelink', 'url': SITE},
    }
    out = head('Wyzestock: Inventory Optimisation, Replenishment & Distribution',
               'Hold less stock and run out less often. Model stock, reorder points, purchase and transfer suggestions and seasonal '
               'forecasts for every item at every location, synced from your ERP.', '/', schema)
    out += nav(home=True)
    out += f'''
<main id="top">

  <section class="hero">
    <div class="wrap hero-inner">
      <div class="eyebrow"><span class="dot"></span> Inventory Optimisation &middot; Replenishment &middot; Distribution</div>
      <h1>Hold <span class="accent">less stock</span>.<br>Run out less often.</h1>
      <p class="hero-sub">
        Wyzestock connects to your ERP and works out, for every item at every location, how much stock you should
        hold, what to order, what to move and what is tied up in excess. Seasonal forecasts, bills of material and a
        demand management report every morning are built in. No spreadsheets.
      </p>
      <div class="hero-ctas">
        <a href="#contact" class="btn btn-primary">Get in touch</a>
        <a href="#video" class="btn btn-ghost" data-play-video>&#9654;&nbsp; Watch the 80-second video</a>
      </div>
      <div class="status-strip">
        <span><span class="sdot"></span> Synced from your ERP twice a day</span>
        <span><span class="sdot"></span> Every item, every location</span>
        <span><span class="sdot"></span> Built on 30 years of supply chain practice</span>
        <span><span class="sdot"></span> Desktop, tablet and phone</span>
      </div>
    </div>
  </section>

  <section class="product-shot">
    <div class="wrap">
      <div class="shot-frame">
        <img src="/images/overview-dark.png" alt="Wyzestock Overview in dark mode: stock value, excess, stock-outs and the items that need attention across the winery and three depots" loading="eager">
      </div>
    </div>
  </section>

  <section class="intro-video" id="video">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">Watch</div>
        <h2>Wyzestock in 80 seconds</h2>
        <p>Too much or too little stock both cost money. See how Wyzestock frees up capital and keeps customers served.</p>
      </div>
      <div class="video-frame">
        <video controls muted playsinline preload="metadata" poster="/images/video-poster.jpg" aria-label="Wyzestock introduction video">
          <source src="/videos/wyzestock-intro.mp4" type="video/mp4">
          Your browser cannot play this video. <a href="/videos/wyzestock-intro.mp4">Download it here</a>.
        </video>
        <button type="button" class="sound-on" hidden>&#128266;&nbsp; Turn on sound</button>
      </div>
      <script>
        (function () {{
          var v = document.querySelector('#video video');
          var sound = document.querySelector('#video .sound-on');
          if (!v) return;
          function withSound() {{
            v.muted = false; v.currentTime = 0; v.play().catch(function () {{}});
            sound.hidden = true;
          }}
          // starts silently when it scrolls into view (browsers only allow muted autoplay), pauses when out of view
          var started = false;
          if ('IntersectionObserver' in window) {{
            new IntersectionObserver(function (entries) {{
              entries.forEach(function (en) {{
                if (en.isIntersecting && en.intersectionRatio >= 0.5) {{
                  if (v.paused && (!started || v.muted)) {{ v.play().catch(function () {{}}); }}
                  if (!started) {{ started = true; if (v.muted) sound.hidden = false; }}
                }} else if (!v.paused && v.muted) {{ v.pause(); }}
              }});
            }}, {{ threshold: [0, 0.5] }}).observe(v);
          }}
          sound.addEventListener('click', withSound);
          v.addEventListener('volumechange', function () {{ if (!v.muted) sound.hidden = true; }});
          document.querySelectorAll('[data-play-video]').forEach(function (btn) {{
            btn.addEventListener('click', function (e) {{
              e.preventDefault();
              document.getElementById('video').scrollIntoView({{ behavior: 'smooth', block: 'center' }});
              withSound();
            }});
          }});
        }})();
      </script>
    </div>
  </section>

  <!-- HUB -->
  <section class="hub" id="hub">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">How it works</div>
        <h2>The right stock, in the right place, and no more</h2>
        <p>Too much stock ties up cash and warehouse space. Too little loses sales. Wyzestock balances the two for every item at every location, from the data already in your ERP.</p>
      </div>

      <div class="hub-svg-wrap">{HUB_SVG}
      </div>

      <div class="hub-mobile">
        <div class="hub-core-m"><strong>Right stock</strong><span>in the right place</span></div>
        <ul>
          <li><b>Stock position</b><span>Model stock, excess, shortfall</span></li>
          <li><b>Forecasting</b><span>Seasonal, every item and location</span></li>
          <li><b>Replenishment</b><span>What to order, and how much</span></li>
          <li><b>Distribution</b><span>What to move between locations</span></li>
          <li><b>Demand management</b><span>Sales against forecast, daily</span></li>
          <li><b>Bills of material</b><span>Components from finished goods</span></li>
        </ul>
      </div>

      <div class="hub-points">
        <div class="hub-point">
          <h3>A target for every item</h3>
          <p>Model stock, reorder point and safety stock are worked out from the forecast, the lead time and the service level each item deserves, so A items are protected and slow sellers are not overstocked.</p>
        </div>
        <div class="hub-point">
          <h3>Action lists, not reports</h3>
          <p>Stock-outs, items about to run out, excess, slow movers, overdue purchase orders and suggested orders and transfers, each in its own list, ready to act on.</p>
        </div>
        <div class="hub-point">
          <h3>Current every day</h3>
          <p>Stock, sales, open orders, purchase orders and recipes are read from your ERP twice a day and everything is recalculated, so the numbers are never last month's.</p>
        </div>
      </div>
    </div>
  </section>
'''
    out += features([
        ('📦', 'Stock position', 'On hand, allocated, available and on order for every item at every location, against its model stock, with days of cover and the run-out date.'),
        ('⚖️', 'Model stock and safety stock', 'Targets from the forecast, the lead time and a service level set by ABC-XYZ class, so stock goes where it earns its keep.'),
        ('🚨', 'Exceptions', 'Stock-outs, potential stock-outs, excess, slow-moving stock and surplus orders, each listed with its value so you start with what matters most.'),
        ('🛒', 'Replenishment', 'Suggested orders per supplier, rounded to the minimum order and pack size, with the economic order quantity alongside.'),
        ('🚚', 'Distribution', 'Transfers between locations that cover shortages from stock you already own, before anything new is bought.'),
        ('📈', 'Seasonal forecasting', 'Holt-Winters forecasts for every item at every location, with sensible handling of new, occasional and dormant items, and manual overrides where you know better.'),
        ('🧾', 'Demand management', 'Sales against forecast, stock cover and production month to date, emailed as an Excel report every morning, plus the Case Sales Predictor.'),
        ('🧩', 'Bills of material', 'Component demand worked out from finished-good sales through your recipes, and a clear view of what each product is made from and used in.'),
        ('✨', 'AI Insights', 'Plain-English explanations of an item\'s figures, what needs attention today and a monthly commentary, with every number checked against your data.'),
    ], 'What Wyzestock does', 'Everything you need to plan stock, in one place', 'One platform that turns the stock, sales and orders already in your ERP into targets, exceptions and suggestions, recalculated every day.')

    out += showcase('stock-position', 'Stock position', 'See what you hold against what you should hold',
                    'Every item at every location, with its model stock beside what is actually on the shelf. The gap, in units and in rand, is the money Wyzestock can free up, or the sales it can protect.',
                    ['On hand, allocated, available and on purchase order', 'Model stock, reorder point and safety stock for each location',
                     'Days of cover and the date it will run out', 'Click any item for its full detail, forecast and bill of material'],
                    [('stock-position.png', 'Wyzestock Stock Position: every wine at every depot with on hand, available, model stock, days cover, excess and shortfall'),
                     ('item-detail.png', 'Wyzestock item detail window: general details, stock, policy, the twelve-month forecast and the same item at other locations')],
                    link=('/stock-optimisation/', 'More about stock optimisation'))
    out += showcase('exceptions', 'Exceptions', 'Start with the items that need you today',
                    'Wyzestock sorts the exceptions out of thousands of item and location combinations and puts a value on each, so the first thing you look at is the thing that costs the most.',
                    ['Stock-outs and items that will run out before stock can arrive', 'Excess above model stock, valued at cost',
                     'Slow-moving stock by 30, 60, 90 and 120 days without a sale', 'Purchase orders that are more than you need'],
                    [('exceptions.png', 'Wyzestock Exceptions: stock-outs, potential stock-outs, excess and slow-moving items with their values')], reverse=True)
    out += showcase('replenishment', 'Replenishment', 'Know what to order, from whom, and how much',
                    'Suggested orders for every supplier, worked out from the model stock, what is already on order and the lead time, and rounded the way you actually buy.',
                    ['Rounded to the minimum order quantity and the pack or pallet multiple', 'Economic order quantity alongside, for the items where it matters',
                     'Open purchase orders, with the overdue ones highlighted', 'Filter by supplier, location, group or category and export to Excel'],
                    [('replenishment.png', 'Wyzestock Replenishment: suggested orders by supplier with model stock, on order, lead time and rounded order quantity'),
                     ('purchase-orders.png', 'Wyzestock Purchase Orders: open orders with due dates, outstanding quantities and overdue lines in red')],
                    link=('/replenishment/', 'More about replenishment'))
    out += showcase('distribution', 'Distribution', 'Move stock before you buy more of it',
                    'One depot is short while another holds too much. Wyzestock suggests the transfers that cover the shortage from stock you already own, from the locations you choose, in the order you choose.',
                    ['Transfers from your production or central warehouse first, then from other depots', 'Lines that cannot be covered, so you know what to make or buy',
                     'The value of every transfer and every uncovered line', 'Press any line to see the item at every location'],
                    [('distribution.png', 'Wyzestock Distribution: suggested transfers from the winery to the Cape Town, Johannesburg and Durban depots')], reverse=True,
                    link=('/distribution/', 'More about distribution'))
    out += showcase('demand-management', 'Demand management', 'The state of the month, in your inbox every morning',
                    'Sales month to date against forecast, the run rate for the rest of the month, stock cover and production against plan, by range and by item. Emailed as an Excel report after the morning update.',
                    ['Overview by range, with the target for the day of the month', 'Detail laid out like the report your team already uses',
                     'Case Sales Predictor: where each item will land at the current run rate', 'Production plan and manual forecast captured in the app'],
                    [('dm-overview.png', 'Wyzestock Demand Management overview: sales against forecast by range with the month-to-date target'),
                     ('case-predictor.png', 'Wyzestock Case Sales Predictor: sales and orders, forecast, run rate per day and projected surplus or shortfall per item')],
                    link=('/demand-management/', 'More about demand management'))
    out += showcase('bom', 'Bills of material', 'From finished goods to every component behind them',
                    'Wyzestock reads your recipes from the ERP, works out component demand from finished-good sales, and shows what each product is made from and where each component is used.',
                    ['Component forecasts from finished-good demand, at the production location', 'Made from: every component, every level, with the stock behind it',
                     'Used in: which finished goods a short component will stop', 'Raw materials, packaging and consumables planned like everything else'],
                    [('bom.png', 'Wyzestock Bill of material window: a wine made from bulk wine, glass, closure, label and carton, with stock and days of cover for each')])
    out += showcase('ai-insights', 'AI Insights', 'Ask why, and get an answer in plain English',
                    'Buttons in Wyzestock explain an item\'s figures, say why it is excess or slow moving, list what needs attention today and write the monthly demand commentary. Every number in the answer is checked against your data before you see it.',
                    ['Explain these figures, for any item at any location', 'What needs attention today, ranked, with a suggested next step',
                     'Monthly commentary for the demand management meeting', 'A review of the forecasts that look out of line'],
                    [('ai-attention.png', 'Wyzestock What needs attention today: stock-outs, items about to run out and overdue orders, each with what to do'),
                     ('ai-explain.png', 'Wyzestock Explain these figures: a plain-English explanation of an item\'s stock, forecast and model stock')], reverse=True,
                    link=('/ai-insights/', 'More about AI Insights'))
    out += f'''
  <!-- SYNC -->
  <section class="showcase-section" id="sync">
    <div class="wrap">
      <div class="showcase-row">
        <div class="showcase-text">
          <div class="section-label">Automatic sync</div>
          <h2>No exports. No spreadsheets. Nobody has to remember to run anything.</h2>
          <p>A small service on your server reads stock, sales, open orders, purchase orders and recipes from your ERP twice a day. Wyzestock recalculates everything and the screens are simply current.</p>
          <ul class="showcase-list">
            <li>Read-only: nothing in your ERP is changed</li>
            <li>Twice a day, at 07:00 and 14:00, automatically</li>
            <li>If a load fails or is late, we know about it before you do</li>
          </ul>
        </div>
        <div class="showcase-image">
          <div class="showcase-frame narrow" style="padding:24px">{SYNC_SVG}
          </div>
        </div>
      </div>
    </div>
  </section>
'''
    out += features([
        ('🎯', 'Service levels by class', 'Every item is classed A, B or C by value and X, Y or Z by how steady its demand is, and each class gets the service level you choose.'),
        ('📅', 'Your working days', 'Public holidays and shutdowns are left out of the working days that drive run rates, review periods and the demand report.'),
        ('🏭', 'Production and distribution', 'Production, depot and stock-only locations, each with its own role and lead time, and the sources each depot draws from.'),
        ('📄', 'Export to PDF and Excel', 'Any list can go out as a PDF or a spreadsheet, with the filters you applied printed at the top.'),
        ('🌗', 'Light and dark, any device', 'Fully responsive on desktop, tablet and phone, with a light and a dark theme.'),
        ('🔐', 'Secure, role-based access', 'Each company\'s data is kept apart, and each user sees what their role allows.'),
    ], 'Built for how stock really moves', 'The details that make it fit', 'Small touches that make Wyzestock feel built for your business.', sid='details', cls='details')
    out += contact_section()
    out += '\n</main>\n' + footer() + tail()
    return out


# ───────────────────────────── Landing pages ─────────────────────────────

def landing(path, crumb, eyebrow, h1, sub, hero_img, how_title, how_sub, steps, benefits_label, benefits_title, benefits,
            side_imgs, bigger, faq, title, desc, chips=None):
    out = head(title, desc, path)
    out += nav()
    st = '\n'.join(f'''        <div class="step"><div class="step-num">{n}</div><h3>{t}</h3>
          <p>{d}</p></div>''' for n, (t, d) in enumerate(steps, 1))
    bl = '\n'.join(f'            <li><strong>{t}</strong>{d}</li>' for t, d in benefits)
    ch = ''
    if chips:
        ch = '\n          <div class="chip-row">' + ''.join(f'<span class="chip"><i style="background:{c}"></i> {t}</span>' for t, c in chips) + '</div>'
    side = '\n          '.join(frame(*i) for i in side_imgs)
    fq = '\n'.join(f'        <details><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in faq)
    out += f'''
<main id="top">

  <section class="hero page-hero">
    <div class="wrap hero-inner">
      <div class="crumbs"><a href="/">Wyzestock</a> &nbsp;/&nbsp; {crumb}</div>
      <div class="eyebrow"><span class="dot"></span> {eyebrow}</div>
      <h1>{h1}</h1>
      <p class="hero-sub">{sub}</p>
      <div class="hero-actions">
        <a href="/#contact" class="btn btn-primary">Talk to us</a>
        {wa_link()}
      </div>
    </div>
  </section>

  <section class="product-shot">
    <div class="wrap">
      <div class="shot-frame">
        <div><img src="/images/{hero_img[0]}" alt="{esc(hero_img[1])}" loading="eager"></div>
      </div>
    </div>
  </section>

  <section class="lp-section">
    <div class="wrap">
      <div class="section-head">
        <div class="section-label">How it works</div>
        <h2>{how_title}</h2>
        <p>{how_sub}</p>
      </div>
      <div class="steps">
{st}
      </div>
    </div>
  </section>

  <section class="lp-section">
    <div class="wrap">
      <div class="two-col">
        <div class="prose">
          <div class="section-label">{benefits_label}</div>
          <h2>{benefits_title}</h2>{ch}
          <ul class="benefit-list">
{bl}
          </ul>
        </div>
        <div class="stack">
          {side}
        </div>
      </div>
    </div>
  </section>

  <section class="lp-section">
    <div class="wrap">
      <div class="section-head" style="margin-bottom:0;">
        <div class="section-label">Part of a bigger picture</div>
        <h2>{bigger[0]}</h2>
        <p>{bigger[1]}</p>
      </div>
    </div>
  </section>

  <section class="lp-section" id="faq">
    <div class="wrap">
      <div class="section-head" style="margin-bottom:36px;">
        <div class="section-label">Questions</div>
        <h2>Frequently asked questions</h2>
      </div>
      <div class="faq">
{fq}
      </div>
    </div>
  </section>

  <section class="cta-band">
    <div class="wrap">
      <h2>See it on your own numbers</h2>
      <p>Tell us what you stock, where you hold it and which ERP you run. We will show you Wyzestock working on a demo company, then on your data.</p>
      <div class="cta-row">
        <a href="/#contact" class="btn btn-primary">Send us a message</a>
        {wa_link()}
      </div>
      <div class="cta-mail">Or email <a href="mailto:{EMAIL}">{EMAIL}</a></div>
    </div>
  </section>

</main>
'''
    out += footer() + tail()
    return out


def a(href, text):
    return f'<a href="{href}" style="color:var(--amber)">{text}</a>'


def stock_page():
    return landing(
        '/stock-optimisation/', 'Stock optimisation', 'Inventory optimisation for any ERP',
        'Free up cash <span class="accent">without running short</span>',
        'Wyzestock works out a model stock for every item at every location from its forecast, its lead time and the service level it deserves. Then it shows you, in units and in rand, where you hold too much and where you are about to run out.',
        ('stock-position.png', 'Wyzestock Stock Position with model stock, excess and shortfall per item and location'),
        'From a list of items to a target for each one', 'Wyzestock does the arithmetic for every item at every location, every day.',
        [('Every item is classified', 'Items are ranked A, B or C by the value of their annual usage, and X, Y or Z by how steady their demand is. Each of the nine classes gets the service level you set.'),
         ('A target is calculated', 'Safety stock comes from the service level and how far actual sales stray from the forecast. Model stock covers the lead time and the review period, plus that safety stock.'),
         ('The gap is valued', 'Stock above the model is excess; stock below the reorder point is a shortfall. Both are valued at cost, so you can see the size of the prize.')],
        'What you can do with it', 'Hold the stock that earns its place, and let the rest go',
        [('See excess in rand', 'Excess above model stock, valued at cost, for every item, location, group and category.'),
         ('Catch stock-outs early', 'Potential stock-outs are items that will run out before a new order could arrive, flagged while there is still time.'),
         ('Find slow movers', 'Items with no sale for 30, 60, 90 or 120 days, with the value tied up in each band.'),
         ('Protect what matters', 'A items with steady demand get a high service level; erratic C items do not, so safety stock goes where it pays.'),
         ('Trust the inputs', 'Lead times, minimum orders and pack sizes come from your ERP and can be set per item and location in Settings.'),
         ('Choose your method', 'Use the service-level method, or the simpler lead-time method many teams already know.')],
        [('exceptions.png', 'Wyzestock Exceptions list with stock-outs, excess and slow-moving stock'),
         ('item-detail.png', 'Wyzestock item detail with stock, policy and forecast')],
        ('Stock optimisation drives everything else', f'The same model stock feeds {a("/replenishment/", "replenishment")}, {a("/distribution/", "distribution")} and the {a("/demand-management/", "demand management report")}. {a("/#hub", "See how it fits together")}.'),
        [('What is model stock?', 'Model stock is the quantity Wyzestock suggests you hold for an item at a location: enough to cover demand over the lead time and the review period, plus safety stock for the service level you want. Anything well above it is excess.'),
         ('How is safety stock worked out?', 'From the service level for the item\'s ABC-XYZ class and how far actual sales have strayed from the forecast. Steady, valuable items get more protection; erratic, low-value items less.'),
         ('Where do lead times come from?', 'From your ERP where they are kept, from each location\'s default, or from the item and location settings in Wyzestock, in that order of preference.'),
         ('Does it work with more than one warehouse?', 'Yes. Every item is calculated at every location, and each location has a role: production, sales depot or stock only.'),
         ('How often is it recalculated?', 'After every load from your ERP, twice a day, and whenever you press Recalculate.')],
        'Stock Optimisation: Model Stock, Excess & Stock-outs | Wyzestock',
        'Model stock, safety stock and reorder points for every item at every location. See excess and shortfall in rand and catch stock-outs early.',
        chips=[('Stock-out', '#EF4444'), ('Potential stock-out', '#F59E0B'), ('Excess', '#8B5CF6'), ('Slow moving', '#3B82F6'), ('On target', '#10B981')])


def replenishment_page():
    return landing(
        '/replenishment/', 'Replenishment', 'Purchase suggestions for any ERP',
        'Order <span class="accent">what you need, when you need it</span>',
        'Wyzestock suggests what to order from every supplier, based on the model stock, what is already on order and the lead time, rounded to the minimum order and the pack size. It tracks your open purchase orders and flags the late ones.',
        ('replenishment.png', 'Wyzestock Replenishment suggestions by supplier'),
        'From a shortfall to a purchase order line', 'The suggestion is worked out item by item, then gathered by supplier.',
        [('Inventory position', 'On hand, less what is allocated to customers, plus what is already on order, for each item at each location.'),
         ('Below the reorder point?', 'When the inventory position drops below the reorder point, Wyzestock suggests enough to bring it back up to the model stock.'),
         ('Rounded the way you buy', 'The suggestion is lifted to the minimum order quantity and rounded to the order multiple, with the economic order quantity shown alongside.')],
        'What you can do with it', 'A buying list you can trust, and fewer surprises from suppliers',
        [('Buy by supplier', 'Filter the list by supplier and see everything you should order from them today.'),
         ('Respect how suppliers sell', 'Minimum order quantities and pack or pallet multiples per item and location.'),
         ('Avoid double ordering', 'Open purchase orders are counted, so a late order does not trigger a second one.'),
         ('Chase late orders', 'Overdue purchase order lines are shown in red, with their value.'),
         ('Spot surplus orders', 'Orders that would take stock well above the model are flagged before the goods arrive.'),
         ('Components too', 'Raw materials and packaging are suggested from finished-good demand through your bills of material.')],
        [('purchase-orders.png', 'Wyzestock Purchase Orders with overdue lines'),
         ('bom.png', 'Wyzestock Bill of material window')],
        ('Replenishment works from the same targets', f'Suggestions come from the {a("/stock-optimisation/", "model stock")}, and stock can often be {a("/distribution/", "moved between locations")} instead of bought. {a("/#hub", "See how it fits together")}.'),
        [('What does the suggested quantity mean?', 'It is the quantity that brings the item back up to its model stock, after counting stock on hand, allocations and open purchase orders, rounded to the minimum order and order multiple.'),
         ('Does Wyzestock place the orders?', 'No. Wyzestock suggests; you place the order in your ERP as usual. The next load picks it up as an open purchase order.'),
         ('Can I export the list for a supplier?', 'Yes. Filter by supplier and export to Excel or PDF; the filters you used are printed at the top.'),
         ('What about supplier stock?', 'Stock held for you at a supplier can be captured in Wyzestock and counted in the picture.'),
         ('Can it plan raw materials and packaging?', 'Yes. Component demand comes from finished-good demand through your recipes, at the production location.')],
        'Replenishment: Purchase Suggestions & Open Orders | Wyzestock',
        'Suggested orders per supplier from model stock, open orders and lead times, rounded to minimum order and pack size, with overdue purchase orders flagged.')


def distribution_page():
    return landing(
        '/distribution/', 'Distribution', 'Transfers between locations',
        'Use the stock <span class="accent">you already own</span>',
        'When one location is short and another holds more than it needs, Wyzestock suggests the transfer. Each depot draws from the sources you choose, in the order you choose, so you move stock before you buy or make more.',
        ('distribution.png', 'Wyzestock Distribution suggested transfers'),
        'From a shortage to a transfer', 'Distribution runs after the stock calculation, for every item at every depot.',
        [('Shortages are found', 'Each depot\'s available stock is compared with its reorder point and model stock.'),
         ('Sources are checked in order', 'Each depot has a ranked list of sources, usually the production location first and then other depots. Only stock above a source\'s own needs is offered.'),
         ('Transfers and gaps', 'Wyzestock suggests the transfers, and lists the shortages that no location can cover, so you know what to make or buy.')],
        'What you can do with it', 'Balance stock across your network before spending more',
        [('Less buying, less making', 'Cover a depot\'s shortage from another location\'s excess instead of a new order.'),
         ('Your rules', 'Choose which locations each depot may draw from, and in which order, in Settings.'),
         ('See what cannot be covered', 'Lines with no source are listed with their value.'),
         ('Value every move', 'Each transfer shows the quantity and its value at cost.'),
         ('Drill into any item', 'Press a line to see the item at every location, with its forecast and bill of material.'),
         ('Export the pick list', 'Send the transfers to the warehouse as Excel or PDF.')],
        [('stock-position.png', 'Wyzestock Stock Position by location')],
        ('Distribution balances the same targets', f'Transfers use the {a("/stock-optimisation/", "model stock")} at every location, and what cannot be covered becomes a {a("/replenishment/", "purchase suggestion")}. {a("/#hub", "See how it fits together")}.'),
        [('Which locations can a depot draw from?', 'The ones you choose in Settings, ranked. A typical setup is the production location first and neighbouring depots after it.'),
         ('Will it strip a source location?', 'No. A source only offers stock above what it needs for itself.'),
         ('Does it create the transfers in my ERP?', 'No. Wyzestock suggests; your team captures the transfer in the ERP as usual.'),
         ('What are the "not covered" lines?', 'Shortages that no source can cover. They tell you what to produce or buy.')],
        'Distribution: Stock Transfers Between Locations | Wyzestock',
        'Suggested transfers between your production location and depots, from the sources you choose, before you buy or make more.')


def dm_page():
    return landing(
        '/demand-management/', 'Demand management', 'Demand management and forecasting',
        'Know where the month <span class="accent">will land</span>, every morning',
        'Sales month to date against forecast, the run rate for the rest of the month, stock cover and production against plan, by range and by item. Wyzestock emails the report as Excel after the morning update, and the Case Sales Predictor shows where each item is heading.',
        ('dm-overview.png', 'Wyzestock Demand Management overview by range'),
        'From yesterday\'s sales to today\'s decisions', 'The report is rebuilt after every load from your ERP.',
        [('Forecasts for every item', 'Holt-Winters seasonal forecasts from up to 36 months of history, with new, occasional and dormant items handled sensibly, and manual forecasts where you know better.'),
         ('Measured against the day', 'Sales and open orders month to date are compared with the forecast and with where you should be for the working day of the month.'),
         ('Sent to the team', 'The report goes out as an Excel file every morning to the people you choose, with a short list of what needs attention at the top.')],
        'What you can do with it', 'Run the demand meeting from one report everyone already has',
        [('Overview by range', 'Each range against its target for the day, with a click through to the detail.'),
         ('Detail like your own report', 'Laid out the way your team already reads it, with groups, categories and totals.'),
         ('Case Sales Predictor', 'Run rate per day now and needed, projected sales and the surplus or shortfall against forecast for every item.'),
         ('Production against plan', 'Planned and produced quantities captured in the app, and the balance of production for the month.'),
         ('Manual forecast', 'Capture a forecast per finished good by month where you know more than the history does.'),
         ('Monthly commentary', 'An AI-written summary of the month for the meeting, with every number checked.')],
        [('case-predictor.png', 'Wyzestock Case Sales Predictor'),
         ('dm-detail.png', 'Wyzestock Demand Management detail report')],
        ('Demand drives the rest', f'The same forecasts set the {a("/stock-optimisation/", "model stock")}, the {a("/replenishment/", "purchase suggestions")} and component demand through your bills of material. {a("/#hub", "See how it fits together")}.'),
        [('Which forecasting method does Wyzestock use?', 'Holt-Winters seasonal forecasting for items with at least a year of history; a flat or category-based forecast for newer items; an average for occasional sellers; and none for items that have stopped selling. Components are forecast from finished goods through the recipes.'),
         ('Can we override the forecast?', 'Yes. A manual forecast per finished good per month replaces the calculated one, and is highlighted wherever it is used.'),
         ('Who receives the morning email?', 'The people you add in Settings. They do not need a Wyzestock login.'),
         ('What happens if the data does not load?', 'No report is sent that day, and Wyzestock support is told straight away so it can be fixed.'),
         ('Does it follow our working days?', 'Yes. Weekends, public holidays and shutdowns are left out of the working days used for the run rate and the target.')],
        'Demand Management & Forecasting | Wyzestock',
        'Daily demand management report by email, sales against forecast and run rate by range and item, seasonal Holt-Winters forecasts and the Case Sales Predictor.')


def ai_page():
    return landing(
        '/ai-insights/', 'AI Insights', 'AI that explains your stock',
        'Ask <span class="accent">why</span>, and get an answer you can trust',
        'Buttons throughout Wyzestock turn the figures into plain English: why an item is excess, what needs attention today, which forecasts look wrong and how the month went. Every number in an answer is checked against your data before you see it.',
        ('ai-attention.png', 'Wyzestock What needs attention today'),
        'Figures first, words second', 'The AI never does the arithmetic. Wyzestock does, and the AI explains it.',
        [('Wyzestock works out the facts', 'The figures for the question, from stock and orders to the forecast and model stock, are calculated in the database first.'),
         ('The AI puts them into words', 'A short explanation in plain English, written for a stock planner, with a suggested next step.'),
         ('Every number is checked', 'Each figure in the answer is compared with the facts. If one does not match, the answer is rejected and the standard wording is shown instead.')],
        'What you can do with it', 'Spend less time working out what the numbers mean',
        [('Explain these figures', 'For any item at any location: what the stock, forecast and model stock say and what to do about it.'),
         ('Why is this excess or slow moving?', 'The likely cause from the history, and a recommended action.'),
         ('What needs attention today', 'Stock-outs, items about to run out, overdue orders and surplus orders, ranked, at the top of the morning email too.'),
         ('Review the forecast', 'Forecasts that look out of line with recent sales, for a second look.'),
         ('Monthly commentary', 'A short write-up of the month for the demand meeting.'),
         ('Under your control', 'Switched on per company, with a daily limit on use.')],
        [('ai-explain.png', 'Wyzestock Explain these figures')],
        ('AI on top of solid numbers', f'Insights sit on the {a("/stock-optimisation/", "stock calculation")}, the {a("/demand-management/", "forecasts")} and your own ERP data. {a("/#hub", "See how it fits together")}.'),
        [('Does the AI make up numbers?', 'No. Wyzestock calculates every figure first, and any answer containing a number that is not in the facts is thrown away.'),
         ('Is my data used to train AI models?', 'No. Only the figures needed for the question are sent, and they are not used for training.'),
         ('Can we switch it off?', 'Yes, per company. Everything else in Wyzestock works the same without it.'),
         ('Does it cost extra?', 'Talk to us. AI Insights is available on request and has a daily limit on use.')],
        'AI Insights for Inventory | Wyzestock',
        'Plain-English explanations of stock, excess and forecasts, what needs attention today and a monthly commentary, with every number checked against your data.')


def partners_page():
    return landing(
        '/partners/', 'For ERP partners', 'For ERP and accounting partners',
        'Give your clients the stock planning <span class="accent">their ERP never did</span>',
        'Your clients already record their stock, sales and purchases in the ERP. Wyzestock turns that into model stock, purchase and transfer suggestions and a daily demand report, without you building or running a planning product.',
        ('overview-dark.png', 'Wyzestock Overview'),
        'From introduction to suggestions', 'We do the connecting and the running; you stay the trusted advisor.',
        [('Tell us the system', 'Which ERP your client runs, how many locations they have, and what they want to achieve.'),
         ('We connect and map', 'We install the read-only extract, map locations and items, and load up to three years of history.'),
         ('Suggestions fill in', 'Once the first load has run, model stock, exceptions and suggestions fill in from the client\'s own data and stay current twice a day.')],
        'What your clients get', 'Stock planning built from their own numbers',
        [('A target for every item', 'Model stock, reorder point and safety stock at every location.'),
         ('Action lists', 'Stock-outs, excess, slow movers, purchase and transfer suggestions.'),
         ('Forecasts', 'Seasonal forecasts for finished goods, and components through the bills of material.'),
         ('A morning report', 'The demand management report by email, every day.'),
         ('Each client kept apart', 'Their own secure space, logins and logo, as in our Fynbos Hill demo.'),
         ('Nothing for you to run', 'We look after the platform, the extract and the support.')],
        [('stock-position.png', 'Wyzestock Stock Position')],
        ('Introduce a client, or bundle us with your services', 'Whether you want to introduce a client, offer Wyzestock alongside your own services, or simply see it on a demo company first, we would like to talk.'),
        [('Which ERP systems do you work with?', 'Wyzestock reads the client\'s ERP database directly, so it is not tied to one product. Tell us the system and version and we will confirm how it connects.'),
         ('What access do you need?', 'Read access to the data we extract, on a schedule. We do not change anything in the ERP.'),
         ('Is each client\'s data kept separate?', 'Yes. Every client has its own secure space, and access is controlled per user.'),
         ('Can I see it before I introduce a client?', 'Yes. We will walk you through our Fynbos Hill demo company, a winery with three depots, then talk about a pilot.')],
        'For ERP Partners | Wyzestock',
        'Offer your ERP clients inventory optimisation, replenishment and distribution planning built from their own data, without building or running it yourself.')


def write(path, text):
    p = ROOT / path.strip('/') / 'index.html' if path != '/' else ROOT / 'index.html'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    print('wrote', p.relative_to(ROOT))


if __name__ == '__main__':
    write('/', home())
    write('/stock-optimisation/', stock_page())
    write('/replenishment/', replenishment_page())
    write('/distribution/', distribution_page())
    write('/demand-management/', dm_page())
    write('/ai-insights/', ai_page())
    write('/partners/', partners_page())
    urls = ['/'] + [p for p, _ in PAGES] + ['/partners/']
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>2026-10-21</lastmod></url>\n' for u in urls) + '</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {SITE}/sitemap.xml\n')
