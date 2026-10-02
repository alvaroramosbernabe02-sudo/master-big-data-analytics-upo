"""Ejercicio 4. Memoria del usuario persistente en SQLite (sobrevive a reinicios de la app)."""
from db import conectar

def guardar(usuario: str, clave: str, valor: str) -> str:
    con = conectar()
    con.execute("INSERT INTO memoria(usuario, clave, valor) VALUES (?,?,?) ON CONFLICT(usuario, clave) DO UPDATE SET valor=excluded.valor, actualizada=CURRENT_TIMESTAMP", (usuario, clave.lower().strip(), valor.strip()))
    con.commit(); con.close()
    return f"Recordaré que {clave} = {valor}."

def leer(usuario: str) -> dict:
    con = conectar(); filas = con.execute("SELECT clave, valor FROM memoria WHERE usuario=? ORDER BY clave", (usuario,)).fetchall(); con.close()
    return {f["clave"]: f["valor"] for f in filas}

def como_texto(usuario: str) -> str:
    m = leer(usuario)
    return "; ".join(f"{k}: {v}" for k, v in m.items()) if m else "(sin datos guardados)"
