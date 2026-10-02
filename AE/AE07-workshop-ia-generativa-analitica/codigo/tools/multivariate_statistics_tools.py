import pandas as pd
from langchain_core.tools import tool
from typing import Any, Dict


@tool("basic_statistics_numeric_numeric")
def basic_statistics_numeric_numeric(dataset_name: str, column_x: str, column_y: str) -> Dict[str, Any]:
    """
    Calcula estadísticos básicos para dos columnas numéricas.
    
    Args:
        dataset_name: Nombre del dataset (sin extensión .csv)
        column_x: Nombre de la primera columna numérica
        column_y: Nombre de la segunda columna numérica
        
    Returns:
        Diccionario con estadísticos bivariantes básicos
    """
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')[[column_x, column_y]].dropna()
    except Exception as e:
        return {"error": str(e)}

    stats = {
        'count': len(data),
        'pearson_correlation': float(data[column_x].corr(data[column_y])),
        'covariance': float(data[column_x].cov(data[column_y]))
    }

    return stats


@tool("basic_statistics_categorical_numeric")
def basic_statistics_categorical_numeric(dataset_name: str, categorical_column: str, numeric_column: str) -> Dict[str, Any]:
    """
    Calcula estadísticos básicos de una variable numérica agrupada por una variable categórica.
    
    Args:
        dataset_name: Nombre del dataset (sin extensión .csv)
        categorical_column: Nombre de la columna categórica
        numeric_column: Nombre de la columna numérica
        
    Returns:
        Diccionario con estadísticos por categoría
    """
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')[[categorical_column, numeric_column]].dropna()
    except Exception as e:
        return {"error": str(e)}

    grouped = data.groupby(categorical_column)[numeric_column]

    stats = grouped.agg(['count', 'mean', 'median', 'min', 'max', 'std']).round(4).to_dict('index')
    return stats


@tool("basic_statistics_categorical_categorical")
def basic_statistics_categorical_categorical(dataset_name: str, column_x: str, column_y: str) -> Dict[str, Any]:
    """
    Calcula estadísticos básicos para dos columnas categóricas.
    
    Args:
        dataset_name: Nombre del dataset (sin extensión .csv)
        column_x: Nombre de la primera columna categórica
        column_y: Nombre de la segunda columna categórica
        
    Returns:
        Diccionario con tabla de contingencia y frecuencias relativas
    """
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')[[column_x, column_y]].dropna()
    except Exception as e:
        return {"error": str(e)}

    contingency_table = pd.crosstab(data[column_x], data[column_y])
    relative_table = pd.crosstab(data[column_x], data[column_y], normalize='all').round(4)

    stats = {
        'count': len(data),
        'contingency_table': contingency_table.to_dict(),
        'relative_frequencies': relative_table.to_dict()
    }

    return stats
