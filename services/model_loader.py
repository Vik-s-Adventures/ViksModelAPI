import os
import pandas as pd
from tensorflow.keras.models import load_model

def cargar_modelos():
    modelos = {}
    for i in range(1, 5):
        ruta = os.path.join("resources", f"modelo_C{i}.keras")
        modelo = load_model(ruta, compile=False)
        modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        modelos[f"C{i}"] = modelo
    return modelos

def cargar_diccionarios():
    diccionarios = {}
    for i in range(1, 5):
        ruta_csv = os.path.join("resources", f"diccionario_rutas_C{i}.csv")
        diccionario = pd.read_csv(ruta_csv)
        diccionario["ruta"] = diccionario["ruta"].apply(eval)
        diccionarios[f"C{i}"] = diccionario
    return diccionarios
