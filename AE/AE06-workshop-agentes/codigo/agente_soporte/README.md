# DeporTienda Asistente - AE06 Workshop de agentes
Álvaro Ramos Bernabé - Máster Big Data & Business Analytics (UPO)

Agente de atención al cliente con modelo local (Qwen2.5 3B vía Ollama), tool calling,
memoria persistente, RAG con fastembed, caché, guardarraíles, API REST y evaluación automática.

## Puesta en marcha
    ollama serve &
    ollama pull qwen2.5:3b
    pip install -r requirements.txt
    chainlit run app.py            # interfaz de chat
    uvicorn api:app --port 8010    # API REST (extra 8.1)
    python evaluar.py              # evaluación automática (extra 8.2)

Variables en `.env`: LLM_BASE_URL, LLM_MODEL, EMBEDDINGS_MODEL, EMBEDDINGS_PATH.
Si no se fija EMBEDDINGS_PATH, fastembed descarga el modelo de embeddings la primera vez.

## Ficheros
- `agent.py`     bucle de razonamiento (observación-acción), hasta 6 pasos
- `tools.py`     7 herramientas con esquemas Pydantic
- `memoria.py`   memoria persistente por usuario
- `rag.py`       base de conocimiento (fastembed + coseno, top-k)
- `cache.py`     caché exacta por hash
- `guardrails.py` validación de entrada/salida, datos sensibles, acciones peligrosas
- `app.py`       interfaz Chainlit;  `api.py` API REST;  `evaluar.py` evaluación
- `conocimiento/` documentos de la base de conocimiento
