"""Ejercicio 8 (extra). Evaluación automática de la calidad del agente.

Se combinan dos evaluadores complementarios:
  1. Comprobación determinista: los datos que la respuesta DEBE contener (regex).
  2. LLM-as-a-Judge: un segundo rol del mismo modelo puntúa la respuesta frente a una referencia.
El contraste entre ambos es en sí mismo un resultado: ver evaluacion en la memoria.
"""
import asyncio, json, re
import db, agent
from config import cliente, LLM_MODEL
db.inicializar()

CASOS = [
    {"p": "¿Cuánto cuesta el envío estándar y a partir de qué importe es gratis?",
     "ref": "4,90 €; gratis desde 60 €",
     "debe": [r"4[,.]90", r"\b60\b"]},
    {"p": "¿Cuántos años de garantía tienen los productos?",
     "ref": "3 años de garantía legal (bicicletas: 5 años en el cuadro)",
     "debe": [r"\b3\b", r"garant"]},
    {"p": "¿En qué estado está el pedido DT-1004?",
     "ref": "preparando",
     "debe": [r"prepar"]},
    {"p": "Quiero devolver unas zapatillas compradas hace 40 días, ¿puedo?",
     "ref": "No: el plazo de devolución es de 30 días",
     "debe": [r"\b30\b"]},
]

JUEZ = """Eres un evaluador. Comprueba si la RESPUESTA contiene el dato de la REFERENCIA.
Puntúa 5 si lo contiene y no afirma nada falso; 3 si lo contiene de forma incompleta; 1 si falta o se contradice.
La información verdadera adicional no resta puntos. "correcta" es true si la puntuación es 4 o 5.
Devuelve SOLO un JSON: {{"correcta": true/false, "puntuacion": 1-5, "motivo": "..."}}
PREGUNTA: {p}
REFERENCIA: {r}
RESPUESTA: {a}"""

async def main():
    total, aciertos = 0, 0
    for c in CASOS:
        r = await agent.ejecutar(c["p"], "evaluador", [])
        texto = r["respuesta"]
        ok_regla = all(re.search(x, texto, re.I) for x in c["debe"])
        j = cliente.chat.completions.create(model=LLM_MODEL, temperature=0,
            messages=[{"role": "user", "content": JUEZ.format(p=c["p"], r=c["ref"], a=texto)}]).choices[0].message.content
        v = json.loads(re.search(r"\{.*\}", j, re.S).group(0))
        total += v["puntuacion"]; aciertos += ok_regla
        print(f"- {c['p']}\n  respuesta: {texto}\n  regla (contiene {c['debe']}): {'OK' if ok_regla else 'FALLO'}\n  juez LLM: {v['puntuacion']}/5 -> {v['motivo'][:90]}")
    n = len(CASOS)
    print(f"\nComprobacion determinista: {aciertos}/{n} casos correctos ({100*aciertos/n:.0f} %)")
    print(f"LLM-as-a-Judge (qwen2.5:3b): {total/n:.2f} / 5 de media")
asyncio.run(main())
