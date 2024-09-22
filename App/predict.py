import streamlit as st
import pandas as pd
import joblib
import base64  
from database import save_prediction

# Loading models and preprocessing pipeline
model_path = 'Model/churn_model_components.pkl'
loaded_components = joblib.load(model_path)
preprocessor = loaded_components['preprocessing']['preprocessor']
tuned_models = loaded_components['tuned_models']

def predict_single(customer_data):
    processed_data = preprocessor.transform(pd.DataFrame([customer_data]))
    predictions = {name: model.predict_proba(processed_data)[:, 1][0] for name, model in tuned_models.items()}
    return predictions

def download_link(df):
    """Generate a download link for a DataFrame in CSV format."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="enhanced_data.csv">Download enhanced data</a>'
    return href


def show():
    st.title('Customer Churn Prediction')

    with st.form("prediction_form"):
        with st.expander("Customer Information"):
            col1, col2 = st.columns(2)
            with col1:
                TENURE = st.selectbox('Tenure', ['K > 24 month', 'I 18-21 month', 'H 15-18 month', 'G 12-15 month', 'F 9-12 month', 'E 6-9 month', 'D 3-6 month', 'C < 3 month'])
                MONTANT = st.number_input('Montant', min_value=0)
                FREQUENCE_RECH = st.number_input('Frequence Recharge', min_value=0)
                REVENUE = st.number_input('Revenue', min_value=0)
                REGION = st.selectbox('Region', ['North', 'South', 'East', 'West'])  # Adding the missing REGION field
            with col2:
                ARPU_SEGMENT = st.number_input('ARPU Segment', min_value=0)
                FREQUENCE = st.number_input('Frequence', min_value=0)
                DATA_VOLUME = st.number_input('Data Volume', min_value=0)
                ON_NET = st.number_input('On-net', min_value=0)

        with st.expander("Service Usage Details"):
            col1, col2 = st.columns(2)
            with col1:
                ORANGE = st.number_input('Orange', min_value=0)
                TIGO = st.number_input('Tigo', min_value=0)
                ZONE1 = st.number_input('Zone 1', min_value=0)
            with col2:
                ZONE2 = st.number_input('Zone 2', min_value=0)
                REGULARITY = st.number_input('Regularity', min_value=0)
                TOP_PACK = st.text_input('Top Pack')
                FREQ_TOP_PACK = st.number_input('Frequency Top Pack', min_value=0)

        submitted = st.form_submit_button("Predict")
        if submitted:
            customer_data = {
                'TENURE': TENURE, 'MONTANT': MONTANT, 'FREQUENCE_RECH': FREQUENCE_RECH, 'REVENUE': REVENUE,
                'ARPU_SEGMENT': ARPU_SEGMENT, 'FREQUENCE': FREQUENCE, 'DATA_VOLUME': DATA_VOLUME,
                'ON_NET': ON_NET, 'ORANGE': ORANGE, 'TIGO': TIGO, 'ZONE1': ZONE1, 'ZONE2': ZONE2,
                'REGULARITY': REGULARITY, 'TOP_PACK': TOP_PACK, 'FREQ_TOP_PACK': FREQ_TOP_PACK,
                'REGION': REGION  # Include REGION in customer_data
            }

            predictions = predict_single(customer_data)
            save_prediction(customer_data, predictions)
            st.write("Prediction results:")
            for model, prob in predictions.items():
                st.write(f"{model}: {'Churn' if prob > 0.5 else 'Not Churn'} with probability {prob:.2f}")

    
    st.header("Bulk Prediction")
    uploaded_file = st.file_uploader("Upload CSV", type='csv')
    if uploaded_file is not None:
        data_to_predict = pd.read_csv(uploaded_file)
        processed_data = preprocessor.transform(data_to_predict)
        
        results_data = data_to_predict.copy()  # Copying the original data

        for name, model in tuned_models.items():
            predictions = model.predict_proba(processed_data)[:, 1]
            results_data[f'{name}_Probability'] = predictions
            results_data[f'{name}_Prediction'] = ['Yes' if x > 0.5 else 'No' for x in predictions]

        st.write("Consolidated Results:")
        st.dataframe(results_data)

        # Download link
        if st.button("Download Enhanced Dataset"):
            tmp_download_link = download_link(results_data)
            st.markdown(tmp_download_link, unsafe_allow_html=True)

if __name__ == "__main__":
    show()