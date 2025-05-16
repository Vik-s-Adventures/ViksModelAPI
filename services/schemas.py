from pydantic import BaseModel
from typing import List

class InputModelo(BaseModel):
    id_estudiante: int
    preguntas: List[int]  # Lista variable, según competencia
    competencia: str  # C1, C2, C3, C4  
