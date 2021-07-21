from fastapi import FastAPI
from starlette.responses import RedirectResponse
from fastapi.params import Depends
from database import models, schema
from sqlalchemy.orm import Session
from database.db import SessionLocal, engine
from typing import List
from fastapi.middleware.cors import CORSMiddleware


tags_metadata = [
    {"name": "Data general"},
    {"name": "Dosis por provincia"}, 
    {"name": "Dosis por vacuna"},
    {"name": "Dosis por provinicia y vacuna"},  
]
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Final Infovis API", description="API para obtener información a cerca de vacunación en Argentina.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

#ALL DATA

@app.get("/datos/", response_model=List[schema.Datos],tags=["Data general"])
def show_data_full(db:Session=Depends(get_db)):
    return db.query(models.Datos).all()

@app.get("/datos/dosis",tags=["Data general"])
def show_all_doses(db: Session = Depends(get_db)):
    return db.execute("SELECT dosis FROM(SELECT sum(primera_dosis_cantidad) as dosis FROM datos  UNION ALL SELECT sum(segunda_dosis_cantidad) FROM datos) as all_first_second_dosis").all()



#DATA BY PROVINCE


@app.get("/datos/provincias/primerdosis",tags=["Dosis por provincia"])
def show_provinces_first_doses(db: Session = Depends(get_db)):
    return db.execute("select jurisdiccion_nombre, SUM(primera_dosis_cantidad) as primer_dosis_cantidad from datos GROUP BY jurisdiccion_nombre ORDER BY primer_dosis_cantidad DESC").all()

@app.get("/datos/provincias/segundadosis",tags=["Dosis por provincia"])
def show_provinces_second_doses(db: Session = Depends(get_db)):
    return db.execute("select jurisdiccion_nombre, SUM(segunda_dosis_cantidad) as segunda_dosis_cantidad from datos GROUP BY jurisdiccion_nombre ORDER BY segunda_dosis_cantidad DESC").all()

@app.get("/datos/provincias/alldosis",tags=["Dosis por provincia"])
def show_provinces_all_doses(db: Session = Depends(get_db)):
    return db.execute("select jurisdiccion_nombre, sum(primera_dosis_cantidad + segunda_dosis_cantidad) as todas_las_dosis from datos GROUP BY jurisdiccion_nombre ORDER BY todas_las_dosis DESC").all()

@app.get("/datos/provincias/alldosisseperated/",tags=["Dosis por provincia"])
def show_provinces_all_doses_seperated(db: Session = Depends(get_db)):
    return db.execute("SELECT jurisdiccion_nombre, dosis, CASE WHEN newfield = 'first' THEN 'Primera Dosis' ELSE 'Segunda Dosis' END AS tipo_de_dosis FROM(SELECT jurisdiccion_nombre, primera_dosis_cantidad as dosis, 'first' AS newfield FROM datos UNION ALL SELECT jurisdiccion_nombre, segunda_dosis_cantidad, 'second' AS newfield FROM datos) as dosis_type_query").all()

@app.get("/datos/provincias/alldosisseperated/top6",tags=["Dosis por provincia"])
def show_provinces_all_doses_seperated_top_six(db: Session = Depends(get_db)):
    return db.execute("SELECT jurisdiccion_nombre, dosis, CASE WHEN newfield = 'first' THEN 'Primera Dosis' ELSE 'Segunda Dosis' END AS tipo_de_dosis FROM(SELECT jurisdiccion_nombre, sum(primera_dosis_cantidad) as dosis, 'first' AS newfield FROM datos GROUP BY jurisdiccion_nombre, newfield UNION ALL SELECT jurisdiccion_nombre, sum(segunda_dosis_cantidad), 'second' AS newfield FROM datos GROUP BY jurisdiccion_nombre, newfield) as dosis_type_query WHERE jurisdiccion_nombre = 'Buenos Aires' or jurisdiccion_nombre = 'CABA' or jurisdiccion_nombre = 'Córdoba' or jurisdiccion_nombre = 'Santa Fe' or jurisdiccion_nombre = 'Mendoza' or jurisdiccion_nombre = 'Tucumán'").all()

#DATA BY VACCINE NAME

@app.get("/datos/vacunanombre/primeradosis",tags=["Dosis por vacuna"])
def show_vaccine_name_first_doses(db: Session = Depends(get_db)):
    return db.execute("select vacuna_nombre, sum(primera_dosis_cantidad) as primera_dosis_cantidad from datos GROUP BY vacuna_nombre ORDER BY primera_dosis_cantidad DESC").all()  

@app.get("/datos/vacunanombre/segundadosis",tags=["Dosis por vacuna"])
def show_vaccine_name_second_doses(db: Session = Depends(get_db)):
    return db.execute("select vacuna_nombre, sum(segunda_dosis_cantidad) as segunda_dosis_cantidad from datos GROUP BY vacuna_nombre ORDER BY segunda_dosis_cantidad DESC").all()  

@app.get("/datos/vacunanombre/alldosis",tags=["Dosis por vacuna"])
def show_vaccine_name_all_doses(db: Session = Depends(get_db)):
    return db.execute("select vacuna_nombre, sum(primera_dosis_cantidad + segunda_dosis_cantidad) as total_dosis from datos GROUP BY vacuna_nombre ORDER BY total_dosis DESC").all()  

#DATA BY PROVINCE AND VACCINE NAME

@app.get("/datos/provincias/vacunanombre/alldosis",tags=["Dosis por provinicia y vacuna"])
def show_provinces_and_vaccine_name_all_doses(db: Session = Depends(get_db)):
    return db.execute("select jurisdiccion_nombre, vacuna_nombre, sum(primera_dosis_cantidad + segunda_dosis_cantidad) as total_dosis from datos GROUP BY jurisdiccion_nombre, vacuna_nombre ORDER BY jurisdiccion_nombre").all()  

@app.get("/datos/provincias/vacunanombretop/primeradosis",tags=["Dosis por provinicia y vacuna"])
def show_provinces_and_top_vaccine_name_first_doses(db: Session = Depends(get_db)):
    return db.execute("SELECT x1.jurisdiccion_nombre, y2.vacuna_nombre, y2.primera_dosis_cantidad FROM ( SELECT jurisdiccion_nombre, max(primera_dosis_cantidad) as primera_dosis FROM datos  GROUP BY jurisdiccion_nombre) as x1 INNER JOIN ( SELECT jurisdiccion_nombre, vacuna_nombre, primera_dosis_cantidad FROM datos) as y2 ON x1.primera_dosis = y2.primera_dosis_cantidad").all()  