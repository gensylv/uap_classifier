import streamlit as st

def render():
    st.title("🛸 UAP Anomaly Classifier")
    st.markdown("""
    <p style='font-family: courier, monospace; font-size: 1.2rem; font-weight: 900; letter-spacing: 0.15em; text-transform: uppercase;'>
    <span style='color: #cc1f1f;'>Classified:</span> <span style='color: white;'>Illuminating the Unexplained</span>
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(""" 
    This app uses a machine learning classifier trained on 2,225 recent [NUFORC](https://nuforc.org/subndx/?id=all) sightings across the US
    to automatically predict whether an incoming report is **anomalous** or **explainable**
    based on shape, location, time of day, and date of occurrence, empowering UAP investigators to 
    bypass the mundane and prioritize the extraordinary. 
    """)

    st.markdown("---")
    st.markdown("### ")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**1. Machine Learning**")
        st.markdown("A Random Forest classifier trained on recent NUFORC data predicts whether sightings are anomalous or explainable.")
    with col2:
        st.markdown("**2. Classification Tool**")
        st.markdown("Enter details of a new sighting and get an instant prediction.")
    with col3:
        st.markdown("**3. Triage Support**")
        st.markdown("Anomalous reports can be flagged for review, while explainable reports may be deprioritized.")

    st.markdown("---")
    st.markdown("### Dataset at a Glance")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reports", "2,225")
    col2.metric("Anomalous", "1,518")
    col3.metric("Explainable", "707")
    col4.metric("Date Range", "2025–2026")

    st.info("👈 Use the sidebar to explore the data or classify a sighting.")
