# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A single-file Streamlit dashboard (`impact_dashboard.py`) that reads a CSV of sprint tasks and renders interactive Plotly charts to help engineers track and visualize their engineering impact over time. The intended audience is individual engineers preparing for performance reviews.

## Running the app

```bash
pip install streamlit pandas plotly
streamlit run impact_dashboard.py
```

The app opens at `http://localhost:8501`. Press `R` in the browser or click "Rerun" to reload after editing `sprint_data.csv`.

There are no tests or linters configured in this project.

## Architecture

Everything lives in `impact_dashboard.py`. Data flows linearly:

1. `sprint_data.csv` is parsed once by `load_data()` (wrapped in `@st.cache_data`) into a Pandas DataFrame.
2. The sidebar sprint selector produces `filtered_df` (a subset of the full `df`).
3. Four chart panels and one table are rendered using `filtered_df` or `df`.

**Important filtering behavior:** The Ownership Heatmap (area chart) and Refinement Trend (line chart) intentionally always use the *unfiltered* `df` — they exist to show full timeline trends. The Treemap, Radar, and Audit Trail table use `filtered_df` and respect the sprint selector.

## Data contract (`sprint_data.csv`)

| Column | Notes |
|---|---|
| `Date` | `YYYY-MM-DD`, parsed to datetime |
| `Sprint` | Free string, populates the sidebar filter |
| `Service` | Microservice name, drives the Treemap |
| `Type` | Must be exactly `Proactive` or `Reactive` |
| `Category` | Drives both the Treemap and the Radar chart |
| `Comments_per_PR` | Integer, drives the Refinement Trend line chart |
| `Proof_Link` | Rendered as a clickable link in the Audit Trail |

## Radar chart categories

The radar chart only plots categories listed in `radar_cats` (line ~99):

```python
radar_cats = ['Design Input', 'Knowledge Share', 'End-User Sync', 'Unblocking', 'Technical Debt']
```

Any `Category` value not in this list will appear in the Treemap and Audit Trail but will be silently omitted from the Radar. If the user adds new category values, update this list.

## GitHub integration

`.github/workflows/claude.yml` runs Claude Code via `anthropics/claude-code-action@v1` when any issue or PR comment contains `@claude`.
