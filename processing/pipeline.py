# processing/pipeline.py

import pandas as pd
from .loaders import cargar_csv, guardar_csv, ruta_archivo
from .cleaning import *
from .transformations import *
from .modeling import entrenar_modelo

competencias = [
    "Resuelve problemas de cantidad",
    "Resuelve problemas de regularidad, equivalencia y cambio",
    "Resuelve problemas de forma, movimiento y localización",
    "Resuelve problemas de gestión de datos e incertidumbre"
]

def ejecutar_pipeline(guardar_archivos=False):
    respuestas = cargar_csv("respuestas.csv")
    matriz = cargar_csv("matriz.csv")
    respuestas_limpias = limpiar_respuestas(respuestas)

    for i, comp in enumerate(competencias, start=1):
        codigos = matriz[matriz["Competencia"] == comp]["Código"].tolist()
        columnas = [c for c in codigos if c in respuestas_limpias.columns]
        df = respuestas_limpias[columnas].copy()
        df = eliminar_filas_y_columnas_vacias(df)
        df = rellenar_faltantes(df)

        consolidado = matriz[matriz["Competencia"] == comp].copy()
        consolidado = consolidado.groupby("Indicador").agg({
            "Código": ", ".join,
            "Capacidad": "first",
            "Campo temático": "first"
        }).reset_index()
        consolidado["Competencia"] = comp

        df, eliminadas, _ = procesar_final(df, consolidado)

        renombres = {}
        mapping = []
        for j, row in consolidado.iterrows():
            preguntas = row['Código'].split(', ')
            preguntas_validas = [p for p in preguntas if p in df.columns]
            nuevo_nombre = f"indicador{j+1}"
            for p in preguntas_validas:
                renombres[p] = nuevo_nombre
            mapping.append({
                "Indicador": nuevo_nombre,
                "Nombre completo": row["Indicador"],
                "Preguntas": ', '.join(preguntas_validas)
            })

        df.rename(columns=renombres, inplace=True)
        df = eliminar_filas_solo_ceros(df)

        columnas_ordenadas = obtener_columnas_ordenadas(df)
        df = df[columnas_ordenadas]
        ruta_ideal = calcular_ruta_global(df, columnas_ordenadas)
        df["ruta"] = df.apply(lambda fila: calcular_ruta_personalizada(fila, ruta_ideal), axis=1)
        df, id_to_ruta = asignar_id_ruta(df)

        df_final = df.drop(columns=["ruta"])

        if guardar_archivos:
            guardar_csv(df_final, f"final_C{i}.csv")
            pd.DataFrame(mapping).to_csv(ruta_archivo(f"indicador_mapping{i}.csv"), index=False)
            pd.DataFrame(list(id_to_ruta.items()), columns=["id_ruta", "ruta"]).to_csv(ruta_archivo(f"diccionario_rutas_c{i}.csv"), index=False)

        print(f"✅ Competencia {i} procesada.")

        # Entrenar modelo
        print(f"🚀 Entrenando modelo para competencia {i}...")
        reporte = entrenar_modelo(i)
        print(reporte)
