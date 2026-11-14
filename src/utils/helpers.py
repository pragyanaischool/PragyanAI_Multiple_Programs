"""
src/utils/helpers.py
Utility helper functions for the PragyanAI Enterprise & Institutional Platform.
"""

import os
import pandas as pd
import streamlit as st

@st.cache_data
def load_master_faq_data() -> pd.DataFrame:
    """
    Loads the master program FAQ CSV file securely from the data directory.
    Uses caching to improve application performance.
    """
    csv_path = "data/PragyanAI_All_Programs_FAQ_Master.csv"
    try:
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        else:
            # Fallback inline dataframe if CSV is not yet synced locally
            return pd.DataFrame({
                "Program Name": [
                    "Program 1: Industry-Integrated AI Engineering Program",
                    "Program 2: 6-Month Super 30 Skill Program",
                    "Program 3: 4-Semester 40-Day AI Engineering Workshop",
                    "Program 4: 8-Weekend GenAI & Agentic AI Master Program",
                    "Program 5: IIT Guwahati & PragyanAI SDP"
                ],
                "Duration": ["4 Years", "6 Months + 12M Placement", "4 Semesters (40 Days)", "8 Weekends + Resort Capstone", "2 Weeks (30 Hours)"],
                "Pricing & Financials": ["Custom B2B Model", "₹1,00,000 - ₹1,50,000", "₹6,000 / semester", "₹50,000 All-Inclusive", "₹885 - ₹1,180 per participant"]
            })
    except Exception as e:
        st.error(f"Error loading master FAQ data: {str(e)}")
        return pd.DataFrame()

def format_currency_inr(amount: float) -> str:
    """
    Formats numeric pricing data into a clean Indian Rupee string representation.
    """
    return f"₹{amount:,.0f}"
