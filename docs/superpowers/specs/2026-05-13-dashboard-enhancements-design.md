# Dashboard Enhancements — Design Spec

**Date:** 2026-05-13  
**Status:** Approved

## Features

### 1. Headline Impact KPIs

Replace the single "Self-Identified (Proactive) Wins" metric in the header with three side-by-side metrics that stay visible at all times, giving reviewers an instant read on three independent dimensions.

**Metrics (all sourced from `filtered_df`):**
- **Proactive %** — `proactive tasks / total tasks × 100`
- **AI Adoption %** — `AI_Assisted == 'Yes' tasks / total tasks × 100`
- **Services Touched** — count of unique `Service` values

**Layout change:** `st.columns([3, 1])` → `st.columns([3, 1, 1, 1])`

PR comments excluded intentionally — too noisy a signal (reflects reviewer style and incomplete acceptance criteria, not engineer quality).

---

### 2. Dynamic Radar Categories

Remove the hardcoded `radar_cats` list and derive categories directly from the data.

**Change:** Replace line ~99:
```python
radar_cats = ['Design Input', 'Knowledge Share', 'End-User Sync', 'Unblocking', 'Technical Debt']
```
With:
```python
radar_cats = sorted(filtered_df['Category'].dropna().unique().tolist())
```

Any `Category` value in the CSV now automatically appears on the radar. No manual sync required.

---

### 3. PDF Export Button

Add a browser-print trigger in the sidebar, below the sprint filter. Zero dependencies — uses the browser's native print/save-as-PDF dialog.

```python
st.markdown('<button onclick="window.print()">🖨️ Export as PDF</button>', unsafe_allow_html=True)
```

Placed in the sidebar so it's always accessible without scrolling.

## Scope

All changes are in `impact_dashboard.py` only. No CSV changes. No new dependencies.
