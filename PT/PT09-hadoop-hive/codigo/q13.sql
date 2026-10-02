USE trafico;
SELECT id, COUNT(*) puntos_medicion FROM trafico_dic2025 GROUP BY id ORDER BY puntos_medicion ASC;
WITH c AS (SELECT id, COUNT(*) n FROM trafico_dic2025 GROUP BY id)
SELECT MAX(n) maximo, MIN(n) minimo, ROUND(AVG(n),1) media,
       SUM(CASE WHEN n < (SELECT MAX(n) FROM c) THEN 1 ELSE 0 END) estaciones_con_menos,
       COUNT(*) total_estaciones FROM c
