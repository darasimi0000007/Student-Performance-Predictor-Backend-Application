from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Blog(Base):

    __tablename__ = "Student Performance Details"
    

    student_id = Column(Integer, primary_key = True, index = True)
    sex = Column(String)
    age = Column(String)
    address = Column(String)
    famsize = Column(String)
    Pstatus = Column(String)
    guardian = Column(Integer)
    traveltime = Column(Integer)
    studytime = Column(Integer)
    failures = Column(Integer)
    schoolsup = Column(Integer)
    famsup= Column(Integer)
    activities = Column(Integer)
    nursery = Column(Integer)
    famrel = Column(Integer)
    health = Column(Integer)
    absences = Column(Integer)
    freetime = Column(Integer)
    goout = Column(Integer)
    internet = Column(Integer)
    romantic = Column(Integer)
    Prediction = Column(String)
















    