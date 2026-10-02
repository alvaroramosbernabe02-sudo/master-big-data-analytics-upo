// Consulta 1: ¿Quiénes leyeron el libro #2?
MATCH (p:Persona)-[r:HA_LEIDO]->(l:Libro {id: 2})
RETURN p.nombre AS lector, r.fecha AS fecha, r.valoracion AS valoracion
ORDER BY r.fecha;

// Consulta 2: ¿Cuál es la valoración promedio del libro #1?
MATCH (:Persona)-[r:HA_LEIDO]->(l:Libro {id: 1})
RETURN l.titulo AS libro, avg(r.valoracion) AS valoracion_media, count(r) AS num_valoraciones;

// Consulta 3: ¿Quién es el usuario de mayor edad?
MATCH (p:Persona)
RETURN p.nombre AS nombre, p.edad AS edad
ORDER BY p.edad DESC
LIMIT 1;
