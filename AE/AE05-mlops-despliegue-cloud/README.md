# AE05 — MLOps: despliegue de un LLM en Google Cloud

**Aplicaciones Empresariales** · Profesor D. Juan Antonio Morente

Poner un modelo de lenguaje a servir peticiones en la nube, con GPU, y desmontarlo después.

## Arquitectura

Un **Cloud Run Job** (`llm-ingestion-job`) descarga los pesos del modelo desde Hugging Face y
los deposita en un bucket de Cloud Storage. Ese bucket se monta después con **FUSE** en
`/mnt/models` dentro de un **servicio de Cloud Run con GPU NVIDIA L4** que ejecuta **vLLM** y
expone una API compatible con OpenAI.

Separar la ingesta del servicio es la clave del patrón: los pesos se descargan **una sola vez**
y quedan en el lago, de modo que el arranque en frío del servidor no depende de Hugging Face
ni de su ancho de banda.

| Parámetro | Valor |
|---|---|
| Proyecto | `mbda-gvdm-2026` |
| Región | `europe-west1` (Bélgica, con disponibilidad de GPU L4) |
| Modelo | `Qwen/Qwen3.5-2B` |
| Repositorio de imágenes | `llm-repo` (Artifact Registry, formato Docker) |

Todo se ejecutó desde **Cloud Shell**, que ya trae `gcloud` autenticado.

## Fases

| Fase | Qué se hizo |
|---|---|
| 1 | Creación del **bucket de pesos** con acceso uniforme a nivel de bucket (sin ACL por objeto), que es la práctica recomendada |
| 2 | **Artifact Registry**: repositorio de imágenes Docker |
| 3 | **Cuenta de servicio** e identidad del despliegue, con permisos mínimos |
| 4 | **Job de ingesta**: construcción de la imagen, despliegue y ejecución |
| 5 | Verificación de los **pesos en el bucket** |
| 6 | **Imagen del servidor vLLM** y manifiesto del servicio de Cloud Run con GPU |
| 7 | **Eliminación de todos los recursos cloud**, con evidencias |

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF, con los comandos `gcloud` de cada fase y las capturas de la consola |
