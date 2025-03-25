```markdown
# 🚀 Chatbot con Flask, ChromaDB y Ollama

## 🌟 Características
- **Backend**: Flask (Python)
- **Vector DB**: ChromaDB
- **LLM**: Ollama con TinyLlama preconfigurado
- **Búsqueda**: OpenSearch
- **Caché**: Redis
- **Proxy**: Nginx

## 🛠 Stack Tecnológico
| Servicio    | Versión   | Puerto | Uso                     |
|-------------|-----------|--------|-------------------------|
| Flask       | 3.0       | 5000   | API principal           |
| ChromaDB    | 0.4.22    | 8000   | DB vectorial            |
| Ollama      | latest    | 11434  | Modelos LLM             |
| OpenSearch  | 2.10.0    | 9200   | Motor de búsqueda       |
| Redis       | 7.0       | 6379   | Caché                   |
| Nginx       | latest    | 80     | Reverse proxy           |

## 🚀 Instalación Rápida
```bash
git clone https://github.com/tu-usuario/flask-chatbot-llama.git
cd flask-chatbot-llama
docker-compose up --build -d
```

## 🔍 Endpoints
- `http://localhost` → Nginx (Frontend)
- `http://localhost:5000` → Flask API
- `http://localhost:8000` → ChromaDB
- `http://localhost:11434` → Ollama API

## 🤖 Ejemplo de Uso
```bash
curl -X POST "http://localhost/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"Explica Docker en 10 palabras"}'
```

## ⚙️ Configuración
### Variables clave en `.env`:
```ini
OLLAMA_MODELS=tinyllama
CHROMA_HOST=chromadb
OPENSEARCH_HOST=opensearch
```

## 🛠️ Comandos útiles
```bash
# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Eliminar todo
docker-compose down -v
```

## 📊 Estructura del Proyecto
```
.
├── app/
│   ├── main.py           # Lógica Flask
│   └── requirements.txt
├── conf.d/
│   └── default.conf      # Config Nginx
├── docker-compose.yml    # Servicios
└── Dockerfiles/          # Config por servicio
```

## 📄 Licencia
MIT License - Ver [LICENSE](LICENSE)
```

