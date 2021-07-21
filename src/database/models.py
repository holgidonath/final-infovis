from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
from enum import Enum, IntEnum

class Datos(Base):

    __tablename__ = "datos"

   
    id = Column(Integer, primary_key=True)
    jurisdiccion_codigo_indec = Column(Integer)
    jurisdiccion_nombre = Column(String)
    vacuna_nombre = Column(String)
    primera_dosis_cantidad = Column(Integer)
    segunda_dosis_cantidad = Column(Integer)
  





    