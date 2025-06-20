from fastapi import FastAPI
from esp_api import router as esp_router

app = FastAPI(title="ESP32 Command Server")

app.include_router(esp_router, prefix="/esp", tags=["ESP32"])
