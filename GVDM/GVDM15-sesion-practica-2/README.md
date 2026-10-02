# GVDM15 — Sesión práctica 2: Wikipedia a MongoDB Atlas desde Google Cloud

**Gestión y Visualización de Datos Masivos** · Profesor Dr. Carlos D. Barranco González

Una arquitectura de dos servicios gestionados: la base de datos como servicio (DBaaS) y la
máquina que hace la carga (IaaS), con la red y los usuarios configurados como en un proyecto
real.

## A1. Carga de un dump de Wikipedia a MongoDB Atlas

**Decisión de partida.** El enunciado permitía elegir proveedor IaaS; se usó **Google Cloud**
en lugar de AWS, por coherencia con el resto de actividades (BigQuery, Bigtable) y para
aprovechar el mismo crédito de prueba.

| Componente | En clase | En esta resolución |
|---|---|---|
| DBaaS | MongoDB Atlas M0 | MongoDB Atlas M0 gratuito, MongoDB 8.0, replica set de 3 nodos |
| Región | La de AWS elegida | GCP Bélgica (`europe-west1`), la más cercana con nivel gratuito |
| IaaS | EC2 (AWS) | Compute Engine `mbda-loader`, `e2-small`, Debian 12, `europe-west1-b` |
| Herramienta de carga | Job de Talend exportado | Script Python `etl_atlas.py` con la misma lógica XPath → documentos |

### Pasos

1. **Clúster en Atlas** — creación del M0 en la misma región que la VM.
2. **Máquina de carga en Compute Engine** — instancia, Python y dependencias.
3. **Seguridad en Atlas** — lista de acceso de red con la IP de la VM y usuario de base de
   datos `mbda_loader` con permisos acotados. Es el paso que más se pasa por alto y el que
   decide si la carga funciona.
4. **Adaptación de la herramienta de carga** — `etl_atlas.py` lee el dump comprimido y hace
   `insert_many` por lotes contra la URI de Atlas.
5. **Ejecución en la nube y verificación** — `cargar.sh` pide la contraseña por teclado (nunca
   va en el fichero), compone la URI y lanza la carga cronometrada.
6. **Limpieza** — eliminación de la VM para no consumir crédito.

## A2. MongoDB sobre Kubernetes en GCP (charla de Olga Moreno)

Resumen de la charla, objetivo final de la arquitectura mostrada, por qué es relevante en un
proyecto de big data, tecnologías que aparecen y para qué sirven, y una **comparación de
costes** entre desplegar MongoDB uno mismo en GCP y pagar MongoDB Atlas.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/etl_atlas.py` | ETL del dump de Wikipedia a MongoDB Atlas |
| `codigo/cargar.sh` | Lanzador: pide la contraseña sin mostrarla, compone `MONGO_URI` y ejecuta la carga |

> `cargar.sh` no contiene credenciales: la contraseña se pide por teclado y el host del
> clúster está sustituido por un marcador.
