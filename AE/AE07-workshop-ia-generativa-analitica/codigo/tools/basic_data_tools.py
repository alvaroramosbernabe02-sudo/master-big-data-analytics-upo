import pandas as pd
from langchain_core.tools import tool
from typing import Any, Dict

@tool("get_dataset_summary")
def get_dataset_summary(dataset_name: str) -> str:
    """Obtiene un resumen de un dataset: número de registros y columnas disponibles."""
    try:
        df = pd.read_csv(f'data/{dataset_name}.csv')
        return f"Dataset: {dataset_name}, {len(df)} registros, columnas: {', '.join(df.columns.tolist())}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool("count_records")
def count_records(dataset_name: str) -> str:
    """Cuenta el número de registros de un dataset."""
    try:
        df = pd.read_csv(f'data/{dataset_name}.csv')
        return f"{len(df)} registros"
    except Exception as e:
        return f"Error: {str(e)}"

@tool("resolve_business_metric")
def resolve_business_metric(metric_name: str) -> Dict[str, Any]:
    """
    Inspecciona las columnas de los datasets y devuelve la coincidencia más simple.

    Args:
        metric_name: Nombre del concepto o métrica solicitada por el usuario

    Returns:
        Diccionario con dataset y columna
    """
    metric = metric_name.strip().lower().replace("_", " ")
    dataset_files = {
        "customer_data": "data/customer_data.csv",
        "sales_data": "data/sales_data.csv",
        "marketing_campaign": "data/marketing_campaign.csv"
    }

    synonyms = {
        "ingresos": "income",
        "ingresos de clientes": "income",
        "ventas": "sales",
        "beneficio": "profit",
        "edad": "age",
        "gasto total": "total_spent"
    }

    target = synonyms.get(metric, metric)

    for dataset_name, file_path in dataset_files.items():
        try:
            columns = pd.read_csv(file_path, nrows=0).columns.tolist()
        except Exception:
            continue

        for column in columns:
            normalized_column = column.lower().replace("_", " ")
            if target == normalized_column:
                return {"dataset_name": dataset_name, "column": column}

    return {"error": f"No se pudo resolver la métrica: {metric_name}"}
