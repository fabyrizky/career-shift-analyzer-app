import streamlit as st
import random
import time
from datetime import datetime
import json
import uuid

# Page configuration
st.set_page_config(
    page_title="Career Chat Assistant V3.0", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🤖"
)

# Enhanced CSS for WhatsApp-like chat interface
st.markdown("""
<style>
    /* Hide all code elements and Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    .stCodeBlock {display: none !important;}
    .stCode {display: none !important;}
    pre {display: none !important;}
    code {display: none !important;}
    .highlight {display: none !important;}
    .language-python {display: none !important;}
    .streamlit-expanderHeader {display: none !important;}
    .stExpander {display: none !important;}
    div[data-testid="stCodeBlock"] {display: none !important;}
    div[data-testid="code-block"] {display: none !important;}
    .stMarkdown pre {display: none !important;}
    .stMarkdown code {display: none !important;}
    
    /* Import Beautiful Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Variables */
    :root {
        --primary-color: #25D366;
        --secondary-color: #128C7E;
        --accent-color: #34B7F1;
        --user-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --assistant-bg: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        --chat-bg: #f0f2f5;
        --message-shadow: 0 2px 8px rgba(0,0,0,0.1);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
    }
    
    /* Global Styles */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header Section */
    .app-header {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        padding: 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 40px rgba(37, 211, 102, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(-20px, -20px) rotate(10deg); }
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }
    
    .version-badge {
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 1rem;
        display: inline-block;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    /* Language Selector */
    .language-selector {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--glass-border);
        display: flex;
        gap: 1rem;
        justify-content: center;
        align-items: center;
    }
    
    .lang-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .lang-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .lang-btn.active {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        box-shadow: 0 5px 15px rgba(37, 211, 102, 0.4);
    }
    
    /* Chat Container */
    .chat-container {
        background: #f8f9fa;
        border-radius: 20px;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        position: relative;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.05);
    }
    
    /* Chat Messages */
    .message-container {
        display: flex;
        margin: 1rem 0;
        align-items: flex-end;
        gap: 0.5rem;
        animation: messageSlide 0.3s ease-out;
    }
    
    @keyframes messageSlide {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message-container.user {
        justify-content: flex-end;
    }
    
    .message-container.assistant {
        justify-content: flex-start;
    }
    
    .message-avatar {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        flex-shrink: 0;
    }
    
    .user-avatar {
        background: var(--user-bg);
        color: white;
    }
    
    .assistant-avatar {
        background: var(--assistant-bg);
        color: white;
    }
    
    .message-bubble {
        max-width: 70%;
        padding: 1rem 1.2rem;
        border-radius: 18px;
        position: relative;
        box-shadow: var(--message-shadow);
        word-wrap: break-word;
        line-height: 1.5;
    }
    
    .user-message {
        background: var(--user-bg);
        color: white;
        border-bottom-right-radius: 6px;
        margin-left: auto;
    }
    
    .assistant-message {
        background: white;
        color: #333;
        border-bottom-left-radius: 6px;
        border: 1px solid #e9ecef;
    }
    
    .message-time {
        font-size: 0.7rem;
        opacity: 0.7;
        margin-top: 0.5rem;
        text-align: right;
    }
    
    .assistant-message .message-time {
        color: #666;
    }
    
    .user-message .message-time {
        color: rgba(255,255,255,0.8);
    }
    
    /* Typing Indicator */
    .typing-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background: white;
        border-radius: 18px;
        border-bottom-left-radius: 6px;
        box-shadow: var(--message-shadow);
        margin: 1rem 0;
        max-width: 100px;
    }
    
    .typing-dots {
        display: flex;
        gap: 3px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #999;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    .typing-dot:nth-child(3) { animation-delay: 0s; }
    
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1.2); opacity: 1; }
    }
    
    /* Quick Suggestions */
    .suggestions-container {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid var(--glass-border);
    }
    
    .suggestions-title {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    .suggestions-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1rem;
    }
    
    .suggestion-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        border-radius: 15px;
        padding: 1.2rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255,255,255,0.2);
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
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .suggestion-card:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .suggestion-card:hover::before {
        left: 100%;
    }
    
    .suggestion-emoji {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .suggestion-title {
        font-weight: 600;
        color: #333;
        margin-bottom: 0.3rem;
        font-size: 1rem;
    }
    
    .suggestion-desc {
        color: #666;
        font-size: 0.85rem;
        line-height: 1.4;
    }
    
    /* Sidebar */
    .sidebar-container {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--glass-border);
        color: white;
    }
    
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.8rem;
        margin: 1rem 0;
    }
    
    .stat-item {
        background: rgba(255,255,255,0.1);
        padding: 0.8rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .stat-value {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    
    .stat-label {
        font-size: 0.7rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Controls */
    .controls-container {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid var(--glass-border);
        display: flex;
        gap: 1rem;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .control-btn {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        font-size: 0.9rem;
        box-shadow: 0 3px 10px rgba(255, 107, 107, 0.3);
    }
    
    .control-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
    }
    
    .export-btn {
        background: linear-gradient(135deg, #34B7F1 0%, #1e90ff 100%);
        box-shadow: 0 3px 10px rgba(52, 183, 241, 0.3);
    }
    
    .export-btn:hover {
        box-shadow: 0 5px 15px rgba(52, 183, 241, 0.4);
    }
    
    /* Input Area */
    .chat-input-container {
        background: white;
        border-radius: 25px;
        padding: 0.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.8rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
        text-transform: none;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4);
    }
    
    /* Status Indicator */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(37, 211, 102, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid rgba(37, 211, 102, 0.3);
        color: white;
        font-size: 0.85rem;
        margin: 0.5rem 0;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: #25D366;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .message-bubble {
            max-width: 85%;
        }
        
        .suggestions-grid {
            grid-template-columns: 1fr;
        }
        
        .header-title {
            font-size: 2.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Language configuration
LANGUAGES = {
    "en": {
        "title": "🤖 Career Chat Assistant V3.0",
        "subtitle": "Smart career guidance with advanced AI technology",
        "suggestions_title": "💬 Quick Questions",
        "chat_title": "Career Consultation",
        "sidebar_title": "🎯 Chat Navigator",
        "stats_title": "📊 Session Stats",
        "controls_title": "🔧 Controls",
        "suggestions": [
            {
                "emoji": "🚀",
                "title": "AI Career Path",
                "desc": "Complete roadmap to become an AI Engineer",
                "query": "What skills do I need to become an AI Engineer?"
            },
            {
                "emoji": "🔗",
                "title": "Blockchain Future",
                "desc": "Explore Web3 and DeFi career opportunities",
                "query": "What are the career prospects in blockchain?"
            },
            {
                "emoji": "📊",
                "title": "Audit Evolution", 
                "desc": "Future of audit careers in digital era",
                "query": "How will audit careers evolve in the next 5 years?"
            },
            {
                "emoji": "💡",
                "title": "Career Transition",
                "desc": "Proven strategies for successful career change",
                "query": "What are the best tips for transitioning to tech industry?"
            }
        ],
        "quick_topics": {
            "🤖 AI Career": "What skills do I need for AI careers?",
            "🔗 Blockchain": "Blockchain career opportunities",
            "💼 Salary Info": "Tech salary benchmarks 2025",
            "🎯 Career Tips": "Career transition strategies"
        },
        "controls": {
            "clear": "🗑️ Clear Chat",
            "export": "💾 Export Chat",
            "help": "Need help with your career?"
        },
        "status": {
            "online": "Online & Ready",
            "messages": "Messages",
            "active": "Active Since",
            "version": "Version"
        }
    },
    "id": {
        "title": "🤖 Career Chat Assistant V3.0",
        "subtitle": "Konsultasi karir cerdas dengan teknologi AI terdepan",
        "suggestions_title": "💬 Pertanyaan Cepat",
        "chat_title": "Konsultasi Karir",
        "sidebar_title": "🎯 Navigator Chat",
        "stats_title": "📊 Statistik Sesi",
        "controls_title": "🔧 Kontrol",
        "suggestions": [
            {
                "emoji": "🚀",
                "title": "Jalur Karir AI",
                "desc": "Roadmap lengkap menjadi AI Engineer",
                "query": "Skill apa yang dibutuhkan untuk menjadi AI Engineer?"
            },
            {
                "emoji": "🔗",
                "title": "Masa Depan Blockchain",
                "desc": "Eksplorasi karir Web3 dan DeFi",
                "query": "Bagaimana prospek karir di blockchain?"
            },
            {
                "emoji": "📊",
                "title": "Evolusi Audit",
                "desc": "Masa depan karir audit di era digital",
                "query": "Bagaimana evolusi karir audit 5 tahun mendatang?"
            },
            {
                "emoji": "💡",
                "title": "Transisi Karir", 
                "desc": "Strategi sukses mengubah karir",
                "query": "Tips terbaik transisi karir ke industri teknologi?"
            }
        ],
        "quick_topics": {
            "🤖 Karir AI": "Skill yang dibutuhkan untuk karir AI?",
            "🔗 Blockchain": "Peluang karir blockchain",
            "💼 Info Gaji": "Benchmark gaji tech 2025",
            "🎯 Tips Karir": "Strategi transisi karir"
        },
        "controls": {
            "clear": "🗑️ Hapus Chat",
            "export": "💾 Ekspor Chat",
            "help": "Butuh bantuan dengan karir Anda?"
        },
        "status": {
            "online": "Online & Siap",
            "messages": "Pesan",
            "active": "Aktif Sejak",
            "version": "Versi"
        }
    }
}

# Enhanced Career Knowledge Base
CAREER_KNOWLEDGE = {
    "en": {
        "ai_career": """
**🤖 AI Engineer Career Guide:**

**Essential Skills:**
• Python Programming (Industry Standard)
• Machine Learning Frameworks (TensorFlow, PyTorch)
• Statistics & Mathematics
• Data Processing (Pandas, NumPy)
• Cloud Platforms (AWS, Google Cloud, Azure)

**Learning Timeline: 6-12 months**
1. **Months 1-2:** Python basics + statistics
2. **Months 3-4:** Machine learning fundamentals  
3. **Months 5-6:** Deep learning & neural networks
4. **Months 7-8:** Specialized areas (NLP, Computer Vision)
5. **Months 9-12:** Portfolio projects + job applications

**Salary Range:** $80,000 - $180,000
**Growth Rate:** 22% annually

**Pro Tips:**
• Start with Andrew Ng's ML course on Coursera
• Build 3-5 portfolio projects on GitHub
• Join AI communities and competitions
• Practice with Kaggle datasets

**Ready to create your personalized AI learning roadmap?** 🚀
        """,
        
        "blockchain_career": """
**🔗 Blockchain & Web3 Career Opportunities:**

**Hot Positions:**
• Smart Contract Developer ($90K-$200K)
• Blockchain Architect ($120K-$250K)
• DeFi Protocol Developer ($100K-$300K)
• Web3 Product Manager ($80K-$180K)

**Essential Skills:**
• Solidity programming
• JavaScript/TypeScript
• Cryptography fundamentals
• DeFi protocol understanding
• Web3 libraries (Web3.js, Ethers.js)

**Industry Reality:**
• High growth but volatile market
• Strong remote work culture
• Equity/token compensation common
• Rapid technological evolution

**Learning Strategy:**
1. **Foundation:** Ethereum whitepaper + Solidity basics
2. **Practice:** Build simple DApps
3. **Advanced:** Study DeFi protocol code
4. **Network:** Join Web3 communities & hackathons

**Market Outlook:** Despite volatility, institutional adoption continues growing. Perfect timing for early adopters! 📈
        """,
        
        "audit_evolution": """
**📊 Audit Career Evolution 2025-2030:**

**Digital Transformation Impact:**
Traditional audit is evolving into **Intelligent Audit** with AI-powered tools replacing manual procedures.

**Emerging Audit Roles:**
• **Digital Audit Specialist** - Data analytics focus
• **ESG Audit Expert** - Sustainability compliance
• **Cybersecurity Auditor** - IT risk assessment  
• **Process Mining Analyst** - Automated audit trails

**Skills Upgrade Roadmap:**
1. **Data Analytics:** Excel → Python/R → Tableau/Power BI
2. **Technology:** IT basics → Cloud platforms → Cybersecurity
3. **ESG:** Traditional audit → Sustainability frameworks
4. **Automation:** Manual testing → Audit software → AI tools

**Market Dynamics:**
• 15-25% salary increase for tech-savvy auditors
• Remote audit capabilities expanding globally
• Big 4 firms investing heavily in audit technology
• Regulatory complexity creating more demand

**Strategic Advice:**
• Pursue CPA + IT audit specialization
• Learn Python for data analysis
• Understand ESG frameworks
• Network with audit technology vendors

**Timeline:** This transformation spans 3-5 years. Early adopters will command premium salaries! 💼
        """,
        
        "career_transition": """
**🎯 Career Transition Blueprint - Proven Strategy:**

**Phase 1: Assessment (Month 1)**
• Skills audit: current vs. required capabilities
• Industry research: salary, market, growth projections
• Network mapping: identify helpful connections

**Phase 2: Skill Building (Months 2-6)**
• 70% focus on hard skills (programming, tools)
• 30% soft skills (communication, leadership)
• Build portfolio with real projects
• Obtain relevant certifications

**Phase 3: Market Entry (Months 7-12)**
• LinkedIn optimization with keywords
• Apply to 5-10 positions weekly
• Network with industry professionals
• Prepare for technical interviews

**Success Metrics:**
• 80% of professionals successfully transition within 12-18 months
• Average salary increase: 20-40%
• Key factor: consistency in learning + networking

**Common Pitfalls:**
❌ Tutorial paralysis - too much learning, not enough practice
❌ Perfectionism - waiting to be "ready" before applying
❌ Isolated learning - not networking with industry

**Pro Tips:**
✅ Start applying when 70% ready
✅ Build in public - share your learning journey
✅ Find mentors in target industry
✅ Join relevant communities early

**Budget:** Allocate $1,000-$2,000 for courses, certifications, and networking events.
        """
    },
    
    "id": {
        "ai_career": """
**🤖 Panduan Karir AI Engineer:**

**Skill Fundamental:**
• Programming Python (Standar Industri)
• Framework Machine Learning (TensorFlow, PyTorch)
• Statistik & Matematika
• Pengolahan Data (Pandas, NumPy)
• Platform Cloud (AWS, Google Cloud, Azure)

**Timeline Belajar: 6-12 bulan**
1. **Bulan 1-2:** Dasar Python + statistik
2. **Bulan 3-4:** Fundamental machine learning
3. **Bulan 5-6:** Deep learning & neural networks
4. **Bulan 7-8:** Area spesialisasi (NLP, Computer Vision)
5. **Bulan 9-12:** Proyek portfolio + melamar kerja

**Range Gaji:** $80,000 - $180,000 (15-50 juta/bulan)
**Tingkat Pertumbuhan:** 22% per tahun

**Tips Pro:**
• Mulai dengan course ML Andrew Ng di Coursera
• Bangun 3-5 proyek portfolio di GitHub
• Gabung komunitas AI dan kompetisi
• Latihan dengan dataset Kaggle

**Siap membuat roadmap pembelajaran AI yang personal?** 🚀
        """,
        
        "blockchain_career": """
**🔗 Peluang Karir Blockchain & Web3:**

**Posisi Populer:**
• Smart Contract Developer ($90K-$200K)
• Blockchain Architect ($120K-$250K)
• DeFi Protocol Developer ($100K-$300K)
• Web3 Product Manager ($80K-$180K)

**Skill Penting:**
• Programming Solidity
• JavaScript/TypeScript
• Dasar kriptografi
• Pemahaman protokol DeFi
• Library Web3 (Web3.js, Ethers.js)

**Realita Industri:**
• Pertumbuhan tinggi tapi pasar volatile
• Budaya remote work yang kuat
• Kompensasi equity/token umum
• Evolusi teknologi yang cepat

**Strategi Belajar:**
1. **Fondasi:** Whitepaper Ethereum + dasar Solidity
2. **Praktik:** Bangun DApp sederhana
3. **Lanjutan:** Pelajari kode protokol DeFi
4. **Network:** Gabung komunitas Web3 & hackathon

**Outlook Pasar:** Meski volatile, adopsi institusional terus tumbuh. Timing sempurna untuk early adopter! 📈
        """,
        
        "audit_evolution": """
**📊 Evolusi Karir Audit 2025-2030:**

**Dampak Transformasi Digital:**
Audit tradisional berevolusi menjadi **Intelligent Audit** dengan tools AI menggantikan prosedur manual.

**Role Audit Baru:**
• **Digital Audit Specialist** - Fokus data analytics
• **ESG Audit Expert** - Compliance sustainability
• **Cybersecurity Auditor** - Penilaian risiko IT
• **Process Mining Analyst** - Audit trail otomatis

**Roadmap Upgrade Skill:**
1. **Data Analytics:** Excel → Python/R → Tableau/Power BI
2. **Teknologi:** Dasar IT → Platform cloud → Cybersecurity
3. **ESG:** Audit tradisional → Framework sustainability
4. **Otomasi:** Testing manual → Software audit → Tools AI

**Dinamika Pasar:**
• Kenaikan gaji 15-25% untuk auditor tech-savvy
• Kemampuan remote audit ekspansi global
• Big 4 investasi besar di teknologi audit
• Kompleksitas regulasi menciptakan demand lebih

**Saran Strategis:**
• Kejar CPA + spesialisasi IT audit
• Pelajari Python untuk analisis data
• Pahami framework ESG
• Network dengan vendor teknologi audit

**Timeline:** Transformasi ini berlangsung 3-5 tahun. Early adopter akan dapat gaji premium! 💼
        """,
        
        "career_transition": """
**🎯 Blueprint Transisi Karir - Strategi Terbukti:**

**Fase 1: Assessment (Bulan 1)**
• Audit skill: kemampuan saat ini vs yang dibutuhkan
• Riset industri: gaji, pasar, proyeksi pertumbuhan
• Pemetaan network: identifikasi koneksi yang membantu

**Fase 2: Skill Building (Bulan 2-6)**
• 70% fokus hard skills (programming, tools)
• 30% soft skills (komunikasi, leadership)
• Bangun portfolio dengan proyek nyata
• Dapatkan sertifikasi relevan

**Fase 3: Market Entry (Bulan 7-12)**
• Optimasi LinkedIn dengan keywords
• Lamar 5-10 posisi per minggu
• Network dengan profesional industri
• Persiapan interview teknis

**Metrik Sukses:**
• 80% profesional berhasil transisi dalam 12-18 bulan
• Rata-rata kenaikan gaji: 20-40%
• Faktor kunci: konsistensi belajar + networking

**Jebakan Umum:**
❌ Tutorial paralysis - terlalu banyak belajar, kurang praktik
❌ Perfeksionisme - menunggu "siap" sebelum melamar
❌ Belajar terisolasi - tidak network dengan industri

**Tips Pro:**
✅ Mulai melamar saat 70% siap
✅ Build in public - share journey belajar
✅ Cari mentor di industri target
✅ Gabung komunitas relevan sejak awal

**Budget:** Alokasikan 15-30 juta untuk kursus, sertifikasi, dan acara networking.
        """
    }
}

def get_smart_response(question, language="en"):
    """Generate contextual responses based on language and question"""
    question_lower = question.lower()
    lang_knowledge = CAREER_KNOWLEDGE[language]
    
    # Greeting responses
    greeting_words_en = ["hello", "hi", "hey", "good morning", "good afternoon"]
    greeting_words_id = ["halo", "hai", "selamat", "pagi", "siang", "sore"]
    
    if language == "en":
        greeting_words = greeting_words_en
        greeting_response = """
👋 **Hello! Welcome to Career Chat Assistant V3.0!**

I'm here to help you navigate your career future with actionable insights and up-to-date guidance.

**I can help you with:**
• Career prospects analysis in future industries
• Learning roadmaps for in-demand skills
• Effective career transition strategies
• Salary benchmarks and growth projections
• Networking and personal branding tips

**What would you like to explore today?** 🚀
        """
    else:
        greeting_words = greeting_words_id
        greeting_response = """
👋 **Halo! Selamat datang di Career Chat Assistant V3.0!**

Saya siap membantu Anda menavigasi masa depan karir dengan insights yang actionable dan guidance terkini.

**Saya bisa bantu dengan:**
• Analisis prospek karir di industri masa depan
• Roadmap pembelajaran untuk skill yang in-demand
• Strategi transisi karir yang efektif
• Benchmark gaji dan proyeksi pertumbuhan
• Tips networking dan personal branding

**Apa yang ingin kita jelajahi hari ini?** 🚀
        """
    
    if any(word in question_lower for word in greeting_words):
        return greeting_response
    
    # Career-specific responses
    ai_keywords = ["ai engineer", "artificial intelligence", "machine learning", "data science", "ai career"]
    blockchain_keywords = ["blockchain", "web3", "crypto", "defi", "smart contract"]
    audit_keywords = ["audit", "auditor", "komite audit", "audit career"]
    transition_keywords = ["transition", "career change", "transisi", "pindah karir", "berubah karir", "tips"]
    
    if any(keyword in question_lower for keyword in ai_keywords):
        return lang_knowledge["ai_career"]
    elif any(keyword in question_lower for keyword in blockchain_keywords):
        return lang_knowledge["blockchain_career"]
    elif any(keyword in question_lower for keyword in audit_keywords):
        return lang_knowledge["audit_evolution"]
    elif any(keyword in question_lower for keyword in transition_keywords):
        return lang_knowledge["career_transition"]
    
    # Default intelligent responses
    if language == "en":
        default_responses = [
            """
**🔮 Career Intelligence Update 2025:**

**Top 3 Industry Trends:**

**1. AI Integration Everywhere**
Not just tech companies - finance, healthcare, retail all adopting AI. Demand for AI literacy increased 300%.

**2. Remote-First Culture**
80% of companies now permanently hybrid. Global opportunities wide open for skilled professionals.

**3. Sustainability Focus**
ESG compliance becoming mandatory. Green jobs projected to grow 400% in 5 years.

**Quick Action Steps:**
• Update skills through online learning platforms
• Optimize LinkedIn with relevant keywords
• Join professional communities in target industries
• Start building a portfolio showcasing your capabilities

**Which area would you like to explore deeper?** 🎯
            """,
            
            """
**💡 Strategic Career Framework:**

**The 3-Pillar Approach for Career Growth:**

**Pillar 1: Skill Stacking**
Unique combination of skills that makes you irreplaceable. Example: Data Analysis + Domain Knowledge + Communication.

**Pillar 2: Network Leverage**
70% of opportunities come from networking. Invest 20% of your time in relationship building.

**Pillar 3: Market Positioning**
Clear personal branding: what's your expertise and who do you serve.

**Implementation Timeline:**
• Week 1-2: Skills assessment & gap analysis
• Week 3-4: Learning plan & resource curation
• Month 2-3: Active learning + portfolio building
• Month 4+: Network expansion + market positioning

**ROI:** This strategy typically results in 25-40% salary increase within 12-18 months.

**Want me to help detail the implementation for your specific situation?** 🚀
            """
        ]
    else:
        default_responses = [
            """
**🔮 Update Career Intelligence 2025:**

**Top 3 Tren Industri:**

**1. Integrasi AI di Mana-Mana**
Bukan hanya perusahaan tech - finance, healthcare, retail semua adopsi AI. Demand untuk AI literacy naik 300%.

**2. Budaya Remote-First**
80% perusahaan sekarang permanent hybrid. Peluang global terbuka lebar untuk profesional skilled.

**3. Fokus Sustainability**
Compliance ESG jadi mandatory. Green jobs diproyeksikan tumbuh 400% dalam 5 tahun.

**Langkah Aksi Cepat:**
• Update skill melalui platform pembelajaran online
• Optimasi LinkedIn dengan kata kunci relevan
• Gabung komunitas profesional di industri target
• Mulai bangun portfolio yang showcase kemampuan

**Area mana yang ingin kita eksplorasi lebih dalam?** 🎯
            """,
            
            """
**💡 Framework Karir Strategis:**

**Pendekatan 3-Pilar untuk Career Growth:**

**Pilar 1: Skill Stacking**
Kombinasi unik skill yang bikin Anda irreplaceable. Contoh: Data Analysis + Domain Knowledge + Communication.

**Pilar 2: Network Leverage**
70% peluang datang dari networking. Invest 20% waktu untuk relationship building.

**Pilar 3: Market Positioning**
Personal branding yang jelas: apa expertise Anda dan untuk siapa.

**Timeline Implementasi:**
• Minggu 1-2: Assessment skill & analisis gap
• Minggu 3-4: Rencana belajar & kurasi resource
• Bulan 2-3: Active learning + portfolio building
• Bulan 4+: Ekspansi network + market positioning

**ROI:** Strategi ini biasanya menghasilkan kenaikan gaji 25-40% dalam 12-18 bulan.

**Mau saya bantu detail implementasi untuk situasi spesifik Anda?** 🚀
            """
        ]
    
    return random.choice(default_responses)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0
if "language" not in st.session_state:
    st.session_state.language = "en"

# Get current language settings
current_lang = st.session_state.language
lang_config = LANGUAGES[current_lang]

# Header Section
st.markdown(f"""
<div class="app-header">
    <div class="header-title">{lang_config['title']}</div>
    <div class="header-subtitle">{lang_config['subtitle']}</div>
    <div class="version-badge">V3.0 • Enhanced Interactive Platform</div>
</div>
""", unsafe_allow_html=True)

# Language Selector
st.markdown("""
<div class="language-selector">
    <span style="color: white; font-weight: 500; margin-right: 1rem;">🌐 Language:</span>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🇺🇸 English", key="lang_en"):
        st.session_state.language = "en"
        st.rerun()

with col2:
    if st.button("🇮🇩 Bahasa Indonesia", key="lang_id"):
        st.session_state.language = "id"
        st.rerun()

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-container">
        <div class="sidebar-title">{lang_config['sidebar_title']}</div>
        <div class="status-indicator">
            <div class="status-dot"></div>
            {lang_config['status']['online']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Session Stats
    st.markdown(f"""
    <div class="sidebar-container">
        <div class="sidebar-title">{lang_config['stats_title']}</div>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{len(st.session_state.messages)}</div>
                <div class="stat-label">{lang_config['status']['messages']}</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{datetime.now().strftime('%H:%M')}</div>
                <div class="stat-label">{lang_config['status']['active']}</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">V3.0</div>
                <div class="stat-label">{lang_config['status']['version']}</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">🟢</div>
                <div class="stat-label">Status</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Topics
    st.markdown(f"""
    <div class="sidebar-container">
        <div class="sidebar-title">⚡ Quick Topics</div>
    </div>
    """, unsafe_allow_html=True)
    
    for label, query in lang_config["quick_topics"].items():
        if st.button(label, key=f"quick_{label}_{current_lang}"):
            st.session_state.suggested_question = query

# Suggestions Section
st.markdown(f"""
<div class="suggestions-container">
    <div class="suggestions-title">{lang_config['suggestions_title']}</div>
    <div class="suggestions-grid">
""", unsafe_allow_html=True)

# Create suggestion cards HTML
suggestions_html = ""
for i, suggestion in enumerate(lang_config["suggestions"]):
    suggestions_html += f"""
    <div class="suggestion-card" onclick="selectSuggestion{i}()">
        <span class="suggestion-emoji">{suggestion['emoji']}</span>
        <div class="suggestion-title">{suggestion['title']}</div>
        <div class="suggestion-desc">{suggestion['desc']}</div>
    </div>
    """

st.markdown(suggestions_html + "</div></div>", unsafe_allow_html=True)

# JavaScript for suggestion clicks
suggestion_js = ""
for i, suggestion in enumerate(lang_config["suggestions"]):
    suggestion_js += f"""
    function selectSuggestion{i}() {{
        const input = window.parent.document.querySelector('[data-testid="textInput-input"]');
        if (input) {{
            input.value = "{suggestion['query']}";
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
    }}
    """

st.markdown(f"<script>{suggestion_js}</script>", unsafe_allow_html=True)

# Chat Interface
st.markdown(f"""
<div class="suggestions-container">
    <div class="suggestions-title">{lang_config['chat_title']}</div>
    <div class="chat-container" id="chatContainer">
""", unsafe_allow_html=True)

# Display chat messages
if st.session_state.messages:
    for message in st.session_state.messages:
        message_time = datetime.now().strftime("%H:%M")
        
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message-container user">
                <div class="message-bubble user-message">
                    {message["content"]}
                    <div class="message-time">{message_time}</div>
                </div>
                <div class="message-avatar user-avatar">👤</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-container assistant">
                <div class="message-avatar assistant-avatar">🤖</div>
                <div class="message-bubble assistant-message">
                    {message["content"]}
                    <div class="message-time">{message_time}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    # Welcome message
    welcome_msg = lang_config["controls"]["help"]
    st.markdown(f"""
    <div class="message-container assistant">
        <div class="message-avatar assistant-avatar">🤖</div>
        <div class="message-bubble assistant-message">
            {welcome_msg}
            <div class="message-time">{datetime.now().strftime("%H:%M")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# Handle suggested questions
if "suggested_question" in st.session_state:
    question = st.session_state.suggested_question
    del st.session_state.suggested_question
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Show typing indicator
    st.markdown("""
    <div class="message-container assistant">
        <div class="message-avatar assistant-avatar">🤖</div>
        <div class="typing-container">
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate thinking time
    time.sleep(2)
    
    # Generate response
    response = get_smart_response(question, current_lang)
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_count += 1
    st.rerun()

# Chat input
if prompt := st.chat_input("Type your career question here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    response = get_smart_response(prompt, current_lang)
    
    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_count += 1
    st.rerun()

# Controls
st.markdown(f"""
<div class="controls-container">
    <div style="color: white; font-weight: 500; margin-right: 1rem;">{lang_config['controls_title']}</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button(lang_config["controls"]["clear"], help="Reset conversation"):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.rerun()

with col2:
    if st.session_state.messages:
        chat_export = {
            "timestamp": datetime.now().isoformat(),
            "language": current_lang,
            "total_messages": len(st.session_state.messages),
            "conversation": st.session_state.messages
        }
        st.download_button(
            lang_config["controls"]["export"],
            data=json.dumps(chat_export, indent=2, ensure_ascii=False),
            file_name=f"career_chat_v3_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            help="Download conversation history"
        )

# Enhanced Footer
st.markdown("---")

def render_v3_footer():
    current_year = datetime.now().year
    version = "3.0.1"
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-top: 3rem;
        text-align: center;
        box-shadow: 0 20px 60px rgba(37, 211, 102, 0.3);
        position: relative;
        overflow: hidden;
    ">
        <div style="position: relative; z-index: 1;">
            <h3 style="margin-bottom: 1.5rem; font-size: 2rem;">🚀 Career Chat Assistant V3.0</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin: 2rem 0;">
                <div style="background: rgba(255,255,255,0.15); padding: 1.5rem; border-radius: 15px; backdrop-filter: blur(10px);">
                    <h4 style="color: #fff; margin-bottom: 1rem;">✨ V3.0 Features</h4>
                    <p style="font-size: 0.9rem; line-height: 1.5;">
                        • WhatsApp-like Chat Interface<br>
                        • Multi-language Support<br>
                        • Enhanced AI Responses<br>
                        • Smooth Animations<br>
                        • Mobile-Optimized Design
                    </p>
                </div>
                
                <div style="background: rgba(255,255,255,0.15); padding: 1.5rem; border-radius: 15px; backdrop-filter: blur(10px);">
                    <h4 style="color: #fff; margin-bottom: 1rem;">🛠️ Technology Stack</h4>
                    <p style="font-size: 0.9rem; line-height: 1.5;">
                        • Python 3.11 + Streamlit<br>
                        • Advanced CSS3 Animations<br>
                        • Responsive Grid Layout<br>
                        • Local AI Processing<br>
                        • Progressive Web App Ready
                    </p>
                </div>
                
                <div style="background: rgba(255,255,255,0.15); padding: 1.5rem; border-radius: 15px; backdrop-filter: blur(10px);">
                    <h4 style="color: #fff; margin-bottom: 1rem;">👥 Development Team</h4>
                    <p style="font-size: 0.9rem; line-height: 1.5;">
                        • <strong>MS Hadianto</strong><br>Lead Project & Innovation<br>
                        • <strong>Faby</strong><br>Co-Lead & UX/UI Design
                    </p>
                </div>
            </div>
            
            <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2);">
                <p style="font-size: 1.1rem; margin-bottom: 1rem; font-weight: 600;">
                    © {current_year} Career Shift Analyzer V{version} • Next-Gen Career Guidance Platform
                </p>
                <p style="font-size: 0.85rem; color: rgba(255,255,255,0.9); line-height: 1.4; max-width: 800px; margin: 0 auto;">
                    <em>Disclaimer: This platform provides educational career guidance. Results may vary based on individual circumstances. 
                    Always verify information and consult with career professionals for personalized advice. 
                    Multi-language support powered by advanced AI technology.</em>
                </p>
                <p style="margin-top: 1.5rem; font-size: 1rem; color: #fff;">
                    🌟 Building the Future of Career Development • 🌍 Available Worldwide
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

render_v3_footer()
