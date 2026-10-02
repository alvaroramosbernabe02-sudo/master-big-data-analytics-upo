import pandas as pd
from langchain_core.tools import tool
from typing import Any, Dict
import numpy as np



@tool("basic_statistics_numeric")
def basic_statistics_numeric (dataset_name: str, column: str) -> Dict[str,Any]:
    """
    Calcula estadísticos básicos para una columna numérica.
    
    Args:
        dataset_name: Nombre del dataset (sin extensión .csv)
        column: Nombre de la columna numérica
        
    Returns:
        Diccionario con estadísticos básicos
    """
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')
        data = data[column].dropna()
    except Exception as e:
        return {"error": str(e)}

    
    stats = {
        'count': len(data),
        'mean': float(data.mean()),
        'median': float(data.median()),
        'mode': float(data.mode()[0]) if len(data.mode()) > 0 else None,
        'std': float(data.std()),
        'variance': float(data.var()),
        'min': float(data.min()),
        'max': float(data.max()),
        'q1': float(data.quantile(0.25)),
        'q3': float(data.quantile(0.75)),
        'iqr': float(data.quantile(0.75) - data.quantile(0.25)),
        'skewness': float(data.skew()),
        'kurtosis': float(data.kurtosis())
    }
    
    return stats

@tool("basic_statistics_categorical")
def basic_statistics_categorical (dataset_name: str, column: str) -> Dict[str,Any]:
    """
    Calcula estadísticos básicos para una columna numérica.
    
    Args:
        dataset_name: Nombre del dataset (sin extensión .csv)
        column: Nombre de la columna numérica
        
    Returns:
        Diccionario con estadísticos básicos
    """
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')
        data = data[column].dropna().astype(str)
    except Exception as e:
        return {"error": str(e)}

    
    value_counts = data.value_counts()

    stats = {
        'count': len(data),
        'unique_count': int(data.nunique()),
        'mode': data.mode().iloc[0] if not data.mode().empty else None,
        'empty_strings': int((data.str.strip() == '').sum()),
        'top_5_values': value_counts.head(5).to_dict(),
        'category_counts': value_counts.to_dict(),
        'top_category_count': int(value_counts.iloc[0]) if not value_counts.empty else 0,
        'top_category_ratio': float(value_counts.iloc[0] / len(data)) if not value_counts.empty else 0.0
    }
    
    return stats

