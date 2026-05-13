# AI Productivity Feature — Design Spec

**Date:** 2026-05-12  
**Status:** Approved  

## Problem

Engineering impact dashboards track *what* was done but not *how efficiently*. With AI tools becoming central to engineering workflows, there's no way to show that AI adoption is driving real productivity gains — more output per sprint.

## Goal

Add a dedicated AI Productivity section to `impact_dashboard.py` that answers two questions a reviewer would ask:

1. Is this engineer actually using AI tools?
2. Is it making them more productive (shipping more)?

## Data Change

Add one new column to `sprint_data.csv`:

| Column | Type | Values | Description |
|---|---|---|---|
| `AI_Assisted` | String | `Yes` / `No` | Whether an AI tool was used to complete this task |

No changes to `load_data()` — Pandas reads the column as-is. Existing rows without the column will surface as `NaN`; handle with `.fillna('No')` at chart render time.

The sample `sprint_data.csv` gets updated rows demonstrating the new column.

## Dashboard Changes

### New Row: "AI-Powered Productivity"

Inserted between the Radar/Refinement row and the Audit Trail. Two columns, mirroring the existing two-column layout.

---

### Panel 5 — Task Throughput

**Chart type:** Stacked bar (`px.bar`)  
**X-axis:** Sprint  
**Y-axis:** Task count  
**Color:** `AI_Assisted` — green (`#3fb950`) for `Yes`, gray (`#30363d`) for `No`  
**Data source:** Full unfiltered `df` (trend panel, same pattern as Ownership Heatmap)  
**Caption:** "Goal: green share and total bar height grow together over time."

Story it tells: total output is climbing AND an increasing share of that output is AI-accelerated.

---

### Panel 6 — AI Acceleration Ratio

**Data source:** Full unfiltered `df`  
**Components (top to bottom):**

1. Two `st.metric` KPIs side by side:
   - **"AI-Assisted This Sprint"** — % of tasks in the most recent sprint flagged `Yes`. "Most recent" = sprint whose tasks have the latest `Date` value in the data.
   - **"Adoption Growth"** — ratio of most-recent-sprint % vs earliest-sprint %. If the earliest sprint has 0% AI-assisted tasks (no baseline to compare), display `"N/A"` instead of the ratio to avoid division by zero.

2. Line chart (`px.line`) of AI-assisted % per sprint over time  
   - X = Sprint, Y = % AI-assisted  
   - Color: `#3fb950`  
   - Caption: "Goal: line climbs — deliberate AI adoption over time."

---

### Sprint Filter Behavior

Both new panels use the full unfiltered `df`. The sprint sidebar filter continues to affect only: Treemap, Radar, and Audit Trail. This is consistent with existing trend panels (Ownership Heatmap, Refinement Trend).

## What Is Explicitly Out of Scope

- Panel B ("AI Feature Work" — tracking tasks that *build* AI features) is a named follow-up, not part of this spec.
- No new `Tool` column (e.g., `Claude`, `Copilot`) — keeping it `Yes/No` for simplicity.
- No time-based metrics (tasks per day, cycle time) — not in the current data model.
