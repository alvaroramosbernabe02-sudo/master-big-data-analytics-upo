USE trafico;
DROP TABLE IF EXISTS traficonov2019;
-- equivalente Spark SQL de read_files('/Volumes/workspace/default/pruebavolumen/11-2019.csv', format=>'csv', sep=>';', header=>true)
CREATE TEMPORARY VIEW read_files_nov USING csv OPTIONS (path '/home/aramber/pt09/volumes/workspace/default/pruebavolumen/11-2019.csv', format 'csv', sep ';', header 'true', inferSchema 'true');
CREATE TABLE traficonov2019 STORED AS PARQUET
AS SELECT * FROM read_files_nov;
SELECT * FROM traficonov2019 LIMIT 3;
SELECT COUNT(*) filas FROM traficonov2019;
DROP TABLE IF EXISTS datos_dicnov;
CREATE TABLE datos_dicnov STORED AS PARQUET AS
SELECT CAST(id AS BIGINT) id, CAST(fecha AS TIMESTAMP) fecha, CAST(intensidad AS BIGINT) intensidad, CAST(ocupacion AS BIGINT) ocupacion FROM traficonov2019
UNION ALL
SELECT id, fecha, intensidad, ocupacion FROM trafico_dic2025;
SELECT date_format(fecha,'yyyy-MM') mes, COUNT(*) filas, COUNT(DISTINCT id) estaciones, ROUND(AVG(intensidad),1) intensidad_media
FROM datos_dicnov GROUP BY date_format(fecha,'yyyy-MM') ORDER BY mes
