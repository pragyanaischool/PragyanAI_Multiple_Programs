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
        "GitHub PDF & Flipbook Hub",
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

elif view_mode == "GitHub PDF & Flipbook Hub":
    st.title("📖 PragyanAI GitHub PDF & Flipbook Viewer")
    st.markdown("Access and view official program PDFs hosted directly on your GitHub repository (`pragyanaischool/PragyanAI_Multiple_Programs`).")
    
    # Official GitHub Raw URLs for seamless rendering
    github_pdf_library = {
        "Enterprise Agentic AI Master Program": "https://raw.githubusercontent.com/pragyanaischool/PragyanAI_Multiple_Programs/main/data/Enterprise_Agentic_AI_Master_Program.pdf",
        "6-Month Offline Training & Placement": "https://raw.githubusercontent.com/pragyanaischool/PragyanAI_Multiple_Programs/main/data/PragyanAI-6%20Month%20Offline%20Training%20-%20Passed%20Out%20Students.pdf",
        "IIT Guwahati SDP Proposal": "https://raw.githubusercontent.com/pragyanaischool/PragyanAI_Multiple_Programs/main/data/SDP_Proposal_EICT_IITG.pdf"
    }
    
    selected_pdf_title = st.selectbox("Select GitHub PDF Document", list(github_pdf_library.keys()))
    pdf_url = github_pdf_library[selected_pdf_title]
    
    st.markdown(f"### 📄 Viewing: `{selected_pdf_title}`")
    
    # Render PDF using Google Docs Viewer wrapper to prevent 'No preview available' browser blocks
    viewer_iframe = f'<iframe src="https://docs.google.com/gview?url={pdf_url}&embedded=true" width="100%" height="700px" style="border-radius: 12px; border: 1px solid #334155;"></iframe>'
    st.markdown(viewer_iframe, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📖 Digital Flipbook Spread View")
    col_prev, col_spread, col_next = st.columns([1, 6, 1])
    with col_prev:
        if st.button("◀ Previous Spread"):
            st.toast("Flipped back one spread.")
    with col_spread:
        st.info("Interactive dual-page spread simulator active.")
        st.image(
            "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=1200&auto=format&fit=crop",
            caption=f"Flipbook Spread — {selected_pdf_title}",
            use_container_width=True
        )
    with col_next:
        if st.button("Next Spread ▶"):
            st.toast("Flipped forward one spread.")

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
