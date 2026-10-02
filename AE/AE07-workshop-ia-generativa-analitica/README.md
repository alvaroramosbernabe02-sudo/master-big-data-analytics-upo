# AE07 — Workshop de IA generativa: agentes para análisis de datos

**Aplicaciones Empresariales** · Profesor D. Benito Martín Gassol

Seis agentes que analizan un conjunto de datos conversando: estadística, visualización,
machine learning y un orquestador que decide a quién llamar.

## Entrega

El entregable principal es un **vídeo de 25 min 45 s** que recorre la ejecución completa, con
un documento que funciona como guía: para cada apartado indica el minuto exacto en que se
lanza la consulta.

> El vídeo se entrega acelerado ×4. Todos los modelos se ejecutan en local (Qwen2.5 3B sobre
> Ollama, **sin GPU**), de modo que cada respuesta tarda entre 1 y 10 minutos reales y la
> grabación original dura 91 minutos. **La aceleración no corta ni edita nada**: se ve la
> ejecución continua de principio a fin.
>
> *(El MP4 no se incluye en el repositorio por tamaño; forma parte de la entrega académica.)*

## Entorno

**Streamlit + LangChain**, con seis agentes cargados desde la carpeta `agents/`. La fábrica
`agents/_llm.py` conmuta automáticamente al modelo local cuando no hay clave de Groq, de modo
que el proyecto funciona sin ninguna API de pago.

## Qué se implementó

| Apartado | Qué se hizo | Fichero |
|---|---|---|
| Laboratorio de set-up | Entorno y agente de prueba; paso 8 del laboratorio: **agente iterativo** | `agents/basic_agent.py`, `agents/iterative_agent.py` |
| **E1. Agente estadístico** (3 pts) | Descriptivos univariantes y multivariantes sobre el dataset | `agents/statistic_agent.py`, `tools/univariate_statistics_tools.py`, `tools/multivariate_statistics_tools.py` |
| **E2. Agente de visualización** (3 pts) | Gráficos univariantes y multivariantes generados a demanda | `agents/visualization_agent.py`, `tools/univariate_plot_tools.py`, `tools/multivariate_plot_tools.py` |
| **E3. Agente orquestador** (2 pts) | Decide qué agente resuelve cada petición y compone la respuesta | `agents/orchestrator_agent.py` |
| **E4 / Actividad 2. Funcionalidad adicional** | 4.1 **Agente de modelos con machine learning** y 4.2 **contraste de hipótesis chi-cuadrado** | `agents/model_agent.py`, `tools/ml_tools.py`, `tools/contraste_de_hipotesis.py` |

## Cómo ejecutarlo

```bash
cd codigo
pip install -r requirements-langchain.txt -r requirements-data.txt -r requirements-ml.txt
cp env.example .env        # sin clave de Groq usa el modelo local de Ollama
streamlit run app_langchain.py
```

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF (guía del vídeo con marcas de tiempo) |
| `codigo/app_langchain.py` | Aplicación Streamlit |
| `codigo/agents/` | Los seis agentes y la fábrica de modelos |
| `codigo/tools/` | Herramientas de estadística, visualización, ML y contraste de hipótesis |
| `codigo/data/` | Conjuntos de datos usados en la demostración |
