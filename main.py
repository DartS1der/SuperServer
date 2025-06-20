print("✅ main.py loaded — server is starting")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from models import User, Device, Task  # 👈 ВАЖНО
from auth import router as auth_router
from esp_api import router as esp_router
from user_api import router as user_router

app = FastAPI(title="ESP32 Command Server")

# Создаём таблицы в БД (если ещё не созданы)
Base.metadata.create_all(bind=engine)

# Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем маршруты
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(esp_router, prefix="/esp", tags=["ESP32"])
