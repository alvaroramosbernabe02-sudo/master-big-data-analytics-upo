# GVDM14 — Bases de datos In-Memory II: benchmark WiredTiger vs. In-Memory

**Gestión y Visualización de Datos Masivos** · Profesor Dr. Domingo Savio Rodríguez Baena

La continuación práctica de [GVDM10](../GVDM10-bd-in-memory-i): medir, no suponer, cuánto
aporta un motor en memoria.

## Diseño del experimento

**Entorno.** MongoDB Enterprise 8.3.11 en Linux (2 vCPU, 7 GB de RAM) con **dos instancias en
la misma máquina**, para que las condiciones sean idénticas:

- `:27017` — motor estándar **WiredTiger** (datos y journal en disco)
- `:27018` — motor **In-Memory** (`--storageEngine inMemory --inMemorySizeGB 1`)

**Tamaños.** La colección crece por pasos acumulativos: 25.000 → 50.000 → 100.000 → 200.000 →
400.000 documentos (cinco tamaños; el enunciado pedía tres como mínimo). En cada paso se
insertan sólo los documentos que faltan, con la función `populatePhones` del enunciado.

**Operaciones medidas.**

| Op. | Implementación | Qué mide |
|---|---|---|
| I1 | `populatePhones(800, inicio, fin)`, un `insertOne` por documento | Tiempo total de carga del lote |
| Q1 | `find({ display: <valor> })` — campo **no** indexado | Búsqueda recorriendo la colección (`COLLSCAN`) |
| Q2 | `find({ _id: <valor> })` — campo indexado | Búsqueda por índice (`IXSCAN`) |
| U1 | `updateOne({ _id: … }, { $set: … })` | Modificación de un único documento |
| U2 | `updateMany({ "components.country": 3 }, { $inc: … })` | Modificación de ~1/8 de la colección |

## Resultados

Los tres apartados del documento son el experimento con WiredTiger (E1), el mismo con el
motor In-Memory (E2) y la **comparativa de tiempos** (E3), con las curvas de cada operación
frente al tamaño de la colección. La lectura que se extrae es la esperable pero conviene
verla medida: la ventaja del motor en memoria no es uniforme, depende de si la operación
estaba limitada por disco o por CPU, y desaparece en cuanto el *working set* de WiredTiger
cabe en caché.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF, con las tablas y gráficas de tiempos |
| `codigo/bench.js`, `codigo/bench2.js` | Scripts de `mongosh` que ejecutan el benchmark y miden cada operación |
