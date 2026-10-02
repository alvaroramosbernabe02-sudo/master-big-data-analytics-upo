"""Cloud Run job de ingesta: descarga el fichero mensual On-Time Performance del BTS (US DOT),
lo descomprime y lo deja en la zona raw del data lake (Cloud Storage)."""
import io, os, sys, zipfile, datetime, requests
from google.cloud import storage

BUCKET = os.environ["BUCKET"]
ANIO, MES = int(os.getenv("ANIO", "2015")), int(os.getenv("MES", "1"))
URL = f"https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{ANIO}_{MES}.zip"

def main():
    print(f"[ingesta] descargando {URL}", flush=True)
    r = requests.get(URL, timeout=600, verify=False); r.raise_for_status()
    print(f"[ingesta] {len(r.content)/1e6:.1f} MB descargados", flush=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    csv = [n for n in z.namelist() if n.endswith(".csv")][0]
    destino = f"raw/ontime/anio={ANIO}/mes={MES:02d}/ontime_{ANIO}_{MES:02d}.csv"
    storage.Client().bucket(BUCKET).blob(destino).upload_from_string(z.read(csv), content_type="text/csv")
    print(f"[ingesta] OK -> gs://{BUCKET}/{destino} ({datetime.datetime.utcnow().isoformat()}Z)", flush=True)

if __name__ == "__main__":
    try: main()
    except Exception as e: print(f"[ingesta] ERROR {e}", file=sys.stderr); sys.exit(1)
