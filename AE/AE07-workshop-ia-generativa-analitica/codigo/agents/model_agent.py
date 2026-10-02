from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from agents._llm import get_llm
from tools.ml_tools import predict_churn_customer, top_churn_risk, detect_outliers

DESCRIPTION = "Predicciones de churn con el modelo entrenado y detección de outliers (herramienta adicional)"

def create_agent():
    llm = get_llm()
    tool_map = {"predict_churn_customer": predict_churn_customer, "top_churn_risk": top_churn_risk, "detect_outliers": detect_outliers}
    llm_with_tools = llm.bind_tools(list(tool_map.values()))
    system_prompt = """Eres un analista de machine learning. Usa SIEMPRE las herramientas:
    - predict_churn_customer: riesgo de abandono de un cliente concreto (customer_id).
    - top_churn_risk: clientes con mayor riesgo de abandono (opcionalmente por segmento).
    - detect_outliers: valores atípicos de una columna numérica (dataset customer_data, sales_data o marketing_campaign).
    No inventes datos. Responde en español con una frase breve y una tabla Markdown con los resultados."""
    def run(pregunta: str) -> str:
        messages = [SystemMessage(content=system_prompt), HumanMessage(content=pregunta)]
        for _ in range(5):
            response = llm_with_tools.invoke(messages); messages.append(response)
            if not response.tool_calls: return str(response.content)
            for tc in response.tool_calls:
                resultado = tool_map[tc["name"]].invoke(tc["args"])
                print(f"[TOOL] {tc['name']} → args: {tc['args']}")
                messages.append(ToolMessage(content=str(resultado), tool_call_id=tc["id"]))
        return str(llm.invoke(messages).content)
    return {"run": run}
