import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Skill Gap Analysis", layout="wide")
st.title("📊 Skill Gap Analysis")
st.markdown("""
Bandingkan skill yang Anda miliki dengan skill yang dibutuhkan di industri masa depan.
Dapatkan analisis mendalam dan roadmap pembelajaran yang personal! 🎯
""")

# Enhanced skill mapping with more details
skill_targets = {
    "Artificial Intelligence": {
        "technical": ["python", "tensorflow", "pytorch", "machine learning", "deep learning", "sql", "statistics"],
        "soft": ["problem solving", "critical thinking", "research"],
        "tools": ["jupyter", "git", "docker", "aws", "google cloud"],
        "salary_range": "$80,000 - $180,000",
        "growth_rate": "22% (Much faster than average)"
    },
    "Blockchain & Web3": {
        "technical": ["solidity", "smart contracts", "cryptography", "defi", "nft", "ethereum", "javascript"],
        "soft": ["attention to detail", "security mindset", "innovation"],
        "tools": ["remix", "truffle", "metamask", "hardhat"],
        "salary_range": "$90,000 - $200,000",
        "growth_rate": "35% (Extremely fast growth)"
    },
    "Renewable Energy": {
        "technical": ["solar technology", "wind energy", "energy storage", "electrical engineering", "sustainability"],
        "soft": ["environmental awareness", "project management", "collaboration"],
        "tools": ["autocad", "matlab", "pvsyst", "homer"],
        "salary_range": "$65,000 - $120,000",
        "growth_rate": "8% (Much faster than average)"
    },
    "Biotechnology": {
        "technical": ["bioinformatics", "genetics", "molecular biology", "lab techniques", "data analysis"],
        "soft": ["attention to detail", "patience", "scientific method"],
        "tools": ["r", "python", "blast", "laboratory equipment"],
        "salary_range": "$70,000 - $140,000",
        "growth_rate": "7% (Faster than average)"
    },
    "Space Technology": {
        "technical": ["aerospace engineering", "physics", "mathematics", "navigation", "satellite technology"],
        "soft": ["precision", "teamwork", "problem solving"],
        "tools": ["matlab", "simulink", "cad software", "mission planning"],
        "salary_range": "$85,000 - $160,000",
        "growth_rate": "6% (As fast as average, but high impact)"
    },
    "Cybersecurity": {
        "technical": ["network security", "penetration testing", "incident response", "risk assessment", "compliance"],
        "soft": ["analytical thinking", "continuous learning", "communication"],
        "tools": ["wireshark", "metasploit", "nmap", "burp suite"],
        "salary_range": "$75,000 - $150,000",
        "growth_rate": "35% (Much faster than average)"
    }
}

# Sidebar for field selection
st.sidebar.header("🎯 Pilih Bidang Karir")
selected_field = st.sidebar.selectbox(
    "Industri masa depan:",
    list(skill_targets.keys()),
    help="Pilih bidang yang ingin Anda analisis"
)

# Display field info
field_data = skill_targets[selected_field]
st.sidebar.markdown(f"""
### 📈 Info Industri
**💰 Salary Range:** {field_data['salary_range']}  
**📊 Growth Rate:** {field_data['growth_rate']}
""")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"🔍 Analisis untuk {selected_field}")
    
    # Skill input
    skills_user = st.text_area(
        "Masukkan skill yang Anda miliki (pisahkan dengan koma):",
        placeholder="Contoh: python, teamwork, excel, problem solving, git",
        help="Tulis semua skill Anda, baik technical maupun soft skills"
    )

with col2:
    st.subheader("💡 Tips Input")
    st.info("""
    **Include both:**
    - Technical skills (programming, tools)
    - Soft skills (communication, leadership)
    - Tools & platforms you've used
    """)

if st.button("🔎 Lihat Analisis Skill Gap", type="primary"):
    if skills_user.strip():
        user_skills = [s.strip().lower() for s in skills_user.split(",")]
        
        # Combine all required skills
        all_required = field_data["technical"] + field_data["soft"] + field_data["tools"]
        
        # Calculate matches
        technical_match = [s for s in user_skills if s in [skill.lower() for skill in field_data["technical"]]]
        soft_match = [s for s in user_skills if s in [skill.lower() for skill in field_data["soft"]]]
        tools_match = [s in user_skills if s in [skill.lower() for skill in field_data["tools"]]]
        
        # Calculate gaps
        technical_gap = [s for s in field_data["technical"] if s.lower() not in [skill.lower() for skill in user_skills]]
        soft_gap = [s for s in field_data["soft"] if s.lower() not in [skill.lower() for skill in user_skills]]
        tools_gap = [s for s in field_data["tools"] if s.lower() not in [skill.lower() for skill in user_skills]]
        
        # Overall score
        total_required = len(all_required)
        total_matched = len(technical_match) + len(soft_match) + len(tools_match)
        skill_percentage = (total_matched / total_required * 100) if total_required > 0 else 0
        
        # Results section
        st.markdown("---")
        st.subheader("📊 Hasil Analisis")
        
        # Score display
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📈 Overall Score", f"{skill_percentage:.1f}%")
        with col2:
            st.metric("✅ Skills Matched", f"{total_matched}/{total_required}")
        with col3:
            st.metric("🔧 Technical Skills", f"{len(technical_match)}/{len(field_data['technical'])}")
        with col4:
            st.metric("🤝 Soft Skills", f"{len(soft_match)}/{len(field_data['soft'])}")
        
        # Progress bar
        st.progress(skill_percentage / 100)
        
        # Detailed breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ Skills yang Sudah Dimiliki")
            if technical_match:
                st.success("**🔧 Technical Skills:**")
                for skill in technical_match:
                    st.write(f"• {skill.title()}")
            
            if soft_match:
                st.success("**🤝 Soft Skills:**")
                for skill in soft_match:
                    st.write(f"• {skill.title()}")
            
            if tools_match:
                st.success("**🛠️ Tools:**")
                for skill in tools_match:
                    st.write(f"• {skill.title()}")
        
        with col2:
            st.subheader("❌ Skills yang Perlu Dipelajari")
            if technical_gap:
                st.error("**🔧 Technical Skills:**")
                for skill in technical_gap:
                    st.write(f"• {skill.title()}")
            
            if soft_gap:
                st.error("**🤝 Soft Skills:**")
                for skill in soft_gap:
                    st.write(f"• {skill.title()}")
            
            if tools_gap:
                st.error("**🛠️ Tools:**")
                for skill in tools_gap:
                    st.write(f"• {skill.title()}")
        
        # Radar chart
        if total_required > 0:
            st.subheader("🎯 Skill Radar Chart")
            
            categories = ['Technical', 'Soft Skills', 'Tools']
            current_scores = [
                len(technical_match) / len(field_data["technical"]) * 100 if field_data["technical"] else 0,
                len(soft_match) / len(field_data["soft"]) * 100 if field_data["soft"] else 0,
                len(tools_match) / len(field_data["tools"]) * 100 if field_data["tools"] else 0
            ]
            target_scores = [100, 100, 100]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=current_scores,
                theta=categories,
                fill='toself',
                name='Current Level',
                line_color='rgb(0, 123, 255)'
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=target_scores,
                theta=categories,
                fill='toself',
                name='Target Level',
                line_color='rgb(255, 99, 132)',
                opacity=0.3
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="Skill Level Comparison"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Learning recommendations
        st.subheader("🎓 Rekomendasi Learning Path")
        
        priority_skills = technical_gap[:3] + soft_gap[:2] + tools_gap[:2]
        
        if priority_skills:
            st.info("**🚀 Priority Skills to Learn (Top recommendations):**")
            
            learning_resources = {
                "python": "https://www.codecademy.com/learn/learn-python-3",
                "machine learning": "https://www.coursera.org/learn/machine-learning",
                "javascript": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/",
                "solidity": "https://cryptozombies.io/",
                "problem solving": "https://www.coursera.org/learn/creative-problem-solving",
                "git": "https://learngitbranching.js.org/"
            }
            
            for i, skill in enumerate(priority_skills[:5], 1):
                resource_url = learning_resources.get(skill.lower(), f"https://www.coursera.org/search?query={skill}")
                st.markdown(f"**{i}. {skill.title()}** → [📚 Learn Here]({resource_url})")
        else:
            st.success("🎉 Congratulations! You have all the essential skills for this field!")
            st.balloons()
    
    else:
        st.warning("⚠️ Please enter your skills to get analysis.")

st.markdown("---")
st.caption("© 2025 Career Shift Analyzer | Data based on industry research and job market trends")

# footer_component.py - Universal Footer for All Pages
# Place this code at the bottom of EVERY page file

import streamlit as st
from datetime import datetime
import os

def render_universal_footer():
    """Universal Footer Component with Team Credits and Disclaimer"""
    
    def get_app_version():
        """Get app version dynamically"""
        try:
            env_version = os.getenv('APP_VERSION')
            if env_version:
                return env_version
            base_version = "1.4"
            build_number = datetime.now().strftime("%y%m%d")
            return f"{base_version}.{build_number}"
        except:
            return "1.0.0"
    
    version = get_app_version()
    current_year = datetime.now().year
    last_updated = datetime.now().strftime("%B %d, %Y")
    
    # Universal Footer CSS
    st.markdown("""
    <style>
    .universal-footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 1rem;
        border-radius: 15px;
        margin-top: 3rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
    }
    .footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    .footer-section h4 {
        color: #ffd700;
        margin-bottom: 1rem;
        font-size: 1.1em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .disclaimer-box {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-size: 0.85em;
        backdrop-filter: blur(5px);
    }
    .team-section {
        background: rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,215,0,0.3);
    }
    .team-members {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    .team-member {
        background: rgba(255,255,255,0.2);
        padding: 1rem 1.5rem;
        border-radius: 20px;
        border: 2px solid rgba(255,215,0,0.5);
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
        text-align: center;
        min-width: 140px;
    }
    .team-member:hover {
        transform: translateY(-5px);
        border-color: #ffd700;
        box-shadow: 0 10px 25px rgba(255,215,0,0.3);
        background: rgba(255,255,255,0.25);
    }
    .team-member strong {
        color: #ffd700;
        font-size: 1em;
        display: block;
        margin-bottom: 0.3rem;
    }
    .team-member span {
        font-size: 0.8em;
        color: rgba(255,255,255,0.9);
        line-height: 1.2;
    }
    .footer-bottom {
        border-top: 1px solid rgba(255,255,255,0.2);
        padding-top: 1.5rem;
        text-align: center;
        font-size: 0.85em;
        color: rgba(255,255,255,0.95);
    }
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #00ff00;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
    }
    .tech-stack {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 0.5rem;
        margin: 0.5rem 0;
    }
    .tech-item {
        background: rgba(255,255,255,0.1);
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8em;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    .footer-link {
        color: #ffd700;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .footer-link:hover {
        color: #fff;
        text-shadow: 0 0 10px #ffd700;
    }
    .version-badge {
        background: rgba(255,215,0,0.2);
        color: #ffd700;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-weight: bold;
        border: 1px solid rgba(255,215,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Footer HTML Content
    footer_html = f"""
    <div class="universal-footer">
        <div class="footer-grid">
            <!-- App Info Section -->
            <div class="footer-section">
                <h4>🚀 Career Shift Analyzer</h4>
                <p><span class="status-indicator"></span><strong>Status:</strong> Online & Active</p>
                <p><strong>Version:</strong> <span class="version-badge">v{version}</span></p>
                <p><strong>Last Updated:</strong> {last_updated}</p>
                <p><strong>Environment:</strong> Production</p>
                
                <div class="team-section">
                    <h5 style="color: #ffd700; margin-bottom: 1rem; text-align: center;">👥 Development Team</h5>
                    <div class="team-members">
                        <div class="team-member">
                            <strong>🎯 MS Hadianto</strong>
                            <span>Lead Project &<br>Architecture</span>
                        </div>
                        <div class="team-member">
                            <strong>🤝 Faby</strong>
                            <span>Co-Lead &<br>Development</span>
                        </div>
                    </div>
                    <p style="text-align: center; font-size: 0.85em; color: rgba(255,255,255,0.8); margin-top: 1rem;">
                        <em>Collaborative innovation for career advancement</em>
                    </p>
                </div>
            </div>
            
            <!-- Legal Disclaimer Section -->
            <div class="footer-section">
                <h4>⚖️ Legal Disclaimer</h4>
                <div class="disclaimer-box">
                    <p><strong>⚠️ Important Notice:</strong></p>
                    <ul style="list-style: none; padding: 0; font-size: 0.85em; line-height: 1.4;">
                        <li>• Career advice for informational purposes only</li>
                        <li>• AI responses are automated, not professional counseling</li>
                        <li>• Salary estimates based on market research, may vary</li>
                        <li>• Individual results depend on personal circumstances</li>
                        <li>• Always verify information with official sources</li>
                        <li>• Not a substitute for professional career counseling</li>
                    </ul>
                </div>
            </div>
            
            <!-- Privacy & Data Section -->
            <div class="footer-section">
                <h4>🔒 Privacy & Data</h4>
                <div class="disclaimer-box">
                    <p><strong>🛡️ Data Protection:</strong></p>
                    <ul style="list-style: none; padding: 0; font-size: 0.85em; line-height: 1.4;">
                        <li>• No personal data permanently stored</li>
                        <li>• Chat sessions are temporary & session-based</li>
                        <li>• Skill assessments processed locally</li>
                        <li>• Third-party APIs governed by separate policies</li>
                        <li>• All session data cleared on browser close</li>
                        <li>• No tracking or analytics cookies</li>
                    </ul>
                </div>
            </div>
            
            <!-- Technical Stack Section -->
            <div class="footer-section">
                <h4>🛠️ Technical Stack</h4>
                <div class="tech-stack">
                    <div class="tech-item">🐍 Python 3.11</div>
                    <div class="tech-item">⚡ Streamlit</div>
                    <div class="tech-item">📊 Plotly</div>
                    <div class="tech-item">🤖 Llama 3.2</div>
                    <div class="tech-item">☁️ Cloud Hosted</div>
                    <div class="tech-item">📱 Responsive</div>
                </div>
                <div style="margin-top: 1rem;">
                    <p><strong>AI Model:</strong> Meta Llama 3.2 via OpenRouter</p>
                    <p><strong>Hosting:</strong> Streamlit Cloud Platform</p>
                    <p><strong>Data Source:</strong> Real-time industry research</p>
                    <p><strong>Updates:</strong> Continuous deployment</p>
                </div>
            </div>
        </div>
        
        <!-- Footer Bottom -->
        <div class="footer-bottom">
            <p style="font-size: 1em; margin-bottom: 0.8rem;">
                <strong>© {current_year} Career Shift Analyzer v{version}</strong>
            </p>
            <p style="margin: 0.5rem 0; font-size: 0.95em;">
                <strong>👥 Proudly Developed by:</strong> 
                <span style="color: #ffd700; font-weight: bold;">MS Hadianto</span> (Lead Project) & 
                <span style="color: #ffd700; font-weight: bold;">Faby</span> (Co-Lead)
            </p>
            <p style="margin: 1rem 0; font-size: 0.8em; line-height: 1.4; color: rgba(255,255,255,0.9);">
                <em><strong>Legal Notice:</strong> This platform provides general career guidance and educational content. 
                It is not a substitute for professional career counseling, financial advice, or job placement services. 
                Users should independently verify all information and consult qualified professionals for personalized advice. 
                Use of this platform constitutes acceptance of our terms and disclaimer.</em>
            </p>
            <p style="margin-top: 1.5rem;">
                🌟 <strong>Open Source Project</strong> | 
                <a href="https://github.com/mshadianto/career_shift_analyzer" target="_blank" class="footer-link">
                    📚 View on GitHub
                </a> | 
                <a href="mailto:support@careershiftanalyzer.com" class="footer-link">
                    📧 Contact Support
                </a>
            </p>
            <p style="margin-top: 0.5rem; font-size: 0.9em; color: #ffd700;">
                Built with ❤️ for empowering career advancement worldwide
            </p>
        </div>
    </div>
    """
    
    # Render the footer
    st.markdown("---")  # Separator line
    st.markdown(footer_html, unsafe_allow_html=True)

# =============================================================================
# USAGE INSTRUCTIONS:
# =============================================================================
# 
# Add this code at the BOTTOM of EVERY page file:
#
# # At the end of main.py:
# render_universal_footer()
#
# # At the end of pages/1_Career_Simulation.py:
# render_universal_footer()
#
# # At the end of pages/2_Skill_Gap_Analysis.py:
# render_universal_footer()
#
# # At the end of pages/3_Career_Chat_Assistant.py:
# render_universal_footer()
#
# =============================================================================