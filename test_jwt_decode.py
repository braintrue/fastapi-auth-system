from jose import jwt  # 👈 가장 중요!!!
from datetime import datetime

SECRET_KEY = "changseop-secret"
ALGORITHM = "HS256"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuZXdncHRAY2hhbmdzZW9wLmtyIiwiZXhwIjoxNzQ1MTM3NDU0fQ.BuqK7-I17v_cniee7DsQo7kWLuSjz_a8YcCBqnGQMPM"
  # 여기에 복사한 JWT를 붙여넣으세요

try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("✅ 디코딩 성공:", decoded)
    exp = decoded.get("exp")
    print("⏰ 만료 시간:", datetime.utcfromtimestamp(exp))
except Exception as e:
    print("❌ 에러 발생:", e)
