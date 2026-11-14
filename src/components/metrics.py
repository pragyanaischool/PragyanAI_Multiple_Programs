import streamlit as st

def render_metric_cards():
    """Renders re-usable executive KPI metric cards for the Streamlit dashboard."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            '<div class="metric-card"><h3>1,000+</h3><p>Learning & Lab Hours</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="metric-card"><h3>100+</h3><p>Verified Portfolio Projects</p></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="metric-card"><h3>100%</h3><p>Placement Support & Targeting</p></div>',
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            '<div class="metric-card"><h3>₹10k</h3><p>Monthly Internship Stipend Tier</p></div>',
            unsafe_allow_html=True,
        )
