USE trafico;
CREATE TEMPORARY VIEW taxis_raw USING csv OPTIONS (path '/home/aramber/pt09/volumes/workspace/default/taxis/taxis.csv', header 'true', inferSchema 'true');
SELECT COUNT(*) filas_brutas, SUM(CASE WHEN passengers<=0 THEN 1 ELSE 0 END) pasajeros_0, SUM(CASE WHEN distance<=0 THEN 1 ELSE 0 END) distancia_0, SUM(CASE WHEN total<=0 THEN 1 ELSE 0 END) total_0 FROM taxis_raw;
DROP TABLE IF EXISTS taxis_limpios;
CREATE TABLE taxis_limpios STORED AS PARQUET AS
SELECT *, ROUND(tip / total * 100, 2) AS tip_pct
FROM taxis_raw
WHERE passengers > 0 AND distance > 0 AND total > 0;
SELECT COUNT(*) filas_limpias FROM taxis_limpios;
SELECT ROUND(100 * AVG(CASE WHEN tip_pct > 10 THEN 1 ELSE 0 END), 2) AS pct_viajes_propina_mas_10 FROM taxis_limpios;
SELECT hour(pickup) hora, ROUND(AVG(tip),2) propina_media_usd, ROUND(SUM(tip),2) propina_total_usd, COUNT(*) viajes FROM taxis_limpios GROUP BY hour(pickup) ORDER BY propina_media_usd DESC LIMIT 5;
SELECT hour(pickup) hora, ROUND(AVG(tip_pct),2) propina_media_pct, COUNT(*) viajes FROM taxis_limpios GROUP BY hour(pickup) ORDER BY propina_media_pct DESC LIMIT 5;
DROP TABLE IF EXISTS taxis_categoria;
CREATE TABLE taxis_categoria STORED AS PARQUET AS
SELECT *, CASE WHEN tip_pct > 20 THEN 'Generoso'
               WHEN tip_pct < 5 AND distance > 10 THEN 'Larga distancia poco Rentable'
               ELSE 'Normal' END AS categoria
FROM taxis_limpios;
SELECT categoria, COUNT(*) viajes FROM taxis_categoria GROUP BY categoria ORDER BY viajes DESC;
DROP TABLE IF EXISTS rutas;
CREATE TABLE rutas STORED AS PARQUET AS
SELECT pickup_zone AS origen, dropoff_zone AS destino, COUNT(*) AS num_viajes,
       ROUND(AVG(fare),2) AS tarifa_media, ROUND(AVG(distance),2) AS distancia_media,
       ROUND(AVG(fare)/AVG(distance),2) AS tarifa_por_milla
FROM taxis_limpios WHERE pickup_zone IS NOT NULL AND dropoff_zone IS NOT NULL
GROUP BY pickup_zone, dropoff_zone;
SELECT COUNT(*) rutas FROM rutas;
SELECT * FROM rutas WHERE num_viajes > 10 ORDER BY tarifa_por_milla DESC LIMIT 5;
SELECT * FROM rutas WHERE num_viajes > 10 ORDER BY tarifa_media DESC LIMIT 5
