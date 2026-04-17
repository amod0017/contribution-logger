import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Impact Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a high-end engineering console vibe
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    h1, h2, h3 { color: #58a6ff !important; font-weight: 600; }
    [data-testid="stMetricValue"] { font-size: 2rem; color: #3fb950; }
    div[data-testid="stExpander"] { border: 1px solid #30363d; background-color: #161b22; border-radius: 6px; }
    hr { border-color: #21262d; }
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
        sprint_list = ["All Time"] + sorted(list(df_temp['Sprint'].unique()), reverse=True)
        selected_sprint = st.selectbox("Select Audit View", sprint_list)
    except:
        selected_sprint = "All Time"

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
filtered_df = df if selected_sprint == "All Time" else df[df['Sprint'] == selected_sprint]

# --- DYNAMIC HEADER ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title(f"🚀 {user_display_name}'s Value Dashboard")
    st.markdown(f"**{user_role}** | Focused on Proactive System Integration & Ownership")
with col_h2:
    proactive_count = len(filtered_df[filtered_df['Type'] == 'Proactive'])
    st.metric("Self-Identified (Proactive) Wins", f"{proactive_count}", help="Tasks you initiated independently")

st.divider()

# --- ROW 1: SYSTEM MAP & OWNERSHIP VELOCITY ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("1. System Architecture Knowledge")
    # Using a Treemap to simulate the "Web" of knowledge across services
    service_counts = filtered_df.groupby(['Service', 'Category']).size().reset_index(name='Impact')
    fig_tree = px.treemap(service_counts, path=['Service', 'Category'], values='Impact',
                          color='Impact', color_continuous_scale='viridis')
    fig_tree.update_layout(margin=dict(t=10, l=10, r=10, b=10), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_tree, use_container_width=True)
    st.caption("Visualizing cross-service expertise (e.g., AuthAPI, PaymentGateway, DataPipeline).")

with c2:
    st.subheader("2. Ownership Heatmap (Proactive vs Reactive)")
    # Area chart to show the "Velocity" of proactivity over time
    velocity_data = df.groupby(['Date', 'Type']).size().reset_index(name='Count')
    fig_area = px.area(velocity_data, x='Date', y='Count', color='Type',
                       color_discrete_map={'Proactive': '#3fb950', 'Reactive': '#58a6ff'})
    fig_area.update_layout(margin=dict(t=10, l=10, r=10, b=10), paper_bgcolor="rgba(0,0,0,0)",
                           xaxis_title="Timeline", yaxis_title="Task Volume")
    st.plotly_chart(fig_area, use_container_width=True)
    st.caption("Goal: The green 'Proactive' area should grow over time.")

st.divider()

# --- ROW 2: RADAR & REFINEMENT TREND ---
c3, c4 = st.columns(2)

with c3:
    st.subheader("3. Voice & Influence Radar")
    # Soft skills tracking
    cat_counts = filtered_df['Category'].value_counts().to_dict()
    radar_cats = ['Design Input', 'Knowledge Share', 'End-User Sync', 'Unblocking', 'Technical Debt']
    values = [cat_counts.get(c, 0) for c in radar_cats]
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=values, theta=radar_cats, fill='toself', marker_color='#a371f7'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), 
                            margin=dict(t=20, l=20, r=20, b=20), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_radar, use_container_width=True)
    st.caption("Tracking proactive communication and design initiatives.")

with c4:
    st.subheader("4. Refinement & Efficiency Trend")
    # Tracking PR Review Cycles / Comments (Global Unfiltered View)
    fig_line = px.line(df.sort_values('Date'), x='Date', y='Comments_per_PR', markers=True,
                       line_shape='spline', color_discrete_sequence=['#f85149'])
    fig_line.update_layout(margin=dict(t=10, l=10, r=10, b=10), paper_bgcolor="rgba(0,0,0,0)",
                           xaxis_title="Timeline", yaxis_title="Comments per PR")
    st.plotly_chart(fig_line, use_container_width=True)
    st.caption("Goal: Downward trend indicates adherence to conventions and self-review.")

st.divider()

# --- ROW 3: THE AUDIT TRAIL ---
st.subheader(f"🔍 The Sprint Audit Trail: {selected_sprint}")
st.markdown("Detailed record of accomplishments. Use links for undeniable proof.")

# Render dataframe with clickable links
st.dataframe(
    filtered_df[['Date', 'Sprint', 'Type', 'Service', 'Category', 'Description', 'Proof_Link']], 
    use_container_width=True, 
    hide_index=True,
    column_config={
        "Proof_Link": st.column_config.LinkColumn("Verification Link (Jira/PR)")
    }
)