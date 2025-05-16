import numpy as np
from .model_loader import cargar_modelos, cargar_diccionarios
from .transformer import transformar_input, transformar_output

modelos = cargar_modelos()
diccionarios = cargar_diccionarios()

def predecir_ruta(input_preguntas, competencia):
    if competencia not in modelos:
        raise ValueError("Competencia inválida. Usa C1, C2, C3 o C4.")

    modelo = modelos[competencia]
    diccionario = diccionarios[competencia]

    input_transformado = transformar_input(input_preguntas, competencia)
    prediccion = modelo.predict(input_transformado)
    id_ruta = np.argmax(prediccion)

    ruta_dict = diccionario.loc[diccionario['id_ruta'] == id_ruta, 'ruta'].values
    if len(ruta_dict) == 0:
        raise ValueError(f"No se encontró ruta para id_ruta {id_ruta}")

    return transformar_output(tuple(ruta_dict[0]), competencia)
