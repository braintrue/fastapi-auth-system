from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import database, models, schemas
from app.auth import oauth2_scheme
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "changseop-secret"
ALGORITHM = "HS256"

def get_current_email(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.put("/users/me", response_model=schemas.User)
def update_user_me(update: schemas.UserUpdate, db: Session = Depends(database.get_db), email: str = Depends(get_current_email)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update.email:
        user.email = update.email
    if update.password:
        user.hashed_password = pwd_context.hash(update.password)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/me", status_code=204)
def delete_user_me(
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # refresh_token도 같이 삭제
    db.query(models.RefreshToken).filter(models.RefreshToken.user_id == user.id).delete()

    db.delete(user)
    db.commit()
    return
