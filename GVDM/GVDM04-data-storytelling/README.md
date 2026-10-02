# GVDM04 — Data storytelling: del dato a la toma de decisiones

**Gestión y Visualización de Datos Masivos** · Profesor José María Pedraza Infante

Construcción de un informe de Power BI sobre la contabilidad de una cadena de tres hoteles,
con el objetivo de que el informe **cuente algo**, no sólo muestre cifras.

## Qué pedía la actividad

Partir de un conjunto de ficheros Excel con movimientos contables y presupuesto, montar el
modelo, crear las medidas de desviación, construir la visualización con filtros y tarjetas KPI,
y terminar con conclusiones de negocio. Como caso adicional, incorporar una dimensión de
categoría de hotel y una comparativa con datos del sector.

## Cómo se resolvió, paso a paso

### 0. Datos de partida y modelo

Los ficheros vienen duplicados con correcciones: se eligen `mcm.xlsx` (78 movimientos
contables del 1T 2019, ya corregidos) y `ptc.xlsx` (108 líneas de presupuesto mensual), más
los maestros de hoteles y departamentos. El modelo es en estrella: dos tablas de hechos
—Real y Presupuesto— contra las dimensiones de hotel, departamento y fecha.

### 1. Medidas de desviación

Ventas reales, presupuesto, desviación absoluta y porcentaje de ejecución, con DAX.

### 2 y 3. Análisis gráfico y filtros

Visuales por hotel y departamento, *Chiclet Slicer* para la selección y filtros por periodo.

### 4. Tarjetas KPI y semántica del color

Tarjetas de KPI con formato condicional, **invirtiendo el código de colores en las cuentas de
gasto**: en gastos, superar el presupuesto es malo, de modo que el verde y el rojo tienen que
significar lo contrario que en ingresos. Es un detalle pequeño que cambia por completo la
lectura del informe.

### 5. Conclusiones del primer trimestre

Lectura de negocio de las desviaciones encontradas.

### 6 y 7. Caso I: categoría de hotel y ventas por habitación

Se incorpora la dimensión **Categoría** desde el Excel de configuración (H1: 65 habitaciones
4★; H2: 130 habitaciones 3★; H3: 150 habitaciones 3★) y se añaden medidas e informe de
ventas por habitación, que es la métrica con la que el sector se compara de verdad.

### 8. Comparativa con el sector

Se trata en Power Query la tabla 2056 del INE con el **RevPAR** nacional por categoría
(enero-marzo 2019) y se enfrenta al RevPAR de cada hotel.

### 9. Conclusiones finales

El dato que cambia la historia: el hotel que parecía peor en cifras absolutas no lo es cuando
se compara con la media de su categoría.

> Las cifras del informe se contrastaron de forma independiente con un cálculo en
> Python/pandas; coinciden.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/modelo.tmdl` | Definición del modelo semántico de Power BI (tablas, relaciones y medidas DAX) |

> El fichero `.pbix` del informe no se incluye por tamaño; el modelo completo está en el `.tmdl`.
