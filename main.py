from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import pickle
import numpy as np
import os

app = FastAPI()

# Load model
model = pickle.load(open("build.pkl", "rb"))

# Connect to MySQL
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

# Input model
class LoanInput(BaseModel):
    Age: int
    Dependents: int
    ApplicantIncome: int
    LoanAmount: int
    Cibil_Score: int
    Tenure: int
    Gender: int
    Married: int
    Education: int
    Self_Employed: int
    Previous_Loan_Taken: int
    Property_Area: int
    Customer_Bandwith: int


@app.get("/")
def home():
    return {"message": "Loan Prediction API is Running"}


@app.post("/predict")
def predict(data: LoanInput):

    final_features = np.array([[
        data.Age,
        data.Dependents,
        data.ApplicantIncome,
        data.LoanAmount,
        data.Cibil_Score,
        data.Tenure,
        data.Gender,
        data.Married,
        data.Education,
        data.Self_Employed,
        data.Previous_Loan_Taken,
        data.Property_Area,
        data.Customer_Bandwith
    ]])

    prediction = model.predict(final_features)

    if prediction[0] == 0:
        result = "Loan is Rejected"
    else:
        result = "Loan is Approved"

    sql = """
    INSERT INTO predictions (
        age,
        dependents,
        income,
        loan_amount,
        cibil_score,
        tenure,
        gender,
        married,
        education,
        self_employed,
        previous_loan_taken,
        property_area,
        customer_bandwidth,
        prediction
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data.Age,
        data.Dependents,
        data.ApplicantIncome,
        data.LoanAmount,
        data.Cibil_Score,
        data.Tenure,
        data.Gender,
        data.Married,
        data.Education,
        data.Self_Employed,
        data.Previous_Loan_Taken,
        data.Property_Area,
        data.Customer_Bandwith,
        result
    )

    cursor.execute(sql, values)   
    db.commit()

    return {"prediction": result}