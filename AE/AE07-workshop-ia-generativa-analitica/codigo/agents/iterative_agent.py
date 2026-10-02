"""Agente iterativo (paso 8 del laboratorio de set-up).

Amplía el agente básico con un bucle de planificación: en lugar de una única llamada a
herramienta, planifica, ejecuta, observa el resultado y vuelve a decidir si necesita otra
herramienta, hasta un máximo de pasos. Permite responder preguntas que requieren encadenar
varias herramientas (por ejemplo, resumir un dataset y después contar sus registros).
"""
from agents._llm import get_llm
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
import os

from tools.basic_data_tools import count_records, get_dataset_summary, resolve_business_metric
from tools.univariate_statistics_tools import basic_statistics_numeric, basic_statistics_categorical

DESCRIPTION = "Agente iterativo: planifica y encadena varias herramientas"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

MAX_STEPS = 5


def create_agent():

    llm = get_llm()

    tool_map = {
        "count_records": count_records,
        "get_dataset_summary": get_dataset_summary,
        "resolve_business_metric": resolve_business_metric,
        "basic_statistics_numeric": basic_statistics_numeric,
        "basic_statistics_categorical": basic_statistics_categorical,
    }

    llm_with_tools = llm.bind_tools(list(tool_map.values()))

    system_prompt = """
        Eres un analista de datos que trabaja de forma iterativa.

        Método de trabajo:
        1. Analiza qué información necesitas para responder.
        2. Llama a UNA herramienta cada vez.
        3. Observa el resultado y decide si necesitas otra herramienta.
        4. Repite hasta tener todo lo necesario y responde entonces al usuario.

        Reglas:
        - Nunca inventes valores: todo dato numérico debe venir de una herramienta.
        - Si la pregunta requiere varias cosas (por ejemplo, un conteo y un estadístico),
          usa una herramienta para cada una antes de responder.
        - Responde en español, de forma breve y clara, sin mencionar nombres de herramientas.

        Datasets disponibles: customer_data, sales_data, marketing_campaign.
        """

    def run(pregunta: str) -> str:
        messages = [SystemMessage(content=system_prompt), HumanMessage(content=pregunta)]
        pasos = 0

        for _ in range(MAX_STEPS):
            response = llm_with_tools.invoke(messages)
            messages.append(response)

            if not response.tool_calls:
                return str(response.content)

            for tc in response.tool_calls:
                pasos += 1
                print(f"[PASO {pasos}] {tc['name']} → args: {tc['args']}")
                try:
                    resultado = tool_map[tc["name"]].invoke(tc["args"])
                except Exception as e:                       # la observación del error también es información
                    resultado = f"Error al ejecutar la herramienta: {e}"
                messages.append(ToolMessage(content=str(resultado), tool_call_id=tc["id"]))

        final = llm.invoke(messages)
        return str(final.content)

    return {"run": run}
