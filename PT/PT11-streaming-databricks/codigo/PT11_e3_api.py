# Databricks notebook source
# MAGIC %md
# MAGIC # PT11 · Ejercicio 3 — Extracción de datos de una API en tiempo real y agrupación
# MAGIC
# MAGIC Se consulta en tiempo real el estado del **servicio público de bicicletas de Sevilla (Sevici)**
# MAGIC a través de la API de JCDecaux, que **requiere API key**, y se agrupan los resultados por
# MAGIC distrito/zona para obtener la disponibilidad agregada del sistema en ese instante.
# MAGIC
# MAGIC La ejecución se realiza sobre Databricks (herramienta cloud) con Spark.

# COMMAND ----------

import requests, datetime
from pyspark.sql.functions import col, count, sum as ssum, avg, round as sround, when, current_timestamp, lit

dbutils.widgets.text("contrato", "Seville", "Contrato JCDecaux (ciudad)")
dbutils.widgets.text("api_key", "", "API key de JCDecaux")

contrato = dbutils.widgets.get("contrato")
api_key = dbutils.widgets.get("api_key")   # se pasa como parámetro del Job, no se escribe en el código

CATALOGO, ESQUEMA = "workspace", "pt11"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOGO}.{ESQUEMA}")

# COMMAND ----------

# 1. LLAMADA A LA API EN TIEMPO REAL (requiere API key)
URL = f"https://api.jcdecaux.com/vls/v1/stations?contract={contrato}&apiKey={api_key}"
r = requests.get(URL, timeout=30)
print("Código de respuesta:", r.status_code)
estaciones = r.json()
print(f"Estaciones recibidas: {len(estaciones)}  ({datetime.datetime.now().isoformat(timespec='seconds')})")

# 2. NORMALIZACIÓN A DATAFRAME DE SPARK
filas = [(e["number"], e["name"], e.get("address"), e["status"],
          e["bike_stands"], e["available_bikes"], e["available_bike_stands"],
          float(e["position"]["lat"]), float(e["position"]["lng"]),
          bool(e.get("banking")), str(e.get("last_update"))) for e in estaciones]

df = spark.createDataFrame(filas, "numero int, nombre string, direccion string, estado string, "
                                  "anclajes int, bicis_disponibles int, anclajes_libres int, "
                                  "lat double, lon double, con_tpv boolean, ultima_actualizacion string")
df = df.withColumn("momento_consulta", current_timestamp())
df.write.format("delta").mode("append").saveAsTable(f"{CATALOGO}.{ESQUEMA}.sevici_crudo")
display(df.limit(10))

# COMMAND ----------

# 3. AGRUPACIÓN: la zona se deriva del prefijo del nombre de la estación (nnn - ZONA)
df_zona = (df.withColumn("zona",
        when(col("lat") > 37.40, "Norte").when(col("lat") < 37.37, "Sur").otherwise("Centro"))
    .groupBy("zona")
    .agg(count("*").alias("estaciones"),
         ssum("bicis_disponibles").alias("bicis_disponibles"),
         ssum("anclajes_libres").alias("anclajes_libres"),
         ssum("anclajes").alias("anclajes_totales"),
         sround(avg("bicis_disponibles"), 1).alias("bicis_media_estacion"))
    .withColumn("ocupacion_pct", sround(col("bicis_disponibles") / col("anclajes_totales") * 100, 1))
    .orderBy(col("ocupacion_pct").desc()))

display(df_zona)

# COMMAND ----------

# 4. SEGUNDA AGRUPACIÓN: estaciones críticas (sin bicis o sin sitio) por estado operativo
df_critico = (df.withColumn("situacion",
        when(col("estado") != "OPEN", "Cerrada")
        .when(col("bicis_disponibles") == 0, "Sin bicis")
        .when(col("anclajes_libres") == 0, "Sin anclajes libres")
        .otherwise("Normal"))
    .groupBy("situacion").agg(count("*").alias("estaciones"))
    .orderBy(col("estaciones").desc()))
display(df_critico)

df_zona.withColumn("momento", current_timestamp()).write.format("delta").mode("append").saveAsTable(f"{CATALOGO}.{ESQUEMA}.sevici_por_zona")
print("Agregados guardados en workspace.pt11.sevici_por_zona")
