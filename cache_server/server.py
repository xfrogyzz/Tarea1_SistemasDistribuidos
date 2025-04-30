import os
from flask import Flask, jsonify
from pymongo import MongoClient
from cache_manager import LRUCache, FIFOCache
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configuración
CACHE_LIMIT = int(os.getenv("CACHE_SIZE", 15))
CACHE_POLICY = os.getenv("POLICY", "LRU")

# Inicializar cache según política
cache = LRUCache(CACHE_LIMIT) if CACHE_POLICY == "LRU" else FIFOCache(CACHE_LIMIT)

# Base de datos Mongo
client = MongoClient("mongodb://mongo-storage:27017")
db = client["waze_db"]
events = db["eventos"]

def transform(doc):
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

@app.route('/evento/<string:ident>', methods=['GET'])
def obtener_evento(ident):
    logging.info(f"→ Buscando: {ident}")
    result = cache.fetch(ident)

    if result:
        return jsonify(result)

    doc = events.find_one({"id": ident})
    if doc:
        parsed = transform(doc)
        cache.insert(ident, parsed)
        return jsonify(parsed)

    return jsonify({"error": "Evento no encontrado"}), 404

@app.route('/metrics')
def estadisticas():
    return jsonify(cache.stats())

if __name__ == '__main__':
    logging.info("Servidor de caché iniciado")
    app.run(host='0.0.0.0', port=5001)
