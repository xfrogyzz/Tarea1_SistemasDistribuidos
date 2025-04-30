# Proyecto de Sistemas Distribuidos - Entrega 1

## Descripción General

Este proyecto implementa un sistema distribuido que recolecta, almacena y analiza eventos de tráfico en tiempo real desde la plataforma Waze. El sistema está dividido en **cuatro módulos principales**, que se comunican de manera secuencial:

1. Scraper
2. Almacenamiento (MongoDB)
3. Generador de Tráfico
4. Sistema de Caché

---

## 1. Scraper

Este módulo se conecta a la **API Waze Live Map** para extraer información geoespacial de usuarios y eventos en la Región Metropolitana de Santiago, Chile.

- Extrae datos cada 5 segundos.
- Guarda los eventos en MongoDB.
- Objetivo: recolectar **10.000 eventos**.
