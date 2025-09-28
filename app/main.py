from fastapi import FastAPI
from app import auth, crud
from app.database import engine
from app.routers import users

app = FastAPI(
    title="FastAPI Auth System",
    description="🧠 RESTful 인증 API 시스템 - FastAPI 기반",
    version="1.0.0"
)

# Router 등록
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(crud.router, prefix="/users", tags=["User Management"])
app.include_router(users.router, tags=["User Profile"])

print("🔥 Using DB at:", engine.url)