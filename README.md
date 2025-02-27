# ViksModelAPI  

## 📌 Descripción del Proyecto  
**ViksModelAPI** es una API desarrollada con **FastAPI** que permite predecir rutas de aprendizaje para estudiantes en función de sus respuestas a un cuestionario de desempeño. Utiliza un modelo de aprendizaje profundo MLP del tipo Feed-Forward entrenado con **TensorFlow/Keras** para asignar a cada estudiante una ruta óptima de aprendizaje basada en sus habilidades y conocimientos previos.  

## 🛠️ Requisitos Previos  
1. **Instalar Python**  
   Se requiere una versión de **Python 3.10 a 3.12** para ejecutar el proyecto correctamente.  
   - Se puede descargar la última versión compatible desde: [Python 3.12.9](https://www.python.org/downloads/release/python-3129/)  
   - Se debe agregar Python al `PATH` durante la instalación.  

2. **Actualizar `pip` (Opcional pero recomendado)**  
   Ejecutar el siguiente comando en la terminal con permisos de administrador:  
   ```sh
   python -m pip install --upgrade pip
   ```

## 📦 Instalación de Dependencias  
Para instalar las bibliotecas necesarias, ejecutar el siguiente comando en la terminal dentro del directorio del proyecto:  
```sh
pip install fastapi pydantic pandas numpy tensorflow uvicorn
```

## 🚀 Ejecución de la API  
Ubicarse en la carpeta donde se encuentra `app.py` y ejecutar:  
```sh
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```
Esto iniciará el servidor en `http://127.0.0.1:8000/`.

## 📡 Uso de la API
### 🔹 Endpoint para predecir rutas de aprendizaje  
**URL:** `http://127.0.0.1:8000/predecir_ruta`  
**Método:** `POST`  
**Encabezados:** `Content-Type: application/json`  

📥 **Cuerpo de la solicitud (`JSON`):**  
```json
{
  "id_estudiante": 123,
  "preguntas": [1, 0, 1, 1, 0, 0, 1, 0, 0, 1]
}
```
📤 **Respuesta esperada (`JSON`):**  
```json
{
  "id_estudiante": 123,
  "ruta": [1, 4, 10, 3, 7, 5, 6, 2, 9, 8]
}
```
📌 **Notas:**  
- `id_estudiante` es un identificador único del estudiante.  
- `preguntas` es una lista de **10 valores binarios (0 o 1)** que representan el desempeño del estudiante en distintas competencias.  
- `ruta` es la lista de desempeños de aprendizaje generada por el modelo, el orden de los mismos corresponde a la ruta sugerida.  

## 📊 Acceder a la documentación interactiva  
FastAPI genera automáticamente documentación de la API en estos enlaces:  
- **Swagger UI:** [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)  
- **Redoc UI:** [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)