import functions_framework
from google.cloud import storage

cliente = storage.Client()

@functions_framework.cloud_event
def borrar_fichero(cloud_event):
    """Se dispara con google.cloud.storage.object.v1.finalized y borra el fichero subido."""
    datos = cloud_event.data
    bucket, nombre = datos["bucket"], datos["name"]
    print(f"Evento {cloud_event['type']} id={cloud_event['id']}: subido gs://{bucket}/{nombre} ({datos.get('size')} bytes)")
    cliente.bucket(bucket).blob(nombre).delete()
    print(f"Fichero gs://{bucket}/{nombre} BORRADO por la Cloud Run function")
