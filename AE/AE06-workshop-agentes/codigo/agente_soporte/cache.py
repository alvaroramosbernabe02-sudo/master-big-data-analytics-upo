"""Ejercicio 6. Caché exacta por hash del prompt normalizado (+ memoria del usuario) en SQLite."""
import hashlib, re, unicodedata
from db import conectar

def _normalizar(t: str) -> str:
    t = unicodedata.normalize("NFKD", t.lower()); t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^\w ]", "", re.sub(r"\s+", " ", t)).strip()

def clave(pregunta: str, contexto: str = "") -> str:
    return hashlib.sha256((_normalizar(pregunta) + "|" + contexto).encode()).hexdigest()

def obtener(h: str):
    con = conectar(); f = con.execute("SELECT respuesta FROM cache WHERE hash=?", (h,)).fetchone()
    if f: con.execute("UPDATE cache SET aciertos=aciertos+1 WHERE hash=?", (h,)); con.commit()
    con.close(); return f["respuesta"] if f else None

def guardar(h: str, pregunta: str, respuesta: str):
    con = conectar(); con.execute("INSERT OR REPLACE INTO cache(hash, pregunta, respuesta) VALUES (?,?,?)", (h, pregunta, respuesta)); con.commit(); con.close()
