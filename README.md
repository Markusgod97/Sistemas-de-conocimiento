 El sistema está basado en dos conceptos: representación del conocimiento con reglas lógicas, y búsqueda heurística
 con el algoritmo A estrella.

El archivo principal está dividido en cuatro partes: 

1 La base de hechos
2 La base de reglas,
3 El motor de inferencia
4 Interfaz de resultados


Enlace a video:

https://www.loom.com/share/45fe02fd702c44f897113c0e7ee2ce96


# Optimización de Sistemas de Transporte Masivo con IA
Proyecto de Inteligencia Artificial enfocado en la segmentación de estaciones y predicción de retrasos en una red de transporte masivo, usando técnicas de aprendizaje supervisado y no supervisado.

# Datos
El proyecto trabaja con dos datasets sintéticos basados en operación real:
Dataset No Supervisado – Caracterización de Estaciones
Permite segmentar estaciones sin etiquetas previas. Variables: ID_Estacion, Afluencia_Promedio, Tiempo_Espera.
Dataset Supervisado – Predicción de Retrasos
Datos históricos etiquetados. Features: Hora_Pico, Clima_Lluvia, Incidente_Vial. Target: Minutos_Retraso.

# Metodología

K-Means — Clustering de estaciones para detectar patrones de congestión ocultos. Se aplicó StandardScaler para normalizar las escalas antes del agrupamiento.
Random Forest — Ensamble de árboles de decisión para predecir retrasos, seleccionado por su manejo de relaciones no lineales entre variables climáticas y operativas.


 # Resultados
ModeloMétricaValorK-MeansNúmero de clusters (K)3Random ForestMAE~1.2 minRandom ForestR² Score0.88
El Método del Codo confirmó K=3 como punto óptimo, distinguiendo estaciones periféricas, de conexión y nodos críticos. El modelo supervisado se entrenó con partición 80/20.

# Enlaces
Video 

https://www.loom.com/share/49db8758abae4e59b488f9c7243f31f3

