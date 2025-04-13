from fastapi import FastAPI
from app import auth, crud
from app.auth import router as auth_router  # auth.py에 있는 router 객체 import
from app.database import engine  # Import the engine object from your database module
from app.routers import users  # ← users.py 위치

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(crud.router, prefix="/users")
app.include_router(users.router)  # ✅ 반드시 추가!

# auth 라우터 추가
app.include_router(auth_router, prefix="/auth", tags=["auth"])

print("🔥 Using DB at:", engine.url)