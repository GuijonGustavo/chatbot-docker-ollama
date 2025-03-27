#!/bin/bash

# ----------------------------
# VERIFICACIÓN DE SERVICIOS
# ----------------------------

echo -e "\n\033[1;36m=== Probando servicios ===\033[0m"

# 1. ChromaDB
echo -e "\n\033[1;33m[ChromaDB]\033[0m"
curl -s -o /dev/null -w "CromaDB Status: %{http_code}\n" http://localhost:8000/api/v1/heartbeat

# 2. OpenSearch
echo -e "\n\033[1;33m[OpenSearch]\033[0m"
curl -s -X GET "http://localhost:9200/_cluster/health?pretty" | grep -E '"status"|"nodes"'

# 3. Redis (usando redis-cli)
echo -e "\n\033[1;33m[Redis]\033[0m"
docker compose exec redis redis-cli PING

# 4. Ollama (modelos disponibles)
echo -e "\n\033[1;33m[Ollama]\033[0m"
curl -s http://localhost:11434/api/tags | jq '.models[] | .name'

# 5. Flask
echo -e "\n\033[1;33m[Flask]\033[0m"
curl -s -o /dev/null -w "Flask Status: %{http_code}\n" http://localhost:5000/health

# 6. Nginx
echo -e "\n\033[1;33m[Nginx]\033[0m"
curl -s -I http://localhost | grep "HTTP/1.1"

# ----------------------------
# VERIFICACIÓN DE DESCARGA
# ----------------------------

echo -e "\n\033[1;36m=== Verificando descarga Ollama ===\033[0m"

# 1. Ver logs de descarga
echo -e "\n\033[1;33m[Logs activos]\033[0m"
docker compose logs ollama --tail=5 | grep -i "pulling"

# 2. Ver archivos temporales
echo -e "\n\033[1;33m[Archivos temporales]\033[0m"
docker compose exec ollama ls -lh /root/.ollama/models | grep -i "tmp"

# 3. Probar generación de texto
echo -e "\n\033[1;33m[Prueba de generación]\033[0m"
curl -s http://localhost:11434/api/generate -d '{
  "model": "tinyllama:latest",
  "prompt": "Hola",
  "stream": false
}' | jq '.response'

# ----------------------------
# ESTADO DEL SISTEMA
# ----------------------------

echo -e "\n\033[1;36m=== Estado del sistema ===\033[0m"
docker compose ps
