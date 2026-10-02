#!/usr/bin/env python3
"""Carga de un dump de Wikipedia en MongoDB Atlas desde una VM de Compute Engine.
Misma lógica que el job de Talend de la Sesión Práctica 1 (XPath -> documento -> tMongoDBOutput),
cambiando sólo el destino: la cadena de conexión de Atlas (mongodb+srv, TLS) se lee de MONGO_URI
para no escribir la contraseña en el código."""
import bz2, os, sys, time, xml.etree.ElementTree as ET
from datetime import datetime
from pymongo import MongoClient

src = sys.argv[1]
NS = '{http://www.mediawiki.org/xml/export-0.11/}'
cli = MongoClient(os.environ['MONGO_URI'], appname='mbda-etl-gce')
col = cli['wikipedia']['articles']
col.drop()
t0 = time.time(); lote, total = [], 0
for ev, el in ET.iterparse(bz2.open(src), events=('end',)):
    if el.tag != NS + 'page':
        continue
    rev = el.find(NS + 'revision'); con = rev.find(NS + 'contributor'); txt = rev.find(NS + 'text')
    lote.append({
        'title': el.findtext(NS + 'title'),
        'ns': int(el.findtext(NS + 'ns')),
        'id': int(el.findtext(NS + 'id')),
        'redirect': el.find(NS + 'redirect') is not None,
        'revisionid': int(rev.findtext(NS + 'id')),
        'timestamp': datetime.fromisoformat(rev.findtext(NS + 'timestamp').replace('Z', '+00:00')),
        'contributorusername': con.findtext(NS + 'username') or con.findtext(NS + 'ip'),
        'contributorid': int(con.findtext(NS + 'id')) if con.findtext(NS + 'id') else None,
        'textbytes': int(txt.get('bytes', 0)) if txt is not None else 0,
    })
    total += 1
    if len(lote) == 1000:
        col.insert_many(lote); lote = []
        if total % 20000 == 0: print(f'  {total} documentos...', flush=True)
    el.clear()
if lote: col.insert_many(lote)
print(f'Documentos cargados en wikipedia.articles: {total} en {time.time() - t0:.0f} s')
print('count_documents:', col.count_documents({}))
print('Top 10 contribuidores (último editor):')
for d in col.aggregate([{'$group': {'_id': '$contributorusername', 'count': {'$sum': 1}}},
                        {'$sort': {'count': -1}}, {'$limit': 10}]):
    print(f"  {d['count']:>6}  {d['_id']}")
st = cli['wikipedia'].command('dbStats')
print(f"dataSize={st['dataSize']/1e6:.1f} MB  storageSize={st['storageSize']/1e6:.1f} MB  indexSize={st['indexSize']/1e6:.1f} MB")
