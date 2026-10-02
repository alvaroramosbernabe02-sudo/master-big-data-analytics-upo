# GVDM09 — Sistemas de recuperación de información (Apache Solr)

**Gestión y Visualización de Datos Masivos** · Profesor D. Alejandro Gómez Morón

Instalar un motor de búsqueda, indexar un catálogo y —lo que de verdad se evalúa— entender
por qué devuelve lo que devuelve.

## Entorno

Ubuntu 24.04, OpenJDK 17 y **Apache Solr 9.9.0** en modo **SolrCloud** (`bin/solr start -c`),
que arranca un ZooKeeper embebido en el puerto 9983.

## Cómo se resolvió, paso a paso

### A1. Instalación

Arranque, `bin/solr status` (puerto 8983, heap de 512 MB, ZooKeeper en 127.0.0.1:9983, un
nodo vivo y cero colecciones) y Dashboard de la consola de administración, con la sección
*Cloud* propia del modo SolrCloud.

### A2. Colección, indexación y búsquedas

- **Ejercicio 0** — creación de la colección `techproducts` con el configset
  `sample_techproducts_configs`.
- **Ejercicio 1** — indexación de los datos de ejemplo.
- **Búsqueda 1** — `The Black Company`.
- **Búsqueda 2** — `System Memory`.
- **Búsqueda 3** — la misma, con **búsqueda facetada** por género.

### A3. Análisis de las consultas

La parte con más contenido: se comparan los resultados de `System`, `Company Cook` y
`Company with Cook` y se explica el comportamiento del parser por defecto —cómo trata los
términos múltiples, el papel del operador implícito y por qué una palabra vacía como *with*
cambia (o no) el conjunto devuelto—. De ahí salen las respuestas a las preguntas del guion.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF, con las capturas de cada consulta y de la consola de Solr |
