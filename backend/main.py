from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import ollama
import faiss

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulación de logs de sistemas embebidos
df = pd.read_csv("data/logs.csv")

# Función para obtener embeddings de Ollama
def get_embedding(text):
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return np.array(response["embedding"], dtype=np.float32)

# Paso 1: Generar embeddings para los datos
embeddings = np.array([get_embedding(text) for text in df["log"].values])

# Paso 2: Normalizar embeddings para usar similitud de coseno
faiss.normalize_L2(embeddings)

# Paso 3: Crear índice en FAISS (Inner Product = Similaridad del coseno)
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# Modelo para la consulta
class QueryModel(BaseModel):
    text: str

@app.post("/search/")
def search_similar_texts(query: QueryModel):
    try:
        # Obtener embedding de la consulta
        query_embedding = get_embedding(query.text)
        faiss.normalize_L2(query_embedding.reshape(1, -1))  # Normalizar consulta

        # Buscar los 3 textos más similares
        D, I = index.search(query_embedding.reshape(1, -1), 3)

        # Construir respuesta
        results = [{ "date": df["date"][i], "key": i, "text": df["log"][I[0][i]], "similarity": float(D[0][i])} for i in range(len(I[0]))]

        return {"query": query.text, "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ruta de prueba
@app.get("/")
def root():
    return {"message": "API de embeddings con FastAPI, Ollama y FAISS"}