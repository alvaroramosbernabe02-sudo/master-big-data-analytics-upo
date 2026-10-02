# TA04 — YOLO: detección y clasificación de imágenes

**Tecnologías Avanzadas** · Profesor José Antonio Lagares Rodríguez

Dos cuadernos ejecutados de principio a fin con **Ultralytics 8.4 y PyTorch 2.14**, entregados
con todas sus salidas. Se usó Jupyter con el mismo código que en Google Colab, sustituyendo
las celdas propias de Colab (montaje de Drive) por rutas locales. **Sin GPU**: el entrenamiento
se hace en CPU, lo que alarga los tiempos pero no altera los resultados.

## E1. Detección de extremo a extremo

El cuaderno recorre el ciclo completo: dataset en formato YOLO → normalización del
`data.yaml` → entrenamiento de **YOLO11n** → métricas → mAP con `supervision` →
visualización.

**Cambio de dataset justificado.** El dataset del guion (`circuit-voltages`, Roboflow) exige
iniciar sesión con una API key de Roboflow. Se usó en su lugar **`medical-pills`**, un dataset
público de Ultralytics con la misma estructura: 1 clase (`pill`), 92 imágenes de entrenamiento
y 23 de validación con 399 pastillas anotadas.

El documento explica además cómo es realmente una anotación YOLO —clase y caja normalizada
(`x_centro, y_centro, ancho, alto`)— y muestra un lote de entrenamiento con el mosaico y los
aumentos que aplica el propio framework.

## E2. Modelo propio: clasificación del tiempo atmosférico

Entrenamiento de un clasificador propio, en dos fases: un **entrenamiento base** de pocas
épocas para validar que el pipeline funciona y un **entrenamiento ampliado** después. El
modelo se prueba sobre imágenes sueltas y sobre vídeo.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/YOLO - Ej1 (resuelto).ipynb` | Detección de extremo a extremo con YOLO11n |
| `codigo/YOLO - Ej2 clasificacion tiempo.ipynb` | Clasificador propio de tiempo atmosférico |
