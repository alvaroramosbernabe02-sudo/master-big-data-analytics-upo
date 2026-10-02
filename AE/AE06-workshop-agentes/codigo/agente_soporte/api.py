"""Ejercicio 8 (extra). El mismo agente expuesto como API REST con FastAPI."""
from fastapi import FastAPI
from pydantic import BaseModel
import db, agent, memoria

db.inicializar()
app = FastAPI(title="Agente DeporTienda", version="1.0")

class Peticion(BaseModel):
    usuario: str = "api"
    mensaje: str

@app.post("/chat")
async def chat(p: Peticion):
    async def no_confirmar(nombre, args): return False  # en la API las acciones sensibles quedan pendientes de un humano
    r = await agent.ejecutar(p.mensaje, p.usuario, [], confirmar=no_confirmar)
    return {"respuesta": r["respuesta"], "herramientas": [x["herramienta"] for x in r["pasos"]], "cache": r["cache"], "avisos": r["avisos"], "segundos": r["tiempo"]}

@app.get("/memoria/{usuario}")
def ver_memoria(usuario: str):
    return memoria.leer(usuario)
