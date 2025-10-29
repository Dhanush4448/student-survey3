import os
from sqlmodel import create_engine, SQLModel, Session

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME", "studentsurvey")

if DB_HOST and DB_USER and DB_PASS:
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = "sqlite:///./studentsurvey_dev.db"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
