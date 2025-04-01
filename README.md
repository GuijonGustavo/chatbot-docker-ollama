# Chatbot con FastAPI y ChromaDB

Este proyecto implementa un chatbot utilizando FastAPI como backend y ChromaDB para la gestión de documentos y consultas.

## Características de esta versión (`fastapi`)

- Implementación con **FastAPI** como framework principal.
- Uso de **ChromaDB** para almacenamiento y recuperación de documentos.
- **CORS habilitado** para permitir accesos desde distintos orígenes.
- Endpoints para **almacenamiento**, **búsqueda**, y **verificación de estado**.
- Contenedor Docker para ejecutar la aplicación.

## Endpoints y pruebas con `curl`

### 1️⃣ Verificar si el servicio está corriendo
```bash
curl -X GET http://localhost:8000/
```
#### 📌 Respuesta esperada:
```json
"¡Hola, FastAPI está funcionando!"
```

### 2️⃣ Verificar el estado de ChromaDB
```bash
curl -X GET http://localhost:8000/health
```
#### 📌 Respuesta esperada si ChromaDB está disponible:
```json
{
    "status": "healthy",
    "services": {"chromadb": "available"}
}
```

### 3️⃣ Almacenar documentos en ChromaDB
```bash
curl -X POST http://localhost:8000/store \
     -H "Content-Type: application/json" \
     -d '{"documents": [{"text": "Ejemplo de documento"}]}'
```
#### 📌 Respuesta esperada:
```json
{
    "status": "success",
    "message": "Documents added successfully",
    "documents_added": 1
}
```

### 4️⃣ Consultar documentos en ChromaDB
```bash
curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"query": "Ejemplo", "collection": "default", "n_results": 3}'
```
#### 📌 Respuesta esperada (si hay documentos coincidentes):
```json
{
    "status": "success",
    "results": { "documents": ["Ejemplo de documento"] }
}
```

## 📌 Notas
- La aplicación está configurada para ejecutarse en el puerto **8000**.
- **ChromaDB** debe estar corriendo en el puerto **8001**.
- Se recomienda probar los endpoints usando **Postman** o `curl`.

## 🚀 Ejecutar con Docker
Si utilizas Docker, asegúrate de que los contenedores están en ejecución:
```bash
docker-compose up -d
```
Puedes verificar los contenedores con:
```bash
docker ps
```


