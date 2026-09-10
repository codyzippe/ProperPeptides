# Generates the HTML pages from a shared shell so header/footer stay identical.
import os
HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Proper Peptides</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
{og}  <link rel="icon" href="assets/logo.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/styles.css">
</head>
<body>

  <div class="gate" id="ageGate">
    <div class="card">
      <div class="ring">18+</div>
      <h2>Age Verification Required</h2>
      <p>You must be 18+ years old to view our peptide research products.</p>
      <div class="actions">
        <button class="yes" type="button">Yes, I'm 18+</button>
        <button class="no" type="button">No, I'm under 18</button>
      </div>
    </div>
  </div>

  <header class="site">
    <div class="wrap">
      <a class="logo" href="index.html" aria-label="Proper Peptides home"><img src="assets/logo.svg" alt="Proper Peptides"></a>
      <nav class="main" id="mainNav" aria-label="Primary">
        <ul>
          <li><a href="index.html"{c_home}>Home</a></li>
          <li><a href="peptides.html"{c_pep}>Peptides</a></li>
          <li><a href="about.html"{c_about}>About Us</a></li>
          <li><a href="contact.html"{c_contact}>Contact</a></li>
        </ul>
      </nav>
      <div class="tools">
        <a class="btn sm" href="peptides.html">Shop Peptides</a>
        <a class="cart-btn" href="cart.html" aria-label="Cart">
          <svg viewBox="0 0 24 24"><path d="M3 4h2l2.4 11.2a1 1 0 0 0 1 .8h9.6a1 1 0 0 0 1-.8L21 8H7"/><circle cx="9" cy="20" r="1.5"/><circle cx="17" cy="20" r="1.5"/></svg>
          <span class="cart-count">0</span>
        </a>
        <button class="burger" id="navToggle" aria-label="Menu" aria-expanded="false" aria-controls="mainNav"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
      </div>
    </div>
  </header>
{ticker}
  <main>
'''
TICKER = '''  <div class="ticker" aria-hidden="true">
    <div class="ticker-track">
      <span>Premium Research Peptides</span><span>Quality Assured &amp; Lab Tested</span><span>Fast Shipping</span><span>99%+ Purity Guaranteed</span><span>For Research Purposes Only</span>
      <span>Premium Research Peptides</span><span>Quality Assured &amp; Lab Tested</span><span>Fast Shipping</span><span>99%+ Purity Guaranteed</span><span>For Research Purposes Only</span>
    </div>
  </div>
'''
FOOT = '''  </main>

  <div class="disclaimer">
    <div class="wrap">
      <p>Our products are for research and/or investigative purposes and are not suitable for direct human consumption or consumers, nor are they intended for clinical or therapeutic use.</p>
      <p>The statements and products listed on this website are not intended to diagnose, treat, cure, or prevent any disease. As such, they have not been evaluated or approved by the Federal Food and Drug Administration (the "FDA"). We are not a compounding pharmacy or outsourcing facility as defined under either Section 503A and 503B of the Federal Food, Drug, and Cosmetic Act.</p>
    </div>
  </div>

  <footer class="site">
    <div class="wrap">
      <div class="foot-grid">
        <div>
          <a class="logo" href="index.html"><img src="assets/logo.svg" alt="Proper Peptides"></a>
          <p style="margin-top:16px">Authorized reseller of thePeptide research grade peptides. Premium research grade peptides for scientific and laboratory applications.</p>
        </div>
        <div>
          <h4>Products</h4>
          <ul>
            <li><a href="peptides.html#glow">GLOW</a></li>
            <li><a href="peptides.html#wolverine">Wolverine</a></li>
            <li><a href="peptides.html#nad">NAD+</a></li>
            <li><a href="peptides.html#cjc-1295-ipamorelin">CJC-1295 / Ipamorelin</a></li>
          </ul>
        </div>
        <div>
          <h4>Company</h4>
          <ul>
            <li><a href="about.html">About Us</a></li>
            <li><a href="contact.html">Contact</a></li>
            <li><a href="cart.html">Cart</a></li>
          </ul>
        </div>
        <div>
          <h4>Get In Touch</h4>
          <ul>
            <li><a href="mailto:properpeptide@gmail.com">properpeptide@gmail.com</a></li>
            <li><a href="mailto:codyzippe1@gmail.com">codyzippe1@gmail.com</a></li>
            <li>Research Use Only</li>
          </ul>
        </div>
      </div>
      <div class="foot-bottom">
        <p>&copy; 2026 Proper Peptides. All rights reserved. For research purposes only.</p>
        <p>Payments by Venmo and Cash App &bull; FedEx shipping</p>
      </div>
    </div>
  </footer>

  <script src="js/products.js"></script>
  <script src="js/main.js"></script>
{extra}
</body>
</html>
'''

SITE = 'https://theproperpeptide.com'
OG_IMAGE = 'https://thepeptide.s3.us-east-1.amazonaws.com/Glow-Front-NoShadow 1 (1)-01K18YQWGPQRKRYGZXY7K4QFFC.png'
OG = '''  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Proper Peptides">
  <meta property="og:title" content="{title} | Proper Peptides">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{image}">
  <meta property="og:url" content="{url}">
  <meta name="twitter:card" content="summary_large_image">
'''

# vercel.json uses cleanUrls, so the public URL for foo.html is /foo (and index.html is /)
def page_url(name):
    return SITE + '/' + ('' if name == 'index.html' else name[:-5])

def page(name, title, desc, body, current, extra='', ticker=False, og=False):
    cur = {k: (' aria-current="page"' if k == current else '') for k in ['home','pep','about','contact']}
    url = page_url(name)
    og_tags = OG.format(title=title, desc=desc, image=OG_IMAGE.replace(' ', '%20'), url=url) if og else ''
    html = HEAD.format(title=title, desc=desc, url=url, og=og_tags, ticker=(TICKER if ticker else ''), c_home=cur['home'], c_pep=cur['pep'], c_about=cur['about'], c_contact=cur['contact']) + body + FOOT.format(extra=extra)
    open(name, 'w').write(html)

# ---------------- HOME ----------------
home = '''
    <section class="hero">
      <div class="wrap">
        <div>
          <span class="eyebrow">Lab Tested &bull; $120 per box &bull; Free FedEx shipping on 6+ boxes</span>
          <h1>Unlock Peak Performance with <span>Proper Peptides</span></h1>
          <p class="sub">Premium research grade peptide compounds from thePeptide, designed for laboratory research and scientific study. Four rigorously tested blends at $120 per box, with free FedEx shipping on 6 or more boxes.</p>
          <div class="hero-actions">
            <a class="btn" href="peptides.html">Browse Peptides <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
            <a class="btn outline" href="about.html">About thePeptide</a>
          </div>
          <div class="trust">
            <span><i><svg viewBox="0 0 24 24"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.5"/><circle cx="17" cy="18" r="1.5"/></svg></i>Fast Shipping</span>
            <span><i><svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg></i>Lab Verified</span>
            <span><i><svg viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M7 15h4"/></svg></i>Venmo &amp; Cash App</span>
          </div>
        </div>
        <div class="tiles" id="homeTiles"></div>
      </div>
    </section>

    <section>
      <div class="wrap center">
        <h2>Why Choose Proper Peptides</h2>
        <p class="sub">Trusted for quality, purity, and reliability, backed by thePeptide's vetted US based manufacturing</p>
        <div class="features">
          <div class="feature"><div class="ico"><svg viewBox="0 0 24 24"><path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/></svg></div><h3>Premium Quality</h3><p>Rigorously tested peptides meeting the highest standards for research applications</p></div>
          <div class="feature"><div class="ico"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/></svg></div><h3>Lab Certified</h3><p>Each batch verified for purity and composition with detailed documentation</p></div>
          <div class="feature"><div class="ico"><svg viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M3 11h18M8 7V5h8v2"/></svg></div><h3>Secure Packaging</h3><p>Professional grade packaging with proper storage and handling specifications</p></div>
          <div class="feature"><div class="ico"><svg viewBox="0 0 24 24"><path d="M6 3h6v6l-4 9a2 2 0 0 0 2 3h4M18 3v6l4 9"/></svg></div><h3>Research Grade</h3><p>Designed exclusively for laboratory and scientific research purposes</p></div>
        </div>
        <div class="callout" style="text-align:left">
          <div class="ico">i</div>
          <div>
            <h3>Important: Research Use Only</h3>
            <p>All peptides sold by Proper Peptides are intended for research purposes only and are not for human consumption. These products are designed for use in laboratory settings by qualified researchers.</p>
          </div>
        </div>
      </div>
    </section>

    <section style="background:var(--navy-900)">
      <div class="wrap center">
        <h2>Proper's Most Popular</h2>
        <p class="sub">Explore our four thePeptide research blends</p>
        <div class="cats" id="homeCats"></div>
      </div>
    </section>
'''
home_extra = '''  <script>
    document.getElementById('homeTiles').innerHTML = PRODUCTS.map(tileHTML).join('');
    document.getElementById('homeCats').innerHTML = PRODUCTS.map(p => `
      <a class="cat" href="peptides.html#${p.id}">
        <div class="img"><img src="${p.image}" alt="${p.name}"></div>
        <span class="tag">${p.count}</span>
        <h3>${p.name} <small style="font-weight:500;color:var(--text-dim);font-size:.8rem">${p.subtitle}</small></h3>
        <p>${p.short}</p>
      </a>`).join('');
    document.querySelector('.cats').style.gridTemplateColumns = 'repeat(4, 1fr)';
    if (window.innerWidth < 1024) document.querySelector('.cats').style.gridTemplateColumns = 'repeat(2, 1fr)';
    if (window.innerWidth < 640) document.querySelector('.cats').style.gridTemplateColumns = '1fr';
  </script>'''
page('index.html', 'Premium Research Peptides', 'Proper Peptides: authorized reseller of thePeptide lab tested research peptides. GLOW, Wolverine, NAD+, CJC-1295/Ipamorelin.', home, 'home', home_extra, ticker=True, og=True)

# ---------------- PEPTIDES ----------------
pep = '''
    <section class="page-hero">
      <div class="wrap center">
        <span class="eyebrow">thePeptide &bull; Lab Tested &bull; Research Use Only</span>
        <h1>Our Peptides</h1>
        <p class="sub">Four research blends manufactured for thePeptide. Every product is lab tested for purity and shipped with tracking.</p>
      </div>
    </section>
    <section style="padding-top:20px">
      <div class="wrap">
        <div class="products-grid" id="productGrid"></div>
      </div>
    </section>
'''
pep_extra = '''  <script>
    const grid = document.getElementById('productGrid');
    grid.innerHTML = PRODUCTS.map(p => `
      <article class="pcard ${p.color}" id="${p.id}">
        <div class="art"><img src="${p.image}" alt="${p.name} ${p.subtitle}"></div>
        <div class="body">
          <span class="tag">${p.count} &bull; Net Wt ${p.weight} &bull; SKU ${p.sku}</span>
          <h3>${p.name}<small>${p.subtitle}</small></h3>
          <p class="desc">${p.short}</p>
          <ul class="specs">${p.perStrip.map(s => `<li>${s}</li>`).join('')}</ul>
          <div class="buy">
            <div class="price">${p.price ? money(p.price) : 'Contact for price'}<small>${p.price ? 'USD' : ''}</small></div>
            <button class="btn sm" data-add="${p.id}">Add to Cart</button>
          </div>
          <a class="details-link" href="#" data-detail="${p.id}">View research details &darr;</a>
        </div>
      </article>
      <div class="detail" id="detail-${p.id}">
        <button class="btn sm outline close" data-close="${p.id}">Close</button>
        <h3>${p.name} ${p.subtitle}</h3>
        ${p.sections.map(s => `<h4>${s.h}</h4><p>${s.p}</p>${s.li.length ? '<ul>' + s.li.map(l => `<li>${l}</li>`).join('') + '</ul>' : ''}`).join('')}
      </div>`).join('');

    grid.addEventListener('click', e => {
      const o = e.target.closest('[data-detail]'); const c = e.target.closest('[data-close]');
      if (o) { e.preventDefault(); const d = document.getElementById('detail-' + o.dataset.detail); d.classList.toggle('open'); if (d.classList.contains('open')) d.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
      if (c) document.getElementById('detail-' + c.dataset.close).classList.remove('open');
    });
    if (location.hash) { const t = document.querySelector(location.hash); if (t) setTimeout(() => t.scrollIntoView({ behavior: 'smooth', block: 'center' }), 200); }
  </script>'''
page('peptides.html', 'Peptides', 'GLOW, Wolverine, NAD+, and CJC-1295/Ipamorelin research peptides from thePeptide, sold by Proper Peptides.', pep, 'pep', pep_extra)

# ---------------- ABOUT ----------------
about = '''
    <section class="about-hero">
      <div class="wrap">
        <div class="about-grid">
          <div>
            <span class="eyebrow">About thePeptide</span>
            <h1>Rigorous Standards, Reliable Results</h1>
            <p class="sub" style="margin-top:18px">Proper Peptides is an authorized reseller of thePeptide, a US based research peptide company. Every product on this site is manufactured for thePeptide and sold through Proper Peptides.</p>
          </div>
          <div class="tiles" id="aboutTiles"></div>
        </div>
      </div>
    </section>

    <section style="padding-top:30px">
      <div class="wrap">
        <div class="about-grid">
          <div>
            <h2>Delivering Clean, Reliable Peptides, Every Time</h2>
            <p style="margin-top:16px">thePeptide's mission is simple: make high quality peptides easy to access, easy to trust, and easy to order. The focus is on what matters most: purity, safety, and real value.</p>
            <p>Every product is lab tested for verified quality and shipped discreetly with care. thePeptide partners with vetted, US based facilities that implement the highest standard of care in preparing products. Peptides are carefully synthesized and tested to meet the exacting needs of scientists, healthcare professionals, and research institutions.</p>
            <p>thePeptide is not a compounding facility. It is a partner in peptide innovation, offering ready to ship, lab tested peptides designed for consistency, performance, and ease of access.</p>
          </div>
          <div>
            <h2 style="font-size:1.6rem">Why Choose thePeptide?</h2>
            <div class="pillars" style="margin-top:20px">
              <div class="pillar"><h3>Uncompromising Quality</h3><p>Every product is tested for purity, potency, and reliability.</p></div>
              <div class="pillar"><h3>Vetted Ingredients</h3><p>Sourced exclusively from vetted, US based facilities that implement the highest standard of care.</p></div>
              <div class="pillar"><h3>No Outsourcing of Standards</h3><p>Quality benchmarks guide every step of the process.</p></div>
              <div class="pillar"><h3>Professionally Packed, Shipped with Tracking</h3><p>Fast fulfillment with support you can count on.</p></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section style="background:var(--navy-900)">
      <div class="wrap center">
        <h2>Our Commitment to Quality</h2>
        <p class="sub">thePeptide goes beyond industry standards to bring you peptides of unmatched purity and effectiveness</p>
        <div class="features">
          <div class="feature"><div class="ico"><svg viewBox="0 0 24 24"><path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/></svg></div><h3>Meticulously Vetted Raw Materials</h3><p>Sourced exclusively from vetted, US based facilities</p></div>
          <div class="feature"><div class="ico"><svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg></div><h3>Rigorous Quality Control</h3><p>Every batch lab tested for purity and potency before it ships</p></div>
          <div class="feature"><div class="ico"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg></div><h3>Decades of Peptide Innovation</h3><p>Built on long standing peptide research and manufacturing experience</p></div>
          <div class="feature"><div class="ico"><svg viewBox="0 0 24 24"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.5"/><circle cx="17" cy="18" r="1.5"/></svg></div><h3>Reliable Shipping and Tracking</h3><p>On all orders, professionally packed</p></div>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="owner">
          <figure>
            <div class="photo"><img src="assets/cody.jpg" alt="Cody Zippe, founder of Proper Peptides"></div>
            <figcaption>Cody Zippe</figcaption>
          </figure>
          <div>
            <span class="eyebrow">Meet the owner</span>
            <h2>Cody Zippe</h2>
            <p class="role">Founder, Proper Peptides &bull; Authorized thePeptide Sales Representative</p>
            <p>Every order is handled personally by thePeptide team, from confirming your payment to packing the box, and ships with FedEx tracking so you always know where your research materials are.</p>
            <div class="owner-cards">
              <div class="card">
                <h4>Business email</h4>
                <p><a href="mailto:codyzippe1@gmail.com">codyzippe1@gmail.com</a></p>
              </div>
              <div class="card">
                <h4>Business inquiries</h4>
                <p>For sales, wholesale, and partnership inquiries, email Cody directly.</p>
              </div>
            </div>
            <a class="btn" href="mailto:codyzippe1@gmail.com">Email Cody <svg viewBox="0 0 24 24"><path d="M4 6h16v12H4z"/><path d="M4 7l8 6 8-6"/></svg></a>
          </div>
        </div>
      </div>
    </section>

    <section style="padding-top:0">
      <div class="wrap center">
        <h2>Proper Peptides &times; thePeptide</h2>
        <p class="sub">Proper Peptides sells thePeptide's four research blends directly. Same lab tested products, same manufacturer, ordered through properpeptides.com.</p>
        <div style="margin-top:28px"><a class="btn" href="peptides.html">Shop the Peptides</a></div>
      </div>
    </section>
'''
about_extra = '''  <script>document.getElementById('aboutTiles').innerHTML = PRODUCTS.map(tileHTML).join('');</script>'''
page('about.html', 'About Us', 'About thePeptide, the US based research peptide manufacturer behind Proper Peptides products.', about, 'about', about_extra)

# ---------------- CONTACT ----------------
contact = '''
    <section class="page-hero">
      <div class="wrap center">
        <h1>Contact Us</h1>
        <p class="sub">Questions about a product, an order, or research documentation? Reach out and we'll get back to you.</p>
      </div>
    </section>
    <section style="padding-top:10px">
      <div class="wrap">
        <div class="contact-grid">
          <div class="contact-card">
            <h3>Get In Touch</h3>
            <p style="margin-top:12px"><strong>Email</strong><br><a href="mailto:properpeptide@gmail.com">properpeptide@gmail.com</a><br><a href="mailto:codyzippe1@gmail.com">codyzippe1@gmail.com</a></p>
            <p><strong>Hours</strong><br>Monday to Friday<br>9:00 a.m. to 6:00 p.m. (PST)</p>
            <p><strong>Manufacturer support</strong><br>thePeptide technical support<br><a href="mailto:support@thepeptide.com">support@thepeptide.com</a></p>
            <p style="font-size:.85rem">Research use only. We cannot answer questions about human use.</p>
          </div>
          <div class="contact-card">
            <form id="contactForm" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
              <div class="row2">
                <div class="field"><label for="name">Name</label><input id="name" name="name" required></div>
                <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" required></div>
              </div>
              <div class="field"><label for="subject">Subject</label>
                <select id="subject" name="subject">
                  <option>Product question</option><option>Order status</option><option>Wholesale / bulk</option><option>Other</option>
                </select>
              </div>
              <div class="field"><label for="message">Message</label><textarea id="message" name="message" required></textarea></div>
              <button class="btn" type="submit">Send Message</button>
              <p style="font-size:.8rem;color:var(--text-dim);margin-top:12px">This form posts to Formspree. Create a free form at formspree.io and paste your form ID into the action URL in contact.html.</p>
            </form>
          </div>
        </div>
      </div>
    </section>
'''
page('contact.html', 'Contact', 'Contact Proper Peptides by email for product questions, order status, and wholesale inquiries. Research use only.', contact, 'contact')

# ---------------- CART / CHECKOUT ----------------
cart = '''
    <section class="page-hero">
      <div class="wrap"><h1 id="pageTitle">Your Cart</h1></div>
    </section>
    <section style="padding-top:10px">
      <div class="wrap">
        <ol class="steps" id="steps" aria-label="Checkout progress">
          <li class="active"><span class="n">1</span><span class="l">Cart</span></li>
          <li><span class="n">2</span><span class="l">Shipping</span></li>
          <li><span class="n">3</span><span class="l">Payment</span></li>
          <li><span class="n">4</span><span class="l">Done</span></li>
        </ol>

        <div class="empty" id="emptyCart" hidden>
          <h3>Your cart is empty</h3>
          <p style="margin:10px 0 20px">Browse the four thePeptide research blends. $120 per box, free FedEx shipping on 6 or more.</p>
          <a class="btn" href="peptides.html">Shop Peptides</a>
        </div>

        <div class="cart-layout" id="checkout">
          <div class="step-panels">

            <div class="step-panel" id="step1">
              <div class="ship-banner" id="shipBanner"></div>
              <div class="cart-list" id="cartList"></div>
            </div>

            <div class="step-panel" id="step2" hidden>
              <form id="shipForm" class="panel">
                <h3>Shipping address</h3>
                <div class="row2">
                  <div class="field"><label for="fName">Full name</label><input id="fName" name="name" autocomplete="name" required></div>
                  <div class="field"><label for="fEmail">Email</label><input id="fEmail" name="email" type="email" autocomplete="email" required></div>
                </div>
                <div class="field"><label for="fPhone">Phone</label><input id="fPhone" name="phone" type="tel" autocomplete="tel" required></div>
                <div class="field"><label for="fStreet">Street address</label><input id="fStreet" name="street" autocomplete="street-address" required></div>
                <div class="row3">
                  <div class="field"><label for="fCity">City</label><input id="fCity" name="city" autocomplete="address-level2" required></div>
                  <div class="field"><label for="fState">State</label><input id="fState" name="state" autocomplete="address-level1" maxlength="2" pattern="[A-Za-z]{2}" title="Two letter state code" placeholder="CA" required></div>
                  <div class="field"><label for="fZip">ZIP</label><input id="fZip" name="zip" inputmode="numeric" autocomplete="postal-code" pattern="\\d{5}(-\\d{4})?" title="5 digit ZIP code" required></div>
                </div>

                <h3 class="mt">Shipping method</h3>
                <div class="opts" id="shipOpts"></div>

                <h3 class="mt">Payment method</h3>
                <div class="opts" id="payOpts">
                  <label class="opt"><input type="radio" name="pay" value="venmo" required><span class="ico venmo">V</span><span class="body"><strong>Venmo</strong><small>@theproperpeptides</small></span></label>
                  <label class="opt"><input type="radio" name="pay" value="cashapp" required><span class="ico cashapp">$</span><span class="body"><strong>Cash App</strong><small>$theproperpeptides</small></span></label>
                </div>

                <label class="agree"><input type="checkbox" name="agree" required><span>I confirm I am 18+ and these products are for research use only.</span></label>
                <button class="btn form-continue" type="submit">Continue to Payment <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
              </form>
            </div>

            <div class="step-panel" id="step3" hidden></div>
            <div class="step-panel" id="step4" hidden></div>
          </div>

          <aside class="summary" id="summary">
            <h3>Order Summary</h3>
            <ul class="sum-items" id="sumItems"></ul>
            <div class="line"><span id="sumSubLabel">Subtotal</span><span id="sumSub">$0.00</span></div>
            <div class="line"><span>Shipping</span><span id="sumShip">Select at checkout</span></div>
            <div class="line total"><span>Total</span><span id="sumTotal">$0.00</span></div>
            <div class="actions" id="sumActions"></div>
            <p class="note">Free FedEx shipping on 6 or more boxes. Pay with Venmo or Cash App.</p>
          </aside>
        </div>
      </div>
    </section>
'''
cart_extra = r'''  <script>
    // ---------- Checkout state (survives a reload within the tab) ----------
    const FRESH = () => ({ step: 1, shipId: STORE.shipping[0].id, pay: 'venmo', info: {}, orderNo: null, order: null, sent: false });
    const CK = {
      key: 'pp_checkout',
      state: FRESH(),
      load() { try { Object.assign(this.state, JSON.parse(sessionStorage.getItem(this.key)) || {}); } catch {} },
      save() { try { sessionStorage.setItem(this.key, JSON.stringify(this.state)); } catch {} },
      reset() { try { sessionStorage.removeItem(this.key); } catch {} Object.assign(this.state, FRESH()); }
    };
    const S = CK.state;
    const $ = id => document.getElementById(id);
    const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
    const shipMethod = id => STORE.shipping.find(m => m.id === id) || STORE.shipping[0];
    const payName = p => p === 'cashapp' ? 'Cash App' : 'Venmo';
    const payHandle = p => p === 'cashapp' ? '$' + STORE.cashTag : '@' + STORE.venmoUser;

    // Live totals from the cart (steps 1 to 3). Step 4 uses the saved order snapshot.
    function totals() {
      if (S.step === 4 && S.order) return S.order;
      const items = Cart.items();
      const boxes = items.reduce((n, i) => n + i.qty, 0);
      const subtotal = items.reduce((n, i) => n + i.price * i.qty, 0);
      const shipping = S.step >= 2 ? shippingFor(S.shipId, boxes) : null;
      return { items, boxes, subtotal, shipping, total: subtotal + (shipping || 0) };
    }

    // Snapshot of everything the owner needs, taken when the customer reaches Payment
    function buildOrder() {
      const t = totals(); const m = shipMethod(S.shipId);
      return {
        orderNumber: S.orderNo,
        items: t.items.map(i => ({ id: i.id, name: i.name + ' ' + i.subtitle, sku: i.sku, qty: i.qty, price: i.price, lineTotal: i.price * i.qty })),
        boxes: t.boxes, subtotal: t.subtotal,
        shippingMethod: m.name + ' (' + m.eta + ')', shipping: t.shipping, total: t.total,
        paymentMethod: payName(S.pay) + ' ' + payHandle(S.pay),
        name: S.info.name, email: S.info.email, phone: S.info.phone,
        address: S.info.street + ', ' + S.info.city + ', ' + (S.info.state || '').toUpperCase() + ' ' + S.info.zip,
        placedAt: new Date().toISOString()
      };
    }

    function goto(step) { S.step = step; CK.save(); render(); window.scrollTo({ top: 0, behavior: 'smooth' }); }

    // ---------- Order emails (api/order.js) ----------
    function apiPayload(o, status) {
      return {
        number: o.orderNumber, name: o.name, email: o.email, phone: o.phone, address: o.address,
        street: S.info.street, city: S.info.city, state: (S.info.state || '').toUpperCase(), zip: S.info.zip,
        items: o.items.map(i => `${i.qty} x ${i.name} (SKU ${i.sku}) @ ${money(i.price)} = ${money(i.lineTotal)}`),
        boxes: o.boxes, subtotal: o.subtotal, shipping: o.shipping, shipMethod: o.shippingMethod, total: o.total,
        payment: o.paymentMethod, status
      };
    }
    async function submitOrder(status) {
      const res = await fetch('/api/order', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(apiPayload(S.order, status)) });
      const data = await res.json().catch(() => ({}));
      if (!res.ok || !data.ok) throw new Error(data.error || 'Request failed');
    }
    // Loading state for whichever buttons drive the current step
    function setBusy(selector, busy, label) {
      document.querySelectorAll(selector).forEach(b => {
        if (busy) { b.dataset.label = b.innerHTML; b.innerHTML = label; b.disabled = true; b.classList.add('busy'); }
        else { if (b.dataset.label) b.innerHTML = b.dataset.label; b.disabled = false; b.classList.remove('busy'); }
      });
    }
    let inflight = false;
    // Step 2 -> 3: email the order as "awaiting payment", only advance if it went through
    async function placeOrder() {
      if (inflight) return; inflight = true;
      if (!S.orderNo) S.orderNo = orderNumber();
      S.order = buildOrder(); CK.save();
      setBusy('#sumSubmit, .form-continue', true, 'Submitting order&hellip;');
      try { await submitOrder('awaiting payment'); goto(3); }
      catch (e) { toast('Could not submit order, please try again'); setBusy('#sumSubmit, .form-continue', false); }
      inflight = false;
    }
    // Step 3 -> 4: email again as "customer says paid", then clear the cart
    async function confirmPaid() {
      if (inflight) return; inflight = true;
      setBusy('[data-paid]', true, 'Sending&hellip;');
      try { await submitOrder('customer says paid'); S.sent = true; CK.save(); Cart.clear(); goto(4); }
      catch (e) { toast('Could not submit order, please try again'); setBusy('[data-paid]', false); }
      inflight = false;
    }

    // ---------- Render ----------
    function render() {
      const t = totals();
      if (S.step < 4 && !t.items.length) {
        $('emptyCart').hidden = false; $('checkout').hidden = true;
        $('pageTitle').textContent = 'Your Cart';
        $('steps').querySelectorAll('li').forEach((li, i) => li.className = i === 0 ? 'active' : '');
        return;
      }
      $('emptyCart').hidden = true; $('checkout').hidden = false;
      $('pageTitle').textContent = ['Your Cart', 'Shipping', 'Payment', 'Order Received'][S.step - 1];
      $('steps').querySelectorAll('li').forEach((li, i) => li.className = i + 1 < S.step ? 'done' : i + 1 === S.step ? 'active' : '');
      [1, 2, 3, 4].forEach(n => $('step' + n).hidden = n !== S.step);
      ({ 1: renderCart, 2: renderShipping, 3: renderPayment, 4: renderDone })[S.step]();
      renderSummary(totals());
    }

    function renderCart() {
      const t = totals(); const need = STORE.freeShipQty - t.boxes;
      const unlocked = need <= 0;
      $('shipBanner').className = 'ship-banner' + (unlocked ? ' unlocked' : '');
      $('shipBanner').innerHTML = `
        <div class="txt"><span>${unlocked ? "You've unlocked free FedEx shipping" : `Add ${need} more box${need === 1 ? '' : 'es'} for free FedEx shipping`}</span><small>${t.boxes} of ${STORE.freeShipQty} boxes</small></div>
        <div class="bar"><span style="width:${Math.min(100, t.boxes / STORE.freeShipQty * 100)}%"></span></div>`;
      $('cartList').innerHTML = t.items.map(i => `
        <div class="cart-item ${i.color}">
          <div class="thumb"><img src="${i.image}" alt="${i.name}"></div>
          <div>
            <h3>${i.name} <span style="font-weight:500;color:var(--text-dim);font-size:.85rem">${i.subtitle}</span></h3>
            <div class="meta">${i.count} &bull; ${money(i.price)} per box</div>
            <div class="qty"><button type="button" data-q="${i.id}" data-d="-1" aria-label="Decrease quantity">&minus;</button><span>${i.qty}</span><button type="button" data-q="${i.id}" data-d="1" aria-label="Increase quantity">+</button></div>
            <button type="button" class="remove" data-rm="${i.id}">Remove</button>
          </div>
          <div class="price">${money(i.price * i.qty)}</div>
        </div>`).join('');
    }

    function renderShipping() {
      const t = totals(); const free = t.boxes >= STORE.freeShipQty;
      const f = $('shipForm');
      ['name', 'email', 'phone', 'street', 'city', 'state', 'zip'].forEach(k => { if (S.info[k] != null) f.elements[k].value = S.info[k]; });
      $('shipOpts').innerHTML = STORE.shipping.map(m => `
        <label class="opt ${m.id === S.shipId ? 'selected' : ''}">
          <input type="radio" name="ship" value="${m.id}" ${m.id === S.shipId ? 'checked' : ''} required>
          <span class="body"><strong>${m.name}</strong><small>${m.eta}</small></span>
          <span class="cost ${free ? 'free' : ''}">${free ? 'FREE' : money(m.price)}</span>
        </label>`).join('');
      f.querySelectorAll('input[name=pay]').forEach(r => { r.checked = r.value === S.pay; r.closest('.opt').classList.toggle('selected', r.checked); });
    }

    function renderPayment() {
      const o = S.order; const cash = S.pay === 'cashapp';
      const link = cash ? cashLink(o.total) : venmoLink(o.total, 'Proper Peptides order ' + o.orderNumber);
      $('step3').innerHTML = `
        <div class="panel pay-panel">
          <span class="tag">Order ${o.orderNumber}</span>
          <h3>Send ${money(o.total)} via ${payName(S.pay)}</h3>
          <p>Tap the button to open ${payName(S.pay)} with the amount pre filled${cash ? '' : ' and the order number in the note'}. Please include your order number <strong>${o.orderNumber}</strong> in the payment note so we can match it to your shipment.</p>
          <a class="pay-btn ${cash ? 'cashapp' : 'venmo'}" href="${link}" target="_blank" rel="noopener">Pay ${money(o.total)} with ${payName(S.pay)}</a>
          <div class="pay-manual">
            <div><small>Send to</small><strong>${payHandle(S.pay)}</strong></div>
            <div><small>Amount</small><strong>${money(o.total)}</strong></div>
            <div><small>Note</small><strong>${o.orderNumber}</strong></div>
          </div>
          <p class="muted">On a desktop? Open ${payName(S.pay)} on your phone and send ${money(o.total)} to ${payHandle(S.pay)} with the note ${o.orderNumber}.</p>
          <button type="button" class="btn" data-paid>I've sent the payment</button>
        </div>`;
    }

    function renderDone() {
      const o = S.order;
      $('step4').innerHTML = `
        <div class="panel done-panel">
          <div class="check-mark"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7"/></svg></div>
          <span class="tag">Order ${o.orderNumber}</span>
          <h3>Thanks, ${esc((o.name || '').split(' ')[0])}. Your order is in.</h3>
          <p>Your order details have been emailed to us and a confirmation was sent to <strong>${esc(o.email)}</strong>. Once we confirm your payment we'll ship with FedEx and email your tracking number.</p>
          <p class="muted">Keep your order number handy. Questions? <a href="mailto:${STORE.ownerEmails[0]}">${STORE.ownerEmails[0]}</a></p>
          <div style="margin-top:24px"><a class="btn" href="peptides.html">Continue Shopping</a></div>
        </div>`;
    }

    function renderSummary(t) {
      $('sumItems').innerHTML = t.items.map(i => `<li><span>${i.name} &times; ${i.qty}</span><span>${money(i.price * i.qty)}</span></li>`).join('');
      $('sumSubLabel').textContent = `Subtotal (${t.boxes} box${t.boxes === 1 ? '' : 'es'})`;
      $('sumSub').textContent = money(t.subtotal);
      $('sumShip').textContent = t.shipping == null ? 'Select at checkout' : t.shipping === 0 ? 'FREE' : money(t.shipping);
      $('sumShip').classList.toggle('free', t.shipping === 0);
      $('sumTotal').textContent = money(t.total);
      const next = '<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
      $('sumActions').innerHTML = {
        1: `<button type="button" class="btn" data-go="2">Continue to Shipping ${next}</button>`,
        2: `<button type="button" class="btn" id="sumSubmit">Continue to Payment ${next}</button><button type="button" class="btn outline" data-go="1">Back to Cart</button>`,
        3: `<button type="button" class="btn" data-paid>I've sent the payment</button><button type="button" class="btn outline" data-go="2">Back to Shipping</button>`,
        4: `<a class="btn" href="peptides.html">Continue Shopping</a>`
      }[S.step];
    }

    // ---------- Events ----------
    document.addEventListener('click', e => {
      const q = e.target.closest('[data-q]'); const r = e.target.closest('[data-rm]'); const g = e.target.closest('[data-go]');
      if (q) { const c = Cart.get(); Cart.set(q.dataset.q, (c[q.dataset.q] || 0) + Number(q.dataset.d)); render(); }
      if (r) { Cart.remove(r.dataset.rm); render(); }
      if (g) goto(Number(g.dataset.go));
      if (e.target.closest('[data-paid]')) confirmPaid();
      if (e.target.closest('#sumSubmit')) { const f = $('shipForm'); f.requestSubmit ? f.requestSubmit() : f.querySelector('[type=submit]').click(); }
    });
    $('shipForm').addEventListener('change', e => {
      if (e.target.name === 'ship') { S.shipId = e.target.value; CK.save(); renderSummary(totals()); }
      if (e.target.name === 'pay') { S.pay = e.target.value; CK.save(); }
      if (e.target.type === 'radio') e.target.closest('.opts').querySelectorAll('.opt').forEach(o => o.classList.toggle('selected', o.querySelector('input').checked));
    });
    $('shipForm').addEventListener('submit', e => {
      e.preventDefault();
      const d = new FormData(e.target);
      ['name', 'email', 'phone', 'street', 'city', 'state', 'zip'].forEach(k => S.info[k] = String(d.get(k) || '').trim());
      S.shipId = d.get('ship'); S.pay = d.get('pay'); CK.save();
      placeOrder();
    });

    // ---------- Boot ----------
    CK.load();
    if (S.step === 4 && (!S.order || S.sent)) CK.reset();   // a finished order starts a fresh cart on the next visit
    render();
  </script>'''
page('cart.html', 'Cart', 'Your Proper Peptides cart and checkout. Pay with Venmo or Cash App, free FedEx shipping on 6 or more boxes.', cart, '', cart_extra)
# ---------------- SEO files ----------------
PAGES = ['index.html', 'peptides.html', 'about.html', 'contact.html', 'cart.html']
open('robots.txt', 'w').write('User-agent: *\nAllow: /\n\nSitemap: ' + SITE + '/sitemap.xml\n')
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join('  <url><loc>' + page_url(n) + '</loc></url>\n' for n in PAGES) + '</urlset>\n')
print("built")
