# pyhroff.github.io

Source of my portfolio site, served by GitHub Pages at <https://pyhroff.github.io>.

It is a static page (`index.html`, Tailwind via CDN), `resume.pdf`, a blog note and a browser playground. Every number on the page links to the repository or pull request it comes from; upstream pull-request statuses are dated on the page.

## Run locally

```bash
python -m http.server 8000
# open http://localhost:8000
```

## Update

Edit `index.html`, keep the counts in the hero, the upstream table and the meta descriptions in sync, and push to the default branch; GitHub Pages redeploys automatically.

## Resume

`resume.pdf` is generated from `resume/resume.html` (A4, one page, single column, selectable text for applicant-tracking systems). To regenerate it, render the HTML to PDF from Chromium, for example with Playwright:
`page.pdf({ format: "A4", preferCSSPageSize: true })`.

## Playground

`playground/` runs the structural tool-poisoning detector from [aisec-suite](https://github.com/Pyhroff/aisec-suite) in the browser with Pyodide (loaded from the jsDelivr CDN), so no server or build step is needed.

- `poison.py` is a vendored copy of `aisec/poison.py`; refresh it with `python playground/sync_detector.py`.
- `glue.py` is the small adapter the page calls; `examples.json` holds the examples, including one the detector misses.
- `python -m pytest playground` checks that each example gives the result the page claims (CI runs this).
