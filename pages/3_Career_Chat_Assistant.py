import streamlit as st
import requests
import json
from datetime import datetime
import os
import random
import time

# Page configuration
st.set_page_config(
    page_title="Career Chat Assistant", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for beautiful UI/UX
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.15"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        font-weight: 400;
        line-height: 1.6;
        position: relative;
        z-index: 1;
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
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: none;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .suggestion-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .suggestion-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(240, 147, 251, 0.4);
    }
    
    .suggestion-card:hover::before {
        left: 100%;
    }
    
    .suggestion-card h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .suggestion-card p {
        margin: 0;
        font-size: 0.95rem;
        opacity: 0.9;
        line-height: 1.4;
    }
    
    /* Chat Interface */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem 1.8rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        font-size: 1rem;
        line-height: 1.6;
        position: relative;
    }
    
    .user-message::after {
        content: '';
        position: absolute;
        bottom: 0;
        right: -5px;
        width: 0;
        height: 0;
        border: 5px solid transparent;
        border-top-color: #764ba2;
        border-right: 0;
        margin-bottom: -5px;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.2rem 1.8rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        max-width: 85%;
        box-shadow: 0 5px 20px rgba(17, 153, 142, 0.3);
        font-size: 1rem;
        line-height: 1.7;
        position: relative;
    }
    
    .assistant-message::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: -5px;
        width: 0;
        height: 0;
        border: 5px solid transparent;
        border-top-color: #38ef7d;
        border-left: 0;
        margin-bottom: -5px;
    }
    
    /* Sidebar Styles */
    .sidebar-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.8rem 0;
        box-shadow: 0 5px 15px rgba(240, 147, 251, 0.3);
    }
    
    /* Typing Animation */
    .typing-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #fff;
        animation: typing 1.5s infinite ease-in-out;
        margin: 0 2px;
    }
    
    .typing-indicator:nth-child(1) { animation-delay: -0.32s; }
    .typing-indicator:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% { 
            transform: scale(0.8);
            opacity: 0.5;
        } 
        40% { 
            transform: scale(1.2);
            opacity: 1;
        }
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        text-transform: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Input Styles */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e1e8ff;
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        text-align: center;
    }
    
    /* Controls */
    .control-button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1.5rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .control-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    
    /* Loading Animation */
    .loading-pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🤖 Career Chat Assistant</div>
    <div class="hero-subtitle">Konsultasi cerdas untuk menavigasi masa depan karir Anda dengan teknologi AI terdepan</div>
</div>
""", unsafe_allow_html=True)

# Enhanced Knowledge Base for fallback responses
career_knowledge = {
    "ai_career": {
        "response": """
        **🤖 Karir AI Engineer - Panduan Lengkap:**
        
        **Skill Fundamental:**
        • Python programming (80% industry standard)
        • Machine Learning frameworks (TensorFlow, PyTorch)
        • Statistics & Mathematics (linear algebra, calculus)
        • Data manipulation (Pandas, NumPy)
        • Cloud platforms (AWS, Google Cloud, Azure)
        
        **Learning Path (6-12 bulan):**
        1. **Bulan 1-2:** Python basics + statistics
        2. **Bulan 3-4:** Machine learning fundamentals
        3. **Bulan 5-6:** Deep learning & neural networks
        4. **Bulan 7-8:** Specialized areas (NLP, Computer Vision)
        5. **Bulan 9-12:** Portfolio projects + job applications
        
        **Salary Range:** $80,000 - $180,000 (Indonesia: 15-50 juta/bulan)
        **Growth Rate:** 22% annually (jauh di atas rata-rata)
        
        **Pro Tips:**
        • Mulai dengan Coursera ML course by Andrew Ng
        • Build 3-5 portfolio projects di GitHub
        • Join komunitas AI Indonesia (PyTorch Indonesia, TensorFlow User Group)
        • Ikuti kompetisi Kaggle untuk practice
        
        **Next Steps:** Mau saya bantu buat roadmap pembelajaran yang lebih spesifik sesuai background Anda?
        """
    },
    
    "blockchain_career": {
        "response": """
        **🔗 Karir Blockchain & Web3 - Future is Now:**
        
        **Hot Positions:**
        • Smart Contract Developer ($90K-$200K)
        • Blockchain Architect ($120K-$250K)
        • DeFi Protocol Developer ($100K-$300K)
        • Web3 Product Manager ($80K-$180K)
        
        **Essential Skills:**
        • Solidity programming (smart contracts)
        • JavaScript/TypeScript (frontend integration)
        • Cryptography basics (hashing, digital signatures)
        • Understanding DeFi protocols (Uniswap, Compound)
        • Web3 libraries (Web3.js, Ethers.js)
        
        **Industry Reality:**
        • 90% of projects are still experimental
        • High risk, high reward environment
        • Remote work opportunities sangat tinggi
        • Equity/token compensation common
        
        **Learning Strategy:**
        1. **Foundation:** Ethereum whitepaper + Solidity docs
        2. **Practice:** Build simple DApp (voting, token)
        3. **Advanced:** Study DeFi protocols source code
        4. **Network:** Join Web3 communities & hackathons
        
        **Market Outlook:** Meski volatile, adoption institutional terus meningkat. Perfect timing untuk masuk sekarang.
        
        **Warning:** Industry ini fast-paced dan risky. Pastikan diversifikasi skill Anda.
        """
    },
    
    "audit_future": {
        "response": """
        **📊 Evolusi Audit Career 2025-2030:**
        
        **Digital Transformation Impact:**
        Traditional audit berevolusi jadi **Intelligent Audit** dengan AI-powered tools. Manual testing mulai digantikan automated procedures.
        
        **New Audit Roles:**
        • **Digital Audit Specialist** - focus on data analytics
        • **ESG Audit Expert** - sustainability compliance (hot trend!)
        • **Cybersecurity Auditor** - IT risk assessment
        • **Process Mining Analyst** - automated audit trails
        
        **Skills Upgrade Roadmap:**
        1. **Data Analytics:** Excel advanced → Python/R → Tableau/Power BI
        2. **Technology:** Basic IT knowledge → Cloud platforms → Cybersecurity
        3. **ESG:** Traditional audit → Sustainability frameworks → Climate risk
        4. **Automation:** Manual testing → Audit software → AI tools
        
        **Market Dynamics:**
        • Salary increase: 15-25% for tech-savvy auditors
        • Remote audit capabilities expanding opportunities
        • Big 4 firms heavily investing in audit tech
        • Regulatory compliance semakin complex = more demand
        
        **Strategic Advice:**
        • Ambil certification: CPA + IT audit specialty
        • Learn basic Python for data analysis
        • Understand ESG frameworks (huge opportunity)
        • Network dengan audit tech vendors
        
        **Timeline:** Transformation ini 3-5 tahun. Early adopters akan dapat premium.
        """
    },
    
    "transition_tips": {
        "response": """
        **🎯 Career Transition Blueprint - Proven Strategy:**
        
        **Phase 1: Assessment (Bulan 1)**
        • Skill audit: apa yang sudah dimiliki vs yang dibutuhkan
        • Industry research: salary, job market, growth projection
        • Network mapping: siapa yang bisa membantu
        
        **Phase 2: Skill Building (Bulan 2-6)**
        • 70% fokus pada hard skills (programming, tools)
        • 30% soft skills (communication, leadership)
        • Build portfolio dengan real projects
        • Get relevant certifications
        
        **Phase 3: Market Entry (Bulan 7-12)**
        • LinkedIn optimization dengan keywords
        • Apply to 5-10 positions per week
        • Network dengan professionals di target industry
        • Prepare untuk technical interviews
        
        **Success Metrics:**
        • 80% professionals berhasil transisi dalam 12-18 bulan
        • Average salary increase: 20-40%
        • Key factor: consistency dalam learning + networking
        
        **Common Pitfalls:**
        ❌ Tutorial hell - terlalu banyak belajar, kurang practice
        ❌ Perfectionism - tunggu "siap" sebelum apply
        ❌ Isolated learning - tidak network dengan industry
        
        **Pro Tips:**
        ✅ Start applying ketika 70% ready
        ✅ Build in public - share learning journey
        ✅ Find mentor di target industry
        ✅ Join relevant communities early
        
        **Budget:** Alokasikan 2-5 juta untuk courses, certification, networking events.
        """
    }
}

def get_ai_response_with_fallback(question):
    """Get AI response with intelligent fallback"""
    try:
        # Check if API key exists in secrets
        if "openrouter" in st.secrets and st.secrets.openrouter.get("api_key"):
            api_key = st.secrets.openrouter["api_key"]
            
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
                        "content": "Kamu adalah konsultan karir expert yang memberikan advice praktis, actionable, dan kontekstual dalam bahasa Indonesia. Berikan response yang natural, engaging, dan helpful untuk career development di industri masa depan."
                    },
                    {"role": "user", "content": question}
                ],
                "max_tokens": 600,
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
            else:
                # Fallback to local knowledge base
                return get_local_response(question)
                
        else:
            # Use local knowledge base when no API key
            return get_local_response(question)
            
    except Exception as e:
        # Fallback to local knowledge base on any error
        return get_local_response(question)

def get_local_response(question):
    """Generate response from local knowledge base"""
    question_lower = question.lower()
    
    # Career-specific responses
    if any(word in question_lower for word in ["ai engineer", "artificial intelligence", "machine learning", "data science"]):
        return career_knowledge["ai_career"]["response"]
    
    elif any(word in question_lower for word in ["blockchain", "web3", "crypto", "defi", "smart contract"]):
        return career_knowledge["blockchain_career"]["response"]
    
    elif any(word in question_lower for word in ["audit", "komite audit", "auditor"]):
        return career_knowledge["audit_future"]["response"]
    
    elif any(word in question_lower for word in ["transisi", "pindah", "berubah", "tips", "saran"]):
        return career_knowledge["transition_tips"]["response"]
    
    # Greeting responses
    elif any(word in question_lower for word in ["halo", "hai", "hello", "hi"]):
        return """
        👋 **Halo! Selamat datang di Career Chat Assistant!**
        
        Saya siap membantu Anda menavigasi masa depan karir dengan insights yang actionable dan up-to-date.
        
        **Saya bisa bantu dengan:**
        • Analisis prospek karir di industri masa depan
        • Roadmap pembelajaran skill yang in-demand
        • Strategi transisi karir yang efektif
        • Benchmark salary dan growth projection
        • Tips networking dan personal branding
        
        Apa yang ingin kita diskusikan hari ini? 🚀
        """
    
    # Default responses with valuable insights
    else:
        insights = [
            """
            **🔮 Career Intelligence Update:**
            
            **Top 3 Industry Trends 2025:**
            
            **1. AI Integration Everywhere** 
            Bukan hanya tech companies - finance, healthcare, retail semua adopt AI. Demand untuk AI literacy meningkat 300%.
            
            **2. Remote-First Culture**
            80% companies permanent hybrid. Opportunities global terbuka lebar untuk skilled professionals.
            
            **3. Sustainability Focus**
            ESG compliance mandatory. Green jobs projected naik 400% dalam 5 tahun.
            
            **Quick Action Steps:**
            • Update skills dengan online learning (Coursera, Udemy)
            • Optimize LinkedIn dengan relevant keywords
            • Join professional communities di target industry
            • Start building portfolio yang showcase capabilities
            
            **Ada area spesifik yang mau kita explore lebih dalam?** 🎯
            """,
            
            """
            **💡 Practical Career Strategy:**
            
            **The 3-Pillar Approach untuk Career Growth:**
            
            **Pillar 1: Skill Stacking**
            Kombinasi unique skills yang bikin Anda irreplaceable. Contoh: Data Analysis + Domain Knowledge + Communication.
            
            **Pillar 2: Network Leverage** 
            70% opportunities datang dari network. Invest 20% waktu untuk relationship building.
            
            **Pillar 3: Market Positioning**
            Personal branding yang clear: apa expertise Anda dan untuk siapa.
            
            **Implementation:**
            • Week 1-2: Skills assessment & gap analysis
            • Week 3-4: Learning plan & resource curation  
            • Month 2-3: Active learning + portfolio building
            • Month 4+: Network expansion + market positioning
            
            **ROI:** Strategy ini typically menghasilkan 25-40% salary increase dalam 12-18 bulan.
            
            **Mau saya bantu detail implementation untuk situation Anda?** 🚀
            """
        ]
        
        return random.choice(insights)

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
        <p><strong>Status:</strong> 🟢 Online</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Topics
    st.markdown("### ⚡ Quick Topics")
    
    quick_buttons = {
        "🤖 AI Career": "Skill apa yang dibutuhkan untuk AI Engineer?",
        "🔗 Blockchain Jobs": "Bagaimana prospek karir di blockchain?", 
        "📊 Audit Future": "Gimana prediksi karir komite audit 5 tahun mendatang?",
        "🎯 Career Tips": "Tips transisi karir ke tech industry",
        "💰 Salary Intel": "Benchmark gaji untuk tech roles 2025"
    }
    
    for label, query in quick_buttons.items():
        if st.button(label, key=f"quick_{label}"):
            st.session_state.suggested_question = query

# Suggested Questions Section
st.markdown('<h2 class="section-header">💭 Popular Questions</h2>', unsafe_allow_html=True)

# Enhanced suggestion cards
suggestions = [
    {
        "emoji": "🚀",
        "title": "Audit Career Evolution",
        "desc": "Prediksi dan transformasi audit 5 tahun mendatang", 
        "query": "Gimana prediksi mu karir komite audit 5 tahun mendatang?"
    },
    {
        "emoji": "🤖", 
        "title": "AI Engineer Roadmap",
        "desc": "Complete guide untuk menjadi AI Engineer profesional",
        "query": "Skill apa yang dibutuhkan untuk AI Engineer?"
    },
    {
        "emoji": "🔗",
        "title": "Blockchain Opportunities", 
        "desc": "Eksplorasi karir di ecosystem Web3 dan DeFi",
        "query": "Bagaimana prospek karir di blockchain?"
    },
    {
        "emoji": "💡",
        "title": "Career Transition Guide",
        "desc": "Strategi proven untuk sukses pindah karir",
        "query": "Tips transisi karir ke tech industry?"
    }
]

# Display suggestions in grid
cols = st.columns(2)
for i, suggestion in enumerate(suggestions):
    with cols[i % 2]:
        if st.button(f"{suggestion['emoji']} **{suggestion['title']}**\n{suggestion['desc']}", key=f"suggest_{i}"):
            st.session_state.suggested_question = suggestion['query']

# Chat Interface
st.markdown('<h2 class="section-header">💬 Career Consultation</h2>', unsafe_allow_html=True)

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
    
    # Generate response with thinking animation
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(
            '<div class="assistant-message loading-pulse">🧠 Analyzing your question<span class="typing-indicator"></span><span class="typing-indicator"></span><span class="typing-indicator"></span></div>',
            unsafe_allow_html=True
        )
        
        # Natural thinking pause
        time.sleep(1.8)
        
        # Get response
        response = get_ai_response_with_fallback(question)
        
        # Display response
        thinking_placeholder.empty()
        st.markdown(f'<div class="assistant-message">{response}</div>', unsafe_allow_html=True)
    
    # Add to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_count += 1
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask me anything about your career future..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)
    
    # Generate response
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(
            '<div class="assistant-message loading-pulse">💭 Processing your query<span class="typing-indicator"></span><span class="typing-indicator"></span><span class="typing-indicator"></span></div>',
            unsafe_allow_html=True
        )
        
        time.sleep(2)
        
        response = get_ai_response_with_fallback(prompt)
        
        thinking_placeholder.empty()
        st.markdown(f'<div class="assistant-message">{response}</div>', unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_count += 1

# Enhanced Controls
st.markdown("### 🔧 Controls")
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🗑️ Clear Chat", help="Reset conversation"):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.rerun()

with col2:
    if st.session_state.messages:
        chat_export = {
            "timestamp": datetime.now().isoformat(),
            "total_messages": len(st.session_state.messages),
            "conversation": st.session_state.messages
        }
        st.download_button(
            "💾 Export Chat",
            data=json.dumps(chat_export, indent=2),
            file_name=f"career_consultation_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            help="Download conversation history"
        )

with col3:
    st.markdown("*Chat automatically saved during session*")

# Enhanced Footer
st.markdown("---")

def render_enhanced_footer():
    """Render beautiful footer without syntax errors"""
    
    def get_app_version():
        try:
            env_version = os.getenv('APP_VERSION')
            if env_version:
                return env_version
            base_version = "2.1"
            build_number = datetime.now().strftime("%y%m%d")
            return f"{base_version}.{build_number}"
        except:
            return "2.1.0"
    
    version = get_app_version()
    current_year = datetime.now().year
    last_updated = datetime.now().strftime("%B %d, %Y")
    
    # Enhanced Footer CSS
    st.markdown("""
    <style>
    .enhanced-footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-top: 3rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .enhanced-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="footerGrain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="1" fill="white" opacity="0.1"/><circle cx="80" cy="80" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="5" r="0.5" fill="white" opacity="0.15"/></pattern></defs><rect width="100" height="100" fill="url(%23footerGrain)"/></svg>');
        pointer-events: none;
    }
    
    .footer-content {
        position: relative;
        z-index: 1;
    }
    
    .footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .footer-section h4 {
        color: #ffd700;
        margin-bottom: 1rem;
        font-size: 1.2em;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .footer-card {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .footer-card:hover {
        background: rgba(255,255,255,0.15);
        transform: translateY(-2px);
    }
    
    .team-showcase {
        background: rgba(255,255,255,0.15);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,215,0,0.3);
        text-align: center;
    }
    
    .team-grid {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }
    
    .team-card {
        background: rgba(255,255,255,0.2);
        padding: 1.5rem 2rem;
        border-radius: 20px;
        border: 2px solid rgba(255,215,0,0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-align: center;
        min-width: 160px;
        cursor: pointer;
    }
    
    .team-card:hover {
        transform: translateY(-8px) scale(1.05);
        border-color: #ffd700;
        box-shadow: 0 15px 40px rgba(255,215,0,0.4);
        background: rgba(255,255,255,0.3);
    }
    
    .team-card strong {
        color: #ffd700;
        font-size: 1.1em;
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .team-card span {
        font-size: 0.9em;
        color: rgba(255,255,255,0.9);
        line-height: 1.3;
    }
    
    .footer-bottom {
        border-top: 1px solid rgba(255,255,255,0.2);
        padding-top: 2rem;
        text-align: center;
        font-size: 0.9em;
        color: rgba(255,255,255,0.95);
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #00ff88;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px #00ff88;
    }
    
    .tech-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 0.8rem;
        margin: 1rem 0;
    }
    
    .tech-badge {
        background: rgba(255,255,255,0.15);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85em;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .tech-badge:hover {
        background: rgba(255,255,255,0.25);
        transform: scale(1.05);
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .footer-link {
        color: #ffd700;
        text-decoration: none;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .footer-link:hover {
        color: #fff;
        text-shadow: 0 0 15px #ffd700;
        transform: translateY(-1px);
    }
    
    .version-badge {
        background: rgba(255,215,0,0.2);
        color: #ffd700;
        padding: 0.4rem 1rem;
        border-radius: 15px;
        font-weight: 600;
        border: 1px solid rgba(255,215,0,0.4);
        display: inline-block;
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(255,255,255,0.1));
        border-radius: 10px;
        padding: 1rem;
        margin: 0.8rem 0;
        border-left: 4px solid #ffd700;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Footer HTML Content
    footer_html = f"""
    <div class="enhanced-footer">
        <div class="footer-content">
            <div class="footer-grid">
                <!-- App Information -->
                <div class="footer-section">
                    <h4>🚀 Career Shift Analyzer</h4>
                    <div class="footer-card">
                        <p><span class="status-indicator"></span><strong>Status:</strong> Online & Optimized</p>
                        <p><strong>Version:</strong> <span class="version-badge">v{version}</span></p>
                        <p><strong>Last Updated:</strong> {last_updated}</p>
                        <p><strong>Environment:</strong> Production Ready</p>
                        <div class="feature-highlight">
                            <strong>🎯 New Features:</strong>
                            <br>• Enhanced UI/UX Design
                            <br>• Intelligent Fallback System
                            <br>• Natural Conversation Flow
                        </div>
                    </div>
                </div>
                
                <!-- Team Showcase -->
                <div class="footer-section">
                    <h4>👥 Development Team</h4>
                    <div class="team-showcase">
                        <h5 style="color: #ffd700; margin-bottom: 1.5rem; font-size: 1.1em;">Collaborative Innovation Team</h5>
                        <div class="team-grid">
                            <div class="team-card">
                                <strong>🎯 MS Hadianto</strong>
                                <span>Lead Project Manager<br>& System Architecture</span>
                            </div>
                            <div class="team-card">
                                <strong>🤝 Faby</strong>
                                <span>Co-Lead Developer<br>& UX/UI Design</span>
                            </div>
                        </div>
                        <p style="margin-top: 1.5rem; font-size: 0.9em; color: rgba(255,255,255,0.8); font-style: italic;">
                            "Empowering career transformations through intelligent technology"
                        </p>
                    </div>
                </div>
                
                <!-- Legal & Privacy -->
                <div class="footer-section">
                    <h4>⚖️ Legal & Privacy</h4>
                    <div class="footer-card">
                        <p><strong>🛡️ Privacy Protection:</strong></p>
                        <ul style="list-style: none; padding: 0; font-size: 0.9em; line-height: 1.5;">
                            <li>✓ No personal data stored permanently</li>
                            <li>✓ Session-based conversations only</li>
                            <li>✓ Local processing when possible</li>
                            <li>✓ Zero tracking or analytics</li>
                            <li>✓ Complete user privacy</li>
                        </ul>
                    </div>
                    <div class="footer-card">
                        <p><strong>⚠️ Important Disclaimer:</strong></p>
                        <ul style="list-style: none; padding: 0; font-size: 0.85em; line-height: 1.4;">
                            <li>• Career advice for informational purposes</li>
                            <li>• Not professional counseling services</li>
                            <li>• Salary data are market estimates</li>
                            <li>• Verify information with official sources</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Technical Information -->
                <div class="footer-section">
                    <h4>🛠️ Technical Stack</h4>
                    <div class="tech-grid">
                        <div class="tech-badge">🐍 Python 3.11</div>
                        <div class="tech-badge">⚡ Streamlit</div>
                        <div class="tech-badge">🤖 AI Enhanced</div>
                        <div class="tech-badge">🎨 Custom CSS</div>
                        <div class="tech-badge">☁️ Cloud Hosted</div>
                        <div class="tech-badge">📱 Responsive</div>
                    </div>
                    <div class="footer-card">
                        <p><strong>🧠 AI Engine:</strong> Meta Llama 3.2 + Local Intelligence</p>
                        <p><strong>🏗️ Infrastructure:</strong> Streamlit Cloud Platform</p>
                        <p><strong>📊 Data Source:</strong> Curated Career Intelligence</p>
                        <p><strong>🔄 Updates:</strong> Continuous Deployment</p>
                    </div>
                </div>
            </div>
            
            <!-- Footer Bottom -->
            <div class="footer-bottom">
                <p style="font-size: 1.1em; margin-bottom: 1rem; font-weight: 600;">
                    <strong>© {current_year} Career Shift Analyzer v{version}</strong>
                </p>
                <p style="margin: 0.8rem 0; font-size: 1em;">
                    <strong>👥 Proudly Developed by:</strong> 
                    <span style="color: #ffd700; font-weight: 600;">MS Hadianto</span> (Lead Project) & 
                    <span style="color: #ffd700; font-weight: 600;">Faby</span> (Co-Lead Development)
                </p>
                <p style="margin: 1.5rem 0; font-size: 0.85em; line-height: 1.6; color: rgba(255,255,255,0.9);">
                    <em><strong>Legal Notice:</strong> This platform provides general career guidance and educational content. 
                    It is not a substitute for professional career counseling, financial advice, or job placement services. 
                    Users should independently verify all information and consult qualified professionals for personalized advice. 
                    Use of this platform constitutes acceptance of our terms and disclaimer.</em>
                </p>
                <p style="margin-top: 2rem; font-size: 1em;">
                    🌟 <strong>Open Source Initiative</strong> | 
                    <a href="https://github.com/mshadianto/career_shift_analyzer" target="_blank" class="footer-link">
                        📚 GitHub Repository
                    </a> | 
                    <a href="mailto:support@careershiftanalyzer.com" class="footer-link">
                        📧 Contact Support
                    </a>
                </p>
                <p style="margin-top: 1rem; font-size: 1em; color: #ffd700; font-weight: 500;">
                    Built with ❤️ for empowering career advancement worldwide 🌍
                </p>
            </div>
        </div>
    </div>
    """
    
    # Render the enhanced footer
    st.markdown("---")
    st.markdown(footer_html, unsafe_allow_html=True)

# Call the enhanced footer function
render_enhanced_footer()
