import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 1. Creación del Dataset Sintético
data = {
    'Estacion': [f'Estacion_{i}' for i in range(1, 21)],
    'Afluencia': [1200, 1500, 300, 450, 1800, 200, 2100, 500, 1600, 400, 
                  1300, 1550, 350, 480, 1900, 250, 2200, 550, 1700, 420],
    'Tiempo_Espera': [2, 3, 10, 8, 4, 12, 5, 9, 3, 11, 
                      2.5, 3.5, 9.5, 7.5, 4.5, 13, 5.5, 8.5, 3.2, 10.5]
}

df = pd.DataFrame(data)

# 2. Preprocesamiento (Escalado de datos)
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[['Afluencia', 'Tiempo_Espera']])

# 3. Aplicación de K-Means
# Usaremos 3 clusters: Alta Demanda, Media y Baja.
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(df_scaled)

# 4. Visualización de resultados
plt.figure(figsize=(10, 6))
plt.scatter(df['Afluencia'], df['Tiempo_Espera'], c=df['Cluster'], cmap='viridis', s=100)
plt.title('Agrupamiento de Estaciones de Transporte Masivo')
plt.xlabel('Afluencia de Pasajeros (Hora Pico)')
plt.ylabel('Tiempo de Espera (Minutos)')
plt.colorbar(label='Cluster ID')
plt.grid(True)
plt.show()

# Resumen de los grupos
print("Resumen por Cluster:")
print(df.groupby('Cluster').mean(numeric_only=True))