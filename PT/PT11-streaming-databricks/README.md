# PT11 — Streaming: arquitectura medallion en Databricks

**Plataformas Tecnológicas** · Profesor D. José Antonio Lagares Rodríguez

De la comparativa de frameworks a un pipeline que se ejecuta solo todos los días y termina en
un cuadro de mando. Es la actividad más completa del bloque de plataformas.

## Cómo se resolvió, paso a paso

### E1. Otros frameworks de tiempo real o micro-batch

Antes de comparar, se fijan los cuatro ejes que de verdad diferencian a los motores:

- **Modelo de ejecución**: evento a evento (latencia de milisegundos) frente a micro-batch
  (latencia de segundos, más rendimiento por registro).
- **Garantías de entrega**: *at-most-once*, *at-least-once* o *exactly-once*, y a qué coste.
- **Gestión de estado y tiempo**: si hay estado con puntos de control y si se distingue tiempo
  de evento de tiempo de proceso (datos que llegan tarde).
- **Modelo operativo**: clúster propio, biblioteca embebida o servicio gestionado.

Con esos ejes se comparan Storm, Trident, Spark Streaming y Flink, y se amplía a la familia
actual de motores.

### E2. Servicios de tiempo real por proveedor cloud

Equivalencias entre AWS, Azure y Google Cloud, y comparación práctica de cuándo elegir cada
una.

### E3. Extracción de una API en tiempo real y agrupación

Ejecución real contra la **API de JCDecaux (Sevici, bicicleta pública de Sevilla)** desde
Databricks:

- Código 200 y **237 estaciones** recibidas.
- Agrupación por zona: Centro 142 estaciones / 1.259 bicis, Norte 61 / 530, Sur 34 / 425.
- Agrupación por situación operativa: 218 normales, 10 sin anclajes libres, 9 sin bicis.
- Resultados persistidos en tablas Delta (`workspace.pt11.sevici_crudo` y `sevici_por_zona`).

La clave de implementación es que la clave de API y el contrato entran por `dbutils.widgets`,
nunca escritos en el notebook.

### E4. Jobs, automatización, pipeline ETL y cuadro de mando

Una **arquitectura medallion** completa sobre datos meteorológicos de tres ciudades
(Open-Meteo, API sin clave):

1. **Bronce** (`PT11_bronce.py`) — extracción de los datos puros, **parametrizada por ciudad,
   latitud y longitud** mediante widgets, en modo `append`.
2. **Plata** (`PT11_plata.py`) — limpieza, deduplicación con `dropDuplicates` y agregación, en
   modo `overwrite`.
3. **Oro** (`PT11_oro.py`) — reglas de negocio con funciones de ventana y `row_number`, con los
   umbrales de calor, frío y viento también parametrizados.
4. **Ejecución automática** — job con *trigger* programado a diario.
5. **Pipeline ETL** — un notebook orquestador que encadena las tres capas con
   `dbutils.notebook.run()` y **dependencias explícitas**: las tres ciudades en bronce, después
   plata, después oro.
6. **Cuadro de mando** — dashboard AI/BI sobre `workspace.pt11.weather_oro`.

```python
BASE = "/Workspace/Users/<usuario>/PT11 Streaming"
r1 = dbutils.notebook.run(BASE + "/PT11_bronce", 900, {"ciudad": "Sevilla", "latitud": "37.39", "longitud": "-5.98"})
r2 = dbutils.notebook.run(BASE + "/PT11_bronce", 900, {"ciudad": "Madrid",  "latitud": "40.41", "longitud": "-3.70"})
r3 = dbutils.notebook.run(BASE + "/PT11_bronce", 900, {"ciudad": "Bilbao",  "latitud": "43.26", "longitud": "-2.93"})
r4 = dbutils.notebook.run(BASE + "/PT11_plata", 900, {"ciudad": "TODAS"})
r5 = dbutils.notebook.run(BASE + "/PT11_oro",   900, {"umbral_calor": "32.0", "umbral_frio": "5.0", "umbral_viento": "40.0"})
```

## Stack

Databricks Free Edition (compute serverless), PySpark, Delta Lake, Unity Catalog, Jobs con
*Schedules & Triggers*, dashboards AI/BI con Genie, y las APIs REST de JCDecaux y Open-Meteo.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF, con las capturas de las ejecuciones, el job programado y el dashboard |
| `codigo/PT11_e3_api.py` | E3: extracción desde la API de JCDecaux y agregaciones |
| `codigo/PT11_bronce.py` | Capa bronce parametrizada por ciudad |
| `codigo/PT11_plata.py` | Capa plata: limpieza y deduplicación |
| `codigo/PT11_oro.py` | Capa oro: reglas de negocio y umbrales |
