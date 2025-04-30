import time
import requests
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime

MONGO_URI = 'mongodb://storage:27017'
DB_NAME = 'waze_db'
COLLECTION_NAME = 'eventos'

ZONA = {
    "norte": -33.35,
    "sur": -33.45,
    "oeste": -70.6,
    "este": -70.5,
    "tipos": "alerts,traffic,users"
}

API_URL = (
    f"https://www.waze.com/live-map/api/georss"
    f"?top={ZONA['norte']}&bottom={ZONA['sur']}&left={ZONA['oeste']}&right={ZONA['este']}"
    f"&env=row&types={ZONA['tipos']}"
)

def establecer_conexion():
    print("Estableciendo conexión con MongoDB...", flush=True)
    try:
        cliente = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        cliente.admin.command("ping")
        print("MongoDB disponible.", flush=True)
        return cliente[DB_NAME][COLLECTION_NAME]
    except ServerSelectionTimeoutError:
        print("No se pudo conectar a MongoDB. ¿Está activo el contenedor 'storage'?", flush=True)
        exit(1)

def pedir_eventos():
    print("Solicitando datos desde la API de Waze...", flush=True)
    try:
        resultado = requests.get(API_URL)
        if resultado.status_code == 200:
            contenido = resultado.json()
            cantidad = len(contenido.get("users", []))
            print(f"Usuarios encontrados: {cantidad}", flush=True)
            return contenido
        else:
            print(f"Error {resultado.status_code} al hacer la petición", flush=True)
    except requests.RequestException as fallo:
        print(f"Falla en la conexión HTTP: {fallo}", flush=True)
    return None

def registrar_eventos(db_collection, info):
    usuarios = info.get("users", [])
    if usuarios:
        for evento in usuarios:
            evento["timestamp"] = datetime.utcnow().isoformat()
        print(f"Guardando {len(usuarios)} eventos...", flush=True)
        db_collection.insert_many(usuarios)

if __name__ == "__main__":
    print("Iniciando el scraper...", flush=True)
    coleccion = establecer_conexion()
    acumulado = 0

    while acumulado < 10000:
        resultado = pedir_eventos()
        if resultado:
            registrar_eventos(coleccion, resultado)
            acumulado += len(resultado.get("users", []))
        time.sleep(5)

    print(f"Finalizado. Total eventos insertados: {acumulado}", flush=True)

