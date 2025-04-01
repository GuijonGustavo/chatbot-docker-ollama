import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

# Inicializar FastAPI
app = FastAPI()

# Configuración de ChromaDB
CHROMA_HOST = "chromadb"
CHROMA_PORT = 8000

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto si es necesario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo Pydantic para los datos
class Document(BaseModel):
    id: str = None
    text: str

class QueryRequest(BaseModel):
    query: str
    collection: str = "default"
    n_results: int = 3


@app.middleware("http")
async def before_request(request: Request, call_next):
    print("Esto se ejecuta antes de cada solicitud")
    response = await call_next(request)
    return response

@app.get("/")
async def home():
    return "¡Hola, FastAPI está funcionando!"

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado del servicio"""
    try:
        chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        chroma_client.heartbeat()
        return {
            "status": "healthy",
            "services": {"chromadb": "available"}
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"ChromaDB unavailable: {str(e)}"
        )

# Ruta para almacenar documentos en ChromaDB
@app.post('/store')
async def store(documents: list[Document]):
    """Almacena los documentos en ChromaDB"""
    
    # Verificar que se recibieron documentos
    if not documents:
        raise HTTPException(status_code=400, detail="No documents provided")

    # Generar ids automáticamente si no se pasan
    ids = []
    texts = []
    for doc in documents:
        if not doc.id:
            doc.id = str(uuid4())
        ids.append(doc.id)
        texts.append(doc.text)

    # Crear o obtener la colección
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    collection = chroma_client.get_or_create_collection("default")

    # Agregar los documentos a la colección
    try:
        collection.add(
            documents=texts,
            ids=ids
        )
        return {
            "status": "success",
            "message": "Documents added successfully",
            "documents_added": len(ids)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database operation failed: {str(e)}")

# Ruta para hacer consultas en ChromaDB
@app.post("/query")
async def query(query_request: QueryRequest):
    """Consulta en ChromaDB"""
    
    query_text = query_request.query
    collection_name = query_request.collection

    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    collection = chroma_client.get_or_create_collection(collection_name)

    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=query_request.n_results
        )
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)

