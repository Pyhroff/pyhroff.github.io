# pyhroff.github.io

Source of my portfolio site, served by GitHub Pages at <https://pyhroff.github.io>.

It is a single static page (`index.html`, Tailwind via CDN) plus `resume.pdf`. Every number on the page links to the repository or pull request it comes from; upstream pull-request statuses are dated on the page.

## Run locally

```bash
python -m http.server 8000
# open http://localhost:8000
```

## Update

Edit `index.html`, keep the counts in the hero, the upstream table and the meta descriptions in sync, and push to the default branch; GitHub Pages redeploys automatically.
