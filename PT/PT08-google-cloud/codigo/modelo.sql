CREATE OR REPLACE MODEL pt08.modelo_automl_bicis
OPTIONS (model_type = 'AUTOML_REGRESSOR',
         input_label_cols = ['cnt'],
         budget_hours = 1.0,
         optimization_objective = 'MINIMIZE_RMSE') AS
SELECT * EXCEPT(dteday) FROM pt08.bike_train;
