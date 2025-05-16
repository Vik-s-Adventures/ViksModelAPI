import os
import pandas as pd

# Ruta base para todos los recursos
RUTA_RECURSOS = r"D:\UNIVERSIDAD\X CICLO\Taller de Proyecto II\ViksAdventures\viks_model\resources"

def cargar_csv(nombre_archivo):
    return pd.read_csv(os.path.join(RUTA_RECURSOS, nombre_archivo))

def guardar_csv(df, nombre_archivo):
    df.to_csv(os.path.join(RUTA_RECURSOS, nombre_archivo), index=False)

def ruta_archivo(nombre_archivo):
    return os.path.join(RUTA_RECURSOS, nombre_archivo)