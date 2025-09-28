from fastapi import FastAPI
from app import auth, crud
from app.database import engine  # Import the engine object from your database module
from app.routers import users

app = FastAPI()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(crud.router, prefix="/users", tags=["users"])
app.include_router(users.router, tags=["user-management"])

print("🔥 Using DB at:", engine.url)