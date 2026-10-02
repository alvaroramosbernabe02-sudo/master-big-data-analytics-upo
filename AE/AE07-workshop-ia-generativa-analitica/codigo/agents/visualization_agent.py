from agents._llm import get_llm
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
import os
from tools.univariate_plot_tools import plot_boxplot, plot_histogram, plot_barplot
from tools.multivariate_plot_tools import plot_scatter, plot_heatmap, plot_boxplot_by_category
from tools.basic_data_tools import resolve_business_metric


DESCRIPTION = "Visualización de datos con gráficos simples"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")


def create_agent():

    llm = get_llm()

    tool_map = {
        "resolve_business_metric": resolve_business_metric,
        "plot_histogram": plot_histogram,
        "plot_boxplot": plot_boxplot,
        "plot_barplot": plot_barplot,
        "plot_scatter": plot_scatter,
        "plot_heatmap": plot_heatmap,
        "plot_boxplot_by_category": plot_boxplot_by_category
    }

    llm_with_tools = llm.bind_tools(list(tool_map.values()))

    system_prompt = """
        Eres un analista de datos experto en visualización. Tienes acceso a distintos datasets de negocio y a varias herramientas de gráficos.

        Datasets disponibles y columnas relevantes:
        - customer_data: age, income, purchases, avg_purchase_value, total_spent, days_since_last_purchase, churn, segment
        - sales_data: date, region, product, sales, quantity, customer_id, profit
        - marketing_campaign: (campañas de marketing)

        === REGLAS ===

        1. Usa siempre herramientas para generar gráficos reales.
        2. No inventes datos ni rutas.
        3. Responde en español, de forma breve y natural.
        4. Si se genera un gráfico, la respuesta final debe ser solo el diccionario devuelto por la tool que contiene plot_path.
        5. No conviertas ese resultado en una frase.
        6. Si hacen falta varias herramientas, combínalas.

        === SELECCIÓN DE HERRAMIENTA ===

        - Distribución de una única variable numérica → plot_histogram o plot_boxplot
        - Distribución de una única variable categórica → plot_barplot
        - Relación entre dos variables numéricas → plot_scatter
        - Relación entre dos variables categóricas → plot_heatmap
          · column_x = primera columna categórica (product, segment, region, churn)
          · column_y = segunda columna categórica (region, product, segment, churn)
          · NUNCA pases columnas numéricas (sales, profit, income) a plot_heatmap
        - Variable numérica comparada por grupos o categorías → plot_boxplot_by_category
          · categorical_column = columna de texto (region, product, segment)
          · numeric_column = columna numérica (sales, profit, income)
        - Usa plot_boxplot solo cuando hay una única variable numérica sin agrupación.
        - Usa plot_boxplot_by_category cuando la consulta mencione "por región", "por producto", "por segmento" o cualquier agrupación.
        - Si el usuario habla de un concepto de negocio y no de una columna, usa resolve_business_metric primero.
        """

    def run(pregunta: str) -> str:
        MAX_STEPS = 5

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=pregunta)
        ]

        all_plot_results = []

        for _ in range(MAX_STEPS):
            response = llm_with_tools.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
                # El LLM ya no llama más herramientas: devolvemos lo acumulado
                if all_plot_results:
                    return str(all_plot_results) if len(all_plot_results) > 1 else str(all_plot_results[0])
                return str(response.content)

            for tc in response.tool_calls:
                resultado = tool_map[tc["name"]].invoke(tc["args"])
                print(f"[TOOL] {tc['name']} → args: {tc['args']}")
                messages.append(
                    ToolMessage(
                        content=str(resultado),
                        tool_call_id=tc["id"]
                    )
                )
                if isinstance(resultado, dict) and "plot_path" in resultado:
                    all_plot_results.append(resultado)

            # Nunca cortamos el bucle aquí: dejamos que el LLM decida si
            # necesita llamar a más herramientas o si ya ha terminado.

        # Si agotamos los pasos con plots pendientes, los devolvemos
        if all_plot_results:
            return str(all_plot_results) if len(all_plot_results) > 1 else str(all_plot_results[0])

        final = llm.invoke(messages)
        return str(final.content)

    return {
        "run": run
    }
