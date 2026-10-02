CREATE OR REPLACE MODEL pt12.modelo_retraso
OPTIONS (model_type = 'BOOSTED_TREE_CLASSIFIER', input_label_cols = ['retraso'],
         data_split_method = 'RANDOM', data_split_eval_fraction = 0.2,
         max_iterations = 30, auto_class_weights = TRUE) AS
SELECT * EXCEPT(fecha) FROM pt12.vuelos_limpios;
