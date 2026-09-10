/* =========================================================
   Proper Peptides  |  shared behaviour
   Age gate, mobile nav, cart (localStorage), toast, helpers
   ========================================================= */

// ---------- Store settings (edit these) ----------
const STORE = {
  venmoUser: "theproperpeptides",                 // https://www.venmo.com/u/theproperpeptides
  cashTag: "theproperpeptides",                   // https://cash.app/$theproperpeptides
  ownerEmails: ["properpeptide@gmail.com", "codyzippe1@gmail.com"], // display only; orders are emailed by api/order.js
  freeShipQty: 6,                                 // boxes needed for free FedEx shipping
  shipping: [
    { id: "ground",    name: "FedEx Ground",    price: 15, eta: "3 to 5 business days" },
    { id: "2day",      name: "FedEx 2Day",      price: 25, eta: "2 business days" },
    { id: "overnight", name: "FedEx Overnight", price: 50, eta: "Next business day" }
  ]
};

// Shipping cost for a method id and box count (free at STORE.freeShipQty or more)
function shippingFor(methodId, qty) {
  const m = STORE.shipping.find(x => x.id === methodId);
  if (!m) return 0;
  return qty >= STORE.freeShipQty ? 0 : m.price;
}

// Order id like PP7K2Q9X (PP + 6 uppercase chars)
function orderNumber() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let id = 'PP';
  for (let i = 0; i < 6; i++) id += chars[Math.floor(Math.random() * chars.length)];
  return id;
}

// Payment deep links with the amount pre filled
function venmoLink(amount, note) {
  return 'https://venmo.com/' + STORE.venmoUser + '?txn=pay&amount=' + Number(amount).toFixed(2) + '&note=' + encodeURIComponent(note);
}
function cashLink(amount) {
  return 'https://cash.app/$' + STORE.cashTag + '/' + Number(amount).toFixed(2);
}

// ---------- Age gate ----------
(function ageGate() {
  const gate = document.getElementById('ageGate');
  if (!gate) return;
  if (localStorage.getItem('pp_age_ok') === '1') { gate.hidden = true; return; }
  document.body.style.overflow = 'hidden';
  gate.querySelector('.yes').addEventListener('click', () => {
    localStorage.setItem('pp_age_ok', '1');
    gate.hidden = true;
    document.body.style.overflow = '';
  });
  gate.querySelector('.no').addEventListener('click', () => {
    window.location.href = 'https://www.google.com';
  });
})();

// ---------- Mobile nav ----------
(function nav() {
  const btn = document.getElementById('navToggle');
  const nav = document.getElementById('mainNav');
  if (!btn || !nav) return;
  btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
})();

// ---------- Toast ----------
function toast(msg, ms = 2200) {
  let t = document.querySelector('.toast');
  if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); }
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._h);
  t._h = setTimeout(() => t.classList.remove('show'), ms);
}

// ---------- Cart ----------
// Items live in localStorage under pp_cart. A 5 minute reservation timer (pp_cart_started)
// starts when the first item lands in an empty cart, is untouched by later adds/removes,
// clears with the cart, pauses once the customer reaches the payment step, and empties
// the cart when it runs out.
const Cart = {
  key: 'pp_cart',
  timerKey: 'pp_cart_started',
  ttl: 5 * 60 * 1000,
  get() { try { return JSON.parse(localStorage.getItem(this.key)) || {}; } catch { return {}; } },
  save(c) { localStorage.setItem(this.key, JSON.stringify(c)); this.syncTimer(); this.badge(); this.tick(); },
  add(id, qty = 1) { const c = this.get(); c[id] = (c[id] || 0) + qty; this.save(c); },
  set(id, qty) { const c = this.get(); if (qty <= 0) delete c[id]; else c[id] = qty; this.save(c); },
  remove(id) { const c = this.get(); delete c[id]; this.save(c); },
  clear() { localStorage.removeItem(this.key); localStorage.removeItem(this.timerKey); this.badge(); this.tick(); },
  count() { return Object.values(this.get()).reduce((a, b) => a + b, 0); },
  items() {
    const c = this.get();
    return Object.keys(c).map(id => ({ ...PRODUCTS.find(p => p.id === id), qty: c[id] })).filter(i => i.id);
  },
  subtotal() { return this.items().reduce((s, i) => s + i.price * i.qty, 0); },
  badge() {
    document.querySelectorAll('.cart-count').forEach(el => {
      const n = this.count();
      el.textContent = n;
      el.style.display = n ? 'grid' : 'none';
    });
  },

  // ---- Reservation countdown ----
  startedAt() { const t = Number(localStorage.getItem(this.timerKey)); return t > 0 ? t : null; },
  remaining() { const t = this.startedAt(); return t ? Math.max(0, t + this.ttl - Date.now()) : null; },
  // Payment step or later in this tab: the customer is already checking out
  checkingOut() { try { return ((JSON.parse(sessionStorage.getItem('pp_checkout')) || {}).step || 1) >= 3; } catch { return false; } },
  // Start on the first item, clear when empty, never reset while running
  syncTimer() {
    if (!this.count()) localStorage.removeItem(this.timerKey);
    else if (!this.startedAt()) localStorage.setItem(this.timerKey, String(Date.now()));
  },
  tick() {
    if (this.checkingOut()) { localStorage.removeItem(this.timerKey); this.renderTimer(null); return; }
    this.syncTimer();
    const ms = this.remaining();
    if (ms === 0) { this.expire(); return; }
    this.renderTimer(ms);
  },
  expire() {
    localStorage.removeItem(this.key); localStorage.removeItem(this.timerKey);
    this.badge(); this.renderTimer(null);
    toast('Your cart expired and was cleared. Add your items again to keep shopping.', 5000);
    document.dispatchEvent(new CustomEvent('cart:expired'));
  },
  fmt(ms) { const s = Math.ceil(ms / 1000); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); },
  renderTimer(ms) {
    const urgent = ms != null && ms < 60000;
    // header badge next to the cart icon
    let b = document.querySelector('.cart-timer');
    if (ms == null) { if (b) b.remove(); }
    else {
      if (!b) {
        const cartBtn = document.querySelector('.cart-btn');
        if (cartBtn) { b = document.createElement('a'); b.className = 'cart-timer'; b.href = 'cart.html'; cartBtn.parentNode.insertBefore(b, cartBtn); }
      }
      if (b) { b.innerHTML = '<span>Cart reserved for</span> <b>' + this.fmt(ms) + '</b>'; b.classList.toggle('urgent', urgent); }
    }
    // full width banner on the cart page
    const ban = document.getElementById('cartTimerBanner');
    if (!ban) return;
    ban.hidden = ms == null;
    if (ms == null) return;
    ban.classList.toggle('urgent', urgent);
    ban.innerHTML = urgent
      ? '<strong>Cart expires in ' + this.fmt(ms) + '</strong><span>Check out now to keep your items.</span>'
      : '<strong>Cart reserved for ' + this.fmt(ms) + '</strong><span>Check out before the timer ends to keep your items.</span>';
  }
};
setInterval(() => Cart.tick(), 1000);

function money(n) { return '$' + Number(n).toFixed(2); }

// Buttons anywhere with data-add="productId"
document.addEventListener('click', e => {
  const b = e.target.closest('[data-add]');
  if (!b) return;
  const p = PRODUCTS.find(x => x.id === b.dataset.add);
  if (!p) return;
  if (!p.price) { toast('Price not set yet. Contact us to order.'); return; }
  Cart.add(p.id, 1);
  toast(p.name + ' added to cart');
});

document.addEventListener('DOMContentLoaded', () => { Cart.badge(); Cart.tick(); });

// ---------- Helpers used by pages ----------
function tileHTML(p) {
  return `<a class="tile ${p.color}" href="peptides.html#${p.id}">
    <img src="${p.image}" alt="${p.name} ${p.subtitle}">
    <span>${p.name === 'CJC-1295' ? 'CJC 1295' : p.name.charAt(0) + p.name.slice(1).toLowerCase()}</span>
  </a>`;
}
