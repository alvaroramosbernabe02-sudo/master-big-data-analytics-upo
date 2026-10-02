USE trafico;
SELECT t.id, substr(e.nombre,1,45) nombre, COUNT(*) n, MAX(t.intensidad) maxi FROM trafico_dic2025 t INNER JOIN estaciones e ON t.id=e.id WHERE t.intensidad>20000 GROUP BY t.id, e.nombre ORDER BY n DESC
