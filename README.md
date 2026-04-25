# UAP Anomaly Classifier
### WGU Computer Science Capstone — C964

A machine learning web application that classifies UAP sighting reports as anomalous or explainable, built to support investigators in triaging incoming reports.

**Live App:** https://uap-anomaly-classifier.streamlit.app/ 
---

## Project Overview

This application uses a Random Forest binary classifier trained on 2,225 recent US sighting records from the National UFO Reporting Center (NUFORC). Given observable characteristics of a sighting — shape, state, year, month, and hour of occurrence — the model predicts whether the report is likely anomalous or explainable, and returns a confidence score alongside feature importance scores.

The app also includes an interactive Data Explorer with four visualizations for descriptive analysis of the dataset.

---

## Application Pages

| Page | Description |
|------|-------------|
| Home | Project overview and dataset summary |
| Data Explorer | Four interactive visualizations for exploratory analysis |
| Classify a Sighting | ML prediction interface with confidence score and feature importance |
| Model Performance | Accuracy, ROC-AUC, classification report, and confusion matrix |

---

## ML Pipeline

| Component | Detail |
|-----------|--------|
| Algorithm | RandomForestClassifier (scikit-learn) |
| Estimators | 100 |
| Features | Shape, State, Year, Month, Hour (label-encoded) |
| Target | Anomalous (1) vs. Explainable (0) |
| Class handling | class_weight='balanced' |
| Train/test split | 80% / 20% stratified |
| Evaluation metrics | Accuracy, ROC-AUC, precision, recall, F1, confusion matrix |

---

## Data Source

National UFO Reporting Center (NUFORC) — All Reports index  
nuforc.org  
3,000 records exported, filtered to 2,225 US sightings with valid state codes

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Frontend | Streamlit 1.56.0 |
| ML | scikit-learn 1.8.0 |
| Data | pandas 3.0.2, openpyxl 3.1.5 |
| Visualizations | Plotly 5.22.0, Streamlit built-in charts |
| Language | Python 3.14 |
| IDE | PyCharm Community Edition 2025.2.5 |

---

## Running Locally

If you prefer to run the application locally rather than accessing the live URL:

1. Clone the repository:
```bash
git clone https://github.com/gensylv/uap_classifier.git
```
2. Navigate to the project folder and install dependencies:
```bash
pip install -r requirements.txt
```
3. Launch the app:
```bash
streamlit run app.py
```

5. Open your browser to `http://localhost:8501`

---

*Genivere Sylvester — Independent Paranormal Machine Learning Consultant*  
*WGU C964 Computer Science Capstone, 2026*