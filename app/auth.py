from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from datetime import datetime, timedelta
from pydantic import BaseModel
import redis
import random
import string
from app import schemas, models, database
from app.models import RefreshToken  # Ensure this model exists

import traceback  # ✅ 추가

# Config
SECRET_KEY = "changseop-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Router
router = APIRouter()


# Utility Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.utcnow() + timedelta(days=7)
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Routes

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    # ✅ RefreshToken 저장!
    new_token = models.RefreshToken(
        user_id=db_user.id,                         # ✅ user_id 필수
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(new_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=schemas.UserInfo)
def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        print("🚀 token:", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email}
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Could not validate token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/refresh", response_model=schemas.Token)
def refresh_token(refresh: schemas.TokenRefresh, db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(refresh.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        exp = payload.get("exp")

        if not email or not exp:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        if datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Refresh token expired")

        token_in_db = db.query(models.RefreshToken).filter_by(token=refresh.refresh_token).first()

        if not token_in_db:
            raise HTTPException(status_code=401, detail="Refresh token not found in DB")

        new_access_token = jwt.encode(
            {"sub": email, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {"access_token": new_access_token, "refresh_token": refresh.refresh_token, "token_type": "bearer"}

    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid JWT format or expired")
    except Exception as e:
        traceback.print_exc()  # ✅ 여기에 전체 에러 트레이스 찍기
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Redis 연결
r = redis.Redis(host='localhost', port=6379, db=0)

router = APIRouter()

class EmailRequest(BaseModel):
    email: str

class VerificationCodeRequest(BaseModel):
    email: str
    code: str

# 이메일 인증 코드 생성 및 Redis에 저장
@router.post("/send-code")
def send_verification_code(request: EmailRequest):
    # 이메일로 인증 코드 생성
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # 6자리 코드
    # Redis에 코드 저장 (expiration 5분)
    r.setex(request.email, timedelta(minutes=5), code)

    return {"message": "Verification code sent to your email", "code": code}  # 실제로는 이메일로 보내야 함

# 입력된 코드 검증
@router.post("/verify-code")
def verify_code(request: VerificationCodeRequest):
    stored_code = r.get(request.email)

    if not stored_code:
        raise HTTPException(status_code=400, detail="Verification code has expired or not sent")

    if stored_code.decode("utf-8") != request.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    return {"message": "Verification successful"}