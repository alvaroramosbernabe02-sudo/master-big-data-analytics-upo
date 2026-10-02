# BDA03 — Social intelligence y agentes de voz

**Big Data Analytics** · Profesor D. Juan Manuel Muñoz Domínguez

Las dos caras del *social intelligence* sobre un mismo negocio ficticio, **EcoAsesores**
(consultora energética para pymes y autónomos): **escuchar** lo que dice el mercado y
**hablar** con el cliente de forma automatizada.

## Ejercicio 1 — Comentarios de Facebook con Apify, Sheets y Make

Extraer automáticamente los comentarios de una publicación y depositarlos en una hoja de
cálculo, sin programar, encadenando tres herramientas.

### Paso 1. Google Sheets

Hoja `FComentarios` con dos pestañas de papeles bien separados: `URLs` (entrada, una fila por
publicación a vigilar) y `Datos` (salida, con `post URL`, `comment date`, `commenter URL`,
`commenter name`, `commenter text` y `likes`).

### Paso 2. Apify

Actor `dz_omar/facebook-comment-scraper`. **Cambio de actor justificado**: el que proponía el
guion (*Facebook Post Comment Scraper*, de easyAPI) sólo ofrece un día de prueba gratuita.
Ejecución real: **20 comentarios en 21 segundos por 0,032 $**. Los elementos del dataset vienen
anidados (`comment.author.name`, `comment.text`, `comment.created_at`,
`comment.total_reactions`…), que es lo que después hay que mapear.

### Paso 3. Make

Escenario **Comentarios de Facebook** con cuatro módulos:

| # | Módulo | Configuración relevante |
|---|---|---|
| 1 | Google Sheets · *Search Rows* | `FComentarios` / `URLs`, con cabeceras |
| 2 | Apify · *Run an Actor* | **Run synchronously = Yes**; la URL fija del JSON de entrada se sustituye por la variable del módulo 1 |
| 3 | Apify · *Get Dataset Items* | `{{2.defaultDatasetId}}`, límite 20 |
| 4 | Google Sheets · *Add a Row* | Pestaña `Datos`, con las seis columnas mapeadas |

**Dos errores que merece la pena documentar**: el primer intento falló con *«Missing value of
required parameter datasetId»* porque el campo cuelga de la raíz del paquete y no del grupo
*Data* que muestra el panel de variables; y Make lee los nombres de columna de la fila 1 de la
hoja destino, de modo que una cabecera mal formada deja el mapeo como `(A)`, `(B)`, `(C)`…

Resultado: los cuatro módulos en verde y **20 filas escritas**. El blueprint exportado está en
`codigo/`.

## Ejercicios 2 y 3 — Agente de voz que presenta el servicio y agenda la cita

### Decisión técnica: VAPI en lugar de Twilio + ElevenLabs + Make

El guion proponía número de Twilio, agente de ElevenLabs y webhook de Make. Se construyó sobre
**VAPI**, que integra STT, LLM, voz y herramientas, por tres motivos concretos:

- **No hace falta comprar número.** La cuenta *trial* de Twilio sólo llama a números
  verificados y antepone un mensaje en inglés que ensucia la grabación entregable. La llamada
  web usa el mismo agente, el mismo prompt y las mismas herramientas; asociar un número después
  no cambia nada.
- **Las herramientas son nativas.** ElevenLabs no puede leer un calendario sin un webhook
  intermedio; VAPI trae herramientas de Google Calendar por OAuth, que es exactamente lo que
  pide el ejercicio 3.
- **La extracción estructurada viene incluida**, en lugar de definir variables y enviarlas a un
  webhook.

### El agente

**Marta - EcoAsesores**, versión 6 publicada: Soniox multilingüe (STT) · GPT-4.1 · voz Elliot.
El prompt está organizado en bloques —objetivo único, estilo, guion de 5 pasos, herramientas,
contexto temporal, datos del cliente, reglas y captación del motivo— y se transcribe íntegro en
el anexo del documento.

Dos bloques nacieron de fallos reales: el agente **se inventó la fecha** (dijo «miércoles 19 de
junio» y devolvió `2024-06-19`), lo que se corrigió inyectando la fecha real con la variable
dinámica `{{now}}`; y **no preguntaba el nombre del cliente**, necesario para el título de la
cita y para la derivación.

### Herramientas y salida estructurada

| Herramienta | Tipo VAPI | Papel |
|---|---|---|
| `google_calendar_check_availability_tool` | `google.calendar.availability.check` | Consulta huecos **antes** de proponer hora |
| `google_calendar_tool` | `google.calendar.event.create` | Crea la cita de 30 minutos |

La *structured output* `derivacion_departamento` extrae automáticamente al colgar: `cliente`,
`categoria` (ALTA, BAJA, FACTURACION, AVERIA, COMERCIAL, OTROS), `departamento`,
`texto_derivacion` y `cita_agendada`.

### La llamada entregada

4 min 5 s, versión v6. El agente se presenta, pide y confirma nombre y apellidos, cualifica
(particular, 5,5 kW, ~180 €/mes), **consulta la agenda antes de proponer hora** y ofrece dos
alternativas reales, crea la cita, y cuando el cliente añade un asunto nuevo —una doble
factura— lo clasifica en voz alta como *facturación*, lo deriva a *administración* y da el
plazo de 48 horas laborables. Tres ejecuciones de herramienta, las tres correctas.

**Limitación detectada y documentada**: el cliente repitió «a las 10» mientras el agente
procesaba y la herramienta de creación se ejecutó dos veces, duplicando la cita. Es un fallo
del prompt, no de la herramienta, y el documento explica la regla que lo evita.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF (22 páginas), con transcripción, salida estructurada, JSON de las herramientas y el prompt completo en anexo |
| `codigo/Comentarios de Facebook.blueprint.json` | Blueprint exportado del escenario de Make |

> La grabación de audio de la llamada forma parte de la entrega académica y no se incluye aquí.
