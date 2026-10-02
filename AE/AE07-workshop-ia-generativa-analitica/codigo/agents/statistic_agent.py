from agents._llm import get_llm
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage
import os
from tools.univariate_statistics_tools import basic_statistics_numeric, basic_statistics_categorical
from tools.multivariate_statistics_tools import basic_statistics_numeric_numeric, basic_statistics_categorical_numeric, basic_statistics_categorical_categorical
from tools.basic_data_tools import resolve_business_metric
from tools.contraste_de_hipotesis import chi_square_test


DESCRIPTION = "Consultas estadísticas de los datos"

GROQ_API_KEY = os.getenv("GROQ_API_KEY","")

def create_agent():

    llm = get_llm()

    tool_map = {
        "resolve_business_metric": resolve_business_metric,
        "basic_statistics_categorical": basic_statistics_categorical,
        "basic_statistics_numeric": basic_statistics_numeric,
        "basic_statistics_numeric_numeric": basic_statistics_numeric_numeric,
        "basic_statistics_categorical_numeric": basic_statistics_categorical_numeric,
        "basic_statistics_categorical_categorical": basic_statistics_categorical_categorical,
        "chi_square_test": chi_square_test,
    }

    llm_with_tools = llm.bind_tools(list(tool_map.values()))

    system_prompt = """
        Eres un analista de datos experto. Tienes acceso a distintos datasets de negocio y a varias herramientas de análisis.

        Datasets disponibles y columnas relevantes:
        - customer_data: age, income, purchases, avg_purchase_value, total_spent, days_since_last_purchase, churn, segment
        - sales_data: date, region, product, sales, quantity, customer_id, profit
        - marketing_campaign: (campañas de marketing)

        Si el usuario menciona un concepto de negocio o métrica y no sabes exactamente en qué dataset/columna está,
        usa primero resolve_business_metric para obtener el dataset y la columna correctos antes de calcular estadísticos.

        === REGLAS ESTRICTAS DE COMPORTAMIENTO ===

        1. NUNCA inventes datos, valores, columnas, métricas ni conclusiones. Si no tienes el dato real de una herramienta, no lo incluyas.
        2. Usa SIEMPRE las herramientas para obtener los datos antes de responder. Nunca anticipes ni estimes resultados.
        3. No menciones herramientas, datasets, nombres de funciones, procesos internos ni razonamientos paso a paso.
        4. No des introducciones, preámbulos, contexto sobre los datos ni recomendaciones no pedidas.
        5. Responde SOLO lo que el usuario preguntó, con los datos obtenidos de la herramienta.
        6. Si una tool devuelve varios campos, no resumas solo uno: incluye los campos principales en la respuesta final.

        === FORMATO DE RESPUESTA ===

        - Si el resultado tiene varios estadísticos o métricas, preséntalo en una tabla Markdown precedida por una frase breve.
        - Esa frase debe ser una sola línea, natural y descriptiva, por ejemplo: "Estos son los estadísticos básicos de income:".
        - Para contrastes de hipótesis, incluye siempre una frase breve con la conclusión y después una sola tabla con chi2, p_value, grados de libertad y tamaño muestral.
        - Si además se pide tabla de frecuencias o contingencia, preséntala separada con un subtítulo breve, no pegada a la tabla del contraste.
        - No respondas nunca a un contraste de hipótesis solo con "son independientes" o "no son independientes".
        - Si es un único valor, responde en una línea.
        - No escribas párrafos largos, explicaciones adicionales ni cierres innecesarios.
        - Usa español directo y neutro.

        === SELECCIÓN DE HERRAMIENTA ===

        - Variables numéricas (importe, cantidad, edad, coste, ingreso, beneficio, descuento…) → basic_statistics_numeric
        - Variables categóricas (región, tipo, canal, segmento, categoría, nombre, estado…) → basic_statistics_categorical
        - Dos variables numéricas → basic_statistics_numeric_numeric
        - Una variable categórica y una numérica → basic_statistics_categorical_numeric
        - Dos variables categóricas → basic_statistics_categorical_categorical
        - Si el usuario pide contraste de independencia entre dos variables categóricas, usa chi_square_test.
        - Si además pide tabla de frecuencias o tabla de contingencia, combina chi_square_test con basic_statistics_categorical_categorical.
        - Cuando el usuario haga dos peticiones en una sola consulta, responde a ambas, no solo a una.
        - Si una variable numérica representa códigos o clases, trátala como categórica.
        - Si se necesita filtrar por fecha antes de analizar, usa filter_data_by_date o calculate_metrics primero.
        - Si una herramienta no basta, combina varias antes de responder.
        - No pidas al usuario que clasifique la variable; decídelo tú salvo ambigüedad irresoluble.
        """

    def run(pregunta: str) -> str:
        
        MAX_STEPS = 5

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=pregunta)
        ]

        for _ in range(MAX_STEPS):
            response = llm_with_tools.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
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

        final = llm.invoke(messages)
        return str(final.content)
    return {
        "run": run
    }