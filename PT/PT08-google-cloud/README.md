# PT08 — Google Cloud: servicios y pipeline mediante ejemplos

**Plataformas Tecnológicas** · Profesor D. Alejandro Gómez Morón

Tres preguntas de criterio y tres ejercicios de ejecución real en GCP.

## Preguntas

**1. Cloud Function frente a Compute Engine** para una transformación breve en tiempo real
(validar un JSON, redimensionar una imagen, enriquecer un evento). La respuesta razonada es
Cloud Run Functions, con la comparación hecha criterio a criterio: unidad de trabajo,
facturación (por invocación y 100 ms de cómputo real, con escala a cero, frente a tiempo de
instancia encendida), escalado (automático e instantáneo frente a manual o con grupos
gestionados) y operación (sin sistema operativo que parchear).

**2. Mecanismo de ingesta** para un volumen ingente de datos en tiempo real.

**3. Desplegar código escrito en Node 16** en Cloud Functions, cuando el runtime ya está
retirado: qué opciones quedan y cuál es la razonable.

## Ejercicios

### E1. Cuenta de GCP

Proyecto `mbda-gvdm-2026` con el crédito de la prueba gratuita.

### E2. Pipeline con Cloud Run Functions

Una función disparada por el evento de subida a un bucket de Cloud Storage que borra el
fichero recién subido. Se entrega el código (`codigo/borrar_fichero/main.py` y su
`requirements.txt`), el comando de despliegue y la prueba de funcionamiento con los logs.

### E3. Modelo automático en BigQuery ML

Sobre un dataset propio, no el del ejemplo:

1. Dataset elegido y justificación.
2. Bucket creado y carga en BigQuery.
3. **Conjuntos de entrenamiento y test** (`codigo/split.sql`).
4. **Entrenamiento del modelo automático** (`codigo/modelo.sql`).
5. **Resultado y evaluación** (`codigo/evaluacion.sql`): **R² = 0,954**.
6. Interpretación de lo que significa realmente la salida del AutoML, que es la parte que el
   enunciado evalúa.

### Eliminación de los recursos

Todos los servicios creados se eliminaron al terminar, con las evidencias en el documento.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/borrar_fichero/main.py` | Cloud Run Function disparada por evento de Cloud Storage |
| `codigo/split.sql` | Partición en entrenamiento y test |
| `codigo/modelo.sql` | `CREATE MODEL` de BigQuery ML (AutoML) |
| `codigo/evaluacion.sql` | `ML.EVALUATE` y métricas del modelo |
