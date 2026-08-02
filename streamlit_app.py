import streamlit as st
import requests

st.title("🏦 Loan Prediction System")

age = st.number_input("Age", min_value=18, max_value=100)
dependents = st.number_input("Dependents", min_value=0)
income = st.number_input("Applicant Income", min_value=0)
loan_amount = st.number_input("Loan Amount", min_value=0)
cibil = st.number_input("CIBIL Score", min_value=300, max_value=900)
tenure = st.number_input("Tenure", min_value=1)

gender = st.selectbox("Gender", ["Male", "Female"])
married = st.selectbox("Married", ["Yes", "No"])
education = st.selectbox("Education", ["Yes", "No"])
self_employed = st.selectbox("Self Employed", ["Yes", "No"])
previous_loan = st.selectbox("Previous Loan Taken", ["Yes", "No"])
property_area = st.selectbox("Property Area", ["Rural", "Semiurban", "Urban"])
customer_bandwidth = st.selectbox("Customer Bandwidth", ["Bad", "Good", "Medium"])

gender = 1 if gender == "Male" else 0
married = 1 if married == "Yes" else 0
education = 1 if education == "Yes" else 0
self_employed = 1 if self_employed == "Yes" else 0
previous_loan = 1 if previous_loan == "Yes" else 0

property_area = {
    "Rural": 0,
    "Semiurban": 1,
    "Urban": 2
}[property_area]

customer_bandwidth = {
    "Bad": 0,
    "Good": 1,
    "Medium": 2
}[customer_bandwidth]

if st.button("Predict"):

    data = {
        "Age": age,
        "Dependents": dependents,
        "ApplicantIncome": income,
        "LoanAmount": loan_amount,
        "Cibil_Score": cibil,
        "Tenure": tenure,
        "Gender": gender,
        "Married": married,
        "Education": education,
        "Self_Employed": self_employed,
        "Previous_Loan_Taken": previous_loan,
        "Property_Area": property_area,
        "Customer_Bandwith": customer_bandwidth
    }

    response = requests.post(
        "http://backend:8000/predict",
        json=data
    )

    st.success(response.json()["prediction"])