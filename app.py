from fastapi import FastAPI, HTTPException
from services.schemas import InputModelo
from services.core import predecir_ruta

app = FastAPI()

@app.post("/predecir_ruta")
def endpoint_predecir_ruta(data: InputModelo):
    try:
        ruta = predecir_ruta(data.preguntas, data.competencia)
        return {"id_estudiante": data.id_estudiante, "ruta": ruta}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
