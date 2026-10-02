# PT12 — Workshop: machine learning y arquitectura cloud de extremo a extremo

**Plataformas Tecnológicas** · Profesores D. José Ignacio Merino y D. José Antonio Lagares

Un mismo problema resuelto dos veces: primero en local con scikit-learn y Keras, después
llevado a una arquitectura de Google Cloud completa.

## Planteamiento y datos

`flights_subsampling.csv` (muestra del *On-Time Performance* del Departamento de Transporte
de EE. UU., 2015) más los catálogos de aerolíneas y aeropuertos. El problema es de
**clasificación binaria**: predecir si un vuelo llegará con más de 15 minutos de retraso
(criterio de la FAA).

Las decisiones de preparación son la parte que más condiciona el resultado:

- Se descartan cancelados y desviados (no tienen hora de llegada real) y los registros sin
  `ARRIVAL_DELAY`. Quedan **89.675 vuelos, de los que el 35,1 % van retrasados**.
- **Sólo se usan variables conocidas antes del despegue**: mes, día, día de la semana, hora
  programada de salida y llegada, duración programada, distancia, aerolínea y aeropuertos.
  Incluir `DEPARTURE_DELAY` o los campos de causa daría métricas artificialmente altas por
  fuga de información, porque sólo se conocen cuando el vuelo ya ha ocurrido.
- Los aeropuertos se reducen a los 40 más frecuentes y el resto se agrupa en `OTRO`, para
  evitar miles de columnas tras la codificación.
- Preprocesado común (`comun.py`): `StandardScaler` en las numéricas y
  `OneHotEncoder(handle_unknown='ignore')` en las categóricas, dentro de un
  `ColumnTransformer` encapsulado en un `Pipeline`, de modo que la transformación se ajusta
  sólo con los datos de entrenamiento de cada partición y no hay filtraciones.
- Partición base: hold-out 80-20 estratificado.

## Ejercicios

| # | Qué se hizo | Fichero |
|---|---|---|
| E1 | Algoritmo de ML clásico (sin redes neuronales) | `codigo/e1_ml.py` |
| E2 | Red neuronal densa y comparación con el anterior | `codigo/e2_red.py` |
| E3 | Validación cruzada frente a hold-out 80-20 y 70-30 | `codigo/e3_validacion.py` |
| E4 | Hiperparametrización y análisis de sobreajuste: **¿existe? ¿cómo se evita?** | `codigo/e4_hiper.py` |
| E5 | La misma solución como **arquitectura cloud de extremo a extremo** | `codigo/cloud/` |

### E5. Arquitectura cloud

1. **Ingesta** — servicio en contenedor (`codigo/cloud/ingesta/`, con su `Dockerfile`).
2. **Procesado** — `codigo/cloud/procesado.sql`.
3. **Algoritmo de ML con BigQuery ML** — `codigo/cloud/ml.sql`.
4. **Resultados y visualización** — `codigo/cloud/resultados.sql` y `e5_visualizacion.py`.
5. **Equivalencia en AWS** — servicio a servicio.
6. **Eliminación de los recursos cloud**, con evidencias.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/comun.py` | Carga, limpieza y preprocesado compartido por todos los modelos |
| `codigo/e1_ml.py` … `codigo/e4_hiper.py` | Ejercicios 1 a 4 |
| `codigo/e5_visualizacion.py` | Visualización de los resultados del ejercicio 5 |
| `codigo/cloud/` | Arquitectura en GCP: ingesta en contenedor y SQL de procesado, ML y resultados |
