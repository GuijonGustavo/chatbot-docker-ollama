# Proyecto FastAPI con ChromaDB, Redis, Ollama, Gunicorn y OpenSearch

Este es un proyecto de ejemplo que utiliza **FastAPI**, **ChromaDB**, **Redis**, **Ollama**, **Gunicorn** y **OpenSearch** para crear una API RESTful que gestiona documentos, consultas y realiza interacciones con Redis y otros servicios.

### Características

- **FastAPI**: Framework rápido para construir APIs con Python.
- **ChromaDB**: Base de datos para almacenar y consultar documentos.
- **Redis**: Usado como sistema de caché y con comandos básicos como `PING`.
- **Ollama**: Servicio para chatbot basado en Ollama.
- **Gunicorn**: Servidor WSGI para FastAPI.
- **OpenSearch**: Motor de búsqueda y análisis de datos.

---

## Comandos de `curl` con `jq`

### 1. **Verificar la salud de la API**

   Para obtener la respuesta del endpoint de salud (`/health`) y procesarla con `jq`:

   ```bash
   curl http://localhost:8000/health | jq .
   ```

   **Respuesta esperada**:

   ```json
   {
     "status": "healthy",
     "services": {
       "chromadb": "available"
     }
   }
   ```

### 2. **Consulta de documentos en ChromaDB**

   Para realizar una consulta y obtener solo los documentos de la respuesta:

   ```bash
   curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query":"documento de prueba","collection":"default","n_results":3}' | jq '.results.documents'
   ```

   **Respuesta esperada**:

   ```json
   [
     "Este es un documento de prueba",
     "Otro documento de prueba"
   ]
   ```

### 3. **Verificar Redis (PING)**

   Para verificar si Redis está activo, puedes usar `netcat` (`nc`) con el siguiente comando:

   ```bash
   echo -e "PING\r\n" | nc localhost 6379 | jq -R .
   ```

   **Respuesta esperada**:

   ```json
   "PONG"
   ```

### 4. **Consultar Ollama (Chatbot)**

   Para interactuar con el servicio Ollama y enviarle un mensaje:

   ```bash
   curl -X POST "http://localhost:11434/api/generate" \
   -H "Content-Type: application/json" \
   -d '{"model": "mistral", "prompt": "Hola, ¿cómo estás?"}' | jq .
   ```

   **Respuesta esperada** (dependerá del modelo de Ollama):

   ```json
   {
     "response": "¡Hola! Estoy bien, ¿y tú?"
   }
   ```

### 5. **Verificar OpenSearch (PING)**

   Para verificar si OpenSearch está funcionando correctamente:

   ```bash
   curl -XGET 'http://localhost:9200/_cluster/health?pretty' | jq .
   ```

   **Respuesta esperada**:

   ```json
   {
     "cluster_name": "docker-cluster",
     "status": "green",
     "timed_out": false,
     "number_of_nodes": 1,
     "number_of_data_nodes": 1,
     "active_primary_shards": 5,
     "active_shards": 5,
     "relocating_shards": 0,
     "initializing_shards": 0,
     "unassigned_shards": 0,
     "delayed_unassigned_shards": 0,
     "number_of_pending_tasks": 0,
     "number_of_in_flight_fetch": 0,
     "task_max_waiting_in_queue_millis": 0,
     "active_shards_percent_as_number": 100.0
   }
   ```

---

## Despliegue

### 1. **Levantar los servicios con Docker Compose**

Si estás usando Docker Compose, asegúrate de que tu archivo `docker-compose.yml` esté configurado correctamente para los contenedores `fastapi`, `chromadb`, `redis`, `ollama`, `gunicorn`, y `opensearch`. Luego, puedes levantar los servicios con:

```bash
docker-compose up
```

### 2. **Levantar los servicios manualmente**

Si no estás usando Docker Compose, puedes levantar los contenedores de la siguiente manera:

- **FastAPI + Gunicorn**:

   ```bash
   docker run -d -p 8000:8000 chatbot-docker-ollama-fastapi-chatbot
   ```

   O si necesitas usar **Gunicorn** para la ejecución de FastAPI:

   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
   ```

- **ChromaDB**:

   ```bash
   docker run -d -p 8001:8000 chatbot-docker-ollama-chromadb
   ```

- **Redis**:

   ```bash
   docker run -d -p 6379:6379 redis:7.0
   ```

- **Ollama**:

   ```bash
   docker run -d -p 11434:11434 chatbot-docker-ollama-ollama
   ```

- **OpenSearch**:

   ```bash
   docker run -d -p 9200:9200 -p 9600:9600 opensearchproject/opensearch:2.10.0
   ```
