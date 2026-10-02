"""Base de datos SQLite de la tienda: catálogo, pedidos, incidencias, memoria y caché."""
import sqlite3
from config import DB_PATH

PRODUCTOS = [
    ("P001", "Zapatillas running Kiprun KS900", "running", 99.99, 12),
    ("P002", "Zapatillas trail Evadict MT Cushion", "trail", 89.99, 0),
    ("P003", "Botas montaña Quechua MH500 impermeables", "montaña", 79.99, 7),
    ("P004", "Bicicleta gravel Triban GRVL 520", "ciclismo", 849.00, 3),
    ("P005", "Casco ciclismo Van Rysel RCR", "ciclismo", 69.99, 25),
    ("P006", "Reloj GPS Coros Pace 3", "electrónica", 229.00, 5),
    ("P007", "Esterilla yoga 5 mm", "fitness", 19.99, 40),
    ("P008", "Mancuernas ajustables 2x10 kg", "fitness", 54.99, 9),
    ("P009", "Chaqueta impermeable MH500", "montaña", 59.99, 14),
    ("P010", "Mochila trail 10 L", "trail", 34.99, 0),
]
PEDIDOS = [
    ("DT-1001", "laura.gomez@email.com", "P001", 1, "entregado", "2026-09-02"),
    ("DT-1002", "laura.gomez@email.com", "P007", 2, "en reparto", "2026-09-18"),
    ("DT-1003", "carlos.ruiz@email.com", "P004", 1, "entregado", "2026-08-21"),
    ("DT-1004", "carlos.ruiz@email.com", "P006", 1, "preparando", "2026-09-19"),
    ("DT-1005", "ana.perez@email.com", "P003", 1, "entregado", "2026-07-30"),
]

def conectar():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def inicializar():
    con = conectar(); c = con.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS productos(id TEXT PRIMARY KEY, nombre TEXT, categoria TEXT, precio REAL, stock INT);
    CREATE TABLE IF NOT EXISTS pedidos(id TEXT PRIMARY KEY, email TEXT, producto TEXT, unidades INT, estado TEXT, fecha TEXT);
    CREATE TABLE IF NOT EXISTS incidencias(id INTEGER PRIMARY KEY AUTOINCREMENT, pedido TEXT, tipo TEXT, descripcion TEXT, estado TEXT, creada TEXT DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS memoria(usuario TEXT, clave TEXT, valor TEXT, actualizada TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(usuario, clave));
    CREATE TABLE IF NOT EXISTS cache(hash TEXT PRIMARY KEY, pregunta TEXT, respuesta TEXT, aciertos INT DEFAULT 0, creada TEXT DEFAULT CURRENT_TIMESTAMP);
    """)
    if c.execute("SELECT COUNT(*) FROM productos").fetchone()[0] == 0:
        c.executemany("INSERT INTO productos VALUES (?,?,?,?,?)", PRODUCTOS)
        c.executemany("INSERT INTO pedidos VALUES (?,?,?,?,?,?)", PEDIDOS)
    con.commit(); con.close()

if __name__ == "__main__":
    inicializar(); print("BD inicializada en", DB_PATH)
