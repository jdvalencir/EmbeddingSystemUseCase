from fastapi import FastAPI
import ollama
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Simulación de logs de sistemas embebidos
logs = [
    "Error en el sensor de temperatura",
    "Falla en la comunicación con el módulo WiFi",
    "Sobrecalentamiento en la CPU del sistema",
    "Pérdida de conexión con el motor principal",
    "Anomalía en la lectura del giroscopio",
    "Funcionamiento normal del sistema",
    "Error en la lectura del sensor de presión",
    "Falla en el sistema de refrigeración",
    "Sistema operativo cargado correctamente",
    "Error en la lectura del sensor de humedad"
    "Correcta inicialización del sistema",
]

# Generar embeddings para cada log usando el modelo `paraphrase-multilingual`
log_embeddings = [ollama.embeddings(model="paraphrase-multilingual", prompt=log)["embedding"] for log in logs]

@app.get("/buscar/")
def buscar_evento(consulta: str):
    # Convertir consulta a embedding
    consulta_emb = ollama.embeddings(model="paraphrase-multilingual", prompt=consulta)["embedding"]

    # Calcular similitud con logs existentes
    similitudes = cosine_similarity([consulta_emb], log_embeddings)[0]
    resultados = sorted(zip(logs, similitudes), key=lambda x: x[1], reverse=True)

    return {"resultados": resultados}  # Retornar los 3 más similares