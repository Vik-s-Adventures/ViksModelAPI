import numpy as np
import pandas as pd

def limpiar_respuestas(df):
    df = df.replace({".": np.nan, 2: 1, "2": 1})
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.map(lambda x: 1 if x == 1 else (0 if x == 0 else np.nan))
    return df

def eliminar_filas_y_columnas_vacias(df):
    return df.dropna(axis=0, how="all").dropna(axis=1, how="all")

def rellenar_faltantes(df):
    return df.fillna(0)

def eliminar_filas_solo_ceros(df, porcentaje=90):
    filas_ceros = df[(df == 0).all(axis=1)]
    eliminar = int(len(filas_ceros) * porcentaje / 100)
    if eliminar > 0:
        df = df.drop(filas_ceros.sample(n=eliminar, random_state=42).index)
    return df
