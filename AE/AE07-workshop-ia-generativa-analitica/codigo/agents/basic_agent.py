from agents._llm import get_llm
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage
import os
from tools.basic_data_tools import count_records,get_dataset_summary


DESCRIPTION = "Consultas básicas: conteos y resumen de datasets"

GROQ_API_KEY = os.getenv("GROQ_API_KEY","")

def create_agent():

    llm = get_llm()

    tool_map = {
        "count_records": count_records,
        "get_dataset_summary": get_dataset_summary
    }

    llm_with_tools = llm.bind_tools(list(tool_map.values()))

    system_prompt = """
        tienes dos herramientas una para contar registros y otra para hacer un resumen de los datos.
        En función de lo que te pida el usuario decide una u otra y le das la respuesta

        """

    def run(pregunta: str) -> str:

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(
                content=f"""
                        Consulta del usuario:

                        {pregunta}

                        Recuerda: elige automáticamente el y usa una tool.
                        """
            )

        ]

        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            for tc in response.tool_calls:
                print(f"[TOOL] {tc['name']} → args: {tc['args']}")
                resultado = tool_map[tc["name"]].invoke(tc["args"])
                messages.append(
                    ToolMessage(
                        content=str(resultado),
                        tool_call_id=tc["id"]
                    )
                )

        final = llm_with_tools.invoke(messages)
        return str(final.content)
    return {
        "run": run
    }