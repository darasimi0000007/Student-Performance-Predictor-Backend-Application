from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import joblib
import uvicorn
import pandas as pd
import schema
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer



app = FastAPI(title="Student Performance Predictor Application",
              description="An API to predict student's academic perfomance based on the student's metrics",
              version="1.0.0")


#loading the model

with open("ml_model/stud_performance_classifier.joblib", "rb") as f:
    clf = joblib.load(f)







@app.get("/home")
async def home():
    return {"message": "Welcome to the Student Performance Predictor API!"}



#prediction using json data
@app.post("/predict_json")
async def predict_json(request: Request):
    #user feeds json that contains the student details for prediction

    input_data = await request.json()
    input_df = pd.DataFrame(input_data)
    
    #predicting with the json data
    predicted_data = clf.predict(input_df)[0]

    if predicted_data == 0:
        return {"Prediction": "Fail"}
    elif predicted_data == 1:
        return {"Prediction": "Pass"}






#prediction using raw input
@app.post("/predict_raw")
async def predict_raw(item: schema.StudentDetails):

    h = item.model_dump()
    #df = pd.DataFrame([h])
    df = pd.DataFrame.from_dict(h, orient="columns")
    return df


    # prediction = clf.predict(df)[0]
    # prediction_final = ["Pass" if (x == 1) else "Fail" for x in prediction]
    # return {f"Prediction : {prediction_final}"}














if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)