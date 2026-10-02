# PT10 — Ingesta de datos en cloud con Apache Kafka

**Plataformas Tecnológicas** · Profesor D. Alejandro Gómez Morón

## Preguntas

### 1. ¿Es 3 siempre el factor de replicación ideal?

No: es un compromiso entre durabilidad, disponibilidad, coste y latencia. RF = 3 es el valor
recomendado por defecto porque, combinado con `min.insync.replicas=2` y `acks=all`, permite
perder un broker sin detener la escritura ni perder mensajes confirmados. Pero:

| Situación | RF | Motivo |
|---|---|---|
| Desarrollo o clúster de 1 nodo | 1 | No hay más brokers; replicar sólo consume disco |
| Datos regenerables o de bajo valor | 1-2 | Prima el coste; perder datos es tolerable |
| Producción estándar | 3 | Tolera la caída de 1 broker o 1 zona manteniendo escrituras |
| Datos críticos o multi-AZ | 4-5 | Tolera 2 fallos simultáneos, o mantenimiento más fallo |
| Servicios gestionados | Fijado por el proveedor | La durabilidad la cubre el SLA |

### 2. ¿Cómo se cambia el factor de replicación?

Procedimiento con el plan de reasignación de particiones.

### 3. Diseño: miniatura y metadatos de cada fotografía

Propuesta de arquitectura de ingesta para el caso planteado.

## Ejercicios

### E1. Productor y consumidor del ejemplo de clase

Se ejecuta el par productor/consumidor, se describe el flujo y qué salida se obtiene, y se
razona si el patrón es **batching o streaming**.

### E2. Dos productores, dos topics y un consumidor

Dos productores independientes (`producer_lotr.py` y `producer_starwars.py`) escriben en
topics distintos y un único consumidor los lee. Se explica qué frases aparecen en el consumidor
y, sobre todo, **por qué** salen en ese orden: el entrelazado depende del reparto de
particiones y del momento de publicación, no de la secuencia en que se lanzaron los
productores.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/ej1/producer.py`, `codigo/ej1/consumer.py` | Ejercicio 1 |
| `codigo/ej2/producer_lotr.py`, `codigo/ej2/producer_starwars.py`, `codigo/ej2/consumer.py` | Ejercicio 2: dos topics, un consumidor |
