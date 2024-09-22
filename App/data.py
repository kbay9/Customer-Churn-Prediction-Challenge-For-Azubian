import streamlit as st
import pandas as pd
import sqlite3
import numpy as np

# Establishing a connection to the SQLite database (churn.db)
def get_connection():
    return sqlite3.connect("churn.db")

# Caching the data loaded from the SQLite database
@st.cache_data
def load_data():
    with get_connection() as conn:
        # Reading data from user_data table
        return pd.read_sql_query("SELECT * FROM user_data", conn)

# Data page UI
def show():
    st.title("Data Exploration")

    # Loading data from the database
    data = load_data()
    st.write("Here is a sample of the dataset:")
    st.dataframe(data.head())  # Displaying the first few rows of the data

    # Feature selection UI
    feature_type = st.selectbox(
        "Select which features to view:",
        options=('Numeric Features', 'Categorical Features'),
        index=0  # Default selection
    )

    # Showing numeric or categorical features based on user selection
    if feature_type == 'Numeric Features':
        st.write("Showing Numeric Features:")
        numeric_data = data.select_dtypes(include=[np.number])
        st.dataframe(numeric_data.head())
    elif feature_type == 'Categorical Features':
        st.write("Showing Categorical Features:")
        categorical_data = data.select_dtypes(exclude=[np.number])
        st.dataframe(categorical_data.head())

# Ensuring the show function is called when running this module
if __name__ == "__main__":
    show()
