# TA02 — Modelos de lenguaje (LLMs): técnicas de prompting

**Tecnologías Avanzadas** · Profesor D. Ignacio Sierra Ruiz

Cinco técnicas de prompting aplicadas en paralelo a dos modelos, con las respuestas
transcritas literalmente para poder compararlas.

## Metodología

Se eligen cinco ejercicios de la presentación de la asignatura, uno por técnica. **Cada prompt
se lanzó literalmente igual en los dos modelos, en conversaciones nuevas e independientes**
para evitar contaminación de contexto.

| | Modelo 1 | Modelo 2 |
|---|---|---|
| Sistema | ChatGPT (OpenAI) | Gemini (Google) |
| Plan | Cuenta gratuita | Cuenta Pro |
| Fecha | 20 de septiembre de 2026 | 20 de septiembre de 2026 |
| Idioma | Español | Español |

Las respuestas que aparecen en las tablas son transcripción literal; cuando una respuesta era
muy extensa se indica expresamente el recorte, sin alterar el contenido.

## Ejercicios

### E1. Precisión y patrón de rol: «el actor confundido»

Primero un prompt vago —*actúa como un rey*— y después el mismo encargo reescrito con máxima
precisión escénica: emoción, vestuario, época, escenario y tono de voz. La comparación entre
ambas salidas es la demostración más clara de por qué la especificidad importa.

### E2. Few-shot prompting

Con un ejemplo propio: cómo dos o tres ejemplos bien elegidos fijan el formato de salida mejor
que cualquier instrucción en prosa.

### E3. Chain-of-thought: el puente y la linterna

El clásico problema de cruzar el puente con una linterna, pidiendo razonamiento paso a paso.
Es donde más se separan los modelos.

### E4. Interview approach

El modelo pregunta antes de responder, para completar el contexto que le falta.

### E5. Generación de código

Problema 2 de la presentación, con comparación de la corrección y la calidad del código
generado por cada modelo.

## Conclusiones

El documento cierra con una comparativa transversal: en qué técnica se comportó mejor cada
modelo y qué patrones son robustos con independencia del sistema usado.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF, con los prompts y las respuestas literales de ambos modelos |
