import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_connection

def load_data():
    """Load data from the user_data table, excluding the user_id column."""
    conn = get_connection()
    # Fetching all columns except user_id from the user_data table
    df = pd.read_sql("SELECT REGION, TENURE, MONTANT, FREQUENCE_RECH, REVENUE, ARPU_SEGMENT, FREQUENCE, DATA_VOLUME, ON_NET, ORANGE, TIGO, MRG, REGULARITY, TOP_PACK, FREQ_TOP_PACK, CHURN FROM user_data", conn)
    conn.close()
    return df

def show_eda_dashboard(df):
    """Display the EDA dashboard."""
    st.title('EDA Dashboard')
    st.header('Dataset Overview')
    st.dataframe(df.describe())  # Displaying the descriptive statistics

    st.header('Select a column to view distribution')
    column_to_plot = st.selectbox('Select Column', df.columns)
    dist_fig = px.histogram(df, x=column_to_plot, color='CHURN', barmode='overlay', hover_data=df.columns.tolist())
    st.plotly_chart(dist_fig, use_container_width=True)

def convert_tenure_to_numeric(df):
    """Converts tenure descriptions to a numeric scale."""
    tenure_mapping = {
        'K > 24 month': 24,
        'I 18-21 month': 19.5,
        'H 15-18 month': 16.5,
        'G 12-15 month': 13.5,
        'F 9-12 month': 10.5,
        'E 6-9 month': 7.5,
        'D 3-6 month': 4.5,
    }
    df['TENURE'] = df['TENURE'].map(tenure_mapping).astype(float)
    return df

def show_analytics_dashboard(df):
    """Display the Analytics dashboard."""
    st.title('Analytics Dashboard')

    df = convert_tenure_to_numeric(df)
    churn_rate = df['CHURN'].mean() * 100
    avg_monthly_charges = df['MONTANT'].mean()  # Calculating average monthly charges
    avg_tenure = df['TENURE'].mean()

    st.markdown('#### Key Performance Indicators')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Churn Rate", value=f"{churn_rate:.2f}%")
    with col2:
        st.metric(label="Average Monthly Charges", value=f"${avg_monthly_charges:.2f}")
    with col3:
        st.metric(label="Average Tenure", value=f"{avg_tenure:.0f} months")

    col1, col2 = st.columns(2)
    with col1:
        avg_tenure_churn = df.groupby('CHURN')['TENURE'].mean()
        churn_tenure_fig = px.bar(avg_tenure_churn, title="Average Tenure for Churned vs Non-Churned Customers")
        st.plotly_chart(churn_tenure_fig, use_container_width=True)

    with col2:
        avg_charges_churn = df.groupby('CHURN')['MONTANT'].mean()
        charges_metric_fig = px.bar(avg_charges_churn, title="Average Monthly Charges for Churned vs Non-Churned Customers")
        st.plotly_chart(charges_metric_fig, use_container_width=True)


def show():
    df = load_data()
    st.sidebar.header('Dashboard Type')
    dashboard_type = st.sidebar.radio("Choose Dashboard Type", ('EDA', 'Analytics'))

    if dashboard_type == 'EDA':
        show_eda_dashboard(df)
    elif dashboard_type == 'Analytics':
        show_analytics_dashboard(df)

if __name__ == "__main__":
    show()
