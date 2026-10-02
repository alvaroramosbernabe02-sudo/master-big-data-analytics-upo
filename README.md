# Máster en Big Data & Business Analytics — Universidad Pablo de Olavide

Trabajos de las asignaturas del máster (curso 2026), resueltos de principio a fin: no son
ejercicios de papel, sino despliegues reales con su código, sus capturas y sus resultados.
Cada actividad tiene aquí su explicación paso a paso, el código fuente y el documento
entregado en PDF.

**Álvaro Ramos Bernabé** · Data Analyst · [LinkedIn](https://www.linkedin.com/in/alvaroramosbernabe)

---

## Cómo está organizado

```
.
├── GVDM/   Gestión y Visualización de Datos Masivos   (11 actividades)
├── PT/     Plataformas Tecnológicas                   ( 5 actividades)
├── AE/     Aplicaciones Empresariales                 ( 5 actividades)
├── TA/     Tecnologías Avanzadas                      ( 2 actividades)
└── BDA/    Big Data Analytics                         ( 2 actividades)
```

Cada carpeta de actividad sigue siempre la misma estructura:

```
XXnn-nombre-de-la-actividad/
├── README.md     explicación paso a paso de cómo se resolvió
├── entrega/      el documento entregado, en PDF
└── codigo/       scripts, notebooks, SQL, Dockerfiles, blueprints… (si los hay)
```

Este README es el **resumen esquemático**: qué se hizo en cada actividad y con qué.
El detalle está en el README de cada carpeta, y el desarrollo completo con capturas de
ejecución, en el PDF.

---

## Resumen de las actividades

### GVDM · Gestión y Visualización de Datos Masivos

| # | Actividad | Qué se hizo | Stack |
|---|---|---|---|
| [01](GVDM/GVDM01-introduccion-datos-masivos) | Introducción a la gestión de datos masivos | Patologías de los SGBD tradicionales (Jacobs 2009), ACID vs. BASE y teorema CAP, elección de motor NoSQL por caso de uso, NewSQL | Ensayo técnico |
| [04](GVDM/GVDM04-data-storytelling) | Data storytelling | Informe de Power BI sobre cuentas de 3 hoteles: modelo estrella, medidas DAX de desviación presupuestaria, KPIs y comparativa con el RevPAR del INE | Power BI, Power Query, DAX |
| [07](GVDM/GVDM07-hbase-masivamente-paralelas) | BD masivamente paralelas | HBase pseudo-distribuido: caída del maestro, maestros de respaldo, 5 region servers, splits, moves y merges; y un clúster totalmente distribuido con Docker | HBase 2.6, Hadoop, ZooKeeper, Docker |
| [08](GVDM/GVDM08-bigquery-bigtable) | BigGoogle | Dataset público GHCN-M en BigQuery, modelo de BigQuery ML sobre temperaturas y comparación con Cloud Bigtable manejado desde `cbt` | BigQuery, BigQuery ML, Bigtable, GCP |
| [09](GVDM/GVDM09-recuperacion-informacion-solr) | Recuperación de información | Solr en modo SolrCloud: colección, indexación, búsquedas, facetas y análisis del comportamiento del parser de consultas | Apache Solr 9.9, SolrCloud |
| [10](GVDM/GVDM10-bd-in-memory-i) | BD In-Memory I | Límites reales de In-Memory OLTP, panorama de MMDB, caso Axis Bank con Redis, motor in-memory de MongoDB e instalación de Redis | MongoDB, Redis, SQL Server (teoría) |
| [11](GVDM/GVDM11-bd-grafos-neo4j) | BD orientadas a grafos | Comparativa Neo4j / Cosmos DB / ArangoDB / OrientDB y una red social de lectores modelada y consultada en Cypher | Neo4j, Cypher |
| [12](GVDM/GVDM12-sesion-practica-1) | Sesión práctica 1 | ETL del top 10 de contribuidores de Wikipedia a MongoDB y carga de multas de Los Ángeles en HBase con `ImportTsv` | Python, MongoDB, HBase |
| [13](GVDM/GVDM13-mongodb-documental) | MongoDB documental | 16 ejercicios de `mongosh`: consultas, arrays y subdocumentos, operadores de actualización, y medición del efecto de un índice único | MongoDB 8.3, mongosh |
| [14](GVDM/GVDM14-bd-in-memory-ii) | BD In-Memory II | Benchmark propio WiredTiger vs. motor In-Memory en 5 tamaños de colección y 5 operaciones, con los tiempos comparados | MongoDB, JavaScript |
| [15](GVDM/GVDM15-sesion-practica-2) | Sesión práctica 2 | Dump de Wikipedia cargado desde Compute Engine a MongoDB Atlas, con red y usuario de Atlas configurados, y análisis de costes GCP vs. Atlas | GCP Compute Engine, MongoDB Atlas, Python |

### PT · Plataformas Tecnológicas

| # | Actividad | Qué se hizo | Stack |
|---|---|---|---|
| [08](PT/PT08-google-cloud) | Google Cloud | Cloud Run Function disparada por subida a un bucket, y modelo automático de BigQuery ML entrenado sobre un dataset propio (R² 0,954) | Cloud Functions, Cloud Storage, BigQuery ML |
| [09](PT/PT09-hadoop-hive) | Hive y Hadoop | Explotación del tráfico de Madrid con HiveQL sobre Spark SQL: joins, agregados por estación, tabla de retenciones y limpieza en la importación | Spark SQL, Hive, Python |
| [10](PT/PT10-ingesta-cloud-kafka) | Ingesta en cloud | Productores y consumidores de Kafka, dos topics y un consumidor, y discusión del factor de replicación y el diseño de ingesta de imágenes | Apache Kafka, Python |
| [11](PT/PT11-streaming-databricks) | Streaming | Arquitectura medallion en Databricks: notebooks bronce/plata/oro parametrizados, orquestación con dependencias, job diario y cuadro de mando AI/BI | Databricks, PySpark, Delta Lake, APIs REST |
| [12](PT/PT12-workshop-ml-cloud) | Workshop | Predicción de retrasos de vuelos: modelos clásicos vs. red densa, validación cruzada, análisis de sobreajuste y la misma solución llevada a una arquitectura cloud | scikit-learn, Keras, BigQuery ML, GCP |

### AE · Aplicaciones Empresariales

| # | Actividad | Qué se hizo | Stack |
|---|---|---|---|
| [03](AE/AE03-ia-generativa-casos-uso) | IA generativa y emprendimiento | Análisis del debate de Goldman Sachs sobre el retorno de la inversión en IA, con postura propia y aplicación al sector energético | Ensayo técnico |
| [04](AE/AE04-caso-retail-forecasting) | Caso retail | Cuatro problemas de predicción: alquiler de bicicletas, ARIMA mensual, regresión diaria y consumo de agua de Sevilla, con búsqueda de hiperparámetros | scikit-learn, statsmodels, pandas |
| [05](AE/AE05-mlops-despliegue-cloud) | MLOps | Despliegue de un LLM en Cloud Run con GPU L4: job de ingesta de pesos a un bucket, imagen de vLLM y API compatible con OpenAI; todo eliminado al terminar | Cloud Run, Artifact Registry, vLLM, GCS |
| [06](AE/AE06-workshop-agentes) | Workshop de agentes | Agente de atención al cliente completo y local: 7 herramientas con tool calling, razonamiento multipaso, memoria, RAG, caché, guardrails, API REST y evaluación automática | Ollama, Chainlit, FastAPI, Pydantic, fastembed |
| [07](AE/AE07-workshop-ia-generativa-analitica) | Workshop de IA generativa | Seis agentes de análisis de datos (estadística, visualización, ML, orquestador) sobre LangChain, demostrados en vídeo de principio a fin | LangChain, Streamlit, Ollama |

### TA · Tecnologías Avanzadas

| # | Actividad | Qué se hizo | Stack |
|---|---|---|---|
| [02](TA/TA02-llms-prompting) | Modelos de lenguaje | Cinco técnicas de prompting (rol, few-shot, chain-of-thought, interview, generación de código) aplicadas en paralelo a ChatGPT y Gemini, con comparativa | ChatGPT, Gemini |
| [04](TA/TA04-yolo-vision) | YOLO | Detección de extremo a extremo con YOLO11n y entrenamiento de un clasificador propio de tiempo atmosférico, probado en imagen y en vídeo | Ultralytics, PyTorch, Jupyter |

### BDA · Big Data Analytics

| # | Actividad | Qué se hizo | Stack |
|---|---|---|---|
| [03](BDA/BDA03-social-intelligence-agentes-voz) | Social intelligence y agentes de voz | Scraping de comentarios de Facebook orquestado en Make, y un agente de voz que cualifica al cliente, consulta la agenda, crea la cita y deriva el caso al departamento correcto | Apify, Make, Google Sheets, VAPI, Google Calendar |
| [04](BDA/BDA04-caso-uso-iot) | Caso de uso de IoT | Análisis del proyecto STAR de i-DE (Iberdrola): arquitectura IoT, capa de datos del contador al analítico y valoración crítica de resultados | Caso de estudio |

---

## Stack que aparece en el repositorio

| Ámbito | Tecnologías |
|---|---|
| Cloud | Google Cloud (BigQuery, BigQuery ML, Bigtable, Cloud Storage, Cloud Run, Cloud Functions, Compute Engine, Artifact Registry), Databricks, MongoDB Atlas |
| Almacenamiento y bases de datos | HBase, Hadoop/HDFS, Hive, MongoDB (WiredTiger e In-Memory), Redis, Neo4j, Solr, Delta Lake |
| Procesamiento | Apache Spark / PySpark, Spark SQL, Apache Kafka, Python (pandas, NumPy) |
| Machine learning | scikit-learn, statsmodels, Keras/TensorFlow, Ultralytics YOLO, BigQuery ML |
| IA generativa y agentes | LangChain, Ollama, vLLM, Chainlit, Streamlit, FastAPI, Pydantic, RAG con fastembed, VAPI |
| Automatización y visualización | Make, Apify, Power BI, Looker/AI-BI dashboards, Google Workspace |
| Infraestructura | Docker, Docker Compose, PowerShell, Bash |

---

## Notas

- **Los PDF de este repositorio son los documentos entregados, con el DNI eliminado** de la
  portada y las direcciones de correo personales enmascaradas. El contenido técnico es el
  mismo que se entregó.
- El código se publica tal y como se ejecutó. Las credenciales nunca estuvieron en el
  repositorio: los scripts que necesitan secretos los leen de variables de entorno o los
  piden por teclado.
- Las actividades marcadas como *ensayo técnico* o *caso de estudio* no tienen código: su
  entregable es el propio análisis.

## Licencia

Trabajo académico publicado con fines de portfolio. El código puede reutilizarse citando la
fuente; los documentos no están pensados para ser presentados como trabajo propio por
terceros.
