from typing import List, Optional
from pydantic import BaseModel



class datos(BaseModel):

    jurisdiccion_codigo_indec : int
    jurisdiccion_nombre : str
    vacuna_nombre : str
    primera_dosis_cantidad : int
    segunda_dosis_cantidad : int

