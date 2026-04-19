from fastapi import FastAPI, Request, Depends, status, Response, HTTPException
from pydantic import BaseModel
import os
import joblib
from sklearn.preprocessing import OneHotEncoder
import uvicorn
import pandas as pd
import schema
import models
import database
from sqlalchemy.orm import Session
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


app = FastAPI(title="Student Performance Predictor Application",
              description="An API to predict student's academic perfomance based on the student's metrics",
              version="1.0.0")



#calling the student details database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


database.Base.metadata.create_all(database.engine)




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
async def predict_raw(item: schema.StudentDetails, db: Session = Depends(get_db)):

    h = item.model_dump(exclude={"student_id"})
    
    # Convert to DataFrame - the pipeline handles all preprocessing internally
    df = pd.DataFrame([h])


    # making prediction with the preprocessed json data and the ml model
    prediction = clf.predict(df)
    prediction_final = ["Pass" if (x == 1) else "Fail" for x in prediction]


    #save into student details database
    new_blog = models.Blog(student_id = item.student_id, sex = item.sex, age = item.age, 
                           address = item.address, famsize = item.famsize, 
                           Pstatus = item.Pstatus, guardian = item.guardian, 
                           traveltime = item.traveltime, studytime = item.studytime, 
                           failures = item.failures, schoolsup = item.schoolsup, 
                           famsup = item.famsup, activities = item.activities, 
                           nursery = item.nursery, famrel = item.famrel, 
                           health = item.health, absences = item.absences, 
                           freetime = item.freetime, goout = item.goout, 
                           internet = item.internet, romantic = item.romantic,
                           Prediction = prediction_final[0])
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return {"Prediction": prediction_final[0]}












#this is for getting all students' past records and prediction data
@app.get("/get_all_records")
async def get_all_records(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs









#getting student's record according to student's student_id
@app.get("/get_all_records/{id_number}")
def get_record_by_id(id_number, response: Response, db: Session = Depends(get_db)):

    blogs = db.query(models.Blog).filter(models.Blog.student_id == id_number).first()

    if not blogs:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Seudent record with id {id_number} is not available")
    
    return blogs










#deleting a student's record using his or her student_id
@app.delete("/get_all_records/{id_number}", status_code = status.HTTP_200_OK)

async def destroy(id_number, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.student_id == id_number)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Student record with id {id_number} not available")
    

    blog.delete(synchronize_session = False)

    
    db.commit()
    return {"response": f"Student's record with id number {id_number} has been deleted"}

    








if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)