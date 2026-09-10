# Generates the HTML pages from a shared shell so header/footer stay identical.
import os
HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Proper Peptides</title>
  <meta name="description" content="{desc}">
  <link rel="icon" href="assets/logo.svg">
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
            <li>Research Use Only</li>
          </ul>
        </div>
      </div>
      <div class="foot-bottom">
        <p>&copy; 2026 Proper Peptides. All rights reserved. For research purposes only.</p>
        <p>Products manufactured for thePeptide</p>
      </div>
    </div>
  </footer>

  <script src="js/products.js"></script>
  <script src="js/main.js"></script>
{extra}
</body>
</html>
'''

def page(name, title, desc, body, current, extra='', ticker=False):
    cur = {k: (' aria-current="page"' if k == current else '') for k in ['home','pep','about','contact']}
    html = HEAD.format(title=title, desc=desc, ticker=(TICKER if ticker else ''), c_home=cur['home'], c_pep=cur['pep'], c_about=cur['about'], c_contact=cur['contact']) + body + FOOT.format(extra=extra)
    open(name, 'w').write(html)

# ---------------- HOME ----------------
home = '''
    <section class="hero">
      <div class="wrap">
        <div>
          <span class="eyebrow">Lab Tested &bull; 99%+ Purity Guaranteed</span>
          <h1>Unlock Peak Performance with <span>Proper Peptides</span></h1>
          <p class="sub">Premium research grade peptide compounds from thePeptide, designed for laboratory research and scientific study. Four rigorously tested blends, ready to ship.</p>
          <div class="hero-actions">
            <a class="btn" href="peptides.html">Browse Peptides <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
            <a class="btn outline" href="about.html">About thePeptide</a>
          </div>
          <div class="trust">
            <span><i><svg viewBox="0 0 24 24"><path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.5"/><circle cx="17" cy="18" r="1.5"/></svg></i>Fast Shipping</span>
            <span><i><svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg></i>Lab Verified</span>
            <span><i><svg viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg></i>Secure Checkout</span>
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
page('index.html', 'Premium Research Peptides', 'Proper Peptides: authorized reseller of thePeptide lab tested research peptides. GLOW, Wolverine, NAD+, CJC-1295/Ipamorelin.', home, 'home', home_extra, ticker=True)

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
            <p style="margin-top:12px"><strong>Email</strong><br><a href="mailto:properpeptide@gmail.com">properpeptide@gmail.com</a></p>
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
page('contact.html', 'Contact', 'Contact Proper Peptides.', contact, 'contact')

# ---------------- CART ----------------
cart = '''
    <section class="page-hero">
      <div class="wrap"><h1>Your Cart</h1></div>
    </section>
    <section style="padding-top:10px">
      <div class="wrap">
        <div class="cart-layout">
          <div class="cart-list" id="cartList"></div>
          <aside class="summary" id="summary">
            <h3>Order Summary</h3>
            <div class="line"><span>Subtotal</span><span id="sumSub">$0.00</span></div>
            <div class="line"><span>Shipping</span><span>Calculated at checkout</span></div>
            <div class="line total"><span>Total</span><span id="sumTotal">$0.00</span></div>
            <button class="btn" id="checkoutBtn">Checkout <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
            <p class="note">Secure payment via Stripe. Research use only.</p>
          </aside>
        </div>
      </div>
    </section>
'''
cart_extra = '''  <script>
    function renderCart() {
      const list = document.getElementById('cartList');
      const items = Cart.items();
      if (!items.length) {
        list.innerHTML = '<div class="empty"><h3>Your cart is empty</h3><p style="margin:10px 0 20px">Browse the four thePeptide research blends.</p><a class="btn" href="peptides.html">Shop Peptides</a></div>';
        document.getElementById('summary').style.display = 'none';
        return;
      }
      document.getElementById('summary').style.display = '';
      list.innerHTML = items.map(i => `
        <div class="cart-item ${i.color}">
          <div class="thumb"><img src="${i.image}" alt="${i.name}"></div>
          <div>
            <h3>${i.name} <span style="font-weight:500;color:var(--text-dim);font-size:.85rem">${i.subtitle}</span></h3>
            <div class="meta">${i.count} &bull; ${money(i.price)} each</div>
            <div class="qty"><button data-q="${i.id}" data-d="-1">&minus;</button><span>${i.qty}</span><button data-q="${i.id}" data-d="1">+</button></div>
            <button class="remove" data-rm="${i.id}">Remove</button>
          </div>
          <div class="price">${money(i.price * i.qty)}</div>
        </div>`).join('');
      const sub = Cart.subtotal();
      document.getElementById('sumSub').textContent = money(sub);
      document.getElementById('sumTotal').textContent = money(sub);
    }
    document.addEventListener('click', e => {
      const q = e.target.closest('[data-q]'); const r = e.target.closest('[data-rm]');
      if (q) { const c = Cart.get(); Cart.set(q.dataset.q, (c[q.dataset.q] || 0) + Number(q.dataset.d)); renderCart(); }
      if (r) { Cart.remove(r.dataset.rm); renderCart(); }
    });
    document.getElementById('checkoutBtn').addEventListener('click', async () => {
      const btn = document.getElementById('checkoutBtn');
      btn.disabled = true; btn.textContent = 'Redirecting to secure checkout...';
      try {
        const res = await fetch('/api/checkout', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ items: Cart.items().map(i => ({ id: i.id, qty: i.qty })) })
        });
        const data = await res.json();
        if (data.url) window.location.href = data.url;
        else throw new Error(data.error || 'Checkout failed');
      } catch (err) {
        toast(err.message);
        btn.disabled = false; btn.textContent = 'Checkout';
      }
    });
    renderCart();
  </script>'''
page('cart.html', 'Cart', 'Your Proper Peptides cart.', cart, '', cart_extra)

# ---------------- SUCCESS ----------------
success = '''
    <section>
      <div class="wrap center" style="max-width:640px">
        <div class="eyebrow">Order received</div>
        <h1>Thank you for your order</h1>
        <p class="sub" style="margin-top:16px">Your payment went through. You'll get a receipt by email from Stripe and a tracking number once your order ships.</p>
        <div style="margin-top:28px"><a class="btn" href="peptides.html">Continue Shopping</a></div>
      </div>
    </section>
'''
page('success.html', 'Order Complete', 'Thanks for your order.', success, '', '  <script>Cart.clear();</script>')
print("built")
