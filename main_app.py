import os
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
selected_program = st.sidebar.selectbox(
    "Select Training Program",
    [
        "1. Industry-Integrated B.E./B.Tech (4 Years)",
        "2. Super 30 Skill Program (6 Months + 12M Placement)",
        "3. AI Engineering Workshop (4 Semesters / 40 Days)",
        "4. GenAI & Agentic AI Master Program (8 Weekends)",
        "5. IIT Guwahati & PragyanAI SDP (12 Modules)",
    ],
)

view_mode = st.sidebar.radio(
    "Dashboard View",
    ["Executive KPI Dashboard", "RAG & GROQ LLM Assistant", "GitHub Code Explorer"],
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
  st.subheader(f"📈 Analytics Overview for: {selected_program}")
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

elif view_mode == "RAG & GROQ LLM Assistant":
  st.title("💬 Intelligent Program Advisor (RAG + Groq LLM)")
  st.markdown(
      "Query curriculum guidelines, institutional pricing, and technical"
      " specifications instantly using high-speed vector retrieval."
  )

  prompt = st.text_input(
      "Ask a question about curriculum, admission criteria, or fees:",
      placeholder=(
          "e.g., What is covered in the 8th week of the working professionals"
          " program?"
      ),
  )

  if st.button("Query RAG Engine"):
    if prompt:
      with st.spinner("Retrieving semantic vectors and generating response..."):
        retrieved_context = search_knowledge_base(prompt)
        ai_response = get_groq_response(prompt, retrieved_context)
        st.success("Query Resolved Successfully via Vector Store & Groq LLM!")
        st.markdown(f"**AI Advisor Response:**\n\n{ai_response}")
    else:
      st.warning("Please enter a query.")

elif view_mode == "GitHub Code Explorer":
  st.title("📂 GitHub Repository File Explorer")
  st.markdown(
      "Examine production-ready modular scripts configured for this program
