#!/bin/bash
# Pide la contraseña del usuario de Atlas sin mostrarla y lanza la carga
read -s -p 'Contraseña de mbda_loader: ' P; echo
P=$(python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=""))' "$P")
export MONGO_URI="mongodb+srv://mbda_loader:$P@<tu-cluster>.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
time ~/v/bin/python etl_atlas.py anwiki-latest-pages-articles.xml.bz2
