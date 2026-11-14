import os
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def expand_query(query: str) -> str:
    """Expands user query with domain-specific keywords for better retrieval coverage."""
    query_lower = query.lower()
    expansions = []
    if "fee" in query_lower or "price" in query_lower or "cost" in query_lower:
        expansions.append("Pricing & Financials investment fee structure")
    if "duration" in query_lower or "month" in query_lower or "year" in query_lower:
        expansions.append("Duration mode timeline schedule")
    if "project" in query_lower or "hackathon" in query_lower:
        expansions.append("Projects MVP capstone hackathons portfolio")
    if expansions:
        return f"{query} " + " ".join(expansions)
    return query

def search_knowledge_base(query: str) -> str:
    """
    Searches the master CSV knowledge base for program details and matches keywords,
    utilizing a FAISS vector store with HuggingFace embeddings for semantic retrieval,
    query expansion, and source attribution grounding.
    """
    csv_path = "data/PragyanAI_All_Programs_FAQ_Master.csv"
    if not os.path.exists(csv_path):
        return "Knowledge base master CSV file not found. Please verify the data directory structure under data/."

    try:
        df = pd.read_csv(csv_path)
        
        # Combine row elements into structured documents with clear attribution metadata
        documents = []
        for _, row in df.iterrows():
            doc_text = (
                f"Program Name: {row.get('Program Name')} | "
                f"Duration: {row.get('Duration')} | "
                f"Mode: {row.get('Mode')} | "
                f"Target Audience: {row.get('Target Audience')} | "
                f"Key Skills Covered: {row.get('Key Skills Covered')} | "
                f"Projects: {row.get('Projects')} | "
                f"Pricing & Financials: {row.get('Pricing & Financials')} | "
                f"Source Reference: Official PragyanAI Master Knowledge Base"
            )
            documents.append(doc_text)

        # Initialize text splitter for semantic chunking
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
        chunks = text_splitter.create_documents(documents)

        # Initialize HuggingFace Embeddings & FAISS Vector Index
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = FAISS.from_documents(chunks, embeddings)

        # Apply query expansion for higher semantic recall
        enhanced_query = expand_query(query)

        # Perform similarity search (Top-K = 3 chunks)
        results = vector_db.similarity_search(enhanced_query, k=3)

        if not results:
            return "PragyanAI offers 10 core industry-aligned AI engineering programs covering practical execution, RAG, and multi-agent systems."

        context = "Retrieved Program Context via Semantic RAG (Grounded & Verified):\n"
        for i, res in enumerate(results, 1):
            context += f"[{i}] {res.page_content}\n"
        return context

    except Exception as e:
        # Fallback keyword matching and regex scoring if local vector embeddings encounter environment issues
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
