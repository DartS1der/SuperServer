from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

# Пример базы данных (временное хранилище в памяти)
esp_tasks = {
    "esp32-001": {"start_time": "2025-06-20T16:00:00", "duration_sec": 10},
    "esp32-002": {"start_time": "2025-06-20T17:00:00", "duration_sec": 20},
}

class ESPRequest(BaseModel):
    device_id: str

class ESPTaskResponse(BaseModel):
    start_time: str  # ISO формат времени
    duration_sec: int

@router.post("/get_task", response_model=ESPTaskResponse)
def get_task(request: ESPRequest):
    if request.device_id not in esp_tasks:
        raise HTTPException(status_code=404, detail="Device not found")

    task = esp_tasks[request.device_id]
    return ESPTaskResponse(**task)
