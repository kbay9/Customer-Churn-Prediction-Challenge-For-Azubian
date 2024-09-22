import streamlit as st
import pandas as pd
from database import get_connection

def fetch_history():
    """Fetch all prediction history from the database."""
    conn = get_connection()
    query = """
        SELECT * FROM customer_data
        ORDER BY id DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # Converting problematic characters
    df = df.applymap(lambda x: x.decode('utf-8', 'replace') if isinstance(x, bytes) else x)

    return df

def show():
    st.title('Prediction History')

    df = fetch_history()

    # Hiding the 'Probability' column
    if 'Probability' in df.columns:
        df = df.drop(columns=['Probability'])

    # Sidebar Filters for the data
    st.sidebar.header('Filters')
    model_used = st.sidebar.multiselect('Model Used', options=df['ModelUsed'].unique())
    prediction_result = st.sidebar.multiselect('Prediction', options=df['CHURN'].unique())

    # Applying filters
    if model_used:
        df = df[df['ModelUsed'].isin(model_used)]
    if prediction_result:
        df = df[df['CHURN'].isin(prediction_result)]

    st.header('Prediction Results')
    st.dataframe(df)

if __name__ == "__main__":
    show()
