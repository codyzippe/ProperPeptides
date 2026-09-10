/* =========================================================
   Proper Peptides  |  shared behaviour
   Age gate, mobile nav, cart (localStorage), toast, helpers
   ========================================================= */

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
function toast(msg) {
  let t = document.querySelector('.toast');
  if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); }
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._h);
  t._h = setTimeout(() => t.classList.remove('show'), 2200);
}

// ---------- Cart ----------
const Cart = {
  key: 'pp_cart',
  get() { try { return JSON.parse(localStorage.getItem(this.key)) || {}; } catch { return {}; } },
  save(c) { localStorage.setItem(this.key, JSON.stringify(c)); this.badge(); },
  add(id, qty = 1) { const c = this.get(); c[id] = (c[id] || 0) + qty; this.save(c); },
  set(id, qty) { const c = this.get(); if (qty <= 0) delete c[id]; else c[id] = qty; this.save(c); },
  remove(id) { const c = this.get(); delete c[id]; this.save(c); },
  clear() { localStorage.removeItem(this.key); this.badge(); },
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
  }
};

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

document.addEventListener('DOMContentLoaded', () => Cart.badge());

// ---------- Helpers used by pages ----------
function tileHTML(p) {
  return `<a class="tile ${p.color}" href="peptides.html#${p.id}">
    <img src="${p.image}" alt="${p.name} ${p.subtitle}">
    <span>${p.name === 'CJC-1295' ? 'CJC 1295' : p.name.charAt(0) + p.name.slice(1).toLowerCase()}</span>
  </a>`;
}
