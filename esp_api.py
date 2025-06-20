from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Device, Task

router = APIRouter()

# 📦 Вспомогательная функция для подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📥 Что ESP32 присылает
class ESPRequest(BaseModel):
    device_id: str

# 📤 Что сервер отдаёт ESP32
class ESPTaskResponse(BaseModel):
    start_time: str  # ISO-8601 строка
    duration_sec: int

# 📡 Запрос задачи по ID устройства
@router.post("/get_task", response_model=ESPTaskResponse)
def get_task(request: ESPRequest, db: Session = Depends(get_db)):
    # Находим устройство по ID
    device = db.query(Device).filter_by(device_id=request.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Ищем связанную задачу
    task = db.query(Task).filter_by(device_id=device.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="No task assigned")

    return ESPTaskResponse(
        start_time=task.start_time.isoformat(),
        duration_sec=task.duration_sec
    )
