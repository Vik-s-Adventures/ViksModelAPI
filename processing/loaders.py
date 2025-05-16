import os
import pandas as pd

# Ruta base para todos los recursos
RUTA_RECURSOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources")

def cargar_csv(nombre_archivo):
    return pd.read_csv(os.path.join(RUTA_RECURSOS, nombre_archivo))

def guardar_csv(df, nombre_archivo):
    df.to_csv(os.path.join(RUTA_RECURSOS, nombre_archivo), index=False)

def ruta_archivo(nombre_archivo):
    return os.path.join(RUTA_RECURSOS, nombre_archivo)