import os
import streamlit as st
from groq import Groq

def get_groq_client():
    """Initializes and returns the Groq client using Streamlit secrets or environment variables."""
    api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", None))
    if not api_key:
        raise ValueError("❌ GROQ API Key not found in Streamlit secrets or environment variables.")
    return Groq(api_key=api_key)

def get_groq_response(prompt: str, context: str = "") -> str:
    """
    Sends a prompt combined with retrieved context to the Groq LLM model
    and returns the generated text response.
    """
    try:
        client = get_groq_client()
        
        system_prompt = (
            "You are an expert AI Data Analytics Assistant and Program Manager for PragyanAI. "
            "Help users understand data, pricing, conversions, program details, and insights. "
            "Give clear, concise, and actionable answers."
        )
        
        user_content = f"Context:\n{context}\n\nUser Question:\n{prompt}" if context else prompt

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error communicating with Groq API: {str(e)}"
