# Proper Peptides

Static site (HTML, CSS, JS) hosted on Vercel. There is no payment processor: customers pay by Venmo or Cash App and the order details are emailed to the owner.

## Pages
- `index.html` Home (landing page)
- `peptides.html` the four thePeptide products with Add to Cart and research details
- `about.html` About thePeptide (manufacturer), Proper Peptides, and the Meet the owner section
- `contact.html` contact form (Formspree)
- `cart.html` cart and 4 step checkout (Cart > Shipping > Payment > Done)

## How checkout works
1. **Cart**: items live in `localStorage`. Adding the same product again increases its quantity. A banner shows progress toward free shipping.
2. **Shipping**: name, email, phone, and address (all required), a FedEx method, a payment method (Venmo or Cash App), and the 18+ / research use checkbox.
3. **Payment**: the site generates an order number (`PP` + 6 characters) and shows a big Venmo or Cash App button that opens the app with the exact total pre filled. Venmo also gets the order number in the note. The customer taps "I've sent the payment".
4. **Done**: confirmation with the order number. The full order (items, quantities, subtotal, shipping, total, payment method, name, address, email, phone) is sent to the owner, then the cart is cleared.

The owner matches the incoming Venmo / Cash App payment to the order number, ships with FedEx, and emails the tracking number.

## Store settings
Everything is at the top of `js/main.js` in the `STORE` object:

| Setting | What it does |
| --- | --- |
| `venmoUser` | Venmo username (`theproperpeptides` = venmo.com/u/theproperpeptides) |
| `cashTag` | Cash App cashtag without the `$` (`theproperpeptides` = cash.app/$theproperpeptides) |
| `orderEmail` | Where orders are emailed (`codyzippe1@gmail.com`) |
| `formspree` | Optional. Paste a real Formspree endpoint and orders POST there as JSON. While it is the `YOUR_FORM_ID` placeholder, the Done step opens a `mailto:` to `orderEmail` with the order in the body instead. |
| `freeShipQty` | Boxes needed for free shipping (6) |
| `shipping` | The FedEx methods and prices: Ground $15 (3 to 5 business days), 2Day $25 (2 business days), Overnight $50 (next business day) |

Helpers next to it: `shippingFor(methodId, qty)` (returns 0 at `freeShipQty` or more boxes), `orderNumber()`, `venmoLink(amount, note)`, `cashLink(amount)`.

## Free shipping rule
Shipping is free on any FedEx method once the cart holds 6 or more boxes (total quantity across all products). Below 6 the selected method's price is added to the subtotal. Total = subtotal + shipping.

## Prices
Set `price` for each product in `js/products.js`. All four are currently $120 per box.

## Before you go live
1. **Logo**: replace `assets/logo.svg` with your real logo.
2. **Headshot**: `assets/cody.jpg` is used on the About page.
3. **Orders by Formspree (optional)**: create a free form at formspree.io and paste the endpoint into `STORE.formspree`. Otherwise orders arrive through the customer's mail app via `mailto:`.
4. **Contact form**: paste your Formspree form ID into the `action` URL in `contact.html` (or in `build.py` and rebuild).
5. **Product images**: currently loaded from thePeptide's S3 bucket. Download them into `assets/` and update `image` in `js/products.js` if you want to self host.

## Deploy
Push to GitHub, then in Vercel: New Project > Import the repo > Deploy. Framework preset: **Other**. No build command or environment variables needed.
Add your domain (properpeptides.com) under Settings > Domains.

## Editing
The HTML pages share a header and footer. Edit `build.py` and run `python3 build.py` to regenerate all pages. Otherwise edit the HTML files directly.
