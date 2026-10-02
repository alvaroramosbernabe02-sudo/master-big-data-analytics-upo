# AE04 — Caso retail: forecasting y regresión

**Business Analytics** · Profesor José Ignacio Merino

Cuatro problemas de predicción distintos, resueltos con la misma disciplina metodológica:
partición fija, búsqueda de hiperparámetros por validación cruzada y una única evaluación
final sobre test.

## Entorno

Python 3.11 con pandas, scikit-learn 1.8 y statsmodels. Los datos son los CSV suministrados en
el Aula Virtual y `day.csv` del *Bike Sharing Dataset* (UCI, 731 días de 2011-2012).

## A1. Alquiler diario de bicicletas

El ejercicio tiene una trampa que hay que ver: `casual + registered = cnt`, de modo que dejar
esas dos columnas daría un error prácticamente nulo **por fuga de información**. Se eliminan,
junto con el identificador y la fecha.

Las categóricas (estación, meteorología, mes y día de la semana) se codifican con one-hot y se
usa el mismo split 80/20 (`random_state=42`) para todos los modelos. Los hiperparámetros se
buscan con `GridSearchCV` (validación cruzada de 5 particiones sobre train, optimizando MAE)
y se evalúa una única vez sobre test. Se comparan Ridge, Random Forest y Gradient Boosting.

## A2. Forecast ARIMA de las ventas mensuales de Fanta 33cl

Serie temporal mensual con statsmodels: identificación del orden, ajuste y predicción.

## A3. Forecast de ventas diarias de Fanta con modelos de regresión

El mismo producto a resolución diaria, pero tratado como problema de regresión con variables
de calendario, para contrastar el enfoque con el del ARIMA del apartado anterior.

## A4. Consumo de agua de Sevilla

Forecast diario y mensual del consumo, cerrando con la comparación entre ambas resoluciones.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/a1_bicis.py` | A1: alquiler diario de bicicletas |
| `codigo/a2_fanta_arima.py` | A2: ARIMA mensual |
| `codigo/a3_fanta_diaria.py` | A3: regresión diaria |
| `codigo/a4_agua.py` | A4: consumo de agua de Sevilla |
