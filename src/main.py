from fastapi import FastAPI
from starlette.responses import RedirectResponse
from fastapi.params import Depends
from database import models, schema
from sqlalchemy.orm import Session
from database.db import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/datos/", response_model=List[schema.datos])
def show_data(db:Session=Depends(get_db)):
    datos = db.query(models.data).all()
    return datos
