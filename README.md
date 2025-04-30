# Proyecto de Sistemas Distribuidos - Entrega 1

## Descripción General

Este proyecto busca desarrollar una plataforma basada en datos colaborativos obtenidos desde Waze para monitorear y analizar el tráfico en la Región Metropolitana de Santiago. La implementación considera un enfoque modular que incluye componentes de scraping, almacenamiento, generación de tráfico sintético y caching. El sistema se ejecuta en contenedores Docker y está diseñado para ser escalable, tolerante a fallos y extensible a otras regiones. Enfocado en la recolección y gestión eficiente de eventos de tráfico.

---

## Uso con Docker

### 1. Levantar todos los servicios
docker compose up --build

### 2. Verificar que MongoDB esté funcionando
docker exec -it mongo-storage mongosh

### 3. Ya dentro del shell de MongoDB, poner el siguiente comando:
use waze_db

db.eventos.count()

### 4. Ver logs del generador de tráfico dentro de la carpeta traffic
cd traffic
docker logs -f traffic_generator

### 5. Ver estadísticas del sistema de caché(Se mostrará la tasa de hits, de miss y cuanto es el tamaño actual del caché).
http://localhost:5001/metrics 

### 6. Parar todos los servicios
docker compose down
