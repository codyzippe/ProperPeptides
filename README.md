# Proper Peptides

Static site (HTML, CSS, JS) plus one Vercel serverless function for Stripe checkout.

## Pages
- `index.html` Home (landing page)
- `peptides.html` the four thePeptide products with Add to Cart and research details
- `about.html` About thePeptide (manufacturer) and Proper Peptides
- `contact.html` contact form (Formspree)
- `cart.html` cart and checkout
- `success.html` post payment thank you

## Before you go live
1. **Logo**: replace `assets/logo.svg` with your real logo (or update the `<img src>` in each page).
2. **Prices**: open `js/products.js` and set `price` for each product (currently 0, which shows "Contact for price" and blocks Add to Cart).
3. **Stripe**: in Vercel, add environment variable `STRIPE_SECRET_KEY` (from dashboard.stripe.com > Developers > API keys). Use the test key first, then the live key.
4. **Contact form**: create a free form at formspree.io and paste the form ID into the `action` URL in `contact.html`.
5. **Product images**: currently loaded from thePeptide's S3 bucket. Download them into `assets/` and update `image` in `js/products.js` if you want to self host.

## Deploy
```
git init
git add .
git commit -m "Proper Peptides site"
# create a repo on GitHub, then:
git remote add origin https://github.com/YOUR_USER/properpeptides.git
git push -u origin main
```
Then in Vercel: New Project > Import the repo > Deploy. Framework preset: **Other**. No build command needed.
Add your domain (properpeptides.com) under Settings > Domains.

## Editing
The HTML pages share a header and footer. If you want to change those in one place, edit `build.py` and run `python3 build.py` to regenerate the pages. Otherwise just edit the HTML files directly.
