import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Career Shift Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Version management
def get_app_version():
    try:
        env_version = os.getenv('APP_VERSION')
        if env_version:
            return env_version
        base_version = "1.4"
        build_number = datetime.now().strftime("%y%m%d")
        return f"{base_version}.{build_number}"
    except:
        return "1.0.0"

# Advanced Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s infinite;
    }
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .feature-card {
        background: linear-gradient(145deg, #ffffff, #f0f2f5);
        padding: 2rem;
        border-radius: 20px;
        border: none;
        margin: 1.5rem 0;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1), 0 1px 8px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        transition: width 0.3s ease;
    }
    .feature-card:hover::before {
        width: 100%;
        opacity: 0.1;
    }
    .feature-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3), 0 10px 20px rgba(0,0,0,0.2);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0.5rem;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.6s;
    }
    .stat-card:hover::before {
        left: 100%;
    }
    .stat-card:hover {
        transform: translateY(-10px) rotateY(5deg) scale(1.05);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.5);
    }
    
    .version-info {
        position: fixed;
        top: 15px;
        right: 15px;
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 25px;
        padding: 0.5rem 1rem;
        font-size: 0.9em;
        color: #667eea;
        z-index: 1000;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }
    .version-info:hover {
        transform: scale(1.05);
        background: rgba(102, 126, 234, 0.2);
    }
    
    .success-story {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 6px solid #28a745;
        transition: all 0.4s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    .success-story::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, #28a745, #20c997);
        border-radius: 50%;
        transform: translate(50%, -50%);
        opacity: 0.1;
    }
    .success-story:hover {
        transform: translateX(15px) scale(1.02);
        box-shadow: 0 20px 40px rgba(40, 167, 69, 0.2);
        border-left-width: 8px;
    }
    
    .quick-action-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 1.2rem 2rem;
        border-radius: 30px;
        font-weight: bold;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    .quick-action-btn::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: radial-gradient(circle, rgba(255,255,255,0.3), transparent);
        transition: all 0.4s ease;
        transform: translate(-50%, -50%);
        border-radius: 50%;
    }
    .quick-action-btn:hover::before {
        width: 300px;
        height: 300px;
    }
    .quick-action-btn:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
    }
    
    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 2rem 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    .chart-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    }
    
    .industry-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    .industry-item {
        background: white;
        border: 2px solid transparent;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
    }
    .industry-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    .industry-item:hover::before {
        transform: scaleX(1);
    }
    .industry-item:hover {
        border-color: #667eea;
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
    }
    
    .universal-footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-top: 4rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    .universal-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.05)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.05)"/></pattern></defs><rect width="100%" height="100%" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 3rem;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }
    .footer-section h4 {
        color: #ffd700;
        margin-bottom: 1.5rem;
        font-size: 1.2em;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .disclaimer-box {
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-size: 0.9em;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .disclaimer-box:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }
    
    .team-section {
        background: rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255,215,0,0.3);
        transition: all 0.3s ease;
    }
    .team-section:hover {
        border-color: rgba(255,215,0,0.6);
        transform: translateY(-3px);
    }
    .team-members {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }
    .team-member {
        background: rgba(255,255,255,0.25);
        padding: 1.5rem 2rem;
        border-radius: 25px;
        border: 3px solid rgba(255,215,0,0.5);
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        backdrop-filter: blur(10px);
        text-align: center;
        min-width: 160px;
        position: relative;
        overflow: hidden;
    }
    .team-member::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,215,0,0.2), transparent);
        transition: left 0.6s;
    }
    .team-member:hover::before {
        left: 100%;
    }
    .team-member:hover {
        transform: translateY(-8px) scale(1.05);
        border-color: #ffd700;
        box-shadow: 0 15px 30px rgba(255,215,0,0.4);
        background: rgba(255,255,255,0.35);
    }
    .team-member strong {
        color: #ffd700;
        font-size: 1.1em;
        display: block;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .footer-bottom {
        border-top: 2px solid rgba(255,255,255,0.3);
        padding-top: 2rem;
        text-align: center;
        font-size: 0.9em;
        color: rgba(255,255,255,0.95);
        position: relative;
        z-index: 1;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #00ff00;
        border-radius: 50%;
        margin-right: 0.8rem;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px #00ff00;
    }
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }
    .footer-link {
        color: #ffd700;
        text-decoration: none;
        transition: all 0.3s ease;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
    }
    .footer-link:hover {
        color: #fff;
        background: rgba(255,215,0,0.2);
        text-shadow: 0 0 15px #ffd700;
        transform: translateY(-1px);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header { padding: 2rem 1rem; }
        .feature-card, .stat-card { margin: 1rem 0; }
        .team-members { flex-direction: column; align-items: center; }
        .footer-grid { grid-template-columns: 1fr; gap: 2rem; }
    }
</style>
""", unsafe_allow_html=True)

# Version display
version = get_app_version()
st.markdown(f"""
<div class="version-info">
    🚀 v{version} Pro
</div>
""", unsafe_allow_html=True)

# Enhanced Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 3em; font-weight: 700;">🚀 Career Shift Analyzer</h1>
    <p style="font-size: 1.3em; margin: 1rem 0; opacity: 0.95;">Navigate Your Future in Emerging Industries</p>
    <p style="font-size: 1em; margin: 0; opacity: 0.8;">
        Professional Career Guidance Platform with AI-Powered Insights
    </p>
</div>
""", unsafe_allow_html=True)

# Hero section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    ### 🎯 Transform Your Career Journey
    
    Discover opportunities in **AI, Blockchain, Renewable Energy, Biotech,** and more. 
    Get personalized insights, skill gap analysis, and AI-powered career guidance.
    """)
    
    if st.button("🚀 Get Started", type="primary", use_container_width=True):
        st.switch_page("pages/2_Skill_Gap_Analysis.py")

# Enhanced Quick stats
st.markdown("### 📊 Industry Insights")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <h3 style="margin: 0 0 1rem 0;">🤖 AI Jobs</h3>
        <p style="font-size: 1.5em; margin: 0.5rem 0; font-weight: bold;">+22%</p>
        <p style="margin: 0.5rem 0;">growth rate</p>
        <p style="margin: 0.5rem 0;">$80K-$180K salary</p>
        <p style="font-size: 0.9em; margin-top: 1rem; opacity: 0.9;">🔥 High Demand</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <h3 style="margin: 0 0 1rem 0;">🔗 Blockchain</h3>
        <p style="font-size: 1.5em; margin: 0.5rem 0; font-weight: bold;">+35%</p>
        <p style="margin: 0.5rem 0;">growth rate</p>
        <p style="margin: 0.5rem 0;">$90K-$200K salary</p>
        <p style="font-size: 0.9em; margin-top: 1rem; opacity: 0.9;">🚀 Emerging</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <h3 style="margin: 0 0 1rem 0;">🌱 Clean Energy</h3>
        <p style="font-size: 1.5em; margin: 0.5rem 0; font-weight: bold;">+8%</p>
        <p style="margin: 0.5rem 0;">growth rate</p>
        <p style="margin: 0.5rem 0;">$65K-$120K salary</p>
        <p style="font-size: 0.9em; margin-top: 1rem; opacity: 0.9;">🌍 Sustainable</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <h3 style="margin: 0 0 1rem 0;">🔒 Cybersecurity</h3>
        <p style="font-size: 1.5em; margin: 0.5rem 0; font-weight: bold;">+35%</p>
        <p style="margin: 0.5rem 0;">growth rate</p>
        <p style="margin: 0.5rem 0;">$75K-$150K salary</p>
        <p style="font-size: 0.9em; margin-top: 1rem; opacity: 0.9;">🛡️ Critical</p>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Features section
st.markdown("### ✨ Platform Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4 style="color: #667eea; margin-bottom: 1rem;">🎯 Career Simulation</h4>
        <p style="line-height: 1.6;">Interactive career path exploration with real market data and personalized recommendations.</p>
        <p style="font-size: 0.9em; color: #667eea; margin-top: 1rem;"><strong>💡 Smart Analytics</strong></p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Try Career Simulation", key="sim"):
        st.switch_page("pages/1_Career_Simulation.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4 style="color: #667eea; margin-bottom: 1rem;">📊 Skill Gap Analysis</h4>
        <p style="line-height: 1.6;">Comprehensive skill assessment with learning roadmaps and industry benchmarks.</p>
        <p style="font-size: 0.9em; color: #667eea; margin-top: 1rem;"><strong>📈 Data-Driven</strong></p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Analyze Your Skills", key="skills"):
        st.switch_page("pages/2_Skill_Gap_Analysis.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4 style="color: #667eea; margin-bottom: 1rem;">🤖 AI Career Assistant</h4>
        <p style="line-height: 1.6;">24/7 AI-powered career counseling with personalized advice and industry insights.</p>
        <p style="font-size: 0.9em; color: #667eea; margin-top: 1rem;"><strong>🧠 AI-Powered</strong></p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Chat with AI Assistant", key="chat"):
        st.switch_page("pages/3_Career_Chat_Assistant.py")

# Enhanced Market trends chart with Plotly
st.markdown("### 📈 Emerging Industry Trends")

# Sample data for trends
trend_data = {
    'Industry': ['Artificial Intelligence', 'Blockchain & Web3', 'Renewable Energy', 
                'Biotechnology', 'Space Technology', 'Cybersecurity'],
    'Job Growth (%)': [22, 35, 8, 7, 6, 35],
    'Avg Salary (K)': [130, 145, 92, 105, 122, 112],
    'Market Size (B)': [190, 67, 300, 760, 400, 170],
    'Difficulty': ['High', 'Very High', 'Medium', 'High', 'Very High', 'High']
}

df = pd.DataFrame(trend_data)

# Create interactive bubble chart
fig = px.scatter(df, x='Job Growth (%)', y='Avg Salary (K)', 
                size='Market Size (B)', hover_name='Industry',
                title='🎯 Industry Growth vs Salary Potential vs Market Size',
                labels={'Job Growth (%)': 'Job Growth Rate (%)', 
                       'Avg Salary (K)': 'Average Salary ($K)',
                       'Market Size (B)': 'Market Size ($B)'},
                color='Difficulty',
                color_discrete_map={
                    'Medium': '#28a745',
                    'High': '#ffc107', 
                    'Very High': '#dc3545'
                },
                size_max=60)

fig.update_layout(
    height=600,
    showlegend=True,
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=12),
    title_font=dict(size=16, color='#333')
)

fig.update_traces(
    marker=dict(line=dict(width=2, color='white')),
    selector=dict(mode='markers')
)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Industry breakdown with radar chart
st.markdown("### 🔍 Industry Skill Requirements")

col1, col2 = st.columns(2)

with col1:
    # Radar chart for skill requirements
    categories = ['Technical Skills', 'Soft Skills', 'Experience Required', 
                 'Learning Curve', 'Market Demand', 'Salary Potential']
    
    ai_scores = [9, 7, 8, 8, 10, 9]
    blockchain_scores = [10, 6, 7, 9, 8, 10]
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=ai_scores,
        theta=categories,
        fill='toself',
        name='AI/ML',
        line_color='rgb(102, 126, 234)'
    ))
    
    fig_radar.add_trace(go.Scatterpolar(
        r=blockchain_scores,
        theta=categories,
        fill='toself',
        name='Blockchain',
        line_color='rgb(118, 75, 162)'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        title="AI vs Blockchain Skill Requirements",
        height=400
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

with col2:
    # Bar chart for salary comparison
    salary_data = {
        'Industry': ['AI/ML', 'Blockchain', 'Cybersecurity', 'Biotech', 'Clean Energy', 'Space Tech'],
        'Min Salary': [80, 90, 75, 70, 65, 85],
        'Max Salary': [180, 200, 150, 140, 120, 160]
    }
    
    salary_df = pd.DataFrame(salary_data)
    
    fig_salary = go.Figure()
    
    fig_salary.add_trace(go.Bar(
        name='Min Salary',
        x=salary_df['Industry'],
        y=salary_df['Min Salary'],
        marker_color='rgba(102, 126, 234, 0.7)'
    ))
    
    fig_salary.add_trace(go.Bar(
        name='Max Salary',
        x=salary_df['Industry'],
        y=salary_df['Max Salary'],
        marker_color='rgba(118, 75, 162, 0.7)'
    ))
    
    fig_salary.update_layout(
        title='💰 Salary Ranges by Industry',
        xaxis_title='Industry',
        yaxis_title='Salary ($K)',
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig_salary, use_container_width=True)

# Enhanced Success stories section
st.markdown("### 🌟 Success Stories")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="success-story">
        <h4 style="color: #28a745; margin-bottom: 1rem;">👨‍💻 From Accountant to AI Engineer</h4>
        <p style="line-height: 1.6; margin-bottom: 1rem;">"Used Career Shift Analyzer to transition from finance to AI. 
        The skill gap analysis showed me exactly what to learn. 
        Now earning 60% more at a tech startup!"</p>
        <p style="font-style: italic; margin-bottom: 1rem;"><em>- Sarah, AI Engineer</em></p>
        <div style="margin-top: 1.5rem;">
            <span style="background: #28a745; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8em; margin-right: 0.5rem;">
                ✅ 8 months transition
            </span>
            <span style="background: #17a2b8; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8em;">
                💰 +60% salary
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="success-story">
        <h4 style="color: #28a745; margin-bottom: 1rem;">🚀 Blockchain Developer Journey</h4>
        <p style="line-height: 1.6; margin-bottom: 1rem;">"The platform's learning roadmap guided me from zero coding 
        experience to landing a blockchain developer role in 8 months. 
        The AI assistant was incredibly helpful!"</p>
        <p style="font-style: italic; margin-bottom: 1rem;"><em>- Ahmad, Blockchain Developer</em></p>
        <div style="margin-top: 1.5rem;">
            <span style="background: #6f42c1; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8em; margin-right: 0.5rem;">
                🚀 Zero to Hero
            </span>
            <span style="background: #fd7e14; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8em;">
                🎯 Remote Job
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Industry overview with enhanced styling
st.markdown("### 🌟 Industry Overview")
st.markdown("""
<div class="industry-grid">
    <div class="industry-item">
        <h4 style="color: #667eea; margin-bottom: 1rem;">🤖 Artificial Intelligence</h4>
        <p><strong>Hot Skills:</strong> Python, Machine Learning, Deep Learning</p>
        <p><strong>Outlook:</strong> Extremely High Demand</p>
    </div>
    <div class="industry-item">
        <h4 style="color: #667eea; margin-bottom: 1rem;">🔗 Blockchain & Web3</h4>
        <p><strong>Hot Skills:</strong> Solidity, Smart Contracts, DeFi</p>
        <p><strong>Outlook:</strong> Rapid Growth Expected</p>
    </div>
    <div class="industry-item">
        <h4 style="color: #667eea; margin-bottom: 1rem;">🌱 Renewable Energy</h4>
        <p><strong>Hot Skills:</strong> Solar Tech, Sustainability, Engineering</p>
        <p><strong>Outlook:</strong> Steady Long-term Growth</p>
    </div>
    <div class="industry-item">
        <h4 style="color: #667eea; margin-bottom: 1rem;">🧬 Biotechnology</h4>
        <p><strong>Hot Skills:</strong> Bioinformatics, Genetics, Lab Skills</p>
        <p><strong>Outlook:</strong> Innovation-driven Growth</p>
    </div>
    <div class="industry-item">
        <h4 style="color: #667eea; margin-bottom: 1rem;">🚀 Space Technology</h4>
        <p><strong>Hot Skills:</strong> Aerospace, Physics, Navigation</p>
        <p><strong>Outlook:</strong> Emerging High-impact Sector</p>
    </div>
    <div class="industry-item">
        <h4 style="color: #667eea; margin-bottom: 1rem;">🔒 Cybersecurity</h4>
        <p><strong>Hot Skills:</strong> Network Security, Penetration Testing</p>
        <p><strong>Outlook:</strong> Critical and Fast-growing</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced Quick actions
st.markdown("### 🎯 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📋 Take Skill Assessment", use_container_width=True, type="secondary"):
        st.switch_page("pages/2_Skill_Gap_Analysis.py")

with col2:
    if st.button("💬 Ask AI Career Question", use_container_width=True, type="secondary"):
        st.switch_page("pages/3_Career_Chat_Assistant.py")

with col3:
    if st.button("🎓 View Learning Paths", use_container_width=True, type="secondary"):
        st.info("🚧 Advanced feature coming soon!")

with col4:
    if st.button("📊 Industry Reports", use_container_width=True, type="secondary"):
        st.info("💎 Premium feature - coming soon!")

# Enhanced Universal Footer with Team Credits
def render_enhanced_footer():
    current_year = datetime.now().year
    last_updated = datetime.now().strftime("%B %d, %Y")
    
    footer_html = f"""
    <div class="universal-footer">
        <div class="footer-grid">
            <div class="footer-section">
                <h4>🚀 Career Shift Analyzer Pro</h4>
                <p><span class="status-indicator"></span><strong>Status:</strong> Online & Active</p>
                <p><strong>Version:</strong> v{version}</p>
                <p><strong>Last Updated:</strong> {last_updated}</p>
                <p><strong>Build:</strong> Production</p>
                <div class="team-section">
                    <h5 style="color: #ffd700; margin-bottom: 1.5rem; text-align: center; font-size: 1.1em;">👥 Development Team</h5>
                    <div class="team-members">
                        <div class="team-member">
                            <strong>🎯 MS Hadianto</strong>
                            <span style="font-size: 0.9em; color: rgba(255,255,255,0.9);">Lead Project &<br>Architecture</span>
                        </div>
                        <div class="team-member">
                            <strong>🤝 Faby</strong>
                            <span style="font-size: 0.9em; color: rgba(255,255,255,0.9);">Co-Lead &<br>Development</span>
                        </div>
                    </div>
                    <p style="margin-top: 1.5rem; font-size: 0.9em; color: rgba(255,255,255,0.8); text-align: center;">
                        <em>Collaborative innovation for empowering career advancement worldwide</em>
                    </p>
                </div>
            </div>
            
            <div class="footer-section">
                <h4>⚖️ Important Disclaimer</h4>
                <div class="disclaimer-box">
                    <p style="margin-bottom: 1rem;"><strong>⚠️ Please Read Carefully:</strong></p>
                    <ul style="list-style: none; padding: 0; font-size: 0.85em; line-height: 1.5;">
                        <li>• Career advice provided for informational purposes only</li>
                        <li>• AI responses are automated, not professional counseling</li>
                        <li>• Salary data are market estimates, actual may vary significantly</li>
                        <li>• Individual results depend on personal circumstances</li>
                        <li>• Always verify information with official industry sources</li>
                        <li>• Not a substitute for professional career counseling services</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-section">
                <h4>🔒 Privacy & Data Protection</h4>
                <div class="disclaimer-box">
                    <p style="margin-bottom: 1rem;"><strong>🛡️ Your Data Security:</strong></p>
                    <ul style="list-style: none; padding: 0; font-size: 0.85em; line-height: 1.5;">
                        <li>• No personal data permanently stored on our servers</li>
                        <li>• Chat sessions are temporary and session-based only</li>
                        <li>• Skill assessments processed locally in your browser</li>
                        <li>• Third-party APIs governed by separate privacy policies</li>
                        <li>• All session data automatically cleared on browser close</li>
                        <li>• No tracking cookies or analytics collection</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-section">
                <h4>🛠️ Technical Stack & Info</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; margin: 1rem 0;">
                    <div style="background: rgba(255,255,255,0.1); padding: 0.5rem; border-radius: 8px; text-align: center; font-size: 0.8em;">
                        🐍 Python 3.11
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 0.5rem; border-radius: 8px; text-align: center; font-size: 0.8em;">
                        ⚡ Streamlit
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 0.5rem; border-radius: 8px; text-align: center; font-size: 0.8em;">
                        📊 Plotly
                    </div>
                    <div style="background: rgba(255,255,255,0.1); padding: 0.5rem; border-radius: 8px; text-align: center; font-size: 0.8em;">
                        🤖 Llama 3.2
                    </div>
                </div>
                <div style="margin-top: 1.5rem;">
                    <p><strong>AI Model:</strong> Meta Llama 3.2 via OpenRouter</p>
                    <p><strong>Hosting:</strong> Streamlit Cloud Platform</p>
                    <p><strong>Data Source:</strong> Real-time industry research</p>
                    <p><strong>Updates:</strong> Continuous deployment pipeline</p>
                </div>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p style="font-size: 1.1em; margin-bottom: 1rem; font-weight: bold;">
                <strong>© {current_year} Career Shift Analyzer Pro v{version}</strong>
            </p>
            <p style="margin: 0.8rem 0; font-size: 1em;">
                <strong>👥 Proudly Developed by:</strong> 
                <span style="color: #ffd700; font-weight: bold;">MS Hadianto</span> (Lead Project) & 
                <span style="color: #ffd700; font-weight: bold;">Faby</span> (Co-Lead)
            </p>
            <p style="margin: 1.2rem 0; font-size: 0.85em; line-height: 1.5; color: rgba(255,255,255,0.9);">
                <em><strong>Legal Notice:</strong> This platform provides general career guidance and educational content. 
                It is not a substitute for professional career counseling, financial advice, or job placement services. 
                Users should independently verify all information and consult qualified professionals for personalized advice. 
                Use of this platform constitutes acceptance of our terms and disclaimer.</em>
            </p>
            <p style="margin-top: 2rem; font-size: 0.95em;">
                🌟 <strong>Open Source Project</strong> | 
                <a href="https://github.com/mshadianto/career_shift_analyzer" target="_blank" class="footer-link">
                    📚 View on GitHub
                </a> | 
                <a href="mailto:support@careershiftanalyzer.com" class="footer-link">
                    📧 Contact Support
                </a>
            </p>
            <p style="margin-top: 1rem; font-size: 1em; color: #ffd700; font-weight: 500;">
                Built with ❤️ for empowering career advancement worldwide
            </p>
        </div>
    </div>
    """
    
    st.markdown("---")
    st.markdown(footer_html, unsafe_allow_html=True)

# Render enhanced footer
render_enhanced_footer()