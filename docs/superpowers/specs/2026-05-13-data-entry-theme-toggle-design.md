# Data Entry Form & Theme Toggle — Design Spec

**Date:** 2026-05-13
**Status:** Approved

## Features

### 1. In-Dashboard Data Entry Form

**Placement:** `st.expander("Log New Entry")` below the Sprint Audit Trail. Full page width.

**Fields (two-column grid):**

| Left | Right |
|---|---|
| Date (`st.date_input`, defaults to today) | Sprint (`st.text_input`) |
| Service (`st.text_input`) | Type (`st.selectbox` → Proactive / Reactive) |
| Category (`st.text_input`) | AI Assisted (`st.selectbox` → Yes / No) |
| Comments per PR (`st.number_input`, min 0, default 0) | Proof Link (`st.text_input`) |
| Description (`st.text_area`, full width, spans both columns) | |

**Validation:** Block submission if Date, Sprint, Service, Type, or Description are empty. Show `st.error` inline — no page reload.

**On submit:**
1. Build new row as a dict matching CSV column order
2. Append to `sprint_data.csv` using `pd.DataFrame([row]).to_csv(mode='a', header=False, index=False)`
3. Call `st.cache_data.clear()` to invalidate cached data
4. Call `st.rerun()` to reload the dashboard — all charts update immediately

**Add only.** No edit or delete — the CSV is local and directly editable for corrections.

---

### 2. Theme Toggle

**Placement:** Sidebar, below the PDF export button.

**Behavior:**
- `st.session_state.theme` stores `'dark'` or `'light'`, initialized to `'dark'` on first load
- Button label reads "Switch to Light Mode" when dark, "Switch to Dark Mode" when light
- On click: flip `st.session_state.theme` and call `st.rerun()`

**CSS:** The hardcoded dark CSS block at the top of the file becomes conditional:
- Dark: existing palette (`#0d1117` background, `#58a6ff` headings, `#3fb950` metrics)
- Light: GitHub-light palette (`#ffffff` background, `#0969da` headings, `#1a7f37` metrics, `#f6f8fa` expander background)

**Scope:** Only the dashboard content area controlled by injected CSS switches. Streamlit's own UI chrome (top bar, sidebar header) is unaffected — this is a Streamlit limitation.

## Scope

All changes in `impact_dashboard.py` only. No new dependencies. No CSV schema changes.
