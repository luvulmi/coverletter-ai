import httpx

# 1. 로그인해서 토큰 받기
login_res = httpx.post(
    "http://localhost:8000/auth/login",
    json={"email": "test@test.com", "password": "test1234"}
)
token = login_res.json()["access_token"]
print(f"토큰 발급 성공: {token[:20]}...")

# 2. 스트리밍 호출
with httpx.stream(
    "POST",
    "http://localhost:8000/cover-letters/generate",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "company_name": "카카오",
        "position": "백엔드 개발자",
        "jd_text": "Python 백엔드 개발자를 찾습니다. FastAPI 경험자 우대.",
        "resume_text": "3년차 풀스택 개발자. Vue, Spring Boot, FastAPI 경험.",
    },
    timeout=60.0
) as response:
    for line in response.iter_lines():
        if line.startswith("data: "):
            chunk = line[6:]  # "data: " 제거
            if chunk == "[DONE]":
                print("\n\n--- 생성 완료 ---")
                break
            print(chunk, end="", flush=True)