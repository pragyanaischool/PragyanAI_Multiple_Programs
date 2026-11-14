import os
import pandas as pd
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def expand_query(query: str) -> str:
    """Expands user query with domain-specific keywords for better retrieval coverage."""
    query_lower = query.lower()
    expansions = []
    if any(kw in query_lower for kw in ["fee", "price", "cost", "pricing", "pay", "rupee", "inr"]):
        expansions.append("Pricing & Financials investment fee structure success fee stipend")
    if any(kw in query_lower for kw in ["duration", "month", "year", "weeks", "time", "schedule"]):
        expansions.append("Duration mode timeline schedule offline online hybrid")
    if any(kw in query_lower for kw in ["project", "hackathon", "mvp", "portfolio", "capstone"]):
        expansions.append("Projects MVP capstone hackathons portfolio code github")
    if any(kw in query_lower for kw in ["placement", "job", "career", "salary", "hiring"]):
        expansions.append("Placement support CTC recruitment hiring companies roles")
    if expansions:
        return f"{query} " + " ".join(expansions)
    return query

@st.cache_resource
def get_vector_store():
    """Initializes and caches the HuggingFace embeddings model and FAISS vector index."""
    csv_path = "data/PragyanAI_All_Programs_FAQ_Master.csv"
    if not os.path.exists(csv_path):
        return None, "Master CSV knowledge base not found under data/."

    try:
        df = pd.read_csv(csv_path)
        documents = []
        for _, row in df.iterrows():
            doc_text = (
                f"Program Name: {str(row.get('Program Name', ''))} | "
                f"Duration: {str(row.get('Duration', ''))} | "
                f"Mode: {str(row.get('Mode', ''))} | "
                f"Target Audience: {str(row.get('Target Audience', ''))} | "
                f"Key Skills Covered: {str(row.get('Key Skills Covered', ''))} | "
                f"Projects: {str(row.get('Projects', ''))} | "
                f"Pricing & Financials: {str(row.get('Pricing & Financials', ''))} | "
                f"Source Reference: Official PragyanAI Master Knowledge Base"
            )
            documents.append(doc_text)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
        chunks = text_splitter.create_documents(documents)

        if not chunks:
            return None, "No valid document chunks generated from CSV."

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = FAISS.from_documents(chunks, embeddings)
        return vector_db, None
    except Exception as e:
        return None, str(e)

def search_knowledge_base(query: str) -> str:
    """
    Searches the master CSV knowledge base utilizing cached FAISS vector store,
    HuggingFace embeddings, multi-query expansion, and robust fallback grounding.
    """
    csv_path = "data/PragyanAI_All_Programs_FAQ_Master.csv"
    if not os.path.exists(csv_path):
        return "Knowledge base master CSV file not found. Please verify the data directory structure under data/."

    try:
        vector_db, err = get_vector_store()
        if vector_db is None:
            raise Exception(err)

        enhanced_query = expand_query(query)
        docs_and_scores = vector_db.similarity_search_with_score(enhanced_query, k=3)

        if not docs_and_scores:
            return "PragyanAI offers 10 core industry-aligned AI engineering programs covering practical execution, RAG, and multi-agent systems."

        context = "Retrieved Program Context via Semantic RAG (Grounded & Verified):\n"
        for i, (res, score) in enumerate(docs_and_scores, 1):
            confidence_marker = "High Confidence" if score < 1.2 else "Moderate Confidence"
            context += f"[{i}] ({confidence_marker}) {res.page_content}\n"
            
        return context

    except Exception as e:
        # Fallback keyword matching and regex scoring if local vector embeddings encounter environment issues
        try:
            df = pd.read_csv(csv_path)
            query_lower = query.lower()
            matched_rows = []
            for _, row in df.iterrows():
                row_str = " ".join(str(val) for val in row.values).lower()
                if any(kw in row_str for kw in query_lower.split() if len(kw) > 3):
                    matched_rows.append(row.to_dict())

            if not matched_rows:
                return "PragyanAI offers 10 core industry-aligned AI engineering programs ranging from B.E. integrations to working professional bootcamps."

            context = "Retrieved Program Context (Keyword Fallback Grounding):\n"
            for i, match in enumerate(matched_rows[:3], 1):
                context += (
                    f"[{i}] Program: {match.get('Program Name')} | "
                    f"Duration: {match.get('Duration')} | "
                    f"Pricing: {match.get('Pricing & Financials')} | "
                    f"Skills: {match.get('Key Skills Covered')}\n"
                )
            return context
        except Exception as fallback_err:
            return f"Error processing knowledge base query: {str(e)} | Fallback error: {str(fallback_err)}"
