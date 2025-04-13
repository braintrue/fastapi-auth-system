import redis

# Redis 서버에 연결
r = redis.Redis(host='localhost', port=6379, db=0)

# Redis에 'test'라는 키를 저장하고 가져오기 (테스트용)
r.set('test', 'Hello, Redis!')
print(r.get('test'))  # 출력: b'Hello, Redis!'
