import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi import APIRouter


# Inicializar FastAPI
app = FastAPI()

class PromptRequest(BaseModel):
    model: str = "tinyllama"
    prompt: str
    stream: bool = False
    options: dict = None

@app.post("/api/generate")
async def generate(prompt_data: PromptRequest):
    if prompt_data.model != "tinyllama":
        raise HTTPException(status_code=400, detail="Modelo no soportado")
    
    # Aquí tu lógica para llamar a TinyLlama
    response = call_tinyllama(
        prompt=prompt_data.prompt,
        temperature=prompt_data.options.get("temperature", 0.7),
        max_tokens=prompt_data.options.get("max_tokens", 200)
    )
    
    return {"response": response}


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
    """Consulta en ChromaDB y genera respuesta para el chatbot"""

    query_text = query_request.query
    collection_name = query_request.collection

    # Conectar a ChromaDB
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    collection = chroma_client.get_or_create_collection(collection_name)

    try:
        # Realizar la consulta
        results = collection.query(
            query_texts=[query_text],
            n_results=query_request.n_results
        )

        # Si no se encontraron resultados
        if not results['documents']:
            return {
                "status": "no_results",
                "message": "No se encontraron resultados relevantes."
            }

        # Generar respuesta (puedes agregar lógica más compleja aquí)
        response_text = "Aquí están los resultados relevantes:\n"
        for result in results['documents']:
            response_text += f"- {result}\n"

        return {
            "status": "success",
            "response": response_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)

