from fastapi import FastAPI, HTTPException
import ollama
import numpy as np
import faiss
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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
data = [
    "Temperature Sensor Reading: 22.5C",
    "Humidity Sensor Reading: 45%",
    "Pressure Sensor Reading: 1013hPa",
    "GPS Coordinates: Lat 40.7128, Long -74.0060",
    "Battery Level: 85%",
    "CPU Usage: 45%",
    "Memory Usage: 60%",
    "Disk Usage: 70%",
    "Network Latency: 20ms",
    "Packet Loss: 0.2%",
    "Fan Speed: 1200 RPM",
    "Power Consumption: 5.5W",
    "WiFi Signal Strength: -65dBm",
    "Bluetooth Connection Status: Connected",
    "System Uptime: 12h 35m",
    "Device Boot Time: 2025-02-18 08:00:00",
    "Firmware Version: 1.2.3",
    "Software Update Available: No",
    "Sensor Calibration Required: No",
    "Last Maintenance Date: 2025-01-15",
    "Flash Memory Usage: 80%",
    "RTC Clock Sync Status: Synced",
    "Motor Speed: 1500 RPM",
    "Actuator Position: 35%",
    "Camera Status: Active",
    "Microphone Status: Muted",
    "Accelerometer Data: X:0.1 Y:0.2 Z:9.8",
    "Gyroscope Data: Pitch:0.5 Roll:0.3 Yaw:0.2",
    "Magnetometer Data: X:15.2 Y:-5.6 Z:32.1",
    "Proximity Sensor: Object Detected",
    "Infrared Sensor: No Obstacle Detected",
    "LIDAR Distance: 1.5m",
    "Ultrasonic Sensor: 0.9m",
    "Energy Harvesting Status: Active",
    "Heat Sink Temperature: 45C",
    "Error Log: Sensor Timeout",
    "Warning Log: High Temperature",
    "Info Log: System Restart",
    "Debug Log: Configuration Loaded",
    "Critical Log: Overvoltage Detected",
    "Bootloader Status: Successful",
    "Watchdog Timer: No Reset Needed",
    "Cloud Sync Status: Completed",
    "Edge Processing Load: 75%",
    "AI Model Inference Time: 35ms",
    "Data Transmission Rate: 1.2Mbps",
    "CAN Bus Status: Active",
    "I2C Communication: Successful",
    "SPI Communication: Timeout",
    "UART Buffer Overflow: No",
    "SD Card Status: Mounted"
]


# Función para obtener embeddings de Ollama
def get_embedding(text):
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return np.array(response["embedding"], dtype=np.float32)

# Paso 1: Generar embeddings para los datos
embeddings = np.array([get_embedding(text) for text in data])

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
        results = [{"key": i, "text": data[I[0][i]], "similarity": float(D[0][i])} for i in range(len(I[0]))]

        return {"query": query.text, "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ruta de prueba
@app.get("/")
def root():
    return {"message": "API de embeddings con FastAPI, Ollama y FAISS"}