# Databricks notebook source
# MAGIC %md
# MAGIC # PT11 · Capa PLATA — Limpieza, deduplicación y agregación
# MAGIC
# MAGIC Lee `weather_bronce`, descarta observaciones no válidas, elimina duplicados
# MAGIC (la misma observación se repite si el Job se ejecuta dos veces dentro de la misma hora)
# MAGIC y calcula métricas agregadas por ciudad en `workspace.pt11.weather_plata`.
# MAGIC
# MAGIC Parámetro opcional `ciudad`: con el valor `TODAS` procesa todas las ciudades ingeridas.

# COMMAND ----------

from pyspark.sql.functions import (col, avg, max as smax, min as smin, count, stddev,
                                   to_timestamp, current_timestamp, lit, round as sround)

dbutils.widgets.text("ciudad", "TODAS", "Ciudad a procesar (TODAS = todas)")
p_ciudad = dbutils.widgets.get("ciudad")

CATALOGO, ESQUEMA = "workspace", "pt11"

# COMMAND ----------

# 1. LECTURA DE LA CAPA BRONCE
df = spark.read.table(f"{CATALOGO}.{ESQUEMA}.weather_bronce")
if p_ciudad.upper() != "TODAS":
    df = df.filter(col("ciudad") == p_ciudad)
print(f"[PLATA] Filas leídas de bronce: {df.count()}")

# 2. LIMPIEZA: tipos correctos, rangos plausibles y deduplicación
df_limpio = (df
    .withColumn("momento", to_timestamp(col("timestamp_sensor")))
    .filter(col("temperatura").between(-40, 55))          # descarta lecturas imposibles
    .filter(col("viento") >= 0)
    .dropDuplicates(["ciudad", "timestamp_sensor"]))       # una observación por ciudad y hora
print(f"[PLATA] Filas tras limpiar y deduplicar: {df_limpio.count()}")

# 3. AGREGACIÓN POR CIUDAD
df_plata = (df_limpio.groupBy("ciudad", "latitud", "longitud")
    .agg(sround(avg("temperatura"), 2).alias("temp_media"),
         smax("temperatura").alias("temp_max"),
         smin("temperatura").alias("temp_min"),
         sround(stddev("temperatura"), 2).alias("temp_desv"),
         sround(avg("viento"), 2).alias("viento_medio"),
         smax("viento").alias("viento_max"),
         sround(avg("humedad"), 1).alias("humedad_media"),
         count("*").alias("observaciones"),
         smax("momento").alias("ultima_observacion"))
    .withColumn("ultima_actualizacion", current_timestamp()))

# 4. ESCRITURA (overwrite: la plata refleja siempre el estado actual del histórico)
(df_plata.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
   .saveAsTable(f"{CATALOGO}.{ESQUEMA}.weather_plata"))

print(f"[PLATA] Tabla {CATALOGO}.{ESQUEMA}.weather_plata actualizada")
display(spark.read.table(f"{CATALOGO}.{ESQUEMA}.weather_plata").orderBy("temp_media", ascending=False))
