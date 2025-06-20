from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Device, Task
from schemas import DeviceCreate, TaskCreate
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
import auth

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Декодирование JWT и получение пользователя
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Привязка ESP32 к пользователю
@router.post("/add_device")
def add_device(device: DeviceCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if db.query(Device).filter_by(device_id=device.device_id).first():
        raise HTTPException(status_code=400, detail="Device already registered")

    new_device = Device(device_id=device.device_id, owner_id=user.id)
    db.add(new_device)
    db.commit()
    return {"msg": "Device added"}

# Установка задачи на устройство
@router.post("/set_task")
def set_task(task: TaskCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    device = db.query(Device).filter_by(device_id=task.device_id, owner_id=user.id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Если уже есть задача — заменяем
    existing_task = db.query(Task).filter_by(device_id=device.id).first()
    if existing_task:
        existing_task.start_time = task.start_time
        existing_task.duration_sec = task.duration_sec
    else:
        new_task = Task(device_id=device.id, start_time=task.start_time, duration_sec=task.duration_sec)
        db.add(new_task)

    db.commit()
    return {"msg": "Task set"}

# Получение списка устройств пользователя
@router.get("/devices")
def list_devices(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    devices = db.query(Device).filter_by(owner_id=user.id).all()
    return [{"device_id": d.device_id} for d in devices]
