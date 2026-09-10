// Vercel serverless function: creates a Stripe Checkout session from the cart.
// Prices are read from the SAME catalog the site uses (js/products.js) so the
// browser can never send its own price.
//
// Setup:
//   1. In Vercel > Project > Settings > Environment Variables add STRIPE_SECRET_KEY
//   2. npm install (stripe is in package.json)
//   3. Redeploy

const fs = require('fs');
const path = require('path');

function loadProducts() {
  const src = fs.readFileSync(path.join(process.cwd(), 'js', 'products.js'), 'utf8');
  const sandbox = {};
  new Function('exports', src + '\nexports.PRODUCTS = PRODUCTS;')(sandbox);
  return sandbox.PRODUCTS;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  if (!process.env.STRIPE_SECRET_KEY) return res.status(500).json({ error: 'Stripe is not configured yet (missing STRIPE_SECRET_KEY).' });

  const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
  const products = loadProducts();
  const items = (req.body && req.body.items) || [];

  const line_items = items.map(({ id, qty }) => {
    const p = products.find(x => x.id === id);
    if (!p || !p.price || qty < 1) return null;
    return {
      quantity: Math.min(Math.floor(qty), 50),
      price_data: {
        currency: 'usd',
        unit_amount: Math.round(p.price * 100),
        product_data: { name: `${p.name} ${p.subtitle}`, description: `${p.count} • SKU ${p.sku} • Research use only`, images: [p.image] }
      }
    };
  }).filter(Boolean);

  if (!line_items.length) return res.status(400).json({ error: 'Cart is empty or prices are not set.' });

  const origin = `https://${req.headers.host}`;
  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      line_items,
      shipping_address_collection: { allowed_countries: ['US'] },
      success_url: `${origin}/success.html`,
      cancel_url: `${origin}/cart.html`,
      custom_text: { submit: { message: 'Products are for research use only and not for human consumption.' } }
    });
    res.status(200).json({ url: session.url });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
