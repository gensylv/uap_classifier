import streamlit as st
import plotly.graph_objects as go
from data_loader import load_data

def render():
    st.title("Data Explorer")
    st.markdown("Browse and filter the NUFORC sightings used to train the classifier.")

    df = load_data()

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Reports", f"{len(df):,}")
    col2.metric("Anomalous", f"{df['is_anomalous'].sum():,}")
    col3.metric("Explainable", f"{(df['is_anomalous'] == 0).sum():,}")

    st.markdown("---")

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        label_filter = st.selectbox("Label", ["All", "Anomalous only", "Explainable only"])
    with col2:
        shape_filter = st.selectbox("Shape", ["All"] + sorted(df['Shape'].unique().tolist()))

    filtered = df.copy()
    if label_filter == "Anomalous only":
        filtered = filtered[filtered['is_anomalous'] == 1]
    elif label_filter == "Explainable only":
        filtered = filtered[filtered['is_anomalous'] == 0]
    if shape_filter != "All":
        filtered = filtered[filtered['Shape'] == shape_filter]

    st.markdown(f"**{len(filtered):,} reports match your filters**")
    st.markdown("---")

    # Shape distribution
    st.markdown("#### Sightings by Shape")
    shape_counts = filtered['Shape'].value_counts().head(15).reset_index()
    shape_counts.columns = ['Shape', 'Count']
    st.bar_chart(shape_counts.set_index('Shape'))

    # Anomalous vs explainable by shape
    st.markdown("#### Anomalous vs Explainable by Shape (Top 10)")
    top_shapes = df['Shape'].value_counts().head(10).index.tolist()
    shape_label = df[df['Shape'].isin(top_shapes)].groupby(['Shape', 'is_anomalous']).size().unstack(fill_value=0)
    shape_label.columns = ['Explainable', 'Anomalous']
    st.bar_chart(shape_label)

    # Choropleth map: Anomalous to explainable ratio by state
    st.markdown("#### Anomalous-to-Explainable Ratio by US State")
    st.caption("Darker = Higher proportion of anomalous sightings relative to total")

    us_df = df[df['Country'].isin(['USA', 'United States', 'United States of America'])]

    state_total = us_df.groupby('State').size().reset_index(name='total')
    state_anom = us_df[us_df['is_anomalous'] == 1].groupby('State').size().reset_index(name='anomalous')
    map_df = state_total.merge(state_anom, on='State', how='left').fillna(0)
    map_df['ratio'] = map_df['anomalous'] / map_df['total']

    fig = go.Figure(go.Choropleth(
        locations=map_df['State'],
        z=map_df['ratio'],
        locationmode='USA-states',
        colorscale=[[0, '#f0faf0'], [0.25, '#a8ddb5'], [0.5, '#4eb3d3'], [0.75, '#2b8cbe'], [1, '#084081']],
        colorbar_title="% Anomalous",
        colorbar_tickformat='.0%',
        marker_line_color='white',
        marker_line_width=0.5,
        zmin=map_df['ratio'].min(),
        zmax=map_df['ratio'].max(),
    ))
    fig.update_layout(
        geo_scope='usa',
        margin=dict(t=0, b=0, l=0, r=0),
        height=400,
    )
    st.plotly_chart(fig, width='stretch')

    # Pie chart: Top explanations
    if label_filter != "Anomalous only":
        st.markdown("#### Top Explanations for UAP Sightings")
        expl = filtered[filtered['is_anomalous'] == 0]['Explanation'].value_counts().head(10)
        fig_pie = go.Figure(go.Pie(
            labels=expl.index,
            values=expl.values,
            hole=0.4,
        ))
        fig_pie.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=400,
        )
        st.plotly_chart(fig_pie, width='stretch')

    # Raw data
    with st.expander("View Raw Data"):
        st.dataframe(
            filtered[['Occurred', 'City', 'State', 'Country', 'Shape', 'Summary', 'Explanation', 'is_anomalous']]
            .reset_index(drop=True),
            width='stretch'
        )
