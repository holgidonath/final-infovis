from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from .db import Base

class datos(Base):

    __tablename__ = "datos"

    id = Column(Integer, primary_key=True)
    jurisdiccion_codigo_indec = Column(Integer)
    jurisdiccion_nombre = Column(String)
    vacuna_nombre = Column(String)
    primera_dosis_cantidad = Column(Integer)
    segunda_dosis_cantidad = Column(Integer)

    class Config:
        orm_mode =True


    