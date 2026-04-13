import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Creación del Dataset Sintético (Aprendizaje Supervisado)
# El 'Target' o etiqueta es 'Retraso_Minutos'
np.random.seed(42)
n_rows = 100

data_supervisado = {
    'Hora_Pico': np.random.randint(0, 2, n_rows), # 1: Sí, 0: No
    'Clima_Lluvia': np.random.randint(0, 2, n_rows), # 1: Lluvia, 0: Despejado
    'Incidente_Vial': np.random.randint(0, 2, n_rows), # 1: Accidente, 0: Limpio
    'Pasajeros_Abordo': np.random.randint(10, 80, n_rows),
    # El retraso se calcula con una lógica base + ruido para que el modelo aprenda
    'Retraso_Minutos': [] 
}

for i in range(n_rows):
    retraso = (data_supervisado['Hora_Pico'][i] * 5) + \
              (data_supervisado['Clima_Lluvia'][i] * 3) + \
              (data_supervisado['Incidente_Vial'][i] * 10) + \
              (data_supervisado['Pasajeros_Abordo'][i] * 0.05) + \
              np.random.normal(0, 1)
    data_supervisado['Retraso_Minutos'].append(round(max(0, retraso), 2))

df_sup = pd.DataFrame(data_supervisado)

# 2. Separación de datos (Features X y Target y)
X = df_sup.drop('Retraso_Minutos', axis=1)
y = df_sup['Retraso_Minutos']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Entrenamiento del Modelo (Random Forest Regressor)
modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# 4. Evaluación
predicciones = modelo.predict(X_test)
mae = mean_absolute_error(y_test, predicciones)
r2 = r2_score(y_test, predicciones)

print(f"Error Medio Absoluto (MAE): {mae:.2f} minutos")
print(f"Precisión del Modelo (R2 Score): {r2:.2f}")

# Ejemplo de predicción: Hora pico (1), con lluvia (1), sin incidentes (0), 50 pasajeros
ejemplo = [[1, 1, 0, 50]]
resultado = modelo.predict(ejemplo)
print(f"\nPredicción para el ejemplo: {resultado[0]:.2f} minutos de retraso.")