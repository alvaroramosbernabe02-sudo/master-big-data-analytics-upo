# AE06 — Workshop de agentes: asistente de atención al cliente

**Aplicaciones Empresariales** · Profesor D. José Antonio Lagares Rodríguez

**DeporTienda Asistente**: un agente de atención al cliente completo, ejecutado **íntegramente
en local y sin ninguna API de pago**.

## Stack

- **Modelo**: Qwen2.5 3B Instruct servido con **Ollama** a través de su endpoint compatible con
  OpenAI (`http://localhost:11434/v1`).
- **Embeddings del RAG**: fastembed (`paraphrase-multilingual-MiniLM-L12-v2`, ONNX cuantizado).
- **Interfaz**: Chainlit. Todas las capturas del documento proceden de ejecuciones reales.

## Qué se implementó

| Ejercicio | Qué se hizo | Fichero |
|---|---|---|
| **E1. Caso de uso** | Usuario objetivo, problema que resuelve, flujo principal de conversación, qué puede y qué no debe hacer el agente, y arquitectura | `README`, `config.py` |
| **E2. Herramientas** | **7 herramientas** con tool calling nativo y argumentos validados con Pydantic | `tools.py` |
| **E3. Razonamiento multipaso** | Bucle observación-acción de hasta **6 pasos**, con varias herramientas por petición | `agent.py` |
| **E4. Memoria** | Memoria persistente por usuario en JSON, inyectada en el system prompt | `memoria.py` |
| **E5. RAG** | 4 documentos propios, fastembed, top-k con umbral y **citas** en la respuesta | `rag.py`, `conocimiento/` |
| **E6. Caché** | Caché exacta por hash, con **exclusión de consultas personales** | `cache.py` |
| **E7. Validación** | Pydantic con reintento, enmascarado de datos sensibles y bloqueo de acciones destructivas | `guardrails.py` |
| **E8.1. Extra** | El agente expuesto como **API REST** con FastAPI | `api.py` |
| **E8.2. Extra** | **Evaluación automática**: LLM-as-a-Judge más comprobaciones deterministas | `evaluar.py` |

El documento cierra con las dificultades encontradas, las decisiones de diseño que hubo que
tomar y las instrucciones para ejecutar el proyecto.

## Cómo ejecutarlo

```bash
cd codigo/agente_soporte
pip install -r requirements.txt
cp env.txt .env            # apunta a Ollama en local por defecto
ollama pull qwen2.5:3b
chainlit run app.py        # interfaz de chat
python api.py              # o la API REST
python evaluar.py          # batería de evaluación
```

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/agente_soporte/agent.py` | Bucle de razonamiento del agente |
| `codigo/agente_soporte/tools.py` | Las 7 herramientas con sus esquemas Pydantic |
| `codigo/agente_soporte/rag.py`, `conocimiento/` | RAG y base de conocimiento (envíos, devoluciones, garantía, tallas) |
| `codigo/agente_soporte/memoria.py`, `cache.py`, `guardrails.py` | Memoria, caché y validación |
| `codigo/agente_soporte/app.py`, `api.py`, `prueba_cli.py` | Interfaz Chainlit, API REST y cliente de consola |
| `codigo/agente_soporte/evaluar.py` | Evaluación automática |
| `codigo/agente_soporte/db.py`, `deportienda.db` | Base de datos de ejemplo de la tienda |
