import os; os.environ['JAVA_TOOL_OPTIONS']=''
from pyspark.sql import SparkSession
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
spark = (SparkSession.builder.master('local[2]').config('spark.sql.warehouse.dir','/home/aramber/pt09/warehouse')
         .config('spark.hadoop.javax.jdo.option.ConnectionURL','jdbc:derby:;databaseName=/home/aramber/pt09/metastore_db;create=true')
         .enableHiveSupport().getOrCreate()); spark.sparkContext.setLogLevel('ERROR')
spark.sql('USE trafico')
df_pandas = spark.table("taxis_limpios").toPandas()
df_cat = spark.table("taxis_categoria").toPandas()
print(type(df_pandas), df_pandas.shape)
print(df_pandas[['pickup','distance','fare','tip','total','tip_pct','pickup_borough']].head())
df_pandas['hora'] = df_pandas.pickup.dt.hour
fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
df_pandas.groupby('hora').tip_pct.mean().plot.bar(ax=ax[0], color='#4A7EBB'); ax[0].set_title('Propina media (% del total) por hora'); ax[0].set_ylabel('%')
df_cat.categoria.value_counts().plot.pie(ax=ax[1], autopct='%1.1f%%', startangle=90); ax[1].set_ylabel(''); ax[1].set_title('Viajes por categoría')
d = df_pandas[df_pandas.distance < 25]
ax[2].scatter(d.distance, d.tip, s=6, alpha=.35, c=(d.payment=='credit card').map({True:'#2E8B57', False:'#D2691E'}))
ax[2].set_xlabel('distancia (millas)'); ax[2].set_ylabel('propina (USD)'); ax[2].set_title('Propina vs distancia (verde: tarjeta, naranja: efectivo)')
plt.tight_layout(); plt.savefig('/opt/w2/shots/pt09_a3_plot.png', dpi=110); print('gráfico guardado: pt09_a3_plot.png')
print('Propina media por forma de pago:'); print(df_pandas.groupby('payment').tip_pct.mean().round(2))
