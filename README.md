# Proper Peptides

Static site (HTML, CSS, JS) hosted on Vercel, plus one serverless function (`api/order.js`) that emails each order through [Resend](https://resend.com). There is no payment processor: customers pay by Venmo or Cash App and the order details are emailed to the owner automatically.

## Pages
- `index.html` Home (landing page)
- `peptides.html` the four thePeptide products with Add to Cart and research details
- `about.html` About thePeptide (manufacturer), Proper Peptides, and the Meet the owner section
- `contact.html` contact form (Formspree)
- `cart.html` cart and 4 step checkout (Cart > Shipping > Payment > Done)

## How checkout works
1. **Cart**: items live in `localStorage`. Adding the same product again increases its quantity. A banner shows progress toward free shipping.
2. **Shipping**: name, email, phone, and address (all required), a FedEx method, a payment method (Venmo or Cash App), and the 18+ / research use checkbox.
3. **Payment**: when the customer taps Continue to Payment the site generates an order number (`PP` + 6 characters) and POSTs the order to `/api/order` with status **awaiting payment**. If that request fails a toast asks them to try again and they stay on step 2. On success they see a big Venmo or Cash App button that opens the app with the exact total pre filled (Venmo also gets the order number in the note). The customer taps "I've sent the payment".
4. **Done**: the order is POSTed again with status **customer says paid**, the cart is cleared, and the customer sees the confirmation.

Each POST sends two emails through Resend: a full order email to **properpeptide@gmail.com and codyzippe1@gmail.com** (subject `Proper Peptides order PPXXXXXX - <status> - <payment> $<total>`, reply-to set to the customer) and a short "We received your order" confirmation to the customer with the same summary and a reminder to put the order number in their Venmo / Cash App note. So you get one email when the order is placed and another when the customer says they paid. The owner matches the incoming Venmo / Cash App payment to the order number, ships with FedEx, and emails the tracking number.

## Order email setup (Resend)
1. Create a free account at [resend.com](https://resend.com).
2. In Resend go to **Domains > Add Domain** and enter `theproperpeptide.com`. Resend shows a few DNS records (DKIM, SPF, and a return path). Add each one in **Vercel > your project > Domains > theproperpeptide.com > DNS Records** (or wherever the domain's DNS is managed), then click **Verify** in Resend.
3. In Resend go to **API Keys > Create API Key** (sending access is enough) and copy the key.
4. In **Vercel > Project > Settings > Environment Variables** add:
   - `RESEND_API_KEY` = the key from step 3 (required)
   - `ORDER_FROM` = the From address, for example `Proper Peptides Orders <orders@theproperpeptide.com>`. It **must** be an address on the verified theproperpeptide.com domain, so set this. (The code default is `orders@properpeptides.com`, which will not send.)
5. **Redeploy** the project so the function picks up the variables.

Until the domain is verified, Resend will only deliver to the email address on your Resend account and anything else is rejected, so verify the domain before going live. The API key is only ever read by the serverless function; the browser never sees it.

To test locally: `npm install`, then `vercel dev` with `RESEND_API_KEY` in a local `.env` file (already git ignored). The function returns `{ "ok": true }` or `{ "ok": false, "error": "..." }`.

## Store settings
Everything is at the top of `js/main.js` in the `STORE` object:

| Setting | What it does |
| --- | --- |
| `venmoUser` | Venmo username (`theproperpeptides` = venmo.com/u/theproperpeptides) |
| `cashTag` | Cash App cashtag without the `$` (`theproperpeptides` = cash.app/$theproperpeptides) |
| `ownerEmails` | Shown on the site for display only. The addresses that actually receive orders are set in `api/order.js`. |
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
3. **Order emails**: follow the Resend setup above and add `RESEND_API_KEY` in Vercel.
4. **Contact form**: paste your Formspree form ID into the `action` URL in `contact.html` (or in `build.py` and rebuild).
5. **Product images**: currently loaded from thePeptide's S3 bucket. Download them into `assets/` and update `image` in `js/products.js` if you want to self host.

## Deploy
Push to GitHub, then in Vercel: New Project > Import the repo > Deploy. Framework preset: **Other**. No build command needed. Add the `RESEND_API_KEY` environment variable (see above) so order emails work.
Add your domain (theproperpeptide.com) under Settings > Domains.

## Editing
The HTML pages share a header and footer. Edit `build.py` and run `python3 build.py` to regenerate all pages. Otherwise edit the HTML files directly.
