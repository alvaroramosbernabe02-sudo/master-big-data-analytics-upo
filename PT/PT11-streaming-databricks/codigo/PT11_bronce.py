# Databricks notebook source
# MAGIC %md
# MAGIC # PT11 · Capa BRONCE — Ingesta de datos crudos desde una API en tiempo real
# MAGIC
# MAGIC Extrae la observación meteorológica actual de la API pública **Open-Meteo** y la deposita
# MAGIC **sin transformar** en la tabla Delta `workspace.pt11.weather_bronce`.
# MAGIC
# MAGIC El notebook está **parametrizado con widgets** (ciudad, latitud, longitud), de modo que el mismo
# MAGIC código sirve para cualquier ciudad: el Job pasa los valores como *Key/Value* en cada tarea.
# MAGIC
# MAGIC Álvaro Ramos Bernabé — Máster Big Data & Business Analytics (UPO)

# COMMAND ----------

import requests
from pyspark.sql.functions import lit, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# 1. PARÁMETROS (widgets) -> el Job los inyecta como parámetros de la tarea
dbutils.widgets.text("ciudad", "Sevilla", "Nombre de la ciudad")
dbutils.widgets.text("latitud", "37.39", "Latitud")
dbutils.widgets.text("longitud", "-5.98", "Longitud")

p_ciudad = dbutils.widgets.get("ciudad")
p_lat = dbutils.widgets.get("latitud")
p_lon = dbutils.widgets.get("longitud")

CATALOGO, ESQUEMA = "workspace", "pt11"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOGO}.{ESQUEMA}")

# COMMAND ----------

# 2. LLAMADA A LA API EN TIEMPO REAL
URL = (f"https://api.open-meteo.com/v1/forecast?latitude={p_lat}&longitude={p_lon}"
       "&current_weather=true&hourly=relative_humidity_2m&timezone=Europe%2FMadrid")

def extraer():
    r = requests.get(URL, timeout=30)
    if r.status_code != 200:
        raise Exception(f"Error en la API ({r.status_code}): {r.text[:200]}")
    j = r.json()
    a = j["current_weather"]
    # humedad de la hora actual (la API la devuelve como serie horaria)
    hora = a["time"]
    try:
        idx = j["hourly"]["time"].index(hora)
        humedad = float(j["hourly"]["relative_humidity_2m"][idx])
    except (ValueError, KeyError):
        humedad = None
    return (float(a["temperature"]), float(a["windspeed"]), int(a["winddirection"]),
            int(a["weathercode"]), humedad, str(hora))

temperatura, viento, direccion, codigo, humedad, ts_api = extraer()
print(f"[BRONCE] {p_ciudad}: {temperatura} ºC, viento {viento} km/h, humedad {humedad} %, observación de {ts_api}")

# COMMAND ----------

# 3. DATAFRAME CRUDO + METADATOS DE INGESTA (trazabilidad)
esquema = StructType([
    StructField("temperatura", DoubleType()), StructField("viento", DoubleType()),
    StructField("direccion_viento", IntegerType()), StructField("codigo_tiempo", IntegerType()),
    StructField("humedad", DoubleType()), StructField("timestamp_sensor", StringType()),
])

df = (spark.createDataFrame([(temperatura, viento, direccion, codigo, humedad, ts_api)], esquema)
      .withColumn("ciudad", lit(p_ciudad))
      .withColumn("latitud", lit(float(p_lat)))
      .withColumn("longitud", lit(float(p_lon)))
      .withColumn("fecha_ingesta", current_timestamp())
      .withColumn("origen", lit("open-meteo/v1/forecast")))

# 4. APPEND: la capa bronce es un histórico inmutable, nunca se sobrescribe
(df.write.format("delta").mode("append")
   .saveAsTable(f"{CATALOGO}.{ESQUEMA}.weather_bronce"))

print(f"[BRONCE] Fila añadida a {CATALOGO}.{ESQUEMA}.weather_bronce")
display(spark.read.table(f"{CATALOGO}.{ESQUEMA}.weather_bronce").orderBy("fecha_ingesta", ascending=False).limit(10))
