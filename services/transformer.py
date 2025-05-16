import numpy as np

EQUIVALENCIAS = {
    "C1": {
        1: [4], 2: [2], 3: [5], 4: [5], 5: [5], 6: [6], 7: [7],
        8: [8], 9: [9], 10: [10, 1], 11: [3], 12: [4]
    },
    "C2": {
        1: [1], 2: [2, 5], 3: [3], 4: [4], 5: [3, 5], 6: [6],
        7: [1], 8: [1], 9: [3, 6], 10: [5], 11: [4]
    },
    "C3": {
        1: [3], 2: [4], 3: [1], 4: [8], 5: [4], 6: [5, 6],
        7: [7], 8: [3, 5], 9: [2, 6], 10: [3, 5], 11: [], 12: [3]
    },
    "C4": {
        1: [2], 2: [2], 3: [2], 4: [3, 4], 5: [3], 6: [2],
        7: [2], 8: [3, 4], 9: [1], 10: [2], 11: [2], 12: [3, 4], 13: [3, 4]
    }
}

LONGITUDES_ESPERADAS = {
    "C1": 10,
    "C2": 6,
    "C3": 8,
    "C4": 4
}

def transformar_input(input_preguntas, competencia):
    esperado = LONGITUDES_ESPERADAS.get(competencia)
    if esperado is None:
        raise ValueError(f"Competencia desconocida: {competencia}")

    if len(input_preguntas) != esperado:
        raise ValueError(f"La cantidad de preguntas para {competencia} debe ser {esperado}, pero recibió {len(input_preguntas)}")

    if any(p not in (0, 1) for p in input_preguntas):
        raise ValueError("Las respuestas solo pueden ser 0 o 1.")

    equivalencia = EQUIVALENCIAS[competencia]
    num_indicadores = max(equivalencia.keys())
    output = []

    for i in range(1, num_indicadores + 1):
        preguntas = equivalencia[i]
        if not preguntas:
            valor = 0
        elif all(1 <= p <= esperado for p in preguntas):
            valor = 1 if all(input_preguntas[p - 1] == 1 for p in preguntas) else 0
        else:
            valor = 0
        output.append(valor)

    return np.array(output, dtype=np.float32).reshape(1, -1)

def transformar_output(ruta_dict, competencia):
    equivalencia = EQUIVALENCIAS[competencia]

    ruta_indices = ruta_dict

    ruta_preguntas = []

    for ind in ruta_indices:
        preguntas = equivalencia.get(ind, [])
        for p in preguntas:
            if p in ruta_preguntas:
                ruta_preguntas.remove(p)
            ruta_preguntas.append(p)
    return ruta_preguntas
