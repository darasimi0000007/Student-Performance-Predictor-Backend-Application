from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Student Performance Predictor Application",
              description="An API to predict student's academic perfomance based on indivdual metrics",
              version="1.0.0")


@app.get("/home")
async def home():
    return {"message": "Welcome to the Student Performance Predictor API!"}