# GVDM11 — Bases de datos orientadas a grafos (Neo4j)

**Gestión y Visualización de Datos Masivos** · Profesor Francisco A. Gómez Vela

## Cómo se resolvió, paso a paso

### A1. Comparativa de cuatro motores

| Motor | Qué lo define | Dónde flojea |
|---|---|---|
| **Neo4j** | Grafo de propiedades nativo con **adyacencia libre de índices**: cada nodo guarda punteros físicos a sus relaciones, así que un salto cuesta lo mismo con independencia del tamaño del grafo. Cypher (base del estándar ISO GQL) y ACID. | La edición Community se limita a un único servidor; clúster y escalado horizontal son Enterprise o AuraDB. |
| **Azure Cosmos DB (Gremlin)** | Servicio gestionado, multimodelo y distribuido globalmente, con SLA de latencia y varios niveles de consistencia. | Las consultas que cruzan particiones y los recorridos de muchos saltos son lentos y caros: se facturan en RU. Sólo existe en Azure. |
| **ArangoDB** | Multimodelo nativo (documentos, clave-valor y grafos) con un único lenguaje, AQL, que combina joins, texto y recorridos. | En recorridos muy profundos no alcanza a un motor nativo. |
| **OrientDB** | Multimodelo con punteros físicos (RID) entre registros, recorridos rápidos. | Comunidad y mantenimiento decaídos tras su adquisición por SAP; su creador impulsa ArcadeDB. Arriesgado para proyectos nuevos. |

En síntesis: Neo4j para análisis de redes y recorridos profundos, Cosmos DB cuando pesa más
el servicio gestionado global, ArangoDB para cargas mixtas.

### A2. Descarga e instalación de Neo4j

Instalación local y arranque del navegador de Neo4j.

### A3. Red social de lectores

1. **Modelo de datos** — nodos de personas y libros, relaciones de amistad, de lectura y de
   valoración; se justifica qué va como nodo, qué como relación y qué como propiedad, que es
   la decisión de diseño que de verdad importa en un grafo.
2. **Consultas en Cypher** — creación de la base (`crear_bd_lectores.cypher`) y batería de
   consultas (`consultas.cypher`): recomendaciones por amigos en común, caminos entre
   lectores, libros más valorados dentro de un círculo, etc.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/crear_bd_lectores.cypher` | Creación del grafo de la red de lectores |
| `codigo/consultas.cypher` | Consultas Cypher de la A3 |
