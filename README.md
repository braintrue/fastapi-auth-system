# 🧠 RESTful 인증 API 시스템 - FastAPI 기반

> 염창섭이 직접 설계하고 구현한 실전 인증 시스템

---

## 🔥 핵심 기능

- ✅ **회원가입 / 로그인** (`/users/`, `/auth/login`)
- ✅ **JWT 기반 인증 (Access + Refresh Token)**
- ✅ **사용자 정보 조회 / 수정 / 삭제**
- ✅ **이메일 인증 코드 발송 + 검증 (Redis TTL 기반)**
- ✅ **FastAPI 기반 Swagger 문서 자동화**

---

## 🧩 기술 스택

| 분야       | 스택 |
|------------|------|
| 언어       | Python 3.13 |
| 웹 프레임워크 | FastAPI |
| DB         | SQLite (SQLAlchemy ORM) |
| 캐시/인증   | Redis (코드 만료 TTL) |
| 인증       | JWT (python-jose) |
| 암호화     | passlib[bcrypt] |
| API 테스트  | Swagger UI, Curl |
| 배포 예정  | GCP Cloud Run + GitHub Actions (CI/CD 자동화)

---

## ✅ 주요 엔드포인트 예시

### 🔐 이메일 인증 흐름

# 인증 코드 전송
curl -X POST http://localhost:8000/auth/send-code \
  -H "Content-Type: application/json" \
  -d '{"email": "your_email@domain.com"}'

# 인증 코드 검증
curl -X POST http://localhost:8000/auth/verify-code \
  -H "Content-Type: application/json" \
  -d '{"email": "your_email@domain.com", "code": "ABC123"}'

# 로그인 → access_token + refresh_token 발급
curl -X POST http://localhost:8000/auth/login ...

# 현재 사용자 정보 조회
curl -X GET http://localhost:8000/auth/me -H "Authorization: Bearer <token>"

# 토큰 재발급
curl -X POST http://localhost:8000/auth/refresh ...

# 1. Redis 실행
brew install redis
brew services start redis

# 2. 가상환경 및 의존성 설치
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. DB 초기화
python init_db.py

# 4. FastAPI 서버 실행
uvicorn app.main:app --reload

🧠 개발 목표
"실제 서비스에서 돌아갈 수 있는 인증 시스템"을 지향

보안, 예외처리, 데이터 정합성을 직접 고민하고 반영

클린 코드 + API 문서 자동화 + 협업 친화 구조

✨ 향후 확장 계획
✉️ SMTP 연동 통한 이메일 실전 발송

🚀 Docker + GitHub Actions 자동 배포 연동

📈 AI 기반 사용자 행동 분석 및 추천 기능 (흥미용 실험)

👨‍💻 개발자 소개
염창섭 | 실전 문제 해결형 백엔드 개발자

"고객의 불편을 코드로 해결하는 개발자.
기술에 감성과 시스템적 사고를 담습니다."

📧 이메일: ckdtjqdlgh@gmail.com

---

## ✅ 다음 작업

1. `.gitignore` 확인 (`venv`, `.db`, `.pyc`, `.env` 등 포함)
2. GitHub 저장소 생성 (예: `fastapi-auth-system`)
3. 리포에 올릴 커밋 메시지 예:
