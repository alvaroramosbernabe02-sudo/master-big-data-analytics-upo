-- Evaluación sobre datos no vistos y comparación del perfil horario
SELECT ROUND(mean_absolute_error,2) AS mae, ROUND(mean_squared_error,1) AS mse, ROUND(r2_score,4) AS r2
FROM ML.EVALUATE(MODEL pt08.modelo_automl_bicis, (SELECT * FROM pt08.bike_test));

SELECT hr AS hora, ROUND(AVG(cnt),1) AS real_medio, ROUND(AVG(predicted_cnt),1) AS prediccion_media
FROM ML.PREDICT(MODEL pt08.modelo_automl_bicis, (SELECT * FROM pt08.bike_test))
GROUP BY hr ORDER BY hr;
