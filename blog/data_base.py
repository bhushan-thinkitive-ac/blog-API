from sqlalchemy import create_engine # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore


SQLALCHAMY_DB_URL = "sqlite:///./blog.db"


engine = create_engine( SQLALCHAMY_DB_URL, connect_args={"check_same_thread": False})

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()  

    try:
        yield db
    finally: 
        db.close()