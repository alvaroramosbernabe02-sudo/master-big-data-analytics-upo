USE trafico;
DROP TABLE IF EXISTS retenciones_diciembre;
CREATE TABLE retenciones_diciembre STORED AS PARQUET AS
SELECT t.id, substr(e.nombre,1,45) nombre, t.fecha, t.intensidad, t.ocupacion
FROM trafico_dic2025 t INNER JOIN estaciones e ON t.id = e.id
WHERE t.ocupacion > 90;
SELECT * FROM retenciones_diciembre LIMIT 5;
SELECT COUNT(*) filas, COUNT(DISTINCT id) estaciones FROM retenciones_diciembre;
SELECT id, nombre, COUNT(*) instantes_ocupacion_90 FROM retenciones_diciembre
GROUP BY id, nombre ORDER BY instantes_ocupacion_90 DESC LIMIT 10
