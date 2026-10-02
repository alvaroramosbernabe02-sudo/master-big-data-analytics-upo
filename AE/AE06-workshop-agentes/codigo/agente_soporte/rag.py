"""Ejercicio 5. RAG local: fragmentación, embeddings con fastembed, recuperación top-k y citas."""
import os, re
from pathlib import Path
import numpy as np
from fastembed import TextEmbedding
from config import RAIZ

class BaseConocimiento:
    def __init__(self, carpeta=RAIZ / "conocimiento", k=3):
        self.k = k
        self.modelo = TextEmbedding(os.getenv("EMBEDDINGS_MODEL"), specific_model_path=os.getenv("EMBEDDINGS_PATH"), lazy_load=False)
        self.fragmentos = []  # (id_cita, documento, texto)
        for f in sorted(Path(carpeta).glob("*.md")):
            parrafos = [p.strip() for p in f.read_text(encoding="utf-8").split("\n") if p.strip() and not p.startswith("#")]
            for i, p in enumerate(parrafos, 1):
                self.fragmentos.append((f"{f.stem}#{i}", f.stem, p))
        self.matriz = np.array(list(self.modelo.embed([t for _, _, t in self.fragmentos])))
        self.matriz /= np.linalg.norm(self.matriz, axis=1, keepdims=True)

    def buscar(self, consulta: str, k=None):
        q = np.array(list(self.modelo.query_embed(consulta)))[0]; q /= np.linalg.norm(q)
        sims = self.matriz @ q
        idx = np.argsort(-sims)[: (k or self.k)]
        return [{"cita": self.fragmentos[i][0], "documento": self.fragmentos[i][1], "similitud": round(float(sims[i]), 3), "texto": self.fragmentos[i][2]} for i in idx]

_bc = None
def base():
    global _bc
    if _bc is None: _bc = BaseConocimiento()
    return _bc
