# PT09 — Hive y distribuciones Hadoop

**Plataformas Tecnológicas** · Profesor José Ignacio Merino Martín

Explotación de datos abiertos de tráfico con HiveQL, con el detalle de que el entorno se
montó en local en lugar de usar Databricks.

## Entorno de ejecución

El guion proponía Databricks Free Edition. Aquí las consultas se ejecutaron sobre
**Apache Spark 3.5.3 con soporte Hive** (`enableHiveSupport()`), metastore Derby y warehouse
locales. Es el mismo motor Spark SQL que usa Databricks y el mismo dialecto HiveQL; las
diferencias se señalan donde aparecen (por ejemplo, `read_files()` es exclusiva de Databricks
y se sustituye por una vista temporal `USING csv` con las mismas opciones). **Todo el SQL puede
pegarse en un notebook de Databricks cambiando sólo la ruta de los ficheros.**

El script `hivesql.py` ejecuta un fichero `.sql` sentencia a sentencia mostrando el resultado
y el tiempo de cada una, como haría la consola `spark-sql`.

## Cómo se resolvió, paso a paso

### A1. Explotar datos con Hive — tráfico de Madrid, diciembre 2025

1. Fechas y horas con **intensidad superior a 20.000 vehículos**, cruzando medidas y
   estaciones con `INNER JOIN`.
2. **Media de intensidad por mes** de cada estación.
3. **Número de puntos de medición** de cada estación.
4-5. Creación de la tabla `retenciones_diciembre` y estaciones con más instantes de
   **ocupación superior al 90 %**.

### A2. Mover datos entre datasets

Mismo ejercicio sobre los datos de noviembre de 2019, practicando el movimiento de datos
entre conjuntos.

### A3. Limpieza de datos en la importación — taxis de Nueva York

Depuración durante la carga: tipos, nulos y registros imposibles. Se incluye además una
versión en pandas (`a3_pandas.py`) para contrastar los resultados.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/hivesql.py` | Ejecutor de ficheros `.sql` sobre Spark SQL con soporte Hive |
| `codigo/a1_carga.sql`, `codigo/a1_consultas.sql` | Carga y consultas de la A1 |
| `codigo/q11.sql` … `codigo/q14.sql` | Consultas numeradas de la A1 |
| `codigo/a2.sql` | A2: movimiento entre datasets |
| `codigo/a3.sql`, `codigo/a3_pandas.py` | A3: limpieza en la importación, en HiveQL y en pandas |
