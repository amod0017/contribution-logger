# 🚀 Engineering Impact & Value Dashboard

Bridging the gap between "code pushed" and "value delivered."

This is a lightweight, data-driven dashboard built for Software Engineers to track, visualize, and prove their impact over time. It shifts the performance review conversation from a list of assigned tasks to a verifiable narrative of **proactive ownership, cross-service architecture knowledge, and technical refinement.**

## 🎯 Why use this?
Managers forget the daily grind. As developers, we often handle "under the hood" tasks like reducing technical debt, unblocking teammates, and debugging complex cross-system issues. 

This dashboard takes a simple CSV log of your sprint tasks and automatically generates a high-end engineering console to visualize:
1. **System Architecture Knowledge:** A Treemap showing the breadth of the microservices you touch.
2. **Ownership Velocity:** An area chart proving your shift from *Reactive* (assigned tickets) to *Proactive* (self-identified gap closures) work.
3. **Voice & Influence:** A radar chart tracking your soft skills (design inputs, knowledge sharing, end-user syncs).
4. **The Sprint Audit Trail:** A filtered, undeniable log of your accomplishments with direct links to your PRs and Jira tickets.

## 🛠️ Tech Stack
* **Python 3.8+**
* **Streamlit** (UI Framework)
* **Plotly** (Interactive Data Visualizations)
* **Pandas** (Data Manipulation)

---

## 🚀 Quick Start

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

## 📋 CSV Data Format

The dashboard reads from a file named `sprint_data.csv` located in the same directory as `impact_dashboard.py`. A sample file is included in the repository to help you get started.

### Required Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `Date` | `YYYY-MM-DD` | Date the task was completed | `2026-04-12` |
| `Sprint` | String | Sprint identifier | `Sprint 26` |
| `Service` | String | Microservice or system area | `PaymentGateway` |
| `Type` | `Proactive` or `Reactive` | Whether you self-identified the work (`Proactive`) or it was assigned (`Reactive`) | `Proactive` |
| `Category` | String | Work category (used for the Radar chart) | `Knowledge Share` |
| `Description` | String | Short summary of the accomplishment | `Created team walkthrough doc` |
| `Comments_per_PR` | Integer | Number of review comments on the associated PR | `2` |
| `Proof_Link` | URL | Link to Jira ticket, GitHub PR, or Confluence page | `https://github.com/...` |

### Supported `Category` values (for the Radar chart)
* `Design Input`
* `Knowledge Share`
* `End-User Sync`
* `Unblocking`
* `Technical Debt`

You can use other category names freely — they will appear in the Treemap and Audit Trail but will not be plotted on the Radar chart unless added to the `radar_cats` list in `impact_dashboard.py`.

### Sample row

```csv
Date,Sprint,Service,Type,Category,Description,Comments_per_PR,Proof_Link
2026-04-12,Sprint 26,NotificationService,Proactive,Design Input,Proposed alternate architecture for cross-service API,2,https://github.com/your-org/notifications/pr/88
```

---

## 🏗️ Implementation Details

### File structure

```
contribution-logger/
├── impact_dashboard.py   # Main Streamlit application
├── sprint_data.csv       # Your personal contribution log (edit this!)
└── README.md
```

### Dashboard components

| Panel | Chart Type | Data Source | Purpose |
|---|---|---|---|
| System Architecture Knowledge | Treemap | `Service` + `Category` columns | Shows breadth of services and work types you contribute to |
| Ownership Heatmap | Area chart | `Date` + `Type` columns | Tracks growth of proactive vs reactive work over time |
| Voice & Influence Radar | Radar / Polar chart | `Category` column | Highlights soft-skill contributions |
| Refinement & Efficiency Trend | Line chart | `Date` + `Comments_per_PR` columns | Tracks code quality improvement (fewer PR comments = better) |
| Sprint Audit Trail | Filterable table | All columns | Full searchable log with clickable proof links |

### Sidebar controls

* **Engineer Name / Role** — Personalises the dashboard header (useful for PDF screenshots).
* **Sprint Filter** — Filters the Treemap, Radar, and Audit Trail to a single sprint. The Area and Line charts always show the full timeline for trend analysis.

### Data loading & caching

Data is loaded with `@st.cache_data` so the CSV is only parsed once per session. If you update `sprint_data.csv` while the app is running, click **"Rerun"** in the Streamlit toolbar (or press `R`) to reload.

### Customising the Radar chart categories

Open `impact_dashboard.py` and edit the `radar_cats` list (around line 100):

```python
radar_cats = ['Design Input', 'Knowledge Share', 'End-User Sync', 'Unblocking', 'Technical Debt']
```

Add, remove, or rename entries to match the `Category` values in your CSV.

---

## 💡 Tips for getting the most out of it

* **Log every Friday** — spend five minutes updating `sprint_data.csv` at the end of each week.
* **Be specific in `Description`** — write it as you would in a performance-review bullet point.
* **Always add a `Proof_Link`** — a GitHub PR or Jira ticket makes your impact undeniable.
* **Screenshot before performance reviews** — use your browser's print-to-PDF on the dashboard for a ready-made impact report.
