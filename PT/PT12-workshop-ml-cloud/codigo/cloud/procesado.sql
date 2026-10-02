-- Zona "curada": solo vuelos operados, variables conocidas antes del despegue y etiqueta de retraso (> 15 min)
CREATE OR REPLACE TABLE pt12.vuelos_limpios AS
SELECT
  FlightDate AS fecha, EXTRACT(DAYOFWEEK FROM FlightDate) AS dia_semana, DayofMonth AS dia_mes,
  Reporting_Airline AS aerolinea, Origin AS origen, Dest AS destino,
  DIV(CAST(CRSDepTime AS INT64), 100) AS hora_salida, CAST(Distance AS FLOAT64) AS distancia,
  CAST(CRSElapsedTime AS FLOAT64) AS duracion_programada,
  IF(CAST(ArrDelay AS FLOAT64) > 15, 1, 0) AS retraso
FROM pt12.ontime_raw
WHERE Cancelled = 0 AND Diverted = 0 AND ArrDelay IS NOT NULL;
