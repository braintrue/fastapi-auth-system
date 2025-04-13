# app/init_db.py
from app.database import engine
from app.models import Base, User, RefreshToken

print("🚀 DB 초기화 중...")
Base.metadata.create_all(bind=engine)
print("✅ 테이블 생성 완료!")
