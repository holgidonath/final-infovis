from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import false

SQLALCHEMY_DATABASES_URL = "postgresql://holgidonath:finta123@localhost:5432/infovis"

engine = create_engine(SQLALCHEMY_DATABASES_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=false, bind=engine)


Base = declarative_base()

