from agents._llm import get_llm
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
import os

import agents.statistic_agent as statistics_agent_module
import agents.visualization_agent as visualization_agent_module
import agents.model_agent as model_agent_module


DESCRIPTION = "Agente orquestador que delega en los agentes especializados"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

_statistics_agent = statistics_agent_module.create_agent()
_visualization_agent = visualization_agent_module.create_agent()
_model_agent = model_agent_module.create_agent()


@tool("ask_statistics_agent")
def ask_statistics_agent(pregunta: str) -> str:
    """
    Delega una consulta estadística al agente especializado en estadística.
    Usar para: estadísticos básicos, distribuciones, correlaciones,
    contrastes de hipótesis, métricas agregadas y filtros temporales.
    """
    return _statistics_agent["run"](pregunta)


@tool("ask_visualization_agent")
def ask_visualization_agent(pregunta: str) -> str:
    """
    Delega una consulta de visualización al agente especializado en gráficos.
    Usar para: histogramas, boxplots, barplots, scatterplots, heatmaps
    y comparativas visuales entre variables.
    """
    return _visualization_agent["run"](pregunta)


@tool("ask_model_agent")
def ask_model_agent(pregunta: str) -> str:
    """
    Delega una consulta de modelos al agente especializado en machine learning.
    Usar para: predicción de churn, segmentación de clientes, previsión de ventas
    y consultas sobre los modelos disponibles.
    """
    return _model_agent["run"](pregunta)


def create_agent():

    llm = get_llm()

    tool_map = {
        "ask_statistics_agent": ask_statistics_agent,
        "ask_visualization_agent": ask_visualization_agent,
        "ask_model_agent": ask_model_agent
    }

    llm_with_tools = llm.bind_tools(list(tool_map.values()))

    system_prompt = """
        Eres un asistente analítico que coordina a tres agentes especializados.

        Agentes disponibles:
        - ask_statistics_agent: estadísticos básicos, correlaciones, contrastes de hipótesis, métricas y filtros.
        - ask_visualization_agent: gráficos e histogramas, boxplots, scatterplots, heatmaps.
        - ask_model_agent: predicciones de churn, segmentación de clientes y previsión de ventas.

        Reglas:
        - Usa siempre una tool para responder. Nunca respondas directamente sin delegar.
        - Elige el agente más adecuado según la intención del usuario.
        - Si la consulta mezcla análisis y visualización, delega cada parte al agente correcto.
        - Transmite la consulta del usuario tal cual al agente delegado, sin reformularla.
        - Responde en español con la respuesta que devuelva el agente delegado, sin añadir texto extra.
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
