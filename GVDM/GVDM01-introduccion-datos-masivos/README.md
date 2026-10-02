# GVDM01 — Introducción a la gestión de datos masivos

**Gestión y Visualización de Datos Masivos**

Actividad de fundamentos: entender *por qué* existe el big data como disciplina antes de
tocar ninguna herramienta. Se responde a cuatro preguntas a partir de la bibliografía de la
asignatura.

## Qué pedía la actividad

Cuatro cuestiones teóricas, con lectura previa de Jacobs (2009) y de McCreary y Kelly (2014):
los problemas de las bases de datos tradicionales, ACID frente a BASE, qué motor NoSQL
conviene a cada aplicación y qué es NewSQL.

## Cómo se resolvió, paso a paso

### E1. Los problemas de las bases de datos tradicionales

Se parte del experimento de Jacobs: un censo ficticio de 6.750 millones de personas (100 GB)
que un programa secuencial procesa en 15 minutos y que PostgreSQL no consigue ni cargar;
un `GROUP BY` sobre mil millones de filas tarda más de 24 horas. De ahí salen cinco
patologías, cada una con su causa y su efecto:

1. **Es más fácil meter los datos que sacarlos** — los SGBD están diseñados para
   transaccionar, no para analizar. El optimizador llegó a ordenar mil millones de filas en
   lugar de agregarlas con una tabla hash.
2. **Inflación del almacenamiento** — la representación interna ocupa 3-4 veces lo necesario;
   la carga se abortó a las 6 horas con el disco lleno.
3. **Patrones de acceso no secuenciales** — el acceso aleatorio a disco es unas 150.000 veces
   más lento que el secuencial, lo que hace carísimos los joins entre tablas grandes y, en
   contra de la intuición relacional, aconseja desnormalizar.
4. **Límites duros del software** — herramientas que cargan todo en memoria o con topes
   arbitrarios (65.536 filas, índices de 32 bits).
5. **Costes de la distribución** — el nodo más lento marca el tiempo, hay que decidir si se
   particiona por tiempo o por entidad, y más nodos significan más averías y necesidad de
   replicar.

La conclusión es que las patologías del big data son de **análisis y de acceso**, no de CPU ni
de almacenamiento, y que el artículo anticipa la motivación de NoSQL, los motores
columnares y MapReduce.

### E2. ACID frente a BASE

Se definen los dos modelos, se contrastan (pesimista frente a optimista) y se explica el
compromiso con el **teorema CAP**: ante una partición de red hay que elegir entre
consistencia y disponibilidad. La conclusión práctica es que no sirven para lo mismo: ACID
cuando un dato incorrecto tiene un coste inaceptable (banca, stock, facturación), BASE cuando
es peor no responder que responder con un dato ligeramente antiguo (carritos, catálogos,
contadores, logs).

### E3. Qué motor NoSQL para cada aplicación

Se asigna familia de motor —clave-valor, documental, columnar o grafo— a cada caso de uso
planteado, justificando la elección por el patrón de acceso, no por la moda.

### E4. Qué es NewSQL

Se sitúa NewSQL como la tercera vía: garantías ACID distribuidas sobre arquitecturas que
escalan horizontalmente, y en qué se diferencia de NoSQL.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
