# GVDM10 — Bases de datos In-Memory I

**Gestión y Visualización de Datos Masivos** · Profesor Dr. Domingo Savio Rodríguez Baena

Primera de las dos actividades sobre motores en memoria: la parte conceptual y la puesta en
marcha. El benchmark viene en [GVDM14](../GVDM14-bd-in-memory-ii).

## Cómo se resolvió, paso a paso

### E1. Los límites reales de In-Memory OLTP

Resumen y valoración del artículo *«Why I don't (yet) recommend In-Memory OLTP to my
customers»* (Klaus Aschenbrenner, 2015). El autor reconoce que la tecnología es impresionante
y aun así no la recomienda, porque es una versión 1.0 con restricciones que sus clientes, que
deciden a cinco años vista, no pueden asumir: sin claves foráneas ni `CHECK`, sin cambios de
esquema (`ALTER TABLE` no admitido), sin planes de ejecución en los procedimientos compilados
de forma nativa, sin recompilaciones, con licencias Enterprise de unos 7.000 USD por núcleo y
una necesidad de RAM del doble del tamaño de las tablas.

La conclusión personal es que el patrón se repite con cada tecnología nueva: la limitación que
mata la adopción no suele ser la de rendimiento, sino la de integración con lo que ya existe.

### E2. *Main Memory Database Systems: An Overview*

Lectura del artículo clásico de García-Molina y Salem: qué cambia cuando se puede asumir que
los datos están en memoria —índices, control de concurrencia, recuperación, representación de
los datos— y por qué un MMDB no es «un SGBD de disco con mucha caché».

### E3. Caso de uso real: Axis Bank con Redis

Análisis de un despliegue real y de qué problema concreto resolvió la capa en memoria.

### E4. Activación del motor In-Memory de MongoDB

Puesta en marcha del motor `inMemory` (`--storageEngine inMemory --inMemorySizeGB`), que es
el que después se compara en GVDM14.

### E5. Instalación de Redis

Instalación y comprobación del servidor.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
