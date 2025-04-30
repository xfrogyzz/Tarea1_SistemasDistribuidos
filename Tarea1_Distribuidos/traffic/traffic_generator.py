
import time
import os
import requests
import random
import numpy as np
from pymongo import MongoClient

# Parámetros de conexión
MONGO_URI = "mongodb://mongo-storage:27017"
CACHE_URL = "http://cache:5001"

def cache_disponible(endpoint="/metrics", reintentos=10, espera=3):
    url = f"{CACHE_URL}{endpoint}"
    for intento in range(reintentos):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print("Caché operativo.")
                return True
        except requests.ConnectionError:
            print(f"Caché no disponible, reintento {intento + 1}/{reintentos}")
            time.sleep(espera)
    raise RuntimeError("No se pudo acceder al caché tras varios intentos.")

def extraer_user_ids():
    cliente = MongoClient(MONGO_URI)
    eventos = cliente["waze_db"]["eventos"]
    ids = eventos.distinct("id")
    print(f"Se encontraron {len(ids)} IDs únicos.")
    return ids

def distribucion_empirica():
    cliente = MongoClient(MONGO_URI)
    eventos = cliente["waze_db"]["eventos"]
    datos = list(eventos.aggregate([{"$group": {"_id": "$id", "n": {"$sum": 1}}}]))
    ids = [e["_id"] for e in datos]
    pesos = [e["n"] for e in datos]
    print(f"Distribución empírica: {len(ids)} IDs.")
    return ids, pesos

def generador_trafico(modo="poisson", tasa=1.0):
    if modo == "empirical":
        ids, pesos = distribucion_empirica()
    else:
        ids = extraer_user_ids()
        pesos = None

    if not ids:
        print("No hay IDs disponibles. Verifica si el scraper insertó eventos.")
        return

    print(f"🚦 Iniciando tráfico con modo: {modo}")

    while True:
        try:
            if modo == "poisson":
                espera = np.random.poisson(tasa)
                usuario = random.choice(ids)
            elif modo == "uniform":
                espera = 1
                usuario = random.choice(ids)
            elif modo == "empirical":
                espera = 1
                usuario = random.choices(ids, weights=pesos, k=1)[0]
            else:
                print("Modo no soportado.")
                break

            print(f"Consultando usuario ID: {usuario} con modo {modo}")
            respuesta = requests.get(f"{CACHE_URL}/evento/{usuario}")
            if respuesta.status_code == 200:
                print(f"Encontrado: {usuario}")
            elif respuesta.status_code == 404:
                print(f"No encontrado: {usuario}")
            else:
                print(f"Código inesperado: {respuesta.status_code}")

            time.sleep(max(espera, 1))

        except KeyboardInterrupt:
            print("Generador detenido manualmente.")
            break
        except Exception as ex:
            print(f"Error en ejecución: {ex}")
            time.sleep(2)

if __name__ == "__main__":
    modo = os.getenv("MODE", "poisson")
    tasa = float(os.getenv("RATE", "2.0"))

    cache_disponible()
    generador_trafico(modo=modo, tasa=tasa)
