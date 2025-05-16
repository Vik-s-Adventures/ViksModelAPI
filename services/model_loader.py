import os
import pandas as pd
from tensorflow.keras.models import load_model

# Ruta absoluta desde app.py a la carpeta resources
RUTA_RECURSOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources")
RUTA_RECURSOS = os.path.abspath(RUTA_RECURSOS) 

def cargar_modelos():
    modelos = {}
    for i in range(1, 5):
        ruta = os.path.join(RUTA_RECURSOS, f"modelo_C{i}.keras")
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"Modelo no encontrado: {ruta}")
        modelo = load_model(ruta, compile=False)
        modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        modelos[f"C{i}"] = modelo
    return modelos

def cargar_diccionarios():
    diccionarios = {}
    for i in range(1, 5):
        ruta_csv = os.path.join(RUTA_RECURSOS, f"diccionario_rutas_c{i}.csv")
        if not os.path.exists(ruta_csv):
            raise FileNotFoundError(f"Diccionario no encontrado: {ruta_csv}")
        diccionario = pd.read_csv(ruta_csv)
        diccionario["ruta"] = diccionario["ruta"].apply(eval)
        diccionarios[f"C{i}"] = diccionario
    return diccionarios