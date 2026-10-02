USE trafico;
SELECT t.fecha, t.id, substr(e.nombre,1,45) nombre, t.intensidad, t.error
FROM trafico_dic2025 t INNER JOIN estaciones e ON t.id = e.id
WHERE t.intensidad > 20000
ORDER BY t.fecha;
SELECT COUNT(*) registros, COUNT(DISTINCT t.id) estaciones
FROM trafico_dic2025 t INNER JOIN estaciones e ON t.id = e.id WHERE t.intensidad > 20000
