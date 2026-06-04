from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


database_url = "sqlite:///./StudentDetails.db"
engine = create_engine(database_url, connect_args={"check_same_thread": False})



SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


#calling the student details database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()