# Wyzestock marketing site

www.wyzestock.co.za. Same look and feel as www.wyzesales.com (AppWyze/wyzesales-marketing).

- Static HTML, hosted on Netlify (publish directory: the repo root, no build command).
- Every page is generated from one layout: edit `_build/build.py` (text) or `_build/site.css` (styles), then run
  `python3 _build/build.py` and commit the regenerated `index.html` files.
- Screenshots in `images/` come from the Fynbos Hill Vineyards demo company (100% made-up data).
- The contact form posts to the Wyzestock Supabase Edge Function `send-contact-email`, which emails support@wyzestock.co.za.
