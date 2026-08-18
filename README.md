# Levelap Games landing page

A concise English-language studio and games showcase based on the Levelap Games
pitch deck. Static HTML/CSS/JS — no build step. Published with GitHub Pages at
[levelapgames.pp.ua](https://levelapgames.pp.ua/).

## Structure

- `index.html` - page content and metadata
- `styles.css` - visual design, responsive layout, mobile navigation
- `script.js` - scroll progress indicator and mobile menu
- `assets/` - game artwork from the pitch deck
- `assets/icons/` - favicon set and web app manifest
- `CNAME`, `.nojekyll`, `robots.txt`, `sitemap.xml` - GitHub Pages / SEO

Open the folder with any static web server, e.g.:

```
python -m http.server 8080
```

Opening `index.html` straight from disk works too, but a server matches production.

## Notes

- Social preview is `assets/og.jpg` (1200x631). Open Graph tags use absolute
  URLs, which link scrapers require - keep them absolute if the domain changes.
- `assets/banana-yellow.jpg` is the source art for the brand mark. Both the
  favicon set and the header logo (`assets/logo-banana.png`) are generated
  from it with the same 88% centre crop, so the tab icon and the header
  show an identical mark. Rounding comes from CSS, not from the file.
- Deployment: GitHub Pages, branch `main`, folder `/ (root)`. The `CNAME` file
  holds the custom domain, so keep it in the repository.
