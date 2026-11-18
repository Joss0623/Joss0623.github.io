# Simengxu Qiao — Academic Homepage

Live site: https://joss0623.github.io/

## Maintain content

Edit `research.json` to update the biography, paper titles, venue/status, summaries, repository links, and display order. One paper maps to one project page and one GitHub repository. CAC is intentionally omitted. SCF uses the ICDE 2027 manuscript version.

```bash
python3 build.py
python3 -m http.server 8765
```

The generated `index.html` and `projects/*/index.html` are committed for buildless GitHub Pages hosting. Assets are local; there are no analytics, trackers, or external font dependencies. Paper links point to author manuscripts or publisher DOI pages. Do not add a publication status, author-contribution marker, or benchmark result without checking its source.

## Structure

- `research.json`: maintained content source.
- `build.py`: static page generator.
- `assets/`: styling, portrait, and method figures.
- `papers/`: available author manuscripts, published with the owner's authorization.
- `projects/`: one generated landing page per paper.

## Attribution

Original layout and implementation by Simengxu Qiao's research portfolio maintenance. The owner provided https://livioni.github.io/, https://dai818.github.io/, and https://lifuguan.github.io/ as academic-homepage references; their source code and text were not copied. Paper figures and manuscripts retain their authors' rights.
