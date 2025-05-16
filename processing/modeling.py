# processing/modeling.py

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from keras.models import Sequential
from keras.layers import Dense, Input
import pandas as pd
from .loaders import ruta_archivo

def entrenar_modelo(competencia_id):
    archivo = ruta_archivo(f"final_C{competencia_id}.csv")
    df = pd.read_csv(archivo)
    X = df.iloc[:, :-1].values
    y = df['id_ruta'].values

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = Sequential([
        Input(shape=(X.shape[1],)),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(len(set(y)), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=32, verbose=1)

    y_pred = model.predict(X_test).argmax(axis=1)
    report = classification_report(y_test, y_pred)

    model.save(ruta_archivo(f"modelo_C{competencia_id}.keras"))
    with open(ruta_archivo(f"reporte_C{competencia_id}.txt"), "w") as f:
        f.write(report)

    return report