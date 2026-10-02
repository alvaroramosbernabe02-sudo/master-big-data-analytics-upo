# Cuenta las líneas de parking-citations.csv leyendo el ZIP en streaming
# (sin descomprimir 2 GB a disco) y guarda las 100.000 primeras (cabecera incluida)
import zipfile, time
t = time.time()
z = zipfile.ZipFile('archive.zip')
n = 0
with z.open('parking-citations.csv') as f, open('parking-small.csv', 'wb') as o:
    for line in f:
        if n < 100000:
            o.write(line)
        n += 1
print('lineas', n, 'seg', round(time.time() - t, 1))
