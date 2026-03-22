from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_database_engine():
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        return engine
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create database engine")

def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get database session")
    finally:
        db.close()