from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class DeviceCreate(BaseModel):
    device_id: str

class TaskCreate(BaseModel):
    device_id: str
    start_time: datetime
    duration_sec: int
