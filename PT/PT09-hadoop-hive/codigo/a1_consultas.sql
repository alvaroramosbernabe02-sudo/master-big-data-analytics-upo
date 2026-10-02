USE trafico;
-- A1.1 fechas/horas con intensidad > 20.000 y estación medidora (INNER JOIN)
SELECT t.fecha, t.id, e.nombre, t.tipo_elem, t.intensidad
FROM trafico_dic2025 t INNER JOIN estaciones e ON t.id = e.id
WHERE t.intensidad > 20000
ORDER BY t.intensidad DESC;
-- A1.2 media de intensidad por mes de cada estación
SELECT e.id, e.nombre, date_format(t.fecha,'yyyy-MM') mes, ROUND(AVG(t.intensidad),1) media_intensidad
FROM trafico_dic2025 t INNER JOIN estaciones e ON t.id = e.id
WHERE t.error = 'N'
GROUP BY e.id, e.nombre, date_format(t.fecha,'yyyy-MM')
ORDER BY media_intensidad DESC;
-- A1.3 número de puntos (registros) de medición por estación
SELECT id, COUNT(*) puntos_medicion FROM trafico_dic2025 GROUP BY id ORDER BY puntos_medicion ASC;
SELECT puntos_medicion, COUNT(*) n_estaciones FROM (SELECT id, COUNT(*) puntos_medicion FROM trafico_dic2025 GROUP BY id) GROUP BY puntos_medicion ORDER BY n_estaciones DESC;
SELECT COUNT(*) estaciones_con_menos_de_2976 FROM (SELECT id, COUNT(*) n FROM trafico_dic2025 GROUP BY id) WHERE n < 31*96;
-- A1.4 tabla retenciones_diciembre (ocupación > 90 %)
DROP TABLE IF EXISTS retenciones_diciembre;
CREATE TABLE retenciones_diciembre STORED AS PARQUET AS
SELECT t.id, e.nombre, t.fecha, t.intensidad, t.ocupacion
FROM trafico_dic2025 t INNER JOIN estaciones e ON t.id = e.id
WHERE t.ocupacion > 90;
SELECT COUNT(*) filas, COUNT(DISTINCT id) estaciones FROM retenciones_diciembre;
-- A1.5 estaciones con más instantes de ocupación > 90 %
SELECT id, nombre, COUNT(*) instantes_ocupacion_90 FROM retenciones_diciembre
GROUP BY id, nombre ORDER BY instantes_ocupacion_90 DESC LIMIT 10
