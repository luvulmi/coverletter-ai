# AI 커버레터 생성기

> JD(채용공고)와 이력서를 입력하면 AI가 맞춤형 커버레터를 실시간으로 생성해주는 웹 서비스

---

## 소개

JD와 이력서를 입력하면 Claude 또는 OpenAI가 맞춤형 커버레터 초안을 실시간 스트리밍으로 생성.
생성된 커버레터는 저장하고 관리 가능.

---

## 주요 기능

- JD + 이력서 입력 → AI 맞춤 커버레터 자동 생성
- SSE(Server-Sent Events) 기반 실시간 스트리밍 출력
- Claude / OpenAI 멀티 LLM 지원 — `.env` 한 줄로 교체
- 생성된 커버레터 히스토리 저장 및 관리
- JWT 기반 회원가입 / 로그인

---

## 기술 스택

### 백엔드
| 기술 | 버전 | 용도 |
|------|------|------|
| Python | 3.12 | 언어 |
| FastAPI | 0.135 | 웹 프레임워크 |
| SQLAlchemy | 2.0 | ORM |
| SQLite / PostgreSQL | - | 데이터베이스 |
| python-jose | 3.5 | JWT 인증 |
| bcrypt | 4.0 | 비밀번호 해싱 |
| anthropic | 0.88 | Claude API |
| openai | latest | OpenAI API |
| uv | latest | 패키지 매니저 |

### 프론트엔드
| 기술 | 버전 | 용도 |
|------|------|------|
| Vue 3 | 3.x | UI 프레임워크 |
| TypeScript | 5.x | 언어 |
| Vite | latest | 번들러 |
| Pinia | latest | 상태 관리 |
| Vue Router | 4.x | 라우팅 |
| Axios | latest | HTTP 클라이언트 |

---

## 아키텍처

```
[Vue 3 + TypeScript]
        |
        | HTTP / SSE
        |
[FastAPI Backend]
        |
        |── [Claude API / OpenAI API] ── 커버레터 스트리밍 생성
        |
        |── [SQLite / PostgreSQL] ── 사용자, 커버레터 히스토리
        |
        └── [JWT Auth] ── 인증/인가
```

### 멀티 LLM 전략 패턴

```
라우터
  └── stream_cover_letter()   ← 공통 진입점
          |
    llm_provider 분기
          ├── "claude"  → _stream_claude()
          └── "openai"  → _stream_openai()
```

`.env`의 `LLM_PROVIDER` 값만 바꾸면 코드 변경 없이 LLM 교체 가능

---

## 프로젝트 구조

```
coverletter-ai/
├── backend/
│   ├── core/
│   │   ├── config.py          # 환경변수 설정
│   │   └── security.py        # JWT, bcrypt 인증 유틸
│   ├── models/
│   │   ├── user.py            # User 테이블
│   │   └── cover_letter.py    # CoverLetter, Resume 테이블
│   ├── routers/
│   │   ├── auth.py            # 회원가입, 로그인
│   │   ├── cover_letters.py   # 커버레터 CRUD + SSE 스트리밍
│   │   └── resume.py          # 이력서 저장/조회
│   ├── schemas/
│   │   └── schemas.py         # Pydantic 요청/응답 스키마
│   ├── services/
│   │   └── llm_service.py     # Claude/OpenAI 멀티 LLM 연동
│   ├── database.py            # DB 연결, 세션
│   ├── main.py                # 앱 진입점
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── index.ts       # Axios 인스턴스 + 인터셉터
│   │   ├── stores/
│   │   │   └── auth.ts        # Pinia 인증 스토어
│   │   ├── views/
│   │   │   ├── LoginView.vue  # 로그인/회원가입
│   │   │   └── HomeView.vue   # 홈
│   │   └── router/
│   │       └── index.ts       # 라우터 + 네비게이션 가드
│   └── package.json
└── docker-compose.yml
```

---

## 로컬 실행 방법

### 사전 준비
- Python 3.12+
- Node.js 20+
- uv (`pip install uv`)
- Anthropic 또는 OpenAI API 키

### 백엔드

```bash
cd backend

# 환경변수 설정
cp .env.example .env
# .env 파일에 API 키 입력

# 패키지 설치 및 서버 실행
uv sync
uv run uvicorn main:app --reload --port 8000
```

### 프론트엔드

```bash
cd frontend

# 환경변수 설정
cp .env.example .env

# 패키지 설치 및 개발 서버 실행
npm install
npm run dev
```

### Docker로 실행

```bash
# 프로젝트 루트에서
cp backend/.env.example backend/.env
# .env 파일에 API 키 입력

docker-compose up --build
```

백엔드: `http://localhost:8000`  
프론트엔드: `http://localhost:5173`  
Swagger: `http://localhost:8000/docs` (DEBUG=true 시)

---

## API 엔드포인트

### 인증
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/auth/register` | 회원가입 |
| POST | `/auth/login` | 로그인 |
| GET | `/auth/me` | 내 정보 조회 |

### 커버레터
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/cover-letters/generate` | SSE 스트리밍 생성 |
| POST | `/cover-letters/` | 커버레터 저장 |
| GET | `/cover-letters/` | 목록 조회 |
| GET | `/cover-letters/{id}` | 단건 조회 |
| PUT | `/cover-letters/{id}` | 수정 |
| DELETE | `/cover-letters/{id}` | 삭제 |

### 이력서
| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/resume/` | 이력서 조회 |
| PUT | `/resume/` | 이력서 저장/수정 |

---

## 환경변수

### backend/.env

```env
DEBUG=true
DATABASE_URL=sqlite:///./coverletter.db

JWT_SECRET=your-secret-key
LLM_PROVIDER=claude              # "claude" 또는 "openai"
LLM_MODEL=claude-sonnet-4-20250514

ANTHROPIC_API_KEY=sk-ant-...     # Claude 사용 시
OPENAI_API_KEY=sk-...            # OpenAI 사용 시
```

### frontend/.env

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 구현 포인트

### SSE 스트리밍
Claude/OpenAI 응답을 `StreamingResponse`로 실시간 전송. 프론트는 `fetch` + `ReadableStream`으로 수신해서 타이핑 효과 구현.

### 멀티 LLM 전략 패턴
전략 패턴 적용으로 LLM 프로바이더 교체 시 코드 변경 없음. `.env`의 `LLM_PROVIDER`만 수정하면 됨.

### JWT 인증
`python-jose`로 토큰 발급/검증. FastAPI `Depends`로 의존성 주입해서 라우터마다 반복 코드 제거.

### IDOR 방지
단건 조회 시 `id`와 `user_id`를 동시에 필터링해서 타인 데이터 접근 차단.

---

## 진행 현황

- [x] 백엔드 API 전체 구현
- [x] JWT 인증
- [x] Claude / OpenAI 멀티 LLM 지원
- [x] SSE 스트리밍 테스트 완료
- [x] Docker 세팅
- [x] Vue 3 + TypeScript 프로젝트 세팅
- [x] Axios 인스턴스 + 인터셉터
- [x] Pinia 인증 스토어
- [x] 로그인 / 회원가입 페이지
- [ ] 이력서 저장 페이지
- [ ] 커버레터 생성 페이지 (SSE)
- [ ] 히스토리 페이지
- [ ] Railway + Vercel 배포