# GVDM08 — BigGoogle: BigQuery y Bigtable

**Gestión y Visualización de Datos Masivos** · Profesor D. Ildefonso Iglesias Escribano

Dos almacenes de Google que suelen confundirse —uno analítico y otro operacional— usados
sobre el mismo problema para que la diferencia se vea.

> Todo se ejecutó en un proyecto propio de Google Cloud (`mbda-gvdm-2026`, crédito de prueba
> gratuita). **La instancia de Bigtable se eliminó al terminar** para no consumir crédito.

## Cómo se resolvió, paso a paso

### E1. El conjunto público «GHCN Monthly»

Se importa desde *Add data → Public datasets* del Marketplace: el proyecto
`bigquery-public-data` queda anclado en el Explorer y `ghcn_m` se consulta sin copiarlo,
pagando sólo por bytes leídos. GHCN-M es la base de NOAA/NCEI con temperaturas medias
mensuales de miles de estaciones, algunas con series desde el siglo XVIII: gran cobertura,
muchos valores ausentes y, por tanto, necesidad de limpieza antes de analizar.

### E2. Localización del conjunto y creación del propio

Consideraciones relevantes del dataset y creación de un conjunto de datos propio donde
guardar las tablas de trabajo.

### E3. Consulta sobre los datos

Resuelto por las dos vías que ofrecía el enunciado: la del perfil analista (uso de la interfaz
y lectura de resultados) y la del perfil técnico (la sentencia SQL propuesta).

### E4. Análisis predictivo

También por las dos vías. En la técnica se entrena un modelo con **BigQuery ML** sobre las
temperaturas máximas, directamente en SQL, sin mover los datos fuera del almacén.

### E5. BigQuery frente a Cloud Bigtable

La comparación es el núcleo de la actividad: BigQuery es un almacén **analítico** columnar
para consultas agregadas sobre mucho histórico; Bigtable es un almacén **operacional**
clave-valor ancho, de latencia baja y acceso por clave de fila. Se crea una instancia, una
tabla y se cargan datos con la herramienta `cbt` desde Cloud Shell.

### E6. Solución para una red de sensores

Diseño propuesto para la plantación del enunciado, eligiendo motor según el patrón de acceso:
ingesta y lectura por sensor y marca de tiempo en Bigtable, agregados históricos en BigQuery.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF, con las capturas de las consultas, del modelo de BigQuery ML y de la sesión `cbt` |
