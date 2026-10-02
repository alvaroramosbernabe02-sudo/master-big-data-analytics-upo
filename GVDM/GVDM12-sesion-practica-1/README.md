# GVDM12 — Sesión práctica 1: ETL sobre Wikipedia y HBase

**Gestión y Visualización de Datos Masivos** · Profesor Dr. Carlos D. Barranco González

## Alcance de la entrega

Las actividades A2, A3 y A4 están resueltas con ejecución real. La **A1 (Talend Open Studio)
no se ejecutó por limitación de hardware**, y así se justifica en el documento: Talend Studio
for Big Data pide al menos 8 GB de RAM (16 recomendados), 2-4 núcleos y JDK 11, y el equipo
disponible no sostiene a la vez un IDE basado en Eclipse y una máquina virtual. **La carga que
en clase hace Talend se sustituyó por un script de Python equivalente** (extracción XPath →
documentos → MongoDB) y por la herramienta nativa `ImportTsv` de HBase, que reproducen la
misma lógica ETL con un consumo de memoria mínimo. El documento incluye además el
procedimiento completo que se habría seguido con un equipo adecuado.

## Cómo se resolvió, paso a paso

### A2. Top 10 de contribuidores de la Wikipedia

- **Extracción y carga** — `etl_wikipedia.py` recorre el dump XML, extrae los campos con XPath
  y los inserta como documentos en MongoDB.
- **Consulta y resultado** — `vecesAutor.js` agrega por autor y devuelve el top 10;
  `cuenta_y_muestra.py` comprueba el volumen cargado. El resultado está en `result.json`.

### A3. Multas de aparcamiento de Los Ángeles en HBase

- **Adquisición y muestra** del dataset abierto.
- **Carga en HBase** con `ImportTsv`, el cargador masivo nativo.
- **Consulta, exportación y suma** de los importes, con el resultado volcado a `out.csv`.

### A4. Propuesta de caso práctico con datos abiertos

Fuente elegida, por qué es interesante, qué análisis permite y planteamiento esquemático de
cómo se abordaría.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/etl_wikipedia.py` | ETL del dump de Wikipedia a MongoDB (sustituye al job de Talend) |
| `codigo/vecesAutor.js` | Agregación en MongoDB para el top 10 de contribuidores |
| `codigo/cuenta_y_muestra.py` | Comprobación del volumen cargado y muestra de documentos |
| `codigo/result.json`, `codigo/out.csv` | Resultados obtenidos |
