# Streamlit application script
# %%writefile app.py

import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load trained model and scaler
model = pickle.load(open("churn_modell.pkl", 'rb'))
scaler = pickle.load(open("scaler.pkl", 'rb'))

# Mapping for categorical values
region_mapping = {
        'FATICK': 0, 'DAKAR': 1, 'LOUGA': 2, 'TAMBACOUNDA': 3, 'KAOLACK': 4,
        'THIES': 5, 'SAINT-LOUIS': 6, 'KOLDA': 7, 'KAFFRINE': 8, 'DIOURBEL': 9,
        'ZIGUINCHOR': 10, 'MATAM': 11, 'SEDHIOU': 12, 'KEDOUGOU': 13
    }
tenure_mapping = {
        '3-6 months': 0, '6-9 months': 1, '9-12 months': 2, '12-15 months': 3,
        '15-18 months': 4, '18-21 months': 5, '21-24 months': 6, '>24 month': 7
    }


# function for performance prediction
def churn_prediction(input_data):

    # convert input to an array
    input_data_array = np.asarray(input_data)

    # reshape so the model can understand it
    input_data_reshape = input_data_array.reshape(1, -1)

    # scale the input data
    input_data_scaled = scaler.transform(input_data_reshape)

    # Getting a prediction 
    prediction = model.predict(input_data_scaled)
    
    if prediction[0] == 0:
        return("Not Churn")
    else:
        return("Churn")
    
def main():

    # Define the Streamlit Title
    st.title("Expresso Churn Prediction Web Application")

    # Input fields for user features
    st.header("Enter Customer Details")


    MONTANT = st.text_input('The amount of money (in CFA francs) the user has paid to the company')
    FREQUENCE_RECH =  st.text_input('The frequency at which the user recharges their phone account')
    REVENUE =  st.text_input('Enter the total revenue')
    ARPU_SEGMENT = st.text_input('Average revenue per segment')
    FREQUENCE =  st.text_input('FREQUENCE')
    DATA_VOLUME = st.text_input('The amount of data used by the user')
    REGULARITY = st.text_input('months between the users first subscription and the current subscription')
    FREQ_TOP_PACK = st.text_input('top service package frequency')
    REGION = st.selectbox('Select region', list(region_mapping.keys()))
    TENURE = st.selectbox('Select Tenure', list(tenure_mapping.keys()))

 
    churn_ = ""
    if st.button("Predict"):
        try:
            input_data = [
                float(MONTANT), float(FREQUENCE_RECH), float(REVENUE),
                float(ARPU_SEGMENT), float(FREQUENCE), float(DATA_VOLUME),
                float(REGULARITY), float(FREQ_TOP_PACK),
                region_mapping[REGION],  # Convert to numerical value
                tenure_mapping[TENURE]   # Convert to numerical value
            ]

            churn_ = churn_prediction(input_data)
            st.success(churn_)

        except ValueError:
            st.error("Please enter valid numerical values for all fields.")


if __name__ == "__main__":
    main()

