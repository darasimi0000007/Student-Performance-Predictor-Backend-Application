from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI(title="Student Performance Predictor Application",
              description="An API to predict student's academic perfomance based on indivdual metrics",
              version="1.0.0")


@app.get("/home")
async def home():
    return {"message": "Welcome to the Student Performance Predictor API!"}


@app.get("/predict")
async def predict():
    #user predicts his chances of doing well in his three semesters here by inputting values manually