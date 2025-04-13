from jose import jwt
from datetime import datetime, timedelta

payload = {
    "sub": "changseop",
    "exp": datetime + timedelta(minutes=30)
}

token = jwt.encode(payload, "changseop-secret", algorithm="HS256")
print(token)
