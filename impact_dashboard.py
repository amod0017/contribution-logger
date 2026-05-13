import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Impact Dashboard", layout="wide", initial_sidebar_state="expanded")

if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

if st.session_state.theme == 'dark':
    st.markdown("""
        <style>
        [data-testid="stApp"] { background-color: #0d1117 !important; }
        [data-testid="stAppViewContainer"] { background-color: #0d1117 !important; }
        [data-testid="stHeader"] { background-color: #0d1117 !important; }
        .main, .block-container { background-color: #0d1117 !important; color: #c9d1d9 !important; }
        p, span, li, label, div { color: #c9d1d9; }
        h1, h2, h3 { color: #58a6ff !important; font-weight: 600; }
        [data-testid="stMetricValue"] { font-size: 2rem; color: #3fb950 !important; }
        [data-testid="stMetricLabel"] { color: #8b949e !important; }
        div[data-testid="stExpander"] { border: 1px solid #30363d !important; background-color: #161b22 !important; border-radius: 6px; }
        [data-testid="stSidebar"] { background-color: #161b22 !important; }
        [data-testid="stButton"] > button {
            background-color: #1f6feb !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 6px !important;
        }
        [data-testid="stButton"] > button:hover { background-color: #388bfd !important; }
        [data-testid="stFormSubmitButton"] > button {
            background-color: #238636 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 6px !important;
        }
        [data-testid="stFormSubmitButton"] > button:hover { background-color: #2ea043 !important; }
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stDateInput"] input { background-color: #0d1117 !important; color: #c9d1d9 !important; border-color: #30363d !important; }
        [data-baseweb="select"] > div { background-color: #0d1117 !important; color: #c9d1d9 !important; border-color: #30363d !important; }
        [data-baseweb="menu"] { background-color: #161b22 !important; color: #c9d1d9 !important; }
        [data-baseweb="option"] { background-color: #161b22 !important; color: #c9d1d9 !important; }
        [data-baseweb="option"]:hover { background-color: #30363d !important; }
        [data-testid="stMultiSelect"] > div { background-color: #0d1117 !important; border-color: #30363d !important; }
        [data-testid="stMultiSelect"] input { color: #c9d1d9 !important; background-color: transparent !important; }
        [data-baseweb="tag"] { background-color: #30363d !important; }
        [data-baseweb="tag"] span { color: #c9d1d9 !important; }
        [data-baseweb="tag"] svg { fill: #c9d1d9 !important; }
        hr { border-color: #21262d; }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        [data-testid="stApp"] { background-color: #f0ede8 !important; }
        [data-testid="stAppViewContainer"] { background-color: #f0ede8 !important; }
        [data-testid="stHeader"] { background-color: #f0ede8 !important; }
        .main, .block-container { background-color: #f0ede8 !important; color: #2d3436 !important; }
        p, span, li, label { color: #2d3436; }
        h1, h2, h3 { color: #2980b9 !important; font-weight: 600; }
        [data-testid="stMetricValue"] { font-size: 2rem; color: #27ae60 !important; }
        [data-testid="stMetricLabel"] { color: #636e72 !important; }
        div[data-testid="stExpander"] { border: 1px solid #ccc8c0 !important; background-color: #e8e4dd !important; border-radius: 6px; }
        [data-testid="stSidebar"] { background-color: #ddd8d0 !important; }
        [data-testid="stButton"] > button {
            background-color: #2980b9 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 6px !important;
        }
        [data-testid="stButton"] > button:hover { background-color: #2471a3 !important; }
        [data-testid="stFormSubmitButton"] > button {
            background-color: #27ae60 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 6px !important;
        }
        [data-testid="stFormSubmitButton"] > button:hover { background-color: #219a52 !important; }
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stDateInput"] input { background-color: #faf8f5 !important; color: #2d3436 !important; border-color: #ccc8c0 !important; }
        [data-baseweb="select"] > div { background-color: #faf8f5 !important; color: #2d3436 !important; border-color: #ccc8c0 !important; }
        [data-baseweb="menu"] { background-color: #f0ede8 !important; color: #2d3436 !important; }
        [data-baseweb="option"] { background-color: #f0ede8 !important; color: #2d3436 !important; }
        [data-baseweb="option"]:hover { background-color: #ddd8d0 !important; }
        [data-testid="stMultiSelect"] > div { background-color: #faf8f5 !important; border-color: #ccc8c0 !important; }
        [data-testid="stMultiSelect"] input { color: #2d3436 !important; background-color: transparent !important; }
        [data-testid="stMultiSelect"] input::placeholder { color: #636e72 !important; opacity: 1 !important; }
        [data-testid="stMultiSelect"] div,
        [data-testid="stMultiSelect"] span,
        [data-testid="stMultiSelect"] p { color: #2d3436 !important; }
        [data-baseweb="tag"] { background-color: #ccc8c0 !important; }
        [data-baseweb="tag"] span { color: #2d3436 !important; }
        [data-baseweb="tag"] svg { fill: #2d3436 !important; }
        hr { border-color: #ccc8c0; }
        </style>
        """, unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Dashboard Settings")
    user_display_name = st.text_input("Engineer Name", value="Amod")
    user_role = st.text_input("Role", value="Senior Software Engineer")
    st.caption("Customize the identity for PDF exports or presentations.")
    st.divider()
    
    st.header("📂 Sprint Filter")
    try:
        df_temp = pd.read_csv('sprint_data.csv')
        sprint_list = sorted(list(df_temp['Sprint'].unique()), reverse=True)
        selected_sprints = st.multiselect("Select Sprints", sprint_list, placeholder="All Time")
    except:
        selected_sprints = []

    st.divider()
    st.markdown('<button onclick="window.print()">🖨️ Export as PDF</button>', unsafe_allow_html=True)
    st.divider()
    theme_label = "Switch to Light Mode" if st.session_state.theme == 'dark' else "Switch to Dark Mode"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

def render_audit_table(df, theme):
    is_dark = theme == 'dark'
    bg       = '#0d1117' if is_dark else '#f0ede8'
    alt_bg   = '#161b22' if is_dark else '#e8e4dd'
    text     = '#c9d1d9' if is_dark else '#2d3436'
    border   = '#30363d' if is_dark else '#ccc8c0'
    hdr_bg   = '#161b22' if is_dark else '#ddd8d0'
    link_col = '#58a6ff' if is_dark else '#2980b9'

    cols   = ['Date', 'Sprint', 'Type', 'Service', 'Category', 'Description', 'Proof_Link']
    labels = {c: c for c in cols}
    labels['Proof_Link'] = 'Verification Link'

    cell = f"padding:8px 12px; border-bottom:1px solid {border}; color:{text}; font-size:14px;"
    hdr  = f"padding:8px 12px; background:{hdr_bg}; color:{text}; font-weight:600; font-size:13px; text-align:left; border-bottom:2px solid {border};"

    headers = ''.join(f'<th style="{hdr}">{labels[c]}</th>' for c in cols)
    rows = ''
    for i, (_, row) in enumerate(df[cols].iterrows()):
        row_bg = alt_bg if i % 2 == 0 else bg
        cells = ''
        for col in cols:
            val = row[col]
            if col == 'Proof_Link' and pd.notna(val) and str(val).strip():
                cells += f'<td style="{cell} background:{row_bg};"><a href="{val}" target="_blank" style="color:{link_col};">Link</a></td>'
            else:
                cells += f'<td style="{cell} background:{row_bg};">{str(val) if pd.notna(val) else ""}</td>'
        rows += f'<tr>{cells}</tr>'

    st.markdown(f'''
    <div style="overflow-x:auto; border-radius:6px; border:1px solid {border}; margin-top:8px;">
        <table style="width:100%; border-collapse:collapse; background:{bg};">
            <thead><tr>{headers}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>''', unsafe_allow_html=True)

def apply_chart_theme(fig):
    is_dark = st.session_state.theme == 'dark'
    font_color = '#c9d1d9' if is_dark else '#2d3436'
    grid_color = '#30363d' if is_dark else '#ddd8d0'
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=font_color),
    )
    fig.update_xaxes(gridcolor=grid_color, linecolor=grid_color, zerolinecolor=grid_color)
    fig.update_yaxes(gridcolor=grid_color, linecolor=grid_color, zerolinecolor=grid_color)
    return fig

# --- GENERIC DATA LOADER ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('sprint_data.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("Missing 'sprint_data.csv'. Please create the file to render the dashboard.")
    st.stop()

# Filter data based on sidebar
filtered_df = df if not selected_sprints else df[df['Sprint'].isin(selected_sprints)]

# --- DYNAMIC HEADER ---
col_h1, col_h2, col_h3, col_h4 = st.columns([3, 1, 1, 1])
with col_h1:
    st.title(f"🚀 {user_display_name}'s Value Dashboard")
    st.markdown(f"**{user_role}** | Focused on Proactive System Integration & Ownership")
with col_h2:
    total = max(len(filtered_df), 1)
    proactive_pct = round(len(filtered_df[filtered_df['Type'] == 'Proactive']) / total * 100)
    st.metric("Proactive", f"{proactive_pct}%", help="% of tasks self-identified")
with col_h3:
    ai_pct = round((filtered_df['AI_Assisted'].fillna('No') == 'Yes').sum() / total * 100)
    st.metric("AI Adoption", f"{ai_pct}%", help="% of tasks AI-assisted")
with col_h4:
    services = filtered_df['Service'].nunique()
    st.metric("Services Touched", services, help="Unique services contributed to")

st.divider()

# --- ROW 1: SYSTEM MAP & OWNERSHIP VELOCITY ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("1. System Architecture Knowledge")
    # Using a Treemap to simulate the "Web" of knowledge across services
    service_counts = filtered_df.groupby(['Service', 'Category']).size().reset_index(name='Impact')
    fig_tree = px.treemap(service_counts, path=['Service', 'Category'], values='Impact',
                          color='Impact', color_continuous_scale='viridis')
    fig_tree.update_layout(margin=dict(t=10, l=10, r=10, b=10))
    apply_chart_theme(fig_tree)
    st.plotly_chart(fig_tree, use_container_width=True)
    st.caption("Visualizing cross-service expertise (e.g., AuthAPI, PaymentGateway, DataPipeline).")

with c2:
    st.subheader("2. Ownership Heatmap (Proactive vs Reactive)")
    # Area chart to show the "Velocity" of proactivity over time
    velocity_data = df.groupby(['Date', 'Type']).size().reset_index(name='Count')
    fig_area = px.area(velocity_data, x='Date', y='Count', color='Type',
                       color_discrete_map={'Proactive': '#3fb950', 'Reactive': '#58a6ff'})
    fig_area.update_layout(margin=dict(t=10, l=10, r=10, b=10), xaxis_title="Timeline", yaxis_title="Task Volume")
    apply_chart_theme(fig_area)
    st.plotly_chart(fig_area, use_container_width=True)
    st.caption("Goal: The green 'Proactive' area should grow over time.")

st.divider()

# --- ROW 2: RADAR & REFINEMENT TREND ---
c3, c4 = st.columns(2)

with c3:
    st.subheader("3. Voice & Influence Radar")
    # Soft skills tracking
    cat_counts = filtered_df['Category'].value_counts().to_dict()
    radar_cats = sorted(filtered_df['Category'].dropna().unique().tolist())
    values = [cat_counts.get(c, 0) for c in radar_cats]
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=values, theta=radar_cats, fill='toself', marker_color='#a371f7'
    ))
    is_dark = st.session_state.theme == 'dark'
    radar_grid  = '#30363d' if is_dark else '#ddd8d0'
    radar_font  = '#c9d1d9' if is_dark else '#2d3436'
    radar_bg    = '#161b22' if is_dark else '#e8e4dd'
    fig_radar.update_layout(
        polar=dict(
            bgcolor=radar_bg,
            radialaxis=dict(visible=True, gridcolor=radar_grid, tickfont=dict(color=radar_font)),
            angularaxis=dict(tickfont=dict(color=radar_font), linecolor=radar_grid),
        ),
        margin=dict(t=20, l=20, r=20, b=20),
    )
    apply_chart_theme(fig_radar)
    st.plotly_chart(fig_radar, use_container_width=True)
    st.caption("Tracking proactive communication and design initiatives.")

with c4:
    st.subheader("4. Refinement & Efficiency Trend")
    # Tracking PR Review Cycles / Comments (Global Unfiltered View)
    fig_line = px.line(df.sort_values('Date'), x='Date', y='Comments_per_PR', markers=True,
                       line_shape='spline', color_discrete_sequence=['#f85149'])
    fig_line.update_layout(margin=dict(t=10, l=10, r=10, b=10), xaxis_title="Timeline", yaxis_title="Comments per PR")
    apply_chart_theme(fig_line)
    st.plotly_chart(fig_line, use_container_width=True)
    st.caption("Goal: Downward trend indicates adherence to conventions and self-review.")

st.divider()

# --- ROW 3: AI-POWERED PRODUCTIVITY ---
c5, c6 = st.columns(2)

sprint_order = df.groupby('Sprint')['Date'].min().sort_values().index.tolist()

with c5:
    st.subheader("5. Task Throughput")
    throughput_src = filtered_df.copy()
    throughput_src['AI_Assisted'] = throughput_src['AI_Assisted'].fillna('No')
    throughput_data = throughput_src.groupby(['Sprint', 'AI_Assisted']).size().reset_index(name='Tasks')
    throughput_data['Sprint'] = pd.Categorical(throughput_data['Sprint'], categories=sprint_order, ordered=True)
    throughput_data = throughput_data.sort_values('Sprint')
    fig_throughput = px.bar(throughput_data, x='Sprint', y='Tasks', color='AI_Assisted',
                            color_discrete_map={'Yes': '#3fb950', 'No': '#30363d'},
                            barmode='stack')
    fig_throughput.update_layout(margin=dict(t=10, l=10, r=10, b=10), legend_title_text='AI Assisted')
    apply_chart_theme(fig_throughput)
    st.plotly_chart(fig_throughput, use_container_width=True)
    st.caption("Goal: green share and total bar height grow together over time.")

with c6:
    st.subheader("6. AI Acceleration Ratio")
    # Trend line always uses full df for context; KPIs reflect the selected sprint view
    ai_full = df.copy()
    ai_full['AI_Assisted'] = ai_full['AI_Assisted'].fillna('No')
    sprint_ai = (
        ai_full.groupby('Sprint')
        .apply(lambda x: round((x['AI_Assisted'] == 'Yes').sum() / len(x) * 100, 1))
        .reset_index(name='AI_Pct')
    )
    sprint_ai['Sprint'] = pd.Categorical(sprint_ai['Sprint'], categories=sprint_order, ordered=True)
    sprint_ai = sprint_ai.sort_values('Sprint')

    # KPIs: use selected sprint/filter for % metric; full df for total count
    ai_filtered = filtered_df.copy()
    ai_filtered['AI_Assisted'] = ai_filtered['AI_Assisted'].fillna('No')
    kpi_pct = round((ai_filtered['AI_Assisted'] == 'Yes').sum() / max(len(ai_filtered), 1) * 100, 1)
    total_ai_tasks = int((ai_full['AI_Assisted'] == 'Yes').sum())

    m1, m2 = st.columns(2)
    m1.metric("AI-Assisted", f"{kpi_pct:.0f}%")
    m2.metric("Total AI Tasks", total_ai_tasks)

    fig_ai_ratio = px.line(sprint_ai, x='Sprint', y='AI_Pct', markers=True,
                           line_shape='spline', color_discrete_sequence=['#3fb950'])
    fig_ai_ratio.update_layout(margin=dict(t=10, l=10, r=10, b=10), yaxis_title="% AI-Assisted", yaxis_range=[0, 100])
    apply_chart_theme(fig_ai_ratio)
    st.plotly_chart(fig_ai_ratio, use_container_width=True)
    st.caption("Goal: line climbs — deliberate AI adoption over time.")

st.divider()

# --- ROW 4: THE AUDIT TRAIL ---
audit_label = ", ".join(selected_sprints) if selected_sprints else "All Time"
st.subheader(f"🔍 The Sprint Audit Trail: {audit_label}")
st.markdown("Detailed record of accomplishments. Use links for undeniable proof.")

render_audit_table(filtered_df, st.session_state.theme)

st.divider()

with st.expander("Log New Entry"):
    with st.form("entry_form", clear_on_submit=True):
        c_a, c_b = st.columns(2)
        with c_a:
            f_date = st.date_input("Date", value=pd.Timestamp.today())
            f_service = st.text_input("Service")
            f_category = st.text_input("Category")
            f_comments = st.number_input("Comments per PR", min_value=0, value=0, step=1)
        with c_b:
            f_sprint = st.text_input("Sprint")
            f_type = st.selectbox("Type", ["Proactive", "Reactive"])
            f_ai = st.selectbox("AI Assisted", ["No", "Yes"])
            f_link = st.text_input("Proof Link")
        f_desc = st.text_area("Description", height=80)
        submitted = st.form_submit_button("Save Entry", use_container_width=True)

    if submitted:
        if not all([f_sprint.strip(), f_service.strip(), f_desc.strip()]):
            st.error("Sprint, Service, and Description are required.")
        else:
            new_row = {
                'Date': f_date.strftime('%Y-%m-%d'),
                'Sprint': f_sprint.strip(),
                'Service': f_service.strip(),
                'Type': f_type,
                'Category': f_category.strip(),
                'Description': f_desc.strip(),
                'Comments_per_PR': int(f_comments),
                'Proof_Link': f_link.strip(),
                'AI_Assisted': f_ai,
            }
            pd.DataFrame([new_row]).to_csv('sprint_data.csv', mode='a', header=False, index=False)
            st.cache_data.clear()
            st.rerun()