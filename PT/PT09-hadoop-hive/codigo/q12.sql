USE trafico;
SELECT e.id, e.nombre, date_format(t.fecha,'yyyy-MM') mes, ROUND(AVG(t.intensidad),1) media_intensidad
FROM trafico_dic2025 t INNER JOIN estaciones e ON t.id = e.id
WHERE t.error = 'N'
GROUP BY e.id, e.nombre, date_format(t.fecha,'yyyy-MM')
ORDER BY media_intensidad DESC
