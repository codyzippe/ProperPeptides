// Vercel serverless function: emails a new order to the owner and a confirmation to the customer.
// Uses Resend (https://resend.com). The API key lives only in the RESEND_API_KEY environment
// variable on Vercel and is never sent to the browser.
//
// POST /api/order  (JSON)
//   number, name, email, phone, address, items (array of strings), boxes, subtotal,
//   shipping, shipMethod, total, payment, status ("awaiting payment" | "customer says paid")
//   optional: street, city, state, zip (shown broken out in the shipping block when present)
// Responds { ok: true } or { ok: false, error }.

const { Resend } = require('resend');

const OWNER_EMAILS = ['properpeptide@gmail.com', 'codyzippe1@gmail.com'];
const DEFAULT_FROM = 'Proper Peptides Orders <orders@properpeptides.com>';
const STATUSES = ['awaiting payment', 'customer says paid'];
const MAX_LEN = 300;

// ---------- Validation ----------
function str(v) { return typeof v === 'string' ? v.trim().slice(0, MAX_LEN) : ''; }
function num(v) { const n = Number(v); return Number.isFinite(n) && n >= 0 ? Math.round(n * 100) / 100 : null; }

function validate(body) {
  const o = {
    number: str(body.number), name: str(body.name), email: str(body.email), phone: str(body.phone),
    address: str(body.address), street: str(body.street), city: str(body.city), state: str(body.state), zip: str(body.zip),
    shipMethod: str(body.shipMethod), payment: str(body.payment), status: str(body.status).toLowerCase(),
    boxes: num(body.boxes), subtotal: num(body.subtotal), shipping: num(body.shipping), total: num(body.total),
    items: Array.isArray(body.items) ? body.items.filter(i => typeof i === 'string').map(i => i.trim().slice(0, MAX_LEN)).filter(Boolean).slice(0, 50) : []
  };
  const missing = ['number', 'name', 'email', 'phone', 'address', 'shipMethod', 'payment'].filter(k => !o[k]);
  ['boxes', 'subtotal', 'shipping', 'total'].forEach(k => { if (o[k] === null) missing.push(k); });
  if (!o.items.length) missing.push('items');
  if (missing.length) return { error: 'Missing or invalid: ' + missing.join(', ') };
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(o.email)) return { error: 'Invalid email address' };
  if (!STATUSES.includes(o.status)) return { error: 'status must be "awaiting payment" or "customer says paid"' };
  if (o.boxes < 1 || !Number.isInteger(o.boxes)) return { error: 'boxes must be a whole number of 1 or more' };
  return { order: o };
}

// ---------- Email formatting ----------
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const money = n => '$' + Number(n).toFixed(2);
const pacificNow = () => new Date().toLocaleString('en-US', { timeZone: 'America/Los_Angeles', dateStyle: 'medium', timeStyle: 'short' }) + ' PT';

function summaryRows(o, when) {
  const shipBlock = o.street && o.city && o.state && o.zip
    ? [['Name', o.name], ['Street address', o.street], ['City', o.city], ['State', o.state.toUpperCase()], ['ZIP', o.zip]]
    : [['Name', o.name], ['Address', o.address]];
  return {
    order: [['Order number', o.number], ['Status', o.status.toUpperCase()], ['Date / time', when],
            ['Payment method', o.payment], ['Amount to look for', money(o.total)]],
    items: o.items,
    totals: [['Boxes', String(o.boxes)], ['Subtotal', money(o.subtotal)],
             ['Shipping', o.shipMethod + ' ' + (o.shipping === 0 ? 'FREE' : money(o.shipping))], ['Total', money(o.total)]],
    shipping: [...shipBlock, ['Phone', o.phone], ['Email', o.email]]
  };
}

function htmlTable(title, rows) {
  const tr = rows.map(([k, v], i) => `
    <tr style="background:${i % 2 ? '#f6f8fb' : '#ffffff'}">
      <td style="padding:10px 12px;color:#5b6b82;font-size:14px;white-space:nowrap;vertical-align:top;border-bottom:1px solid #e6eaf0">${esc(k)}</td>
      <td style="padding:10px 12px;color:#0d1626;font-size:15px;font-weight:600;vertical-align:top;border-bottom:1px solid #e6eaf0">${esc(v)}</td>
    </tr>`).join('');
  return `
    <h3 style="font:700 14px/1.3 Poppins,Arial,sans-serif;color:#4a7fd6;letter-spacing:.06em;text-transform:uppercase;margin:24px 0 8px">${esc(title)}</h3>
    <table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse;border:1px solid #e6eaf0;border-radius:10px;overflow:hidden">${tr}</table>`;
}
function htmlItems(items) {
  const li = items.map((it, i) => `
    <tr style="background:${i % 2 ? '#f6f8fb' : '#ffffff'}">
      <td style="padding:10px 12px;color:#0d1626;font-size:15px;font-weight:600;border-bottom:1px solid #e6eaf0">${esc(it)}</td>
    </tr>`).join('');
  return `
    <h3 style="font:700 14px/1.3 Poppins,Arial,sans-serif;color:#4a7fd6;letter-spacing:.06em;text-transform:uppercase;margin:24px 0 8px">Items</h3>
    <table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse;border:1px solid #e6eaf0;border-radius:10px;overflow:hidden">${li}</table>`;
}
function wrap(heading, intro, inner) {
  return `<!DOCTYPE html><html><body style="margin:0;padding:0;background:#eef2f7">
  <div style="max-width:560px;margin:0 auto;padding:24px 14px;font-family:Inter,Arial,sans-serif">
    <div style="background:#ffffff;border-radius:16px;padding:24px 20px">
      <p style="margin:0 0 4px;font:700 12px/1.3 Poppins,Arial,sans-serif;color:#4a7fd6;letter-spacing:.08em;text-transform:uppercase">Proper Peptides</p>
      <h1 style="margin:0 0 8px;font:800 22px/1.25 Poppins,Arial,sans-serif;color:#0d1626">${esc(heading)}</h1>
      ${intro ? `<p style="margin:0 0 6px;color:#3b4a61;font-size:15px;line-height:1.55">${intro}</p>` : ''}
      ${inner}
    </div>
    <p style="margin:16px 0 0;color:#7a879a;font-size:12px;text-align:center">Research use only. Proper Peptides, authorized reseller of thePeptide.</p>
  </div></body></html>`;
}
function textVersion(heading, r) {
  const line = ([k, v]) => `${k}: ${v}`;
  return [heading, '', ...r.order.map(line), '', 'ITEMS', ...r.items.map(i => ' - ' + i), '', ...r.totals.map(line), '', 'SHIP TO', ...r.shipping.map(line)].join('\n');
}

function ownerEmail(o, when) {
  const r = summaryRows(o, when);
  const heading = `Order ${o.number} - ${o.status}`;
  const html = wrap(heading, `Look for <strong>${esc(money(o.total))}</strong> via <strong>${esc(o.payment)}</strong> with note <strong>${esc(o.number)}</strong>.`,
    htmlTable('Order', r.order) + htmlItems(r.items) + htmlTable('Totals', r.totals) + htmlTable('Ship to', r.shipping));
  return { subject: `Proper Peptides order ${o.number} - ${o.status} - ${o.payment} ${money(o.total)}`, html, text: textVersion(heading, r) };
}
function customerEmail(o, when) {
  const r = summaryRows(o, when);
  const heading = `We received your order ${o.number}`;
  const intro = `Thanks, ${esc(o.name.split(' ')[0])}. Please send <strong>${esc(money(o.total))}</strong> via <strong>${esc(o.payment)}</strong> and include your order number <strong>${esc(o.number)}</strong> in the payment note. Once we confirm your payment we'll ship with FedEx and email your tracking number.`;
  const html = wrap(heading, intro, htmlTable('Order', r.order) + htmlItems(r.items) + htmlTable('Totals', r.totals) + htmlTable('Ship to', r.shipping));
  return { subject: heading, html, text: textVersion(heading, r) + `\n\nPlease include ${o.number} in your ${o.payment} note.` };
}

// ---------- Handler ----------
module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method not allowed' });
  if (!process.env.RESEND_API_KEY) return res.status(500).json({ ok: false, error: 'Email is not configured (missing RESEND_API_KEY).' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = null; } }
  if (!body || typeof body !== 'object') return res.status(400).json({ ok: false, error: 'Invalid JSON body' });

  const { order, error } = validate(body);
  if (error) return res.status(400).json({ ok: false, error });

  const resend = new Resend(process.env.RESEND_API_KEY);
  const from = process.env.ORDER_FROM || DEFAULT_FROM;
  const when = pacificNow();

  // Owner email first: this one must succeed.
  const own = ownerEmail(order, when);
  const sent = await resend.emails.send({ from, to: OWNER_EMAILS, replyTo: order.email, subject: own.subject, html: own.html, text: own.text });
  if (sent.error) {
    console.error('Owner email failed', sent.error);
    return res.status(502).json({ ok: false, error: sent.error.message || 'Could not send order email' });
  }

  // Customer confirmation: best effort.
  try {
    const cust = customerEmail(order, when);
    const c = await resend.emails.send({ from, to: order.email, replyTo: OWNER_EMAILS[0], subject: cust.subject, html: cust.html, text: cust.text });
    if (c.error) console.error('Customer email failed', c.error);
  } catch (e) {
    console.error('Customer email failed', e);
  }

  return res.status(200).json({ ok: true });
};
