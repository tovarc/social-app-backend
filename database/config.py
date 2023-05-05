from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "postgresql://postgres:temporal123@localhost/social_app"
DATABASE_URL = "postgresql://postgres:567322963@socialapp.coldyyfud5g4.us-east-1.rds.amazonaws.com:5432/postgres"

engine = create_engine(DATABASE_URL)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
