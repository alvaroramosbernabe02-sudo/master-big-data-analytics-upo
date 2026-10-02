"""Ejercicio 2. Herramientas propias del agente (tool calling) con validación Pydantic de argumentos."""
import re, json
from functools import lru_cache
from pydantic import BaseModel, Field, EmailStr, field_validator
from db import conectar
import memoria, rag

# ---------- esquemas de argumentos (Ejercicio 7: validación con Pydantic) ----------
class ArgsBuscarProducto(BaseModel):
    texto: str = Field(min_length=2, max_length=60)
class ArgsPedido(BaseModel):
    pedido: str
    @field_validator("pedido")
    @classmethod
    def formato(cls, v):
        v = v.strip().upper()
        if not re.fullmatch(r"DT-\d{4}", v): raise ValueError("el número de pedido debe tener el formato DT-1234")
        return v
class Linea(BaseModel):
    producto: str
    unidades: int = Field(ge=1, le=20)
class ArgsPresupuesto(BaseModel):
    lineas: list[Linea] = Field(min_length=1, max_length=10)
    envio: str = Field(default="estandar", pattern="^(estandar|expres|tienda)$")
    cupon: str | None = None
class ArgsIncidencia(BaseModel):
    pedido: str
    tipo: str = Field(pattern="^(devolucion|garantia|retraso|otro)$")
    descripcion: str = Field(min_length=5, max_length=400)
    @field_validator("pedido")
    @classmethod
    def formato(cls, v):
        return ArgsPedido(pedido=v).pedido
class ArgsEmail(BaseModel):
    email: str
class ArgsRecordar(BaseModel):
    clave: str = Field(min_length=2, max_length=30)
    valor: str = Field(min_length=1, max_length=80)
class ArgsConocimiento(BaseModel):
    pregunta: str = Field(min_length=3)

# ---------- implementación ----------
import unicodedata
def _norm(t):
    t = unicodedata.normalize("NFKD", t.lower()); return "".join(c for c in t if not unicodedata.combining(c))

def _buscar(texto: str):
    """Búsqueda por palabras: puntúa cada producto por nº de términos que aparecen en id, nombre o categoría."""
    con = conectar(); filas = [dict(f) for f in con.execute("SELECT * FROM productos").fetchall()]; con.close()
    terminos = [w for w in re.findall(r"\w+", _norm(texto)) if len(w) > 2 and w not in {"con", "para", "los", "las", "del", "unas", "unos"}]
    punt = [(sum(w.rstrip("s") in _norm(f"{f['id']} {f['nombre']} {f['categoria']}") for w in terminos), f) for f in filas]
    mejor = max((p for p, _ in punt), default=0)
    return [f for p, f in punt if p == mejor and p > 0]

@lru_cache(maxsize=128)          # Ejercicio 6: reutilización de resultados de tools deterministas
def buscar_producto(texto: str) -> str:
    filas = _buscar(texto)
    if not filas: return "No hay productos que coincidan."
    return json.dumps([f | {"disponible": f["stock"] > 0} for f in filas], ensure_ascii=False)

def consultar_pedido(pedido: str) -> str:
    con = conectar(); f = con.execute("SELECT p.*, pr.nombre, pr.precio FROM pedidos p JOIN productos pr ON pr.id=p.producto WHERE p.id=?", (pedido,)).fetchone(); con.close()
    if not f: return f"No existe el pedido {pedido}."
    d = dict(f); d["fecha_del_pedido"] = d.pop("fecha")          # evita que se confunda con la fecha de entrega
    return json.dumps(d, ensure_ascii=False)

def calcular_presupuesto(lineas: list, envio: str = "estandar", cupon: str | None = None) -> str:
    con = conectar(); detalle, subtotal = [], 0.0
    for l in lineas:
        c = _buscar(l["producto"]); f = c[0] if c else None
        if not f: con.close(); return f"Producto no encontrado: {l['producto']}"
        imp = round(f["precio"] * l["unidades"], 2); subtotal += imp
        detalle.append({"id": f["id"], "producto": f["nombre"], "unidades": l["unidades"], "importe": imp, "hay_stock": f["stock"] >= l["unidades"]})
    con.close()
    descuento = round(subtotal * 0.10, 2) if (cupon or "").upper() == "MBDA10" else 0.0
    base = subtotal - descuento
    coste_envio = 0.0 if envio == "tienda" or (envio == "estandar" and base >= 60) else (9.90 if envio == "expres" else 4.90)
    total = round(base + coste_envio, 2)
    eur = lambda x: f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
    resumen = "; ".join(f"{d['unidades']} x {d['producto']} = {eur(d['importe'])} ({'hay stock' if d['hay_stock'] else 'sin stock'})" for d in detalle)
    resumen += f". Subtotal {eur(subtotal)}, descuento {eur(descuento)}, envío {eur(coste_envio)}, TOTAL {eur(total)} (IVA incluido)."
    return json.dumps({"resumen": resumen, "lineas": detalle, "subtotal": round(subtotal, 2), "descuento": descuento, "envio": coste_envio, "total_iva_incluido": total}, ensure_ascii=False)

def crear_incidencia(pedido: str, tipo: str, descripcion: str) -> str:
    con = conectar(); cur = con.execute("INSERT INTO incidencias(pedido, tipo, descripcion, estado) VALUES (?,?,?, 'abierta')", (pedido, tipo, descripcion)); con.commit(); n = cur.lastrowid; con.close()
    return f"Incidencia INC-{n:04d} creada para {pedido} ({tipo}). El equipo responderá en 72 h."

def validar_email(email: str) -> str:
    try:
        class _E(BaseModel): e: EmailStr
        _E(e=email); ok = True
    except Exception: ok = False
    con = conectar(); n = con.execute("SELECT COUNT(*) FROM pedidos WHERE email=?", (email,)).fetchone()[0]; con.close()
    return json.dumps({"email": email, "formato_valido": ok, "pedidos_asociados": n})

def buscar_conocimiento(pregunta: str) -> str:
    res = rag.base().buscar(pregunta)
    return json.dumps(res, ensure_ascii=False)

# ---------- registro para el LLM ----------
def _limpiar(x):
    if isinstance(x, dict):
        return {k: _limpiar(v) for k, v in x.items() if k not in ("title", "default") and not (k == "anyOf" and False)}
    if isinstance(x, list): return [_limpiar(v) for v in x]
    return x

def _schema(nombre, desc, modelo):
    return {"type": "function", "function": {"name": nombre, "description": desc, "parameters": _limpiar(modelo.model_json_schema())}}

TOOLS = {
    "buscar_producto": (buscar_producto, ArgsBuscarProducto, "Busca productos del catálogo por nombre, categoría o id (P001...). Devuelve precio y stock."),
    "consultar_pedido": (consultar_pedido, ArgsPedido, "Consulta el estado de un pedido por su número DT-XXXX."),
    "calcular_presupuesto": (calcular_presupuesto, ArgsPresupuesto, "Calcula el importe total de una compra: lista de líneas {producto, unidades}, tipo de envío (estandar, expres, tienda) y cupón opcional."),
    "crear_incidencia": (crear_incidencia, ArgsIncidencia, "Abre una incidencia (devolucion, garantia, retraso u otro) para un pedido. Acción sensible: requiere confirmación humana."),
    "validar_email": (validar_email, ArgsEmail, "Valida el formato de un email y comprueba si tiene pedidos."),
    "buscar_conocimiento": (buscar_conocimiento, ArgsConocimiento, "Busca en la base de conocimiento de la tienda (devoluciones, envíos, garantía, tallas). Úsala para cualquier pregunta sobre políticas."),
    "recordar_dato": (None, ArgsRecordar, "Guarda un dato relevante del usuario para recordarlo en el futuro (nombre, talla, deporte, email...)."),
}
SCHEMAS = [_schema(n, d, m) for n, (_, m, d) in TOOLS.items()]
ACCIONES_SENSIBLES = {"crear_incidencia"}
