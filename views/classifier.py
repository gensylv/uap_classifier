import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from data_loader import load_data

@st.cache_resource
def train_model():
    df = load_data()

    le_shape = LabelEncoder()
    le_state = LabelEncoder()

    df['shape_enc'] = le_shape.fit_transform(df['Shape'])
    df['state_enc'] = le_state.fit_transform(df['State'])

    features = ['shape_enc', 'state_enc', 'year', 'month', 'hour']
    target = 'is_anomalous'

    df_model = df.dropna(subset=features + [target])
    X = df_model[features]
    y = df_model[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=50,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    return model, le_shape, le_state, X_test, y_test, features


def render():
    st.title("Classify a Sighting")
    st.markdown("Enter the details of a US UAP report to get an instant anomaly prediction.")
    st.info("This classifier is trained on US sightings only.")

    with st.spinner("Loading model..."):
        model, le_shape, le_state, X_test, y_test, features = train_model()

    df = load_data()

    st.markdown("---")
    st.markdown("#### Sighting Details")

    col1, col2 = st.columns(2)
    with col1:
        selected_shape = st.selectbox("Shape", sorted(le_shape.classes_.tolist()))
        selected_state = st.selectbox("State", sorted(le_state.classes_.tolist()))

    with col2:
        selected_year = st.number_input("Year", min_value=2025, max_value=2026, value=2026)
        selected_month = st.slider("Month", 1, 12, 4)
        selected_hour = st.slider("Hour (24hr)", 0, 23, 21,
                                   help="e.g. 21 = 9:00 PM")

    if st.button("Classify this Sighting →", type="primary"):
        shape_enc = le_shape.transform([selected_shape])[0]
        state_enc = le_state.transform([selected_state])[0]

        X_input = pd.DataFrame([[shape_enc, state_enc,
                                  selected_year, selected_month, selected_hour]],
                                columns=features)

        prediction = model.predict(X_input)[0]
        proba = model.predict_proba(X_input)[0]
        anomalous_prob = proba[1]
        explainable_prob = proba[0]

        st.markdown("---")

        if prediction == 1:
            st.error(f"### Anomalous: {anomalous_prob:.0%} confidence")
            st.markdown(
                "This report matches patterns seen in unexplained sightings. <span style='color: red'>Investigator review recommended.</span>",
                unsafe_allow_html=True)
        else:
            st.success(f"### Explainable: {explainable_prob:.0%} confidence")
            st.markdown("This report matches patterns associated with explainable sightings.")

        st.markdown("#### Confidence Breakdown")
        prob_df = pd.DataFrame({
            'Classification': ['Anomalous', 'Explainable'],
            'Probability': [anomalous_prob, explainable_prob]
        })
        st.bar_chart(prob_df.set_index('Classification'))

        st.markdown("#### What drove this prediction?")
        importances = model.feature_importances_
        feat_labels = ['Shape', 'State', 'Year', 'Month', 'Hour']
        imp_df = pd.DataFrame({'Feature': feat_labels, 'Importance': importances})
        imp_df = imp_df.sort_values('Importance', ascending=False)
        st.bar_chart(imp_df.set_index('Feature'))