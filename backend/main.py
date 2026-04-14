from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from database import init_db
from routers import auth, cover_letters, resume


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    앱 시작/종료 시 실행할 코드 정의
    lifespan 방식은 FastAPI 0.93 이후 on_event 대신 권장되는 최신 방식
    yield 전 = 시작 시 실행, yield 후 = 종료 시 실행
    """
    # 서버 시작 시 — 테이블 없으면 자동 생성
    init_db()
    yield
    # 서버 종료 시 — 필요한 정리 작업 (현재는 없음)


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    # debug=True일 때만 Swagger 문서 활성화 — 운영 환경 노출 방지
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    # 허용할 출처 목록 — 로컬 Vue 개발 서버 + 추후 배포 도메인 추가
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,  # 쿠키/인증 헤더 허용
    allow_methods=["*"],     # GET, POST, PUT, DELETE 등 전부 허용
    allow_headers=["*"],     # Authorization 헤더 포함 전부 허용
)

# 라우터 등록 — 각 파일의 prefix가 앞에 붙음
# /auth/register, /auth/login, /cover-letters/..., /resume/...
app.include_router(auth.router)
app.include_router(cover_letters.router)
app.include_router(resume.router)


@app.get("/health")
def health():
    """
    서버 상태 확인용 엔드포인트
    Railway 배포 시 헬스체크로 사용됨
    """
    return {"status": "ok", "provider": settings.llm_provider}