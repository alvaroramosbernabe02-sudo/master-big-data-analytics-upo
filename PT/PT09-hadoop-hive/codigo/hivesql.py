"""Ejecuta un fichero .sql sobre Spark SQL con soporte Hive (metastore + warehouse locales) y muestra cada sentencia y su resultado."""
import sys, time, re, os
os.environ.setdefault('JAVA_TOOL_OPTIONS','')
from pyspark.sql import SparkSession
spark = (SparkSession.builder.appName('hive-trafico').master('local[2]')
         .config('spark.sql.warehouse.dir','/home/aramber/pt09/warehouse')
         .config('spark.driver.memory','4g').config('spark.sql.shuffle.partitions','8')
         .config('spark.ui.showConsoleProgress','false')
         .config('spark.hadoop.javax.jdo.option.ConnectionURL','jdbc:derby:;databaseName=/home/aramber/pt09/metastore_db;create=true')
         .enableHiveSupport().getOrCreate())
spark.sparkContext.setLogLevel('ERROR')
src = open(sys.argv[1], encoding='utf-8').read()
src = re.sub(r'--[^\n]*', '', src)
for st in [x.strip() for x in re.split(r';[ \t]*(?:\n|$)', src) if x.strip()]:
    print('spark-sql> ' + st.replace('\n', '\n         > '))
    t = time.time(); df = spark.sql(st)
    if df.columns and not re.match(r'(?is)^(create|insert|drop|use|set|cache|load|alter)', st):
        n = int(os.environ.get('ROWS', '20'))
        df.show(n, truncate=False)
    else:
        df.collect()
    print(f'Time taken: {time.time()-t:.2f} seconds\n')
