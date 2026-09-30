# SideFi — Monthly Spending Dashboard

A single-file personal finance dashboard: monthly and yearly spending views,
category breakdowns with per-transaction drill-down, income tracking, and a net
spending trend chart. Pure HTML/CSS/JS, no build step, no backend — open
`index.html` in a browser.

## What's in this repo

- `index.html` — the dashboard, running entirely on **sample data**
  (Jul–Sep 2026, fictional merchants and amounts).
- `build_sample.py` — the sanitizer that generates `index.html` from the
  private dashboard export. It swaps in coherent fake transactions, removes
  hardcoded copy tied to real data (takeaways, chart annotations, peak
  markers), and asserts no real-data fingerprints ship.

## Sample data only

This repository intentionally contains **no real financial records**. Account
labels, merchants, amounts, and narratives are fictional. The live dashboard
with real data is private and is never pushed here.

## Updating

Whenever the private dashboard changes, regenerate and push:

```sh
python3 build_sample.py   # rebuilds index.html from the latest export
```

Then commit and push. The sanitizer fails loudly if a real-data fingerprint
is detected in the output.

## License

MIT — see [LICENSE](LICENSE).
