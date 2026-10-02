# GVDM13 — MongoDB: bases de datos documentales

**Gestión y Visualización de Datos Masivos** · Profesor Dr. Domingo Savio Rodríguez Baena

Dieciséis ejercicios encadenados en `mongosh`, de la instalación al efecto medible de un
índice. Es la actividad que recorre el modelo documental entero.

## Entorno

**MongoDB Enterprise Server 8.3.11** y **mongosh 2.12.0**. Las capturas reproducen la sesión
interactiva: tras el prompt `mbda>` va el comando y debajo su resultado. No se usó Compass
porque la máquina de pruebas no tiene entorno gráfico, pero todo es idéntico desde el shell
integrado de Compass.

## Cómo se resolvió, paso a paso

| # | Ejercicio | Qué se trabaja |
|---|---|---|
| E1 | Instalación | Descompresión del `.tgz`, directorios de datos y logs, arranque de `mongod --dbpath` y comprobación con `db.runCommand({ping:1})` |
| E2 | Base `mbda` y colección `towns` | Creación implícita y primeras inserciones |
| E3 | Colecciones sin esquema fijo | Documentos con campos distintos en la misma colección |
| E4 | El identificador `_id` | Qué es un ObjectId y qué garantiza |
| E5 | Funciones JavaScript | `insertCity` definida y ejecutada en el shell |
| E6 | Consultas simples y proyecciones | `find` con filtros y selección de campos |
| E7 | Consultas compuestas | Operadores lógicos y de comparación |
| E8 | Arrays y subdocumentos | Consulta sobre estructuras anidadas |
| E9 | `$exists`, colección `countries`, `_id` duplicado | Qué ocurre al insertar un `_id` repetido |
| E10 | `$elemMatch` | Condiciones conjuntas sobre un mismo elemento de array |
| E11 | `updateOne` con `$set` frente a `replaceOne` | La diferencia que más errores causa en producción |
| E12 | `$inc` | Incremento atómico |
| E13 | Borrado | `deleteOne` / `deleteMany` |
| E14 | Rendimiento **sin** índice | `COLLSCAN`: recorrido completo |
| E15 | Índice `UNIQUE` sobre `display` | Creación y efecto sobre las inserciones |
| E16 | Rendimiento **con** índice | `IXSCAN` y comparación de tiempos y documentos examinados |

Los tres últimos ejercicios son los que dan sentido a todo: muestran, con `explain()`, la
diferencia entre recorrer la colección y recorrer un índice.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF, con la sesión de `mongosh` completa |
