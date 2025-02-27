from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import os
from tensorflow.keras.models import load_model


# Crear la instancia de FastAPI
app = FastAPI()

# Cargar el modelo previamente entrenado
ruta_modelo = os.path.join(os.path.dirname(__file__), "..", "resources", "ruta.keras")

# Cargar el modelo
modelo = load_model(ruta_modelo, compile=False)
modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Cargar el diccionario de rutas desde CSV
ruta_diccionario = os.path.join(os.path.dirname(__file__), "..", "resources", "diccionario_rutas.csv")
diccionario_rutas = pd.read_csv(ruta_diccionario)
diccionario_rutas["ruta"] = diccionario_rutas["ruta"].apply(eval)  # Convertir string a tupla

# Tabla de equivalencia global
EQUIVALENCIA = {
    1: [8],  2: [10], 3: [3], 4: [6], 5: [7], 6: [6],
    7: [7], 8: [8], 9: [9], 10: [5], 11: [2], 12: [1, 4]
}

# Definir el esquema de entrada
class InputModelo(BaseModel):
    id_estudiante: int
    preguntas: list[int]  # Lista de 10 enteros (0s y 1s)

# Función para transformar el input de 10 a 12 indicadores
def transformar_input(input10):
    if len(input10) != 10:
        raise ValueError("El input debe ser un arreglo de 10 elementos.")

    output12 = []
    for i in range(1, 13):
        preguntas = EQUIVALENCIA[i]
        if len(preguntas) == 1:
            valor = input10[preguntas[0] - 1]
        elif i == 12:  # Para el caso de la posición 12 (P1 y P4), usar AND
            valor = 1 if all(input10[p - 1] == 1 for p in preguntas) else 0
        else:  # Para los demás casos con múltiples preguntas, usar OR
            valor = 1 if any(input10[p - 1] == 1 for p in preguntas) else 0
        output12.append(valor)

    return np.array(output12, dtype=np.float32).reshape(1, -1)

# Función para transformar la salida de 12 indicadores a 10
def transformar_output(ruta_dict):
    ruta_1a12 = [x + 1 for x in ruta_dict]  # Convertir índices de 0-11 a 1-12
    ruta_preliminar = [EQUIVALENCIA[i] for i in ruta_1a12]

    ruta_final = []
    for item in ruta_preliminar:
        for elem in item:
            if elem in ruta_final:
                ruta_final.remove(elem)
            ruta_final.append(elem)

    return ruta_final

# Función para predecir la ruta
def predecir_ruta(input10):
    input_transformado = transformar_input(input10)
    prediccion = modelo.predict(input_transformado)
    id_ruta = np.argmax(prediccion)  # Tomamos la clase con mayor probabilidad

    # Buscar la ruta en el diccionario
    ruta_dict = diccionario_rutas.loc[diccionario_rutas['id_ruta'] == id_ruta, 'ruta'].values
    if len(ruta_dict) == 0:
        raise ValueError(f"No se encontró la ruta para el id_ruta {id_ruta}")

    return transformar_output(tuple(ruta_dict[0]))  # Transformar la ruta a 10 indicadores

# Endpoint para predecir la ruta
@app.post("/predecir_ruta")
def endpoint_predecir_ruta(data: InputModelo):
    try:
        ruta = predecir_ruta(data.preguntas)
        return {"id_estudiante": data.id_estudiante, "ruta": ruta}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))