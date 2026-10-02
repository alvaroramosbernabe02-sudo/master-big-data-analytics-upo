# Databricks notebook source
# MAGIC %md
# MAGIC # PT11 · Capa ORO — KPIs, alertas y decisiones
# MAGIC
# MAGIC Convierte las métricas de la capa plata en **decisiones accionables**: nivel de riesgo por
# MAGIC temperatura, recomendación operativa y ranking de ciudades. El resultado alimenta el
# MAGIC cuadro de mando y se guarda en modo *append* para conservar el histórico de alertas emitidas.
# MAGIC
# MAGIC Parámetros: umbrales de calor y de frío, para reutilizar el mismo código en otras campañas.

# COMMAND ----------

from pyspark.sql.functions import col, when, current_timestamp, lit, round as sround
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

dbutils.widgets.text("umbral_calor", "32.0", "Umbral de alerta por calor (ºC)")
dbutils.widgets.text("umbral_frio", "5.0", "Umbral de alerta por frío (ºC)")
dbutils.widgets.text("umbral_viento", "40.0", "Umbral de alerta por viento (km/h)")

u_calor = float(dbutils.widgets.get("umbral_calor"))
u_frio = float(dbutils.widgets.get("umbral_frio"))
u_viento = float(dbutils.widgets.get("umbral_viento"))

CATALOGO, ESQUEMA = "workspace", "pt11"

# COMMAND ----------

df_plata = spark.read.table(f"{CATALOGO}.{ESQUEMA}.weather_plata")

# 1. REGLAS DE NEGOCIO -> nivel de riesgo y recomendación
df_oro = (df_plata
    .withColumn("nivel_riesgo",
        when(col("temp_max") > u_calor + 5, "ALTO")
        .when((col("temp_max") > u_calor) | (col("temp_min") < u_frio) | (col("viento_max") > u_viento), "MEDIO")
        .otherwise("BAJO"))
    .withColumn("recomendacion",
        when(col("temp_max") > u_calor, "Activar protocolo de calor: refuerzo de hidratación y turnos")
        .when(col("temp_min") < u_frio, "Activar protocolo de frío: revisión de instalaciones expuestas")
        .when(col("viento_max") > u_viento, "Aviso por viento: asegurar elementos en exterior")
        .otherwise("Sin acción: condiciones dentro de los umbrales"))
    .withColumn("amplitud_termica", sround(col("temp_max") - col("temp_min"), 2))
    .withColumn("fecha_decision", current_timestamp())
    .withColumn("umbral_calor_aplicado", lit(u_calor))
    .withColumn("umbral_frio_aplicado", lit(u_frio)))

# 2. RANKING por temperatura media (KPI de comparación entre ciudades)
ventana = Window.orderBy(col("temp_media").desc())
df_oro = df_oro.withColumn("ranking_calor", row_number().over(ventana))

columnas = ["ciudad", "temp_media", "temp_max", "temp_min", "amplitud_termica", "viento_max",
            "humedad_media", "observaciones", "nivel_riesgo", "recomendacion", "ranking_calor",
            "umbral_calor_aplicado", "umbral_frio_aplicado", "fecha_decision"]

(df_oro.select(*columnas).write.format("delta").mode("append").option("mergeSchema", "true")
   .saveAsTable(f"{CATALOGO}.{ESQUEMA}.weather_oro"))

print(f"[ORO] Alertas añadidas a {CATALOGO}.{ESQUEMA}.weather_oro")
display(spark.read.table(f"{CATALOGO}.{ESQUEMA}.weather_oro").orderBy("fecha_decision", ascending=False))
