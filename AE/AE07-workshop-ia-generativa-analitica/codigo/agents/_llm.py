"""Fábrica del LLM. Por defecto usa Groq (como en el taller); si no hay GROQ_API_KEY,
usa un modelo local servido por Ollama con la misma interfaz de LangChain (bind_tools/invoke)."""
import os

def get_llm(temperature=0.1, model=None):
    if os.getenv("GROQ_API_KEY"):
        from langchain_groq import ChatGroq
        return ChatGroq(model=model or "openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"), temperature=temperature)
    from langchain_ollama import ChatOllama
    return ChatOllama(model=os.getenv("OLLAMA_MODEL", "qwen2.5:3b"), temperature=temperature, num_ctx=8192)
