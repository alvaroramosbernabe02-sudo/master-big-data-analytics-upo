-- Guardar resultados: predicción por vuelo y KPIs agregados para el cuadro de mando
CREATE OR REPLACE TABLE pt12.predicciones AS
SELECT fecha, aerolinea, origen, destino, hora_salida, retraso AS retraso_real,
       predicted_retraso AS retraso_predicho,
       (SELECT prob FROM UNNEST(predicted_retraso_probs) WHERE label = 1) AS prob_retraso
FROM ML.PREDICT(MODEL pt12.modelo_retraso, (SELECT * FROM pt12.vuelos_limpios));
CREATE OR REPLACE TABLE pt12.kpi_aerolinea AS
SELECT aerolinea, COUNT(*) AS vuelos, ROUND(AVG(retraso_real) * 100, 1) AS pct_retraso_real,
       ROUND(AVG(prob_retraso) * 100, 1) AS pct_retraso_previsto
FROM pt12.predicciones GROUP BY aerolinea ORDER BY pct_retraso_real DESC;
SELECT * FROM pt12.kpi_aerolinea;
