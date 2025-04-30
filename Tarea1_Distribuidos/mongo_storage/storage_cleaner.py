from pymongo import MongoClient
from datetime import datetime
import pytz
import time
from pymongo.errors import ServerSelectionTimeoutError

def esperar_mongo(cliente, intentos=10, intervalo=3):
    for i in range(intentos):
        try:
            cliente.admin.command("ping")
            print("Mongo operativo.")
            return
        except ServerSelectionTimeoutError:
            print(f"Esperando Mongo... intento {i+1}/{intentos}")
            time.sleep(intervalo)
    raise RuntimeError("Mongo no respondió a tiempo.")

cliente = MongoClient("mongodb://mongo-storage:27017")
esperar_mongo(cliente)

db = cliente["waze_db"]
coleccion = db["eventos"]

def evento_valido(evento):
    claves = ["location", "speed", "mood"]
    if not all(c in evento and evento[c] not in [None, "", {}] for c in claves):
        return False
    if not isinstance(evento.get("location"), dict):
        return False
    if not isinstance(evento.get("speed"), (int, float)):
        return False
    return True

def limpiar_eventos():
    total = coleccion.count_documents({})
    print(f"Eventos totales antes de limpieza: {total}")

    eliminados = 0
    actualizados = 0

    for evento in coleccion.find({}):
        _id = evento["_id"]

        if not evento_valido(evento):
            coleccion.delete_one({"_id": _id})
            eliminados += 1
            continue

        if isinstance(evento.get("timestamp"), str):
            try:
                ts = datetime.fromisoformat(evento["timestamp"]).astimezone(pytz.UTC)
                coleccion.update_one({"_id": _id}, {"$set": {"timestamp": ts}})
                actualizados += 1
            except Exception as e:
                print(f"Timestamp inválido en {_id}: {e}")
                coleccion.delete_one({"_id": _id})
                eliminados += 1

    print(f"Eliminados: {eliminados}")
    print(f"Timestamps normalizados: {actualizados}")
    print(f"Eventos restantes: {coleccion.count_documents({})}")

if __name__ == "__main__":
    limpiar_eventos()
