import streamlit as st
import requests
import json

st.set_page_config(page_title="Career Chat Assistant", layout="wide")

st.title("🤖 Career Chat Assistant")
st.markdown("""
Tanyakan apa saja seputar pergeseran karier ke industri masa depan seperti AI, Blockchain, BioTech, dsb. 
Jawaban dihasilkan oleh model AI melalui OpenRouter. 🧠
""")

# Suggested questions
st.subheader("💡 Pertanyaan Populer:")
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Gimana prediksi mu karir komite audit 5 tahun mendatang?"):
        st.session_state.suggested_question = "Gimana prediksi mu karir komite audit 5 tahun mendatang?"
    if st.button("💼 Skill apa yang dibutuhkan untuk AI Engineer?"):
        st.session_state.suggested_question = "Skill apa yang dibutuhkan untuk AI Engineer?"

with col2:
    if st.button("🔗 Bagaimana prospek karir di blockchain?"):
        st.session_state.suggested_question = "Bagaimana prospek karir di blockchain?"
    if st.button("🎯 Tips transisi karir ke tech industry?"):
        st.session_state.suggested_question = "Tips transisi karir ke tech industry?"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to get AI response
def get_ai_response(question):
    try:
        # Check if API key exists
        if "openrouter" not in st.secrets or not st.secrets.openrouter.get("api_key"):
            return "⚠️ API key OpenRouter belum di-setup. Silakan tambahkan di Streamlit Cloud Settings → Secrets."
        
        api_key = st.secrets.openrouter["api_key"]
        
        # OpenRouter API call with free model
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Title": "Career Shift Analyzer"
        }
        
        data = {
            "model": "meta-llama/llama-3.2-3b-instruct:free",  # Free model
            "messages": [
                {
                    "role": "system", 
                    "content": "Kamu adalah konsultan karir yang ahli dalam industri masa depan seperti AI, blockchain, biotech, renewable energy, dan space tech. Berikan saran yang praktis dan actionable dalam bahasa Indonesia."
                },
                {"role": "user", "content": question}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        elif response.status_code == 401:
            return "🔑 API key tidak valid. Silakan periksa kembali API key OpenRouter Anda."
        elif response.status_code == 402:
            return "💳 Credit OpenRouter habis. Silakan top-up di openrouter.ai/credits"
        else:
            return f"❌ Error {response.status_code}: {response.text}"
            
    except requests.exceptions.Timeout:
        return "⏱️ Request timeout. Silakan coba lagi."
    except requests.exceptions.RequestException as e:
        return f"🌐 Network error: {str(e)}"
    except Exception as e:
        return f"🚫 Unexpected error: {str(e)}"

# Handle suggested questions
if "suggested_question" in st.session_state:
    question = st.session_state.suggested_question
    del st.session_state.suggested_question
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(question)
    
    # Get and display AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Sedang berpikir..."):
            response = get_ai_response(question)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Chat input
if prompt := st.chat_input("Tanyakan sesuatu tentang karier masa depan..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get and display AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Sedang berpikir..."):
            response = get_ai_response(prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.markdown("---")
st.caption("© 2025 Career Shift Analyzer | Powered by Llama 3.2 via OpenRouter")

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