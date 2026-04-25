import streamlit as st
import pandas as pd
from sklearn.metrics import (classification_report, confusion_matrix,
                              accuracy_score, roc_auc_score)
from views.classifier import train_model

def render():
    st.title("Model Performance")
    st.markdown("UAP Anomaly Classifier Evaluation Metrics")

    with st.spinner("Loading model..."):
        model, le_shape, le_state, X_test, y_test, features = train_model()

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    st.markdown("---")
    st.markdown("#### Summary Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Accuracy", f"{accuracy_score(y_test, y_pred):.1%}")
    col2.metric("ROC-AUC", f"{roc_auc_score(y_test, y_proba):.3f}")
    col3.metric("Test Set Size", f"{len(y_test):,} Sightings")

    st.markdown("---")
    st.markdown("#### Classification Report")
    report = classification_report(y_test, y_pred,
                                    target_names=['Explainable', 'Anomalous'],
                                    output_dict=True)
    report_df = pd.DataFrame(report).T
    st.dataframe(report_df.style.format("{:.2f}"), use_container_width=True)

    st.markdown("---")
    st.markdown("#### Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(cm,
                          index=['Actual: Explainable', 'Actual: Anomalous'],
                          columns=['Predicted: Explainable', 'Predicted: Anomalous'])
    st.dataframe(cm_df, use_container_width=True)

    st.markdown("---")
    st.markdown("#### About the Model")
    st.markdown("""
    | Parameter | Value |
    |-----------|-------|
    | Algorithm | RandomForestClassifier |
    | Estimators | 100 |
    | Class Weight | Balanced (handles imbalance) |
    | Train/Test Split | 80% / 20% |
    | Features | Shape, Country, State, Year, Month, Hour |
    | Target | Anomalous (1) vs Explainable (0) |
    | Data source | NUFORC (2,225 recent sightings) |
    """)
