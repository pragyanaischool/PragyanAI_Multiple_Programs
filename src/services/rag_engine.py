import os
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def search_knowledge_base(query: str) -> str:
    """
    Searches the master CSV knowledge base for program details and matches keywords,
    utilizing a FAISS vector store with HuggingFace embeddings for semantic retrieval
    as specified in PragyanAI's RAG Architecture guidelines.
    """
    csv_path = "data/PragyanAI_All_Programs_FAQ_Master.csv"
    if not os.path.exists(csv_path):
        return "Knowledge base master CSV file not found. Please verify the data directory structure."

    try:
        df = pd.read_csv(csv_path)
        
        # Combine row elements into clean text documents for vector chunking
        documents = []
        for _, row in df.iterrows():
            doc_text = " | ".join(f"{col}: {val}" for col, val in row.items() if pd.notna(val))
            documents.append(doc_text)

        # Initialize text splitter for semantic chunking
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
        chunks = text_splitter.create_documents(documents)

        # Initialize HuggingFace Embeddings & FAISS Vector Index
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = FAISS.from_documents(chunks, embeddings)

        # Perform similarity search
        results = vector_db.similarity_search(query, k=3)

        if not results:
            return "PragyanAI offers 5 core industry-aligned AI engineering programs covering practical execution and RAG engineering."

        context = "Retrieved Program Context via Semantic RAG:\n"
        for res in results:
            context += f"- {res.page_content}\n"
        return context

    except Exception as e:
        # Fallback keyword matching if embeddings/FAISS environment encounter local dependencies issues
        df = pd.read_csv(csv_path)
        query_lower = query.lower()
        matched_rows = []
        for _, row in df.iterrows():
            row_str = " ".join(str(val) for val in row.values).lower()
            if any(kw in row_str for kw in query_lower.split() if len(kw) > 3):
                matched_rows.append(row.to_dict())

        if not matched_rows:
            return "PragyanAI offers 5 core industry-aligned AI engineering programs ranging from B.E. integrations to working professional bootcamps."

        context = "Retrieved Program Context (Keyword Fallback):\n"
        for match in matched_rows[:3]:
            context += f"- Program: {match.get('Program Name')} | Duration: {match.get('Duration')} | Pricing: {match.get('Pricing & Financials')} | Skills: {match.get('Key Skills Covered')}\n"
        return context
