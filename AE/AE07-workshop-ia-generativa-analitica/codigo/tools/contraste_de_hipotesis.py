import pandas as pd
from langchain_core.tools import tool
from typing import Any, Dict


@tool("chi_square_test")
def chi_square_test(dataset_name: str, column_x: str, column_y: str) -> Dict[str, Any]:
    """
    Realiza una prueba chi-cuadrado de independencia entre dos variables categóricas.
    
    Args:
        dataset_name: Nombre del dataset (sin extensión .csv)
        column_x: Nombre de la primera columna categórica
        column_y: Nombre de la segunda columna categórica
        
    Returns:
        Diccionario con el resultado del test
    """
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')[[column_x, column_y]].dropna()
    except Exception as e:
        return {"error": str(e)}

    try:
        from scipy.stats import chi2_contingency
    except ImportError:
        return {"error": "scipy no está instalado"}

    contingency_table = pd.crosstab(data[column_x], data[column_y])
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    conclusion = "Las variables no son independientes" if p_value < 0.05 else "Las variables son independientes"

    return {
        'count': len(data),
        'chi2': float(chi2),
        'p_value': float(p_value),
        'degrees_of_freedom': int(dof),
        'expected_frequencies': expected.tolist(),
        'conclusion': conclusion
    }
