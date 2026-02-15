import streamlit as st
import pandas as pd
import pickle
import os

st.set_page_config(page_title="Loan Prediction App")
st.title("Loan Prediction App")

# Load model
MODEL_PATH = "Loan_prediction_Model.pkl"

if not os.path.exists(MODEL_PATH):
    st.error("Loan_prediction_Model.pkl not found")
    st.stop()

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# Inputs
gender = st.selectbox("Gender", ["Male", "Female"])
married = st.selectbox("Married", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
education = st.selectbox("Education", ["Graduate", "Not Graduate"])
self_employed = st.selectbox("Self Employed", ["Yes", "No"])
property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

applicant_income = st.number_input("Applicant Income", min_value=0)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
loan_amount = st.number_input("Loan Amount", min_value=0)
loan_amount_term = st.number_input("Loan Amount Term", min_value=0)
credit_history = st.selectbox("Credit History", [0, 1])

# Manual encoding
input_data = {
    "Gender": 1 if gender == "Male" else 0,
    "Married": 1 if married == "Yes" else 0,
    "Dependents": 3 if dependents == "3+" else int(dependents),
    "Education": 1 if education == "Graduate" else 0,
    "Self_Employed": 1 if self_employed == "Yes" else 0,
    "ApplicantIncome": applicant_income,
    "CoapplicantIncome": coapplicant_income,
    "LoanAmount": loan_amount,
    "Loan_Amount_Term": loan_amount_term,
    "Credit_History": credit_history,
    "Property_Area": 2 if property_area == "Urban" else 1 if property_area == "Semiurban" else 0
}

input_df = pd.DataFrame([input_data])

# Prediction
if st.button("Predict Loan Status"):
    result = model.predict(input_df)
    if result[0] == 1:
        st.write("Loan Approved")
    else:
        st.write("Loan Not Approved")
