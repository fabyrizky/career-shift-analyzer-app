import streamlit as st
import random
import time
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Career Simulation", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI/UX with natural appearance
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Global Styles */
    .main > div {
        padding-top: 1rem;
    }
    
    /* Header Styles */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
        margin-bottom: 0;
        font-weight: 300;
    }
    
    /* Chat Interface */
    .chat-container {
        background: #ffffff;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e8f0fe;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.8rem 0;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 3px 12px rgba(102, 126, 234, 0.25);
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.8rem 0;
        max-width: 85%;
        box-shadow: 0 3px 12px rgba(17, 153, 142, 0.25);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Suggestion Cards */
    .suggestion-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .suggestion-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 6px 20px rgba(240, 147, 251, 0.25);
        font-size: 0.9rem;
    }
    
    .suggestion-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.35);
    }
    
    /* Sidebar Styles */
    .sidebar-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.25);
    }
    
    .stats-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 0.8rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }
    
    /* Animated Elements */
    .typing-indicator {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #fff;
        animation: typing 1.4s infinite ease-in-out;
        margin: 0 1px;
    }
    
    .typing-indicator:nth-child(1) { animation-delay: -0.32s; }
    .typing-indicator:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { 
            transform: scale(0);
            opacity: 0.6;
        } 
        40% { 
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.25);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.35);
    }
    
    /* Hide code blocks and technical details */
    .stCodeBlock {
        display: none !important;
    }
    
    /* Natural conversation styling */
    .chat-message {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🤖 Career Chat Assistant</div>
    <div class="hero-subtitle">Konsultasi cerdas untuk masa depan karir Anda</div>
</div>
""", unsafe_allow_html=True)

# Enhanced Knowledge Base with more natural, contextual responses
career_insights = {
    "ai_trends": {
        "content": "AI sedang mengubah lanskap karir secara fundamental. Posisi seperti AI Engineer, Data Scientist, dan Machine Learning Specialist mengalami pertumbuhan 40-50% per tahun. Gaji rata-rata berkisar $85,000-$180,000 dengan peluang remote work yang tinggi.",
        "skills": ["Python", "TensorFlow", "Statistics", "Problem Solving"],
        "next_steps": "Mulai dengan course online Python, bangun portfolio di GitHub, dan praktik dengan dataset real."
    },
    
    "blockchain_career": {
        "content": "Industri blockchain berkembang pesat dengan adopsi DeFi dan NFT. Smart Contract Developer dan Blockchain Architect sangat dicari. Salary range $90,000-$200,000 dengan potensi equity yang menarik di startup Web3.",
        "skills": ["Solidity", "JavaScript", "Cryptography", "Web3"],
        "next_steps": "Pelajari Ethereum basics, coba develop smart contract sederhana, join komunitas Web3 lokal."
    },
    
    "career_transition": {
        "content": "Transisi karir ke tech membutuhkan strategi yang tepat. 70% profesional berhasil beralih dalam 12-18 bulan dengan pendekatan yang terstruktur. Kunci utamanya: skill development, networking, dan portfolio building.",
        "steps": ["Assessment skill gap", "Buat learning roadmap", "Build portfolio", "Network building", "Apply strategically"],
        "timeline": "6-12 bulan untuk hasil optimal"
    },
    
    "future_jobs": {
        "content": "Pekerjaan masa depan fokus pada sustainability, AI ethics, dan human-machine collaboration. Emerging roles: AI Ethicist, Sustainability Consultant, Human-AI Interaction Designer. Soft skills seperti adaptability dan critical thinking semakin penting.",
        "trends": ["Remote-first culture", "AI augmentation", "Green jobs", "Mental health awareness"],
        "preparation": "Develop hybrid skills: technical + soft skills + domain expertise"
    }
}

def generate_contextual_response(user_input):
    """Generate natural, contextual responses"""
    user_input_lower = user_input.lower()
    
    # Greeting responses
    if any(word in user_input_lower for word in ["halo", "hai", "hello", "hi", "selamat"]):
        return "Halo! 👋 Saya siap membantu Anda menjelajahi peluang karir masa depan. Ada bidang tertentu yang menarik perhatian Anda?"
    
    # AI and tech career responses
    if any(word in user_input_lower for word in ["ai", "artificial intelligence", "machine learning", "data science"]):
        insight = career_insights["ai_trends"]
        return f"""
        **🤖 Karir di AI & Data Science:**
        
        {insight['content']}
        
        **Skill prioritas:** {', '.join(insight['skills'][:3])}
        
        **Langkah selanjutnya:** {insight['next_steps']}
        
        Mau saya bantu buat roadmap pembelajaran yang spesifik? 🎯
        """
    
    # Blockchain queries
    if any(word in user_input_lower for word in ["blockchain", "web3", "crypto", "defi", "nft"]):
        insight = career_insights["blockchain_career"]
        return f"""
        **🔗 Ekosistem Blockchain & Web3:**
        
        {insight['content']}
        
        **Skill yang dibutuhkan:** {', '.join(insight['skills'])}
        
        **Cara memulai:** {insight['next_steps']}
        
        Industri ini masih sangat early-stage, jadi peluang untuk first-mover advantage masih terbuka lebar! 🚀
        """
    
    # Career transition advice
    if any(word in user_input_lower for word in ["transisi", "pindah", "berubah", "tips", "saran", "ganti"]):
        insight = career_insights["career_transition"]
        return f"""
        **🎯 Strategi Transisi Karir yang Efektif:**
        
        {insight['content']}
        
        **Timeline realistis:** {insight['timeline']}
        
        **Step-by-step approach:**
        • {insight['steps'][0]} - evaluasi kemampuan saat ini
        • {insight['steps'][1]} - tentukan target pembelajaran  
        • {insight['steps'][2]} - kerjakan project nyata
        • {insight['steps'][3]} - hubungkan dengan profesional
        • {insight['steps'][4]} - lamar posisi yang tepat
        
        Yang mana yang ingin kita diskusikan lebih detail? 💡
        """
    
    # Audit career specific
    if any(word in user_input_lower for word in ["audit", "komite audit", "auditor"]):
        return """
        **📊 Evolusi Karir Audit 2025-2030:**
        
        Profesi audit mengalami transformasi digital yang signifikan. Traditional audit berkembang menjadi **Digital Audit** dengan fokus pada data analytics, risk intelligence, dan automated testing.
        
        **Tren yang menguntungkan:**
        • ESG audit demand meningkat 60%
        • Technology audit specialist sangat dicari
        • Cybersecurity audit jadi mandatory
        • Remote audit capabilities jadi standar
        
        **Skill upgrade yang diperlukan:**
        • Data visualization (Tableau, Power BI)
        • Basic programming (Python, R)
        • ESG framework knowledge
        • Cybersecurity fundamentals
        
        **Proyeksi gaji:** $75,000 - $140,000 (naik 15-20% dari sekarang)
        
        Mau saya buatkan learning path untuk digital audit transformation? 🎓
        """
    
    # Future of work
    if any(word in user_input_lower for word in ["masa depan", "future", "trend", "prediksi"]):
        insight = career_insights["future_jobs"]
        return f"""
        **🔮 Landscape Karir 2025-2030:**
        
        {insight['content']}
        
        **Trend kunci:**
        • {insight['trends'][0]} - 80% companies adopt hybrid work
        • {insight['trends'][1]} - AI tools jadi daily companion
        • {insight['trends'][2]} - sustainability roles naik 300%
        • {insight['trends'][3]} - wellbeing specialist in-demand
        
        **Persiapan optimal:** {insight['preparation']}
        
        Intinya, masa depan karir bukan tentang manusia vs mesin, tapi manusia + mesin. Yang adapt cepat akan unggul! ⚡
        """
    
    # Default responses with actionable insights
    responses = [
        """
        **🎯 Quick Career Intelligence:**
        
        Berdasarkan trend global, 3 sektor paling promising:
        
        **1. AI & Automation** (40% growth)
        → Perfect untuk analytical minds yang suka problem-solving
        
        **2. Green Technology** (60% growth)  
        → Ideal untuk yang passionate tentang sustainability
        
        **3. Digital Health** (35% growth)
        → Cocok untuk yang ingin impact langsung ke masyarakat
        
        Mana yang resonates dengan background dan interest Anda? 🤔
        """,
        
        """
        **💡 Career Strategy 2025:**
        
        **Hot Skills yang wajib dimiliki:**
        • Digital literacy (basic coding, data analysis)
        • Emotional intelligence (leadership, empathy)  
        • Adaptability (learning agility, resilience)
        • Systems thinking (big picture perspective)
        
        **Quick wins untuk career acceleration:**
        • Update LinkedIn dengan skill keywords
        • Join 2-3 professional communities  
        • Start side project di bidang yang diminati
        • Network dengan 5 orang baru per bulan
        
        Mau saya help elaborate strategi mana yang paling cocok untuk situasi Anda? 🚀
        """,
        
        """
        **📈 Market Reality Check:**
        
        **Good news:** Job market untuk skilled professionals sangat kuat. Companies struggle finding qualified talent.
        
        **Key insight:** 65% recruiters prioritize skills over formal education sekarang.
        
        **Opportunity areas:**
        • Remote work expanding globally (bisa kerja untuk company manapun)
        • Freelance/consultant market growing 25% annually
        • AI tools making individual productivity 10x higher
        
        **Actionable step:** Identify 1 high-value skill yang bisa dipelajari dalam 3 bulan, then execute with focus.
        
        Ada skill tertentu yang sedang Anda pertimbangkan? 🎯
        """
    ]
    
    return random.choice(responses)

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
        <p>Intelligent career guidance companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    st.markdown(f"""
    <div class="stats-card">
        <h4>📊 Session</h4>
        <p><strong>Messages:</strong> {len(st.session_state.messages)}</p>
        <p><strong>Active:</strong> {datetime.now().strftime('%H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    
    quick_topics = {
        "🤖 AI Career Path": "Bagaimana memulai karir di artificial intelligence?",
        "🔗 Blockchain Opportunities": "Prospek karir di blockchain dan Web3",
        "💼 Career Transition": "Tips sukses transisi karir ke tech",
        "📊 Salary Insights": "Benchmark gaji untuk tech roles 2025",
        "🌱 Future Skills": "Skill apa yang akan penting 5 tahun mendatang?"
    }
    
    for topic, query in quick_topics.items():
        if st.button(topic, key=f"quick_{topic}"):
            st.session_state.suggested_question = query

# Suggested Questions
st.markdown("### 💭 Popular Questions")

suggestions = [
    {
        "title": "🚀 Audit Career Evolution",
        "query": "Gimana prediksi karir komite audit 5 tahun mendatang?"
    },
    {
        "title": "🤖 AI Engineer Roadmap", 
        "query": "Skill apa yang dibutuhkan untuk jadi AI Engineer?"
    },
    {
        "title": "🔗 Blockchain Future",
        "query": "Bagaimana prospek karir di blockchain?"
    },
    {
        "title": "💡 Career Transition Guide",
        "query": "Tips praktis transisi karir ke tech industry"
    }
]

# Display suggestions in a clean grid
cols = st.columns(2)
for i, suggestion in enumerate(suggestions):
    with cols[i % 2]:
        if st.button(suggestion['title'], key=f"sug_{i}"):
            st.session_state.suggested_question = suggestion['query']

# Chat Interface
st.markdown("### 💬 Career Consultation")

# Display chat messages
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
    
    # Generate and display response
    with st.chat_message("assistant"):
        # Thinking animation
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(
            '<div class="assistant-message">💭 Analyzing<span class="typing-indicator"></span><span class="typing-indicator"></span><span class="typing-indicator"></span></div>',
            unsafe_allow_html=True
        )
        
        time.sleep(1.2)  # Natural thinking pause
        
        response = generate_contextual_response(question)
        thinking_placeholder.empty()
        st.markdown(f'<div class="assistant-message">{response}</div>', unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_count += 1
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask about your career future..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
    
    # Generate response
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(
            '<div class="assistant-message">🧠 Processing<span class="typing-indicator"></span><span class="typing-indicator"></span><span class="typing-indicator"></span></div>',
            unsafe_allow_html=True
        )
        
        time.sleep(1.5)
        
        response = generate_contextual_response(prompt)
        thinking_placeholder.empty()
        st.markdown(f'<div class="assistant-message">{response}</div>', unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_count += 1

# Clean Controls
col1, col2 = st.columns([1, 3])

with col1:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.rerun()

with col2:
    if st.session_state.messages and st.button("💾 Export Conversation"):
        chat_data = {
            "timestamp": datetime.now().isoformat(),
            "messages": st.session_state.messages
        }
        st.download_button(
            "📥 Download",
            data=json.dumps(chat_data, indent=2),
            file_name=f"career_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )

# Clean Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 12px; margin: 2rem 0;">
    <h4>🚀 Career Shift Analyzer</h4>
    <p>Intelligent Career Guidance • No Setup Required • 100% Free</p>
</div>
""", unsafe_allow_html=True)

# Universal Footer (simplified for cleaner appearance)
def render_clean_footer():
    """Clean, minimal footer"""
    current_year = datetime.now().year
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    ">
        <h4 style="margin-bottom: 1rem;">© {current_year} Career Shift Analyzer</h4>
        <p style="margin: 0.5rem 0;">
            <strong>Developed by:</strong> 
            <span style="color: #ffd700;">MS Hadianto</span> & 
            <span style="color: #ffd700;">Faby</span>
        </p>
        <p style="margin: 1rem 0; font-size: 0.9em; opacity: 0.9;">
            Empowering career transitions through intelligent guidance
        </p>
        <p style="font-size: 0.85em; opacity: 0.8;">
            Built with ❤️ for professional growth worldwide
        </p>
    </div>
    """, unsafe_allow_html=True)

render_clean_footer()
