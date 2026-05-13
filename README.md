# Engineering Impact & Value Dashboard

Bridging the gap between "code pushed" and "value delivered."

A lightweight, data-driven dashboard for Software Engineers to track, visualize, and prove their impact over time. It shifts the performance review conversation from a list of assigned tasks to a verifiable narrative of **proactive ownership, cross-service architecture knowledge, and technical refinement.**

## Why use this?

Managers forget the daily grind. As developers, we often handle "under the hood" tasks like reducing technical debt, unblocking teammates, and debugging complex cross-system issues.

This dashboard takes a simple CSV log of your sprint tasks and automatically generates an engineering console to visualize:

1. **Headline Impact:** Three always-visible KPIs — Proactive %, AI Adoption %, and Services Touched — that update with your sprint filter.
2. **System Architecture Knowledge:** A Treemap showing the breadth of the microservices you touch.
3. **Ownership Velocity:** An area chart proving your shift from *Reactive* (assigned tickets) to *Proactive* (self-identified gap closures) work.
4. **Voice & Influence:** A radar chart tracking your soft skills (design inputs, knowledge sharing, end-user syncs) — automatically derived from your CSV categories.
5. **AI Productivity:** Two panels showing task throughput with AI-assisted tasks highlighted, and an AI adoption trend over time.
6. **The Sprint Audit Trail:** A filtered, undeniable log of your accomplishments with direct links to your PRs and Jira tickets.

## Tech Stack

* **Python 3.8+**
* **Streamlit** (UI Framework)
* **Plotly** (Interactive Data Visualizations)
* **Pandas** (Data Manipulation)

---

## Quick Start

Get the dashboard running locally in under two minutes:

### 1. Clone the repository
```bash
git clone https://github.com/amod0017/contribution-logger.git
cd contribution-logger
```

### 2. Install dependencies

```bash
pip install streamlit pandas plotly
```

### 3. Run the dashboard

```bash
streamlit run impact_dashboard.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## CSV Data Format

The dashboard reads from `sprint_data.csv` in the same directory. A sample file is included.

### Required Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `Date` | `YYYY-MM-DD` | Date the task was completed | `2026-04-12` |
| `Sprint` | String | Sprint identifier | `Sprint 26` |
| `Service` | String | Microservice or system area | `PaymentGateway` |
| `Type` | `Proactive` or `Reactive` | Whether you self-identified the work or it was assigned | `Proactive` |
| `Category` | String | Work category | `Knowledge Share` |
| `Description` | String | Short summary of the accomplishment | `Created team walkthrough doc` |
| `Comments_per_PR` | Integer | Number of review comments on the associated PR | `2` |
| `Proof_Link` | URL | Link to Jira ticket, GitHub PR, or Confluence page | `https://github.com/...` |
| `AI_Assisted` | `Yes` or `No` | Whether an AI tool (Claude, Copilot, etc.) was used | `Yes` |

### Sample row

```csv
Date,Sprint,Service,Type,Category,Description,Comments_per_PR,Proof_Link,AI_Assisted
2026-04-12,Sprint 26,NotificationService,Proactive,Design Input,Proposed alternate architecture for cross-service API,2,https://github.com/your-org/notifications/pr/88,Yes
```

---

## Dashboard Components

| Panel | Chart Type | Data Source | Purpose |
|---|---|---|---|
| Headline KPIs | Metrics | All columns | Always-visible Proactive %, AI Adoption %, Services Touched |
| System Architecture Knowledge | Treemap | `Service` + `Category` | Shows breadth of services and work types you contribute to |
| Ownership Heatmap | Area chart | `Date` + `Type` | Tracks growth of proactive vs reactive work over time |
| Voice & Influence Radar | Radar / Polar chart | `Category` | Highlights soft-skill contributions (auto-derived from your CSV) |
| Refinement & Efficiency Trend | Line chart | `Date` + `Comments_per_PR` | Tracks code quality improvement over time |
| Task Throughput | Stacked bar | `Sprint` + `AI_Assisted` | Total tasks per sprint with AI-assisted portion highlighted |
| AI Acceleration Ratio | Metrics + Line chart | `Sprint` + `AI_Assisted` | AI adoption % per sprint and trend over time |
| Sprint Audit Trail | Filterable table | All columns | Full searchable log with clickable proof links |

The Ownership Heatmap, Refinement Trend, and AI panels always show the **full timeline** regardless of the sprint filter — they exist for trend analysis. All other panels respect the sprint filter.

## Sidebar Controls

* **Engineer Name / Role** — Personalises the dashboard header (useful for PDF exports).
* **Sprint Filter** — Multi-select filter; choose one or more sprints to focus the Treemap, Radar, Headline KPIs, and Audit Trail. Leave empty for an all-time view.
* **Export as PDF** — Triggers your browser's print dialog. Use "Save as PDF" to capture the full dashboard as a portable report.

## Data Loading & Caching

Data is loaded with `@st.cache_data` so the CSV is only parsed once per session. If you update `sprint_data.csv` while the app is running, click **"Rerun"** in the Streamlit toolbar (or press `R`) to reload.

---

## Tips for Getting the Most Out of It

* **Log every Friday** — spend five minutes updating `sprint_data.csv` at the end of each week.
* **Be specific in `Description`** — write it as you would in a performance-review bullet point.
* **Always add a `Proof_Link`** — a GitHub PR or Jira ticket makes your impact undeniable.
* **Mark AI-assisted tasks honestly** — even partial AI use counts. The trend is what matters, not perfection.
* **Export before performance reviews** — click "Export as PDF" in the sidebar for a ready-made impact report.
