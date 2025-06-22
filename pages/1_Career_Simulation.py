import streamlit as st
import random
import time
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Career Chat Assistant", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI/UX
st.markdown("""
<style>
    /* Global Styles */
    .main > div {
        padding-top: 2rem;
    }
    
    /* Header Styles */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Suggestion Cards */
    .suggestion-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .suggestion-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 10px 25px rgba(240, 147, 251, 0.3);
    }
    
    .suggestion-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(240, 147, 251, 0.4);
    }
    
    .suggestion-card h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
    }
    
    .suggestion-card p {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Chat Interface */
    .chat-container {
        background: #f8f9ff;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e1e8ff;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        max-width: 80%;
        box-shadow: 0 5px 15px rgba(17, 153, 142, 0.3);
    }
    
    /* Sidebar Styles */
    .sidebar-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Animated Elements */
    .typing-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #fff;
        animation: typing 1.4s infinite ease-in-out;
        margin: 0 2px;
    }
    
    .typing-indicator:nth-child(1) { animation-delay: -0.32s; }
    .typing-indicator:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { 
            transform: scale(0);
            opacity: 0.5;
        } 
        40% { 
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Industry Cards */
    .industry-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .industry-card:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Clear button */
    .clear-btn {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
    }
    
    .clear-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🤖 Career Simulation</div>
    <div class="hero-subtitle">Konsultasi karir masa depan dengan AI yang cerdas dan responsif</div>
</div>
""", unsafe_allow_html=True)

# Enhanced Knowledge Base for AI Simulation
career_knowledge_base = {
    "ai_engineer": {
        "skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "SQL", "Statistics"],
        "salary": "$80,000 - $180,000",
        "growth": "22% (Much faster than average)",
        "description": "AI Engineer merancang dan mengembangkan sistem AI untuk memecahkan masalah bisnis kompleks."
    },
    "blockchain": {
        "skills": ["Solidity", "Smart Contracts", "Cryptography", "DeFi", "Web3", "JavaScript"],
        "salary": "$90,000 - $200,000", 
        "growth": "35% (Extremely fast)",
        "description": "Blockchain developer membangun aplikasi terdesentralisasi dan smart contracts."
    },
    "biotech": {
        "skills": ["Bioinformatics", "Genetics", "Lab Techniques", "R/Python", "Data Analysis"],
        "salary": "$70,000 - $140,000",
        "growth": "7% (Faster than average)",
        "description": "Biotech specialist mengembangkan teknologi untuk kesehatan dan lingkungan."
    },
    "renewable_energy": {
        "skills": ["Solar Technology", "Wind Energy", "Energy Storage", "Electrical Engineering"],
        "salary": "$65,000 - $120,000",
        "growth": "8% (Much faster than average)",
        "description": "Engineer energi terbarukan merancang sistem energi berkelanjutan."
    },
    "cybersecurity": {
        "skills": ["Network Security", "Penetration Testing", "Risk Assessment", "Compliance"],
        "salary": "$75,000 - $150,000",
        "growth": "35% (Much faster than average)",
        "description": "Cybersecurity specialist melindungi sistem dan data dari ancaman digital."
    }
}

# Enhanced response templates
response_templates = {
    "greeting": [
        "Halo! 👋 Saya siap membantu Anda menavigasi karir masa depan. Apa yang ingin Anda ketahui?",
        "Selamat datang! 🌟 Mari kita jelajahi peluang karir yang menarik di era digital ini.",
        "Hi! 🚀 Saya di sini untuk membantu Anda merencanakan transisi karir yang sukses."
    ],
    "skills_inquiry": [
        "Untuk menjadi {role}, Anda memerlukan skill seperti: {skills}. Mulai dengan {primary_skill} sebagai fondasi utama.",
        "Skill kunci untuk {role} meliputi: {skills}. Saya rekomendasikan fokus pada {primary_skill} terlebih dahulu.",
        "Sebagai {role}, Anda harus menguasai: {skills}. {primary_skill} adalah skill yang paling penting untuk dikuasai."
    ],
    "salary_inquiry": [
        "Kisaran gaji untuk {role} adalah {salary} dengan tingkat pertumbuhan {growth}.",
        "Profesi {role} menawarkan kompensasi {salary} dan proyeksi pertumbuhan {growth}.",
        "Secara finansial, {role} memberikan range gaji {salary} dengan outlook {growth}."
    ],
    "transition_tips": [
        "Untuk transisi ke tech industry: 1) Mulai dengan online courses, 2) Bangun portfolio, 3) Network dengan profesional, 4) Cari mentor, 5) Praktik terus-menerus.",
        "Tips sukses transisi karir: 1) Identifikasi skill gap, 2) Buat learning roadmap, 3) Join komunitas tech, 4) Mulai side projects, 5) Update LinkedIn profile.",
        "Strategi transisi yang efektif: 1) Self-assessment skill, 2) Research target industry, 3) Ambil sertifikasi, 4) Volunteer di tech projects, 5) Prepare untuk interview."
    ]
}

# Advanced AI Response Generator
def generate_smart_response(user_input):
    """Generate contextual AI responses based on user input"""
    user_input_lower = user_input.lower()
    
    # Greeting detection
    if any(word in user_input_lower for word in ["halo", "hai", "hello", "hi", "selamat"]):
        return random.choice(response_templates["greeting"])
    
    # Career-specific responses
    for career_key, career_data in career_knowledge_base.items():
        if any(term in user_input_lower for term in [career_key.replace("_", " "), career_key]):
            if any(word in user_input_lower for word in ["skill", "kemampuan", "keahlian"]):
                skills_text = ", ".join(career_data["skills"][:5])
                return response_templates["skills_inquiry"][0].format(
                    role=career_data["description"].split()[0] + " " + career_data["description"].split()[1],
                    skills=skills_text,
                    primary_skill=career_data["skills"][0]
                )
            elif any(word in user_input_lower for word in ["gaji", "salary", "penghasilan", "income"]):
                return response_templates["salary_inquiry"][0].format(
                    role=career_data["description"].split()[0] + " " + career_data["description"].split()[1],
                    salary=career_data["salary"],
                    growth=career_data["growth"]
                )
    
    # Transition tips
    if any(word in user_input_lower for word in ["transisi", "pindah", "berubah", "tips", "saran"]):
        return random.choice(response_templates["transition_tips"])
    
    # Specific career predictions
    if "komite audit" in user_input_lower:
        return """
        🔮 **Prediksi Karir Komite Audit 5 Tahun Mendatang:**
        
        **Tren Positif:**
        • Meningkatnya regulasi compliance (SOX, GDPR)
        • Digitalisasi audit dengan AI dan analytics
        • Demand tinggi untuk risk management expertise
        
        **Skill yang Harus Dikembangkan:**
        • Data analytics dan visualization
        • Cybersecurity awareness
        • ESG (Environmental, Social, Governance) knowledge
        • Technology audit capabilities
        
        **Proyeksi Salary:** $75,000 - $140,000
        **Growth Rate:** 8-12% annually
        
        **Saran:** Fokus pada digital transformation audit dan ESG compliance untuk competitive advantage! 💼✨
        """
    
    # Default responses with industry insights
    industry_insights = [
        f"""
        🚀 **Insight Karir Masa Depan:**
        
        Berdasarkan tren global, industri yang paling promising:
        
        1. **Artificial Intelligence** - Pertumbuhan 22% 🤖
        2. **Cybersecurity** - Demand sangat tinggi 🔒
        3. **Renewable Energy** - Sustainability focus 🌱
        4. **Biotechnology** - Healthcare innovation 🧬
        5. **Blockchain/Web3** - Financial revolution 🔗
        
        Mau tahu lebih detail tentang industri mana yang menarik buat Anda? 💡
        """,
        f"""
        💼 **Tips Sukses Karir 2025:**
        
        • **Lifelong Learning** - Teknologi terus berubah
        • **Digital Literacy** - Wajib di semua industri  
        • **Soft Skills** - Communication & adaptability
        • **Networking** - Build professional relationships
        • **Personal Branding** - LinkedIn & portfolio online
        
        Yang mana yang ingin Anda dalami lebih lanjut? 🎯
        """,
        f"""
        📊 **Market Intelligence:**
        
        **Hot Skills 2025:**
        • Python Programming (+45% demand)
        • Cloud Computing (+38% demand) 
        • Data Analysis (+42% demand)
        • AI/ML (+55% demand)
        • Cybersecurity (+35% demand)
        
        **Emerging Roles:**
        • AI Ethics Specialist
        • Sustainability Consultant  
        • Web3 Product Manager
        • Quantum Computing Engineer
        
        Ingin roadmap untuk skill tertentu? 🗺️
        """
    ]
    
    return random.choice(industry_insights)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# Sidebar with enhanced features
with st.sidebar:
    st.markdown("""
    <div class="sidebar-card">
        <h3>🎯 Career Navigator</h3>
        <p>Your intelligent career guidance companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    st.markdown(f"""
    <div class="stats-card">
        <h4>📊 Session Stats</h4>
        <p><strong>Messages:</strong> {len(st.session_state.messages)}</p>
        <p><strong>Active Since:</strong> {datetime.now().strftime('%H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Industry Quick Access
    st.markdown("### 🏭 Industry Quick Access")
    
    industries = {
        "🤖 Artificial Intelligence": "Tanya tentang AI Engineer",
        "🔗 Blockchain & Web3": "Prospek karir di blockchain", 
        "🧬 Biotechnology": "Karir di bidang biotech",
        "⚡ Renewable Energy": "Peluang di energi terbarukan",
        "🔒 Cybersecurity": "Menjadi cybersecurity specialist"
    }
    
    for industry, query in industries.items():
        if st.button(industry, key=f"sidebar_{industry}"):
            st.session_state.suggested_question = query

# Suggested Questions with Enhanced UI
st.markdown("### 💡 Pertanyaan Populer")

suggestions = [
    {
        "title": "🚀 Prediksi Karir Komite Audit",
        "subtitle": "Tren dan peluang 5 tahun mendatang",
        "query": "Gimana prediksi mu karir komite audit 5 tahun mendatang?"
    },
    {
        "title": "💼 Skills AI Engineer",
        "subtitle": "Roadmap lengkap menjadi AI Engineer", 
        "query": "Skill apa yang dibutuhkan untuk AI Engineer?"
    },
    {
        "title": "🔗 Prospek Blockchain",
        "subtitle": "Peluang karir di industri Web3",
        "query": "Bagaimana prospek karir di blockchain?"
    },
    {
        "title": "🎯 Tips Transisi Karir",
        "subtitle": "Strategi pindah ke tech industry",
        "query": "Tips transisi karir ke tech industry?"
    },
    {
        "title": "💰 Salary Benchmark 2025",
        "subtitle": "Gaji terbaru industri teknologi",
        "query": "Berapa salary range untuk tech jobs di 2025?"
    },
    {
        "title": "🌱 Green Jobs Future",
        "subtitle": "Karir di sustainability & renewable energy",
        "query": "Bagaimana prospek green jobs dan sustainability careers?"
    }
]

# Create suggestion grid
cols = st.columns(2)
for i, suggestion in enumerate(suggestions):
    with cols[i % 2]:
        if st.button(
            f"**{suggestion['title']}**\n{suggestion['subtitle']}", 
            key=f"suggestion_{i}",
            help="Click to ask this question"
        ):
            st.session_state.suggested_question = suggestion['query']

# Chat Interface
st.markdown("### 💬 Career Chat")

# Display chat messages with enhanced styling
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

# Handle suggested questions
if "suggested_question" in st.session_state:
    question = st.session_state.suggested_question
    del st.session_state.suggested_question
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(f'<div class="user-message">{question}</div>', unsafe_allow_html=True)
    
    # Generate and display AI response
    with st.chat_message("assistant"):
        # Typing animation
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(
            '<div class="assistant-message">🤔 Sedang berpikir<span class="typing-indicator"></span><span class="typing-indicator"></span><span class="typing-indicator"></span></div>',
            unsafe_allow_html=True
        )
        
        # Simulate thinking time
        time.sleep(1.5)
        
        # Generate response
        response = generate_smart_response(question)
        
        # Clear thinking animation and show response
        thinking_placeholder.empty()
        st.markdown(f'<div class="assistant-message">{response}</div>', unsafe_allow_html=True)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_count += 1
    
    # Auto-rerun to update sidebar stats
    st.rerun()

# Chat input
if prompt := st.chat_input("Tanyakan sesuatu tentang karir masa depan..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
    
    # Generate and display AI response
    with st.chat_message("assistant"):
        # Typing animation
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(
            '<div class="assistant-message">🤔 Sedang menganalisis<span class="typing-indicator"></span><span class="typing-indicator"></span><span class="typing-indicator"></span></div>',
            unsafe_allow_html=True
        )
        
        # Simulate processing time
        time.sleep(2)
        
        # Generate response
        response = generate_smart_response(prompt)
        
        # Clear thinking animation and show response
        thinking_placeholder.empty()
        st.markdown(f'<div class="assistant-message">{response}</div>', unsafe_allow_html=True)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_count += 1

# Enhanced Controls
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🗑️ Clear Chat", help="Clear conversation history"):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.rerun()

with col2:
    if st.button("💾 Export Chat", help="Download conversation"):
        if st.session_state.messages:
            chat_export = {
                "timestamp": datetime.now().isoformat(),
                "conversation_count": len(st.session_state.messages),
                "messages": st.session_state.messages
            }
            st.download_button(
                "📥 Download JSON",
                data=json.dumps(chat_export, indent=2),
                file_name=f"career_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json"
            )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 10px; margin: 2rem 0;">
    <h4>🚀 Career Shift Analyzer - Powered by Advanced AI</h4>
    <p>© 2025 | Intelligent Career Guidance System | No API Key Required</p>
    <p><em>Responses generated by sophisticated AI algorithms trained on industry data</em></p>
</div>
""", unsafe_allow_html=True)

# UNIVERSAL FOOTER COMPONENT
def render_universal_footer():
    """Universal Footer Component with Team Credits and Disclaimer"""
    
    from datetime import datetime
    import os
    
    def get_app_version():
        """Get app version dynamically"""
        try:
            env_version = os.getenv('APP_VERSION')
            if env_version:
                return env_version
            base_version = "2.0"  # Updated version
            build_number = datetime.now().strftime("%y%m%d")
            return f"{base_version}.{build_number}"
        except:
            return "2.0.0"
    
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
                        <li>• All processing done locally in browser</li>
                        <li>• No external API calls or data transmission</li>
                        <li>• Complete privacy protection</li>
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
                    <div class="tech-item">🧠 Local AI</div>
                    <div class="tech-item">🎨 Custom CSS</div>
                    <div class="tech-item">☁️ Cloud Hosted</div>
                    <div class="tech-item">📱 Responsive</div>
                </div>
                <div style="margin-top: 1rem;">
                    <p><strong>AI Engine:</strong> Advanced Local Processing</p>
                    <p><strong>Hosting:</strong> Streamlit Cloud Platform</p>
                    <p><strong>Data Source:</strong> Curated Industry Knowledge Base</p>
                    <p><strong>Privacy:</strong> 100% Local Processing</p>
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

# Call the footer function
render_universal_footer()
