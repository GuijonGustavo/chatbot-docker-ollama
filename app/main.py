import requests
import chromadb
from flask import Flask, request, jsonify
from uuid import uuid4
from flask_cors import CORS

app = Flask(__name__)

# Configuración de ChromaDB
CHROMA_HOST = "chromadb"
CHROMA_PORT = 8000

# Habilitar CORS
CORS(app)

@app.before_request
def check_services():
    """Verifica que los servicios esenciales estén disponibles"""
    try:
        # Verificar conexión con ChromaDB
        chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        chroma_client.heartbeat()  # Lanza excepción si no hay conexión
    except Exception as e:
        return jsonify({
            "error": "Service unavailable",
            "message": f"ChromaDB connection failed: {str(e)}"
        }), 503

@app.route("/")
def home():
    return "¡Hola, Flask está funcionando!"

@app.route("/health")
def health_check():
    """Endpoint para verificar el estado del servicio"""
    try:
        chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        chroma_client.heartbeat()
        return jsonify({
            "status": "healthy",
            "services": {
                "chromadb": "available"
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "services": {
                "chromadb": f"unavailable: {str(e)}"
            }
        }), 503

# Ruta para almacenar documentos en ChromaDB
@app.route('/store', methods=['POST'])
def store():
    data = request.get_json()
    
    # Verificar que se recibieron documentos
    if not data or 'documents' not in data:
        return jsonify({"error": "No documents provided"}), 400
    
    documents = data['documents']

    # Generar ids automáticamente si no se pasan
    ids = []
    texts = []
    for doc in documents:
        if 'id' not in doc:
            doc['id'] = str(uuid4())
        ids.append(doc['id'])
        texts.append(doc['text'])
    
    # Crear o obtener la colección
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    collection = chroma_client.get_or_create_collection("default")
    
    # Agregar los documentos a la colección
    try:
        collection.add(
            documents=texts,
            ids=ids
        )
        return jsonify({
            "status": "success",
            "message": "Documents added successfully",
            "documents_added": len(ids)
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Database operation failed",
            "message": str(e)
        }), 500

# Ruta para hacer consultas en ChromaDB
@app.route("/query", methods=["POST"])
def query():
    """Consulta en ChromaDB"""
    data = request.json
    
    if not data or 'query' not in data:
        return jsonify({"error": "No query provided"}), 400
    
    query_text = data['query']
    collection_name = data.get("collection", "default")

    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    collection = chroma_client.get_or_create_collection(collection_name)
    
    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=data.get("n_results", 3)
        )
        return jsonify({
            "status": "success",
            "results": results
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Query failed",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
