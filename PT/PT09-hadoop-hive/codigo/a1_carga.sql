CREATE DATABASE IF NOT EXISTS trafico;
USE trafico;
-- tabla externa sobre el CSV original (formato Hive: delimitado por ';')
CREATE TEMPORARY VIEW v_dic USING csv OPTIONS (path '/home/aramber/pt09/data/12-2025.csv', header 'true', sep ';', inferSchema 'false');
DROP TABLE IF EXISTS trafico_dic2025;
CREATE TABLE trafico_dic2025 STORED AS PARQUET AS
SELECT CAST(id AS BIGINT) id, CAST(fecha AS TIMESTAMP) fecha, tipo_elem, CAST(intensidad AS BIGINT) intensidad,
       CAST(ocupacion AS BIGINT) ocupacion, CAST(carga AS BIGINT) carga, CAST(vmed AS DOUBLE) vmed, error,
       CAST(periodo_integracion AS BIGINT) periodo_integracion FROM v_dic;
CREATE TEMPORARY VIEW v_pmed USING csv OPTIONS (path '/home/aramber/pt09/data/pmed_ubicacion.csv', header 'true', sep ';', encoding 'ISO-8859-1');
DROP TABLE IF EXISTS estaciones;
CREATE TABLE estaciones STORED AS PARQUET AS
SELECT CAST(id AS BIGINT) id, tipo_elem, CAST(distrito AS INT) distrito, cod_cent, nombre, CAST(latitud AS DOUBLE) latitud, CAST(longitud AS DOUBLE) longitud FROM v_pmed;
SHOW TABLES;
DESCRIBE trafico_dic2025;
SELECT COUNT(*) filas, MIN(fecha) desde, MAX(fecha) hasta, COUNT(DISTINCT id) puntos FROM trafico_dic2025;
SELECT COUNT(*) estaciones FROM estaciones
