# Engineering Impact & Value Dashboard

A data-driven dashboard for software engineers to track, visualize, and prove their impact over time. Built to shift the performance review conversation from a list of assigned tasks to a verifiable record of proactive ownership, cross-service breadth, and technical refinement.

---

## Why

Managers forget the daily grind. The work that matters most — reducing technical debt, unblocking teammates, navigating cross-system complexity — rarely shows up in a ticket queue. This tool gives you an audit trail with proof links, and turns that trail into a set of charts that tell a coherent story.

---

## Getting Started

**Install dependencies**
```bash
pip install streamlit pandas plotly
```

**Run the dashboard**
```bash
streamlit run impact_dashboard.py
```

Opens at `http://localhost:8501`. New entries logged via the in-app form reload the dashboard automatically.

---

## Data Format

The dashboard reads from `sprint_data.csv` in the same directory. A sample file is included.

| Column | Type | Description |
|---|---|---|
| `Date` | `YYYY-MM-DD` | Date the task was completed |
| `Sprint` | String | Sprint identifier, e.g. `Sprint 26` |
| `Service` | String | Microservice or system area, e.g. `PaymentGateway` |
| `Type` | `Proactive` / `Reactive` | Self-identified work vs. assigned ticket |
| `Category` | String | Work category, e.g. `Knowledge Share`, `Technical Debt` |
| `Description` | String | One-line summary, written as a performance review bullet |
| `Comments_per_PR` | Integer | PR review comment count |
| `Proof_Link` | URL | Jira ticket, GitHub PR, or Confluence link |
| `AI_Assisted` | `Yes` / `No` | Whether an AI tool was used on this task |

**Sample row**
```csv
Date,Sprint,Service,Type,Category,Description,Comments_per_PR,Proof_Link,AI_Assisted
2026-04-12,Sprint 26,NotificationService,Proactive,Design Input,Proposed alternate architecture for cross-service API,2,https://github.com/your-org/notifications/pr/88,Yes
```

---

## Dashboard Panels

| Panel | Chart | Purpose |
|---|---|---|
| Headline KPIs | Metrics | Proactive %, AI Adoption %, Services Touched — always visible, updates with filter |
| System Architecture Knowledge | Treemap | Breadth of services and work types contributed to |
| Ownership Heatmap | Area chart | Proactive vs. reactive task volume over time |
| Voice & Influence | Radar | Soft-skill category contributions, auto-derived from CSV |
| Refinement Trend | Line chart | PR comment count over time — downward trend signals improving quality |
| Task Throughput | Stacked bar | Tasks per sprint with AI-assisted portion highlighted |
| AI Acceleration Ratio | Metrics + line | AI adoption % per sprint with trend line |
| Sprint Audit Trail | Filterable table | Full log with clickable proof links |

The Ownership Heatmap, Refinement Trend, and AI panels always render the full timeline regardless of the sprint filter — they are trend views. All other panels respect the filter.

---

## Sidebar

| Control | Description |
|---|---|
| Engineer Name / Role | Personalizes the header — useful when exporting for a review |
| Sprint Filter | Multi-select; leave empty for an all-time view |
| Export as PDF | Triggers the browser print dialog — use Save as PDF for a portable report |
| Theme | Toggle between dark mode and a warm light mode |

---

## Logging Entries

Expand **Log New Entry** at the bottom of the dashboard to add a task without touching the CSV. All fields are available in a two-column form. Required fields: Date, Sprint, Service, Type, and Description. On save, the dashboard reloads immediately and all charts update.

You can also edit `sprint_data.csv` directly for bulk updates or corrections — press `R` in the browser to reload after manual edits.

---

## Tips

- **Log weekly.** Five minutes at the end of each sprint keeps the data useful.
- **Write descriptions for the review, not the ticket.** Make each line read like a performance review bullet.
- **Always include a proof link.** A PR or Jira ticket makes every claim verifiable.
- **Mark AI-assisted tasks consistently.** The adoption trend over time is what tells the story — individual entries matter less than the pattern.
