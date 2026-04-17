import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Dev Impact Dashboard", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    div[data-testid="stExpander"] { border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- GENERIC DATA LOADER ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('sprint_data.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except FileNotFoundError:
        st.error("Missing 'sprint_data.csv'. Please provide a data source.")
        return None

df = load_data()

if df is not None:
    # --- HEADER ---
    st.title("🚀 Engineering Value & Impact Dashboard")
    st.markdown("---")

    # --- GLOBAL FILTERS ---
    with st.sidebar:
        st.header("Dashboard Controls")
        selected_sprint = st.selectbox("Select Sprint Audit View", ["All Time"] + list(df['Sprint'].unique()))
        
    filtered_df = df if selected_sprint == "All Time" else df[df['Sprint'] == selected_sprint]

    # --- MODULE 1 & 2: KNOWLEDGE WEB & OWNERSHIP ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. System Knowledge Breadth")
        service_counts = filtered_df['Service'].value_counts().reset_index()
        fig_pie = px.pie(service_counts, values='count', names='Service', hole=0.4, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.caption("Visualizing impact across different microservices and boundaries.")

    with col2:
        st.subheader("2. Ownership Velocity (Proactive vs Reactive)")
        # Showcasing the shift to identifying tasks independently [cite: 118, 120]
        type_counts = filtered_df.groupby(['Date', 'Type']).size().reset_index(name='Count')
        fig_bar = px.bar(type_counts, x='Date', y='Count', color='Type', barmode='stack',
                         color_discrete_map={'Proactive': '#00CC96', 'Reactive': '#636EFA'})
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- MODULE 3 & 4: RADAR & REFINEMENT ---
    col3, col4 = st.columns([1, 1])

    with col3:
        st.subheader("3. Influence & Soft Skill Execution")
        # Aggregating categories to show growth in "Voice" [cite: 96, 97]
        cat_counts = filtered_df['Category'].value_counts().to_dict()
        categories = ['Technical', 'Leadership', 'Collaboration', 'Product', 'Mentorship']
        values = [cat_counts.get(c, 0) for c in categories]
        
        fig_radar = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, max(values)+1 if values else 5])))
        st.plotly_chart(fig_radar, use_container_width=True)

    with col4:
        st.subheader("4. Refinement & Efficiency Trend")
        # Tracking the reduction in PR review cycles [cite: 125, 127]
        fig_line = px.line(df.sort_values('Date'), x='Date', y='Comments_per_PR', 
                           title="Comments per PR (Goal: Downward Trend)", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

    # --- THE AUDIT TRAIL (THE INDISPUTABLE LOG) ---
    st.divider()
    st.subheader(f"5. The Sprint Audit Trail: {selected_sprint}")
    st.dataframe(filtered_df[['Sprint', 'Type', 'Service', 'Description', 'Proof_Link']], 
                 use_container_width=True, hide_index=True)
    
    # Export capability
    if st.button("Generate PDF Brag Document"):
        st.balloons()
        st.success("Report generated (simulated). You are ready for your review!")