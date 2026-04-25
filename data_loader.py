import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_excel("data/latest_uap_sightings_ALL_REPORTS.xlsx", engine="openpyxl")

    # Target Variable: 1 = anomalous, 0 = explainable ---
    df['is_anomalous'] = df['Explanation'].isna().astype(int)

    # Parse Occurred datetime
    df['Occurred'] = pd.to_datetime(df['Occurred'], errors='coerce')
    df['year'] = df['Occurred'].dt.year
    df['month'] = df['Occurred'].dt.month
    df['hour'] = df['Occurred'].dt.hour  # 24-hour format

    # Clean Shape
    df['Shape'] = df['Shape'].fillna('Unknown').str.strip().str.title()

    # Clean Country
    df['Country'] = df['Country'].fillna('Unknown').str.strip()

    # Clean State
    df['State'] = df['State'].str.strip().str.upper()

    # Map full state names to abbreviations
    state_name_map = {
        'ALABAMA': 'AL', 'ALASKA': 'AK', 'ARIZONA': 'AZ', 'ARKANSAS': 'AR', 'CALIFORNIA': 'CA',
        'COLORADO': 'CO', 'CONNECTICUT': 'CT', 'DELAWARE': 'DE', 'FLORIDA': 'FL', 'GEORGIA': 'GA',
        'HAWAII': 'HI', 'IDAHO': 'ID', 'ILLINOIS': 'IL', 'INDIANA': 'IN', 'IOWA': 'IA',
        'KANSAS': 'KS', 'KENTUCKY': 'KY', 'LOUISIANA': 'LA', 'MAINE': 'ME', 'MARYLAND': 'MD',
        'MASSACHUSETTS': 'MA', 'MICHIGAN': 'MI', 'MINNESOTA': 'MN', 'MISSISSIPPI': 'MS',
        'MISSOURI': 'MO', 'MONTANA': 'MT', 'NEBRASKA': 'NE', 'NEVADA': 'NV', 'NEW HAMPSHIRE': 'NH',
        'NEW JERSEY': 'NJ', 'NEW MEXICO': 'NM', 'NEW YORK': 'NY', 'NORTH CAROLINA': 'NC',
        'NORTH DAKOTA': 'ND', 'OHIO': 'OH', 'OKLAHOMA': 'OK', 'OREGON': 'OR', 'PENNSYLVANIA': 'PA',
        'RHODE ISLAND': 'RI', 'SOUTH CAROLINA': 'SC', 'SOUTH DAKOTA': 'SD', 'TENNESSEE': 'TN',
        'TEXAS': 'TX', 'UTAH': 'UT', 'VERMONT': 'VT', 'VIRGINIA': 'VA', 'WASHINGTON': 'WA',
        'WEST VIRGINIA': 'WV', 'WISCONSIN': 'WI', 'WYOMING': 'WY', 'DISTRICT OF COLUMBIA': 'DC'
    }
    df['State'] = df['State'].replace(state_name_map)

    # Filter to US only, valid state codes, ignore invalid entries like "-"
    valid_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
                    'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                    'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
                    'WI', 'WY', 'DC', 'GU', 'PR']
    df = df[df['Country'].isin(['USA', 'United States', 'United States of America']) & df['State'].isin(valid_states)]

    # Clean Summary
    df['Summary'] = df['Summary'].astype(str)

    # Normalize explanation categories by removing trailing question marks
    df['Explanation'] = df['Explanation'].str.rstrip('?').str.strip()

    # --- drop rows with no Occurred date ---
    df = df.dropna(subset=['Occurred'])

    return df
