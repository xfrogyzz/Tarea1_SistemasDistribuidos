# Proyecto de Sistemas Distribuidos - Entrega 1

## Descripción General

Este proyecto implementa un sistema distribuido que recolecta, almacena y analiza eventos de tráfico en tiempo real desde la plataforma Waze. El sistema está dividido en **cuatro módulos principales**, que se comunican de manera secuencial:

1. Scraper
2. Almacenamiento (MongoDB)
3. Generador de Tráfico
4. Sistema de Caché

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
