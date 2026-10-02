import os
import pandas as pd
import matplotlib.pyplot as plt
from langchain_core.tools import tool
from typing import Dict


PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


@tool("plot_scatter")
def plot_scatter(dataset_name: str, column_x: str, column_y: str) -> Dict[str, str]:
    """Genera un scatterplot para dos columnas numéricas."""
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')[[column_x, column_y]].dropna()
    except Exception as e:
        return {"error": str(e)}

    output_path = f"{PLOTS_DIR}/{dataset_name}_{column_x}_{column_y}_scatter.png"
    plt.figure(figsize=(7, 5))
    plt.scatter(data[column_x], data[column_y], alpha=0.7)
    plt.title(f"Scatterplot de {column_x} vs {column_y}")
    plt.xlabel(column_x)
    plt.ylabel(column_y)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return {"plot_path": output_path}


@tool("plot_heatmap")
def plot_heatmap(dataset_name: str, column_x: str, column_y: str) -> Dict[str, str]:
    """
    Genera un heatmap de frecuencias (tabla de contingencia) entre dos columnas categóricas.
    Usar cuando el usuario quiere ver cómo se combinan o relacionan dos variables de texto.
    dataset_name: nombre del dataset (sin extensión), p. ej. 'sales_data' o 'customer_data'.
    column_x: columna categórica para el eje X, p. ej. 'product', 'segment'.
    column_y: columna categórica para el eje Y, p. ej. 'region', 'churn'.
    Nunca uses columnas numéricas (sales, profit, income) como column_x o column_y.
    """
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')[[column_x, column_y]].dropna()
    except Exception as e:
        return {"error": str(e)}

    contingency = pd.crosstab(data[column_y], data[column_x])
    output_path = f"{PLOTS_DIR}/{dataset_name}_{column_x}_{column_y}_heatmap.png"
    fig, ax = plt.subplots(figsize=(max(5, len(contingency.columns) * 1.2),
                                    max(4, len(contingency.index) * 0.9)))
    im = ax.imshow(contingency, cmap="Blues", interpolation="nearest")
    ax.set_xticks(range(len(contingency.columns)))
    ax.set_xticklabels(contingency.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(contingency.index)))
    ax.set_yticklabels(contingency.index)
    for i in range(len(contingency.index)):
        for j in range(len(contingency.columns)):
            ax.text(j, i, str(contingency.iloc[i, j]),
                    ha="center", va="center", fontsize=10, fontweight="bold")
    plt.colorbar(im, ax=ax, label="Frecuencia")
    ax.set_title(f"Frecuencias: {column_x} × {column_y}")
    ax.set_xlabel(column_x)
    ax.set_ylabel(column_y)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return {"plot_path": output_path}


@tool("plot_boxplot_by_category")
def plot_boxplot_by_category(dataset_name: str, categorical_column: str, numeric_column: str) -> Dict[str, str]:
    """
    Genera un boxplot de una variable numérica agrupada por una variable categórica.
    Usar cuando el usuario pide comparar o visualizar una magnitud numérica según
    grupos, categorías o etiquetas, como ventas por región, beneficio por producto,
    ingresos por segmento, etc.
    categorical_column debe ser una columna de texto o etiquetas (ej. region, product, segment).
    numeric_column debe ser una columna numérica (ej. sales, profit, income).
    """
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')[[categorical_column, numeric_column]].dropna()
    except Exception as e:
        return {"error": str(e)}

    output_path = f"{PLOTS_DIR}/{dataset_name}_{categorical_column}_{numeric_column}_boxplot.png"
    plt.figure(figsize=(8, 5))
    data.boxplot(column=numeric_column, by=categorical_column)
    plt.title(f"{numeric_column} por {categorical_column}")
    plt.suptitle("")
    plt.xlabel(categorical_column)
    plt.ylabel(numeric_column)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return {"plot_path": output_path}
