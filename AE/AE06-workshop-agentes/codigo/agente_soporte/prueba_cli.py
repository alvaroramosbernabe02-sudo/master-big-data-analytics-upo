import asyncio, json, sys, time
import db, agent
db.inicializar()
async def ev(p): print(f"  [TOOL paso {p['paso']}] {p['herramienta']}({json.dumps(p['argumentos'], ensure_ascii=False)}) -> {p['resultado'][:160]}")
async def conf(n, a): print(f"  [CONFIRMACIÓN] {n} {a} -> sí"); return True
async def main():
    hist=[]
    for q in sys.argv[1:]:
        print(f"\n>>> {q}")
        r = await agent.ejecutar(q, "cli", hist, ev, conf)
        print("RESPUESTA:", r["respuesta"]); print("   ", {k: r[k] for k in ("cache","avisos","tiempo")})
        hist += [{"role":"user","content":q},{"role":"assistant","content":r["respuesta"]}]
asyncio.run(main())
