# GVDM07 — Bases de datos masivamente paralelas (HBase)

**Gestión y Visualización de Datos Masivos** · Profesor Dr. Carlos D. Barranco González

La actividad más de sistemas de todo el máster: levantar HBase, romperlo a propósito y
observar cómo se recupera.

## Entorno

Ubuntu 24.04 (2 vCPU, 7 GB de RAM), OpenJDK 17 y Apache HBase 2.6.6 sobre sistema de
ficheros local, con ZooKeeper gestionado por el propio HBase. Se sigue la opción de perfil
desarrollador: instalación propia en **modo pseudo-distribuido**, con cada demonio
(ZooKeeper, HMaster, HRegionServer) en su propia JVM.

## Cómo se resolvió, paso a paso

### A1. Instalación pseudo-distribuida

`hbase.cluster.distributed=true`, `hbase.rootdir=file:///…` y desactivación de
`hbase.unsafe.stream.capability.enforce` (necesaria al no haber HDFS). En `hbase-env.sh` se
fija `JAVA_HOME`, `HBASE_MANAGES_ZK=true` y un heap de 512 MB. Como los scripts de
arranque usan SSH contra `localhost`, se configura acceso por clave sin contraseña.
`start-hbase.sh` levanta en orden ZooKeeper → HMaster → HRegionServer.

### A2. Caída del único maestro

Se mata el HMaster y se observa qué sigue funcionando y qué no: las lecturas y escrituras
sobre regiones ya asignadas continúan, pero se pierde la capacidad de asignar regiones,
crear tablas o balancear.

### A3. Maestros de respaldo y conmutación por error

Se arrancan maestros de backup y se fuerza la caída del activo para ver la elección del nuevo
maestro a través de ZooKeeper.

### A4. Ampliación a cinco servidores de regiones

Se escala el clúster y se comprueba el reparto de regiones.

### A5. Carga de datos, regiones y `hbase:meta`

Se carga una tabla de clientes y se responde, con evidencia de la interfaz web y del `scan`
de la tabla META: en cuántas regiones se ha dividido la tabla y por qué, qué información
expone la interfaz y cuál es el cometido real de `hbase:meta` como catálogo de ubicación de
regiones.

### A6. Split, move, caída de un region server y merge

El bloque más interesante: se fuerza el particionado de una región (`split`), se mueve una
región a otro servidor (`move`), se tira un region server para ver la reasignación automática
y se fusionan dos regiones (`merge`).

### A7 (opcional). Instalación completamente distribuida

Un clúster real sobre **Docker Compose**: HDFS (NameNode y DataNodes), ZooKeeper y HBase
en contenedores separados, con su propio `Dockerfile` y `hbase-site.xml`. Los scripts
PowerShell `s1/s2/s3.ps1` automatizan el despliegue y la verificación; las salidas reales de
cada comprobación están en `codigo/A7_hbase_distribuido/work/`.

## Contenido de esta carpeta

| Ruta | Qué es |
|---|---|
| `entrega/` | Documento entregado en PDF |
| `codigo/A7_hbase_distribuido/docker-compose.yml` | Clúster distribuido: HDFS + ZooKeeper + HBase |
| `codigo/A7_hbase_distribuido/hbase/` | `Dockerfile` y `hbase-site.xml` de la imagen de HBase |
| `codigo/A7_hbase_distribuido/s1.ps1`, `s2.ps1`, `s3.ps1` | Despliegue y verificación paso a paso |
| `codigo/A7_hbase_distribuido/work/` | Salidas reales de las comprobaciones (`dfsadmin`, `status`, `fsck`, ZooKeeper…) |
| `codigo/hbase_A5_clientes.hb` | Script del shell de HBase para la carga de la A5 |
