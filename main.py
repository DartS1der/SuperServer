from fastapi import FastAPI
from database import Base, engine
from auth import router as auth_router
from esp_api import router as esp_router
from user_api import router as user_router  # мы его добавим в следующем шаге

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(esp_router, prefix="/esp", tags=["ESP32"])
# app.include_router(user_router, prefix="/user", tags=["User"])
