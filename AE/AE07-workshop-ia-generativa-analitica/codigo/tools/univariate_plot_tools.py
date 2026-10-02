import os
import pandas as pd
import matplotlib.pyplot as plt
from langchain_core.tools import tool
from typing import Dict


PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


@tool("plot_histogram")
def plot_histogram(dataset_name: str, column: str) -> Dict[str, str]:
    """Genera un histograma para una columna numérica."""
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')[column].dropna()
    except Exception as e:
        return {"error": str(e)}

    output_path = f"{PLOTS_DIR}/{dataset_name}_{column}_histogram.png"
    plt.figure(figsize=(8, 5))
    plt.hist(data, bins=20, edgecolor="black")
    plt.title(f"Histograma de {column}")
    plt.xlabel(column)
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return {"plot_path": output_path}


@tool("plot_boxplot")
def plot_boxplot(dataset_name: str, column: str) -> Dict[str, str]:
    """Genera un boxplot para una columna numérica."""
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')[column].dropna()
    except Exception as e:
        return {"error": str(e)}

    output_path = f"{PLOTS_DIR}/{dataset_name}_{column}_boxplot.png"
    plt.figure(figsize=(6, 4))
    plt.boxplot(data)
    plt.title(f"Boxplot de {column}")
    plt.ylabel(column)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return {"plot_path": output_path}


@tool("plot_barplot")
def plot_barplot(dataset_name: str, column: str) -> Dict[str, str]:
    """Genera un barplot para una columna categórica."""
    try:
        data = pd.read_csv(f'data/{dataset_name}.csv')[column].dropna().astype(str)
    except Exception as e:
        return {"error": str(e)}

    counts = data.value_counts().head(10)
    output_path = f"{PLOTS_DIR}/{dataset_name}_{column}_barplot.png"
    plt.figure(figsize=(8, 5))
    counts.plot(kind="bar")
    plt.title(f"Barplot de {column}")
    plt.xlabel(column)
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return {"plot_path": output_path}
