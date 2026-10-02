-- 80 % entrenamiento / 20 % test, reparto determinista por hash de la clave
CREATE OR REPLACE TABLE pt08.bike_train AS
SELECT * EXCEPT(instant, casual, registered) FROM pt08.bike_hour
WHERE MOD(ABS(FARM_FINGERPRINT(CAST(instant AS STRING))), 10) < 8;
CREATE OR REPLACE TABLE pt08.bike_test AS
SELECT * EXCEPT(instant, casual, registered) FROM pt08.bike_hour
WHERE MOD(ABS(FARM_FINGERPRINT(CAST(instant AS STRING))), 10) >= 8;
SELECT 'train' AS conjunto, COUNT(*) AS filas FROM pt08.bike_train UNION ALL SELECT 'test', COUNT(*) FROM pt08.bike_test;
