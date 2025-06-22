import streamlit as st
import requests
import json
from datetime import datetime
import os

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
            "model": "meta-llama/llama-3.2-3b-instruct:free",
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

# Universal Footer
def render_universal_footer():
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
    
    version = get_app_version()
    current_year = datetime.now().year
    last_updated = datetime.now().strftime("%B %d, %Y")
    
    # Footer CSS
    st.markdown("""
    <style>
    .universal-footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 1rem;
        border-radius: 15px;
        margin-top: 3rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
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
    }
    .disclaimer-box {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-size: 0.85em;
    }
    .team-section {
        background: rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
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
        text-align: center;
        min-width: 140px;
    }
    .team-member:hover {
        transform: translateY(-5px);
        border-color: #ffd700;
        box-shadow: 0 10px 25px rgba(255,215,0,0.3);
    }
    .team-member strong {
        color: #ffd700;
        font-size: 1em;
        display: block;
        margin-bottom: 0.3rem;
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
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
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
    </style>
    """, unsafe_allow_html=True)
    
    # Footer HTML
    footer_html = f"""
    <div class="universal-footer">
        <div class="footer-grid">
            <div class="footer-section">
                <h4>🚀 Career Shift Analyzer</h4>
                <p><span class="status-indicator"></span><strong>Status:</strong> Online</p>
                <p><strong>Version:</strong> v{version}</p>
                <p><strong>Updated:</strong> {last_updated}</p>
                
                <div class="team-section">
                    <h5 style="color: #ffd700; margin-bottom: 1rem; text-align: center;">👥 Development Team</h5>
                    <div class="team-members">
                        <div class="team-member">
                            <strong>🎯 MS Hadianto</strong>
                            <span style="font-size: 0.8em;">Lead Project</span>
                        </div>
                        <div class="team-member">
                            <strong>🤝 Faby</strong>
                            <span style="font-size: 0.8em;">Co-Lead</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="footer-section">
                <h4>⚖️ Legal Disclaimer</h4>
                <div class="disclaimer-box">
                    <ul style="list-style: none; padding: 0; font-size: 0.85em;">
                        <li>• Career advice for informational purposes only</li>
                        <li>• AI responses are automated, not professional counseling</li>
                        <li>• Salary data are estimates, actual may vary</li>
                        <li>• Always verify with official sources</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-section">
                <h4>🔒 Privacy & Data</h4>
                <div class="disclaimer-box">
                    <ul style="list-style: none; padding: 0; font-size: 0.85em;">
                        <li>• No personal data permanently stored</li>
                        <li>• Chat sessions are temporary</li>
                        <li>• Skill assessments processed locally</li>
                        <li>• Session data cleared on browser close</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer-section">
                <h4>🛠️ Technical</h4>
                <p><strong>AI Model:</strong> Meta Llama 3.2</p>
                <p><strong>Hosting:</strong> Streamlit Cloud</p>
                <p><strong>Language:</strong> Python 3.11</p>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p><strong>© {current_year} Career Shift Analyzer v{version}</strong></p>
            <p style="margin: 0.5rem 0;">
                <strong>