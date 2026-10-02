#!/usr/bin/env python3
"""ETL del caso práctico 1 (sustituye al job de Talend):
Extract : lee el dump XML de la Wikipedia en extremeño (pages-articles.xml.bz2) en streaming.
Transform: aplana cada <page> a un documento JSON (mismos campos que el job de clase: title, ns, id,
           revisionid, timestamp, contributorusername, contributorid, textbytes).
Load    : inserta en MongoDB, base de datos 'wikipedia', colección 'articles' (insertMany por lotes)."""
import bz2, sys, xml.etree.ElementTree as ET
from datetime import datetime
from pymongo import MongoClient

src = sys.argv[1]
NS = '{http://www.mediawiki.org/xml/export-0.11/}'
col = MongoClient('mongodb://localhost:27017')['wikipedia']['articles']
col.drop()
lote, total = [], 0
for ev, el in ET.iterparse(bz2.open(src), events=('end',)):
    if el.tag != NS + 'page':
        continue
    rev = el.find(NS + 'revision'); con = rev.find(NS + 'contributor'); txt = rev.find(NS + 'text')
    doc = {
        'title': el.findtext(NS + 'title'),
        'ns': int(el.findtext(NS + 'ns')),
        'id': int(el.findtext(NS + 'id')),
        'redirect': el.find(NS + 'redirect') is not None,
        'revisionid': int(rev.findtext(NS + 'id')),
        'timestamp': datetime.fromisoformat(rev.findtext(NS + 'timestamp').replace('Z', '+00:00')),
        'contributorusername': con.findtext(NS + 'username') or con.findtext(NS + 'ip'),
        'contributorid': int(con.findtext(NS + 'id')) if con.findtext(NS + 'id') else None,
        'textbytes': int(txt.get('bytes', 0)) if txt is not None else 0,
    }
    lote.append(doc); total += 1
    if len(lote) == 1000:
        col.insert_many(lote); lote = []
    el.clear()
if lote: col.insert_many(lote)
print(f'Documentos cargados en wikipedia.articles: {total}')
