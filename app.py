import streamlit as st

st.set_page_config(
    page_title="UAP Anomaly Classifier",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&family=Space+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}
code, .mono {
    font-family: 'Space Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🛸 UAP Anomaly Classifier")
    st.markdown("*Automated anomaly detection for UAP investigators*")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Home", "🔍 Data Explorer", "🛸 Classify a Sighting", "📊 Model Performance"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Data: [National UFO Reporting Center Online Database](https://nuforc.org/subndx/?id=all)· 2,225 recent sightings")

if page == "🏠 Home":
    from views import home
    home.render()
elif page == "🔍 Data Explorer":
    from views import explorer
    explorer.render()
elif page == "🛸 Classify a Sighting":
    from views import classifier
    classifier.render()
elif page == "📊 Model Performance":
    from views import performance
    performance.render()
