import database
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Blog(Base):

    __tablename__ = "Student Performance Details"
    

    student_id = Column(String, primary_key = True, index = True)
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
    institution_id = Column(String, ForeignKey("users.institution_id"))


    creator = relationship("User", back_populates = "creator_blogs")


class User(database.Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    role = Column(String)
    institution_id = Column(String)
    email = Column(String)
    password = Column(String)
    

    creator_blogs = relationship("Blog", back_populates = "creator")












    