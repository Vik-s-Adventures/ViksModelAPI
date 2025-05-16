# processing/transformations.py

def procesar_final(df, consolidado):
    eliminadas, razones = [], []
    for _, row in consolidado.iterrows():
        preguntas = [p for p in row['Código'].split(', ') if p in df.columns]
        if len(preguntas) > 1:
            correctas = df[preguntas].sum()
            principal = correctas.idxmax()
            eliminar = [p for p in preguntas if p != principal]
            df.drop(columns=eliminar, inplace=True)
            eliminadas.extend(eliminar)
            razones.extend([(p, correctas[p]) for p in eliminar])
    return df, eliminadas, razones

def obtener_columnas_ordenadas(df):
    columnas_indicador = [col for col in df.columns if col.startswith("indicador")]
    return sorted(columnas_indicador, key=lambda x: int(x.replace("indicador", "")))

def calcular_ruta_global(df, columnas_indicadores):
    return list(df[columnas_indicadores].sum().sort_values(ascending=False).index)

def calcular_ruta_personalizada(fila, ruta_ideal):
    correctos = [col for col in ruta_ideal if fila[col] == 1]
    incorrectos = [col for col in ruta_ideal if fila[col] == 0]
    return [int(col.replace("indicador", "")) for col in correctos + incorrectos]

def asignar_id_ruta(df):
    ruta_to_id = {}
    id_to_ruta = {}
    id_actual = 0

    def obtener_id(ruta):
        nonlocal id_actual
        ruta = tuple(ruta)
        if ruta not in ruta_to_id:
            ruta_to_id[ruta] = id_actual
            id_to_ruta[id_actual] = ruta
            id_actual += 1
        return ruta_to_id[ruta]

    df['id_ruta'] = df['ruta'].apply(obtener_id)
    return df, id_to_ruta
