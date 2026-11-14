import os
import base64
import streamlit as st
from PIL import Image
from src.services.rag_engine import search_knowledge_base
from src.services.groq_client import get_groq_response

# Page Configuration & Executive Layout
st.set_page_config(
    page_title="PragyanAI Enterprise AI & Institutional Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS Injection for Modern Styling & Executive UI
st.markdown(
    """
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background: linear-gradient(90deg, #f97316 0%, #ea580c 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ea580c 0%, #c2410c 100%);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation with Attached Transparent Logo
if os.path.exists("assets/images/PragyanAI_Transperent_2.png"):
    st.sidebar.image("assets/images/PragyanAI_Transperent_2.png", use_container_width=True)
else:
    st.sidebar.title("⚡ PragyanAI Hub")

st.sidebar.markdown("---")

view_mode = st.sidebar.radio(
    "Dashboard View",
    [
        "Executive KPI Dashboard", 
        "Program Flipbook & Document Hub",
        "RAG & GROQ LLM Assistant", 
        "Program Fee & ROI Calculator",
        "GitHub Code Explorer"
    ],
)

# Main Content Renderer
if view_mode == "Executive KPI Dashboard":
    st.title("📊 Enterprise Program Analytics & ROI Dashboard")
    st.markdown(
        "Real-time operational metrics across institutional partnerships, active"
        " cohorts, and student portfolio outcomes."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            '<div class="metric-card"><h3>1,000+</h3><p>Learning & Lab'
            " Hours</p></div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="metric-card"><h3>100+</h3><p>Verified Portfolio'
            " Projects</p></div>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="metric-card"><h3>100%</h3><p>Placement Support &'
            " Targeting</p></div>",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            '<div class="metric-card"><h3>₹10k</h3><p>Monthly Internship'
            " Stipend Tier</p></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.subheader("📈 Analytics Overview across Skill Tracks")
    st.bar_chart({
        "Skill Track": [
            "Python Full Stack",
            "Data Science & BI",
            "Machine Learning",
            "Deep Learning & CV",
            "Generative AI & RAG",
            "Agentic AI Swarms",
        ],
        "Completion Weight (%)": [15, 15, 20, 15, 20, 15],
    })

elif view_mode == "Program Flipbook & Document Hub":
    st.title("📖 PragyanAI Program Document & Flipbook Hub")
    st.markdown("Select any of the 10 core programs below or upload a custom program PDF brochure to open its dedicated view with visual flyers and interactive flipbook spreads.")
    
    programs_mapping = {
        "1. Industry-Integrated AI Engineering Program (4 Years)": {
            "duration": "4 Years (8 Semesters)",
            "desc": "Partnering with engineering colleges to offer an admission-oriented AI Engineering Program for 12th standard students[cite: 107].",
            "image": "PragyanAI_4Year_Industry_Integrated_Program.png"
        },
        "2. 6-Month Offline Training & Placement Program": {
            "duration": "6 Months Training + 12 Months Placement",
            "desc": "Intensive offline AI & GenAI training in Bangalore with 100+ projects and startup MVP exposure[cite: 108].",
            "image": "6Months_Program.png"
        },
        "3. 4-Semester 40-Day AI Engineering Workshop": {
            "duration": "4 Semesters (40 Days Total)",
            "desc": "On-campus training aligned with academic calendar covering 8 technical skill areas and 40 projects[cite: 109].",
            "image": "4Sem_40Days_Program.jpg"
        },
        "4. 8-Weekend GenAI & Agentic AI Master Program": {
            "duration": "8 Weekends + 3 Days Resort Capstone",
            "desc": "Working professional masterclass covering Transformer mechanics, RAG, LangGraph multi-agent swarms[cite: 110, 111].",
            "image": "IITG Program.jpg"
        },
        "5. IIT Guwahati & PragyanAI Skill Development Programme (SDP)": {
            "duration": "2 Weeks (30 Hours Live Online)",
            "desc": "12 AIML modules in collaboration with E&ICT Academy, IIT Guwahati, featuring hands-on learning[cite: 3].",
            "image": "IITG Program.jpg"
        },
        "6. Flexible Bootcamps & Academic Integrations": {
            "duration": "Half-Day to 5 Days",
            "desc": "Workshops, Faculty Development Programs (FDP), and guest lectures aligned with university curricula.",
            "image": "IITG Program.jpg"
        },
        "7. PragyanAI Skill Sprint PRO": {
            "duration": "10 Days Offline + 15 Days Online Hackathon",
            "desc": "Intensive daily hands-on and competitive hackathons delivering portfolio-ready projects.",
            "image": "6Months_Program.png"
        },
        "8. Project Series (12–24 Months)": {
            "duration": "12–24 Months (Fully Online)",
            "desc": "Monthly structured projects across AI/ML and Data Analytics building strong GitHub portfolios.",
            "image": "PragyanAI_4Year_Industry_Integrated_Program.png"
        },
        "9. 12-Month Working Professionals Program": {
            "duration": "12 Months (Hybrid / Weekend)",
            "desc": "Career acceleration for working professionals transitioning into GenAI and Agentic AI roles.",
            "image": "IITG Program.jpg"
        },
        "10. 2-Year Advanced AI/ML Program": {
            "duration": "2 Years (Work While You Learn)",
            "desc": "6 months foundation followed by 18 months real team execution with monthly stipend and direct hiring pathway.",
            "image": "6Months_Program.png"
        }
    }
    
    selected_program = st.selectbox("Select Training Program to View", list(programs_mapping.keys()))
    prog_data = programs_mapping[selected_program]
    
    st.markdown("---")
    st.header(f"📌 Program View: {selected_program}")
    
    col_details, col_visual = st.columns([1, 1])
    
    with col_details:
        st.subheader("📋 Program Overview & Highlights")
        st.write(f"**Duration:** {prog_data['duration']}")
        st.write(f"**Description:** {prog_data['desc']}")
        st.markdown("### 🔑 Key Skill Stack")
        st.success("✅ Python Full Stack, Data Science, Machine Learning, Deep Learning, GenAI & Agentic AI Swarms.")
        st.markdown("### 🏆 Expected Outcomes")
        st.info("• 100+ GitHub portfolio projects\n• Startup-Ready MVP or Industry Placement\n• Verifiable Digital Skill Passport")
        
    with col_visual:
        st.subheader("🎨 Official Program Flyer & Visual Asset")
        if os.path.exists(prog_data["image"]):
            st.image(prog_data["image"], caption=f"Official Flyer — {selected_program}", use_container_width=True)
        else:
            st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop", caption="Visual Asset Placeholder", use_container_width=True)

    st.markdown("---")
    st.subheader("📖 Interactive Digital PDF & Flipbook Spread Viewer")
    st.markdown("Upload a program brochure or PDF document below to render an interactive document viewer and flipbook spread simulator.")
    
    uploaded_pdf = st.file_uploader("Upload Program PDF Brochure", type=["pdf"])
    if uploaded_pdf is not None:
        st.success(f"Successfully loaded: **{uploaded_pdf.name}**")
        base64_pdf = base64.b64encode(uploaded_pdf.read()).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" style="border-radius: 12px; border: 1px solid #334155;"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        c_prev, c_view, c_next = st.columns([1, 5, 1])
        with c_prev:
            if st.button("◀ Previous Page"):
                st.toast("Flipped back one page.")
        with c_view:
            st.info(f"📄 Interactive Flipbook Spread — **{selected_program}**")
            st.image("https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=1200&auto=format&fit=crop", caption="Spread View (Pages 1 & 2)", use_container_width=True)
        with c_next:
            if st.button("Next Page ▶"):
                st.toast("Flipped forward one page.")

elif view_mode == "RAG & GROQ LLM Assistant":
    st.title("💬 Intelligent Program Advisor (RAG + Groq LLM)")
    st.markdown("Query curriculum guidelines, institutional pricing, and technical specifications instantly using high-speed vector retrieval.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about curriculum, admission criteria, or fees..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving semantic vectors and generating response..."):
                retrieved_context = search_knowledge_base(prompt)
                ai_response = get_groq_response(prompt, retrieved_context)
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

elif view_mode == "Program Fee & ROI Calculator":
    st.title("🧮 Program Fee & Career ROI Estimator")
    st.markdown("Calculate tuition investments, stipend returns, and salary payback periods instantly.")
    
    prog_type = st.selectbox("Choose Program", ["6-Month Super 30 Program", "8-Weekend Master Program", "4-Year B.E. Integration"])
    
    if prog_type == "6-Month Super 30 Program":
        tier = st.radio("Select Enrollment Tier", ["Founding Batch (Discounted + Success Fee)", "Standard Paid Track"])
        if "Founding" in tier:
            st.write("**Investment Breakdown:** ₹50,000 Initial Training Fee + ₹50,000 Success Fee (Post-Placement) = **₹1,00,000 Total**[cite: 102]")
        else:
            st.write("**Investment Breakdown:** Standard Flat Fee of **₹1,50,000** (Eligible for ₹10,000/mo stipend internship tier)")
    else:
        st.write("**Investment Breakdown:** All-inclusive promotional pricing starting at **₹50,000** including resort hackathon stay[cite: 148].")
        
    expected_salary = st.slider("Expected Starting Annual CTC (LPA)", 4.0, 30.0, 12.0, 0.5)
    st.success(f"Estimated Payback Period at ₹{expected_salary} LPA: **Less than 3 to 4 months** of employment!")

elif view_mode == "GitHub Code Explorer":
    st.title("📂 GitHub Repository File Explorer")
    st.markdown("Examine production-ready modular scripts configured for this program.")

    file_selected = st.selectbox(
        "Select File to Inspect",
        [
            "src/services/rag_engine.py",
            "src/services/groq_client.py",
            "data/PragyanAI_All_Programs_FAQ_Master.csv",
            "requirements.txt",
        ],
    )

    if file_selected == "src/services/rag_engine.py":
        with open("src/services/rag_engine.py", "r") as f:
            st.code(f.read(), language="python")
    elif file_selected == "src/services/groq_client.py":
        with open("src/services/groq_client.py", "r") as f:
            st.code(f.read(), language="python")
    elif file_selected == "data/PragyanAI_All_Programs_FAQ_Master.csv":
        with open("data/PragyanAI_All_Programs_FAQ_Master.csv", "r") as f:
            st.code(f.read(), language="csv")
    else:
        with open("requirements.txt", "r") as f:
            st.code(f.read(), language="text")
