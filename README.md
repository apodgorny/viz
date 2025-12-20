# Viz

Lightweight helper to render numeric series plus text “info” columns into an interactive Plotly chart, served by a minimal FastAPI/uvicorn app.

## Components
- `viz.py` — top-level API (`Viz.Frame`, `Viz.Series`, `Viz.Info`, `Viz.render`). Saves frame data to `json/`, spins up uvicorn at `http://127.0.0.1:8000`, opens a browser, and stops after ~30s.
- `viz_frame.py` — container that accepts `VizSeries` and `VizInfo` columns and serializes them to JSON (`columns` and `rows`).
- `viz_series.py` — numeric series with attrs (`color`, `width`, `units`, `dots`).
- `viz_info.py` — info/text column container (attrs `color`, `size`).
- `server.py` — FastAPI endpoint `/plot/{uid}` that reads the saved JSON and renders `templates/plot.html`.
- `templates/plot.html` — loads Plotly + jQuery, injects JSON into `window.VIZ_DATA`, and loads `static/plot.js`.
- `static/plot.js` — builds Plotly traces for `VizSeries`, shows hover-synced info rows for `VizInfo`.
- `static/plot.css` — dark theme + two-column info layout.

## Demo (from `test.py`)
```python
import math
from viz import Viz

x = list(range(50))

frame = Viz.Frame(
    Viz.Series(
        name  = 'Late Interaction',
        data  = [math.sin(i / 5) + 1 for i in x],
        color = '#ff5555',
        units = 'score',
        dots  = True,
    ),
    Viz.Series(
        name  = 'Bayes',
        data  = [math.cos(i / 7) + 1 for i in x],
        color = '#55ff55',
        units = 'prob',
        dots  = False,
    ),
    Viz.Info(
        name = 'Sample text 1',
        data = [f'Sample 1 #{i}: synthetic test sentence' for i in x],
    ),
    Viz.Info(
        name = 'Sample text 2',
        data = [f'Sample 2 #{i}: synthetic test sentence' for i in x],
    ),
)

Viz.render(view='plot', data=frame)
```

## How to run
1) Activate your venv with FastAPI/uvicorn installed (e.g., `pip install fastapi uvicorn` if needed).
2) From the repo root, run the demo: `python test.py` (or `py test.py` in your shell).
3) A browser tab will open at `http://127.0.0.1:8000/plot/<uid>` showing the chart; hover any point to see the info columns in the lower panel. The server auto-stops after ~30 seconds.

## Data shape
- `columns`: one entry per series/info column with `name`, `type` (`VizSeries` or `VizInfo`), plus attrs.
- `rows`: aligned rows where keys match column names; missing data is serialized as `null`.

Notes:
- Duplicate column names overwrite prior ones in the frame.
- Both numeric and info columns must be list-like; lengths do not have to match (missing entries become `null`).
