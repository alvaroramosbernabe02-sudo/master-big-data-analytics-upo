"""Ejercicios 2, 3, 6 y 7. Bucle ReAct con tool calling nativo:
petición -> decisión del modelo -> ejecución de herramientas -> observación -> nueva llamada -> respuesta final."""
import asyncio, json, time
from pydantic import ValidationError
from config import cliente, LLM_MODEL, MAX_STEPS, TEMPERATURE
import tools, memoria, cache, guardrails, rag

SISTEMA = """Eres el asistente de atención al cliente de DeporTienda, una tienda online de material deportivo.
Puedes: buscar productos, consultar pedidos, calcular presupuestos, abrir incidencias, validar emails,
responder dudas sobre devoluciones, envíos, garantía y tallas (SIEMPRE con buscar_conocimiento) y recordar datos del usuario.
No debes: inventar datos, dar consejo médico, pedir DNI ni datos bancarios, ni prometer reembolsos sin incidencia.
Reglas:
- Usa las herramientas para cualquier dato; si hacen falta varias, llámalas una tras otra.
- Cuando el usuario diga su nombre, talla, deporte o email, guárdalo con recordar_dato.
- Si usas la base de conocimiento, cita la fuente entre corchetes, p. ej. [devoluciones#1].
- Responde en español, en 2-6 frases, con importes en euros.
- Si en el mensaje aparece [DNI OCULTO], [TARJETA OCULTA] o [IBAN OCULTO], ignóralos (los ha enmascarado el filtro de seguridad) y atiende con normalidad el resto de la petición: nunca los pidas de nuevo.
- Limítate a los datos que devuelven las herramientas: no inventes fechas de entrega, plazos ni precios que no aparezcan en ellas.
Datos recordados de este usuario: {memoria}"""

CACHEABLES = {"buscar_conocimiento", "buscar_producto"}

def _llm(mensajes):
    return cliente.chat.completions.create(model=LLM_MODEL, messages=mensajes, tools=tools.SCHEMAS, temperature=TEMPERATURE)

async def ejecutar(pregunta: str, usuario: str, historial: list, on_evento=None, confirmar=None) -> dict:
    """Devuelve {'respuesta', 'pasos', 'cache', 'avisos', 'tiempo'}. on_evento/confirmar son callbacks async de la UI."""
    t0 = time.time(); evento = on_evento or (lambda *a, **k: asyncio.sleep(0))
    texto, avisos = guardrails.revisar_entrada(pregunta)
    if guardrails.es_peligrosa(texto):
        return {"respuesta": "No puedo ejecutar acciones destructivas sobre los datos de la tienda.", "pasos": [], "cache": False, "avisos": avisos + ["Acción peligrosa bloqueada por el guardarraíl."], "tiempo": 0}
    h = cache.clave(texto)
    if (r := cache.obtener(h)):
        return {"respuesta": r, "pasos": [], "cache": True, "avisos": avisos, "tiempo": round(time.time() - t0, 2)}
    pasos, usadas, reintentos = [], set(), 0
    # RAG: recuperación top-k previa; si hay fragmentos relevantes se inyectan en el prompt con su cita
    recuperados = [d for d in rag.base().buscar(texto) if d["similitud"] >= 0.45]
    contenido = texto
    if recuperados:
        contexto = "\n".join(f"[{d['cita']}] {d['texto']}" for d in recuperados)
        contenido = f"{texto}\n\nCONTEXTO DE LA BASE DE CONOCIMIENTO (responde usándolo y cita las fuentes entre corchetes):\n{contexto}"
        pasos.append({"paso": 0, "herramienta": "buscar_conocimiento", "argumentos": {"pregunta": texto, "top_k": 3}, "resultado": json.dumps(recuperados, ensure_ascii=False)})
        usadas.add("buscar_conocimiento"); await evento(pasos[-1])
    mensajes = [{"role": "system", "content": SISTEMA.format(memoria=memoria.como_texto(usuario))}] + historial[-6:] + [{"role": "user", "content": contenido}]
    for paso in range(1, MAX_STEPS + 1):
        resp = await asyncio.to_thread(_llm, mensajes); msg = resp.choices[0].message
        if not msg.tool_calls:
            try:
                final = guardrails.RespuestaFinal(texto=msg.content or "").texto
            except ValidationError as e:
                if reintentos < 1:
                    reintentos += 1; mensajes += [{"role": "assistant", "content": msg.content or ""}, {"role": "user", "content": f"Tu respuesta no es válida ({e.errors()[0]['msg']}). Responde de nuevo solo con texto para el cliente."}]
                    avisos.append("Salida no válida: se ha pedido al modelo que la regenere."); continue
                final = "Lo siento, no he podido generar una respuesta válida."
            if usadas and usadas <= CACHEABLES or not usadas:
                if not any(k in texto.lower() for k in ["mi ", "mis ", "me llamo", "soy "]): cache.guardar(h, texto, final)
            return {"respuesta": final, "pasos": pasos, "cache": False, "avisos": avisos, "tiempo": round(time.time() - t0, 2)}
        mensajes.append({"role": "assistant", "content": msg.content or "", "tool_calls": [tc.model_dump() for tc in msg.tool_calls]})
        for tc in msg.tool_calls:
            nombre = tc.function.name
            try: args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError: args = {}
            if nombre not in tools.TOOLS:
                obs = f"Error: la herramienta {nombre} no existe."
            else:
                funcion, Esquema, _ = tools.TOOLS[nombre]
                try:
                    validos = Esquema(**args).model_dump()
                    if nombre in tools.ACCIONES_SENSIBLES and confirmar and not await confirmar(nombre, validos):
                        obs = "Accion sensible pendiente de confirmacion humana: NO se ha ejecutado. Informa al cliente de que queda pendiente de aprobacion."
                    elif nombre == "recordar_dato":
                        obs = memoria.guardar(usuario, **validos)
                    else:
                        obs = funcion(**validos)
                except ValidationError as e:
                    obs = f"Argumentos no válidos: {e.errors()[0]['loc']} {e.errors()[0]['msg']}. Corrige y vuelve a intentarlo."
                usadas.add(nombre)
            pasos.append({"paso": paso, "herramienta": nombre, "argumentos": args, "resultado": obs})
            await evento(pasos[-1])
            mensajes.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
    avisos.append(f"Se alcanzó el límite de {MAX_STEPS} pasos del agente.")
    return {"respuesta": "He alcanzado el número máximo de pasos. ¿Puedes concretar la petición?", "pasos": pasos, "cache": False, "avisos": avisos, "tiempo": round(time.time() - t0, 2)}
