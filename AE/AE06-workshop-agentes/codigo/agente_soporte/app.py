"""Interfaz Chainlit del agente de DeporTienda (muestra cada herramienta ejecutada con sus argumentos)."""
import json
import chainlit as cl
import db, agent, memoria

db.inicializar()

@cl.on_chat_start
async def inicio():
    cl.user_session.set("usuario", "cliente_demo"); cl.user_session.set("historial", [])
    await cl.Message(content="Hola, soy el asistente de **DeporTienda**. Puedo buscar productos, consultar pedidos, calcular presupuestos, abrir incidencias y resolver dudas de devoluciones, envíos, garantía y tallas.").send()

async def confirmar(nombre, args):
    r = await cl.AskActionMessage(content=f"⚠️ Acción sensible **{nombre}** con `{json.dumps(args, ensure_ascii=False)}`. ¿La confirmas?",
        actions=[cl.Action(name="si", payload={"ok": True}, label="✅ Confirmar"), cl.Action(name="no", payload={"ok": False}, label="❌ Cancelar")], timeout=600).send()
    return bool(r and r.get("payload", {}).get("ok"))

@cl.on_message
async def mensaje(m: cl.Message):
    usuario = cl.user_session.get("usuario"); hist = cl.user_session.get("historial")
    async def evento(p):
        async with cl.Step(name=f"🔧 {p['herramienta']}", type="tool") as s:
            s.input = json.dumps(p["argumentos"], ensure_ascii=False, indent=1); s.output = p["resultado"][:1500]
    r = await agent.ejecutar(m.content, usuario, hist, on_evento=evento, confirmar=confirmar)
    extra = []
    if r["cache"]: extra.append("⚡ respuesta servida desde caché (sin llamar al LLM)")
    extra += [f"🛡️ {a}" for a in r["avisos"]]
    pie = f"\n\n---\n*{len(r['pasos'])} llamadas a herramientas · {r['tiempo']} s*" + ("".join(f"\n\n{e}" for e in extra))
    await cl.Message(content=r["respuesta"] + pie).send()
    hist += [{"role": "user", "content": m.content}, {"role": "assistant", "content": r["respuesta"]}]
    cl.user_session.set("historial", hist)
