from fastapi import APIRouter

from schemas import StudentInput

import joblib

import pandas as pd


router = APIRouter()


model = joblib.load("models/salary_model.pkl")

scaler = joblib.load("models/scaler_salary.pkl")

encoders = joblib.load("models/encoder_salary.pkl")


@router.post("/predict-salary")

def predict_salary(student: StudentInput):

    data = pd.DataFrame([student.dict()])


    for col, encoder in encoders.items():

        data[col] = encoder.transform(data[col])


    data = scaler.transform(data)


    prediction = model.predict(data)


    return {

        "Predicted Salary": float(prediction[0])

    }