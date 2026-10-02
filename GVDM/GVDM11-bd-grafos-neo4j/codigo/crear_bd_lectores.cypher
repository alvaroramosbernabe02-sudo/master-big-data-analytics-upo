// ============================================================
// GVDM11 – Bases de datos orientadas a grafos (Neo4j)
// Script de creación de la base de datos de la red de lectores
// GVDM11 - Álvaro Ramos Bernabé
// ============================================================

// 0) Limpieza (permite relanzar el script)
MATCH (n) DETACH DELETE n;

// 1) Restricciones de unicidad (crean además un índice)
CREATE CONSTRAINT persona_nombre IF NOT EXISTS FOR (p:Persona) REQUIRE p.nombre IS UNIQUE;
CREATE CONSTRAINT libro_id IF NOT EXISTS FOR (l:Libro) REQUIRE l.id IS UNIQUE;

// 2) Nodos Persona
CREATE (:Persona {nombre: 'Juan',     edad: 22}),
       (:Persona {nombre: 'María',    edad: 27}),
       (:Persona {nombre: 'Luisa',    edad: 32}),
       (:Persona {nombre: 'Alberto',  edad: 29}),
       (:Persona {nombre: 'Fernando', edad: 47});

// 3) Nodos Libro, Autor y Editorial
CREATE (l1:Libro {id: 1, titulo: 'El médico', anio: 2008}),
       (l2:Libro {id: 2, titulo: 'La pirámide inmortal', anio: 2015}),
       (a1:Autor {nombre: 'Noah Gordon'}),
       (a2:Autor {nombre: 'Javier Sierra'}),
       (e1:Editorial {nombre: 'Rocabolsillo'}),
       (e2:Editorial {nombre: 'Planeta'}),
       (l1)-[:ESCRITO_POR]->(a1),
       (l2)-[:ESCRITO_POR]->(a2),
       (l1)-[:PUBLICADO_POR]->(e1),
       (l2)-[:PUBLICADO_POR]->(e2);

// 4) Amistades (relación simétrica: se guarda una vez y se consulta sin dirección)
UNWIND [['María','Alberto'], ['María','Fernando'],
        ['Luisa','Alberto'], ['Luisa','Juan'],
        ['Juan','Alberto'],  ['Juan','Fernando']] AS par
MATCH (a:Persona {nombre: par[0]}), (b:Persona {nombre: par[1]})
CREATE (a)-[:AMIGO_DE]->(b);

// 5) Lecturas con fecha y valoración como propiedades de la relación
UNWIND [
  {p: 'Juan',     l: 1, fecha: '2015-02-16', val: 9},
  {p: 'María',    l: 1, fecha: '2015-07-15', val: 8},
  {p: 'Fernando', l: 2, fecha: '2015-04-08', val: 7},
  {p: 'Luisa',    l: 2, fecha: '2016-03-16', val: 9},
  {p: 'María',    l: 2, fecha: '2016-09-15', val: 8}
] AS r
MATCH (p:Persona {nombre: r.p}), (l:Libro {id: r.l})
CREATE (p)-[:HA_LEIDO {fecha: date(r.fecha), valoracion: r.val}]->(l);
