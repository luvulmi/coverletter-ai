# 앱 전역 설정
# .env 파일에서 환경 변수를 읽어 Settings 인스턴스로 주입
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI 커버레터 생성기"
    debug: bool = False

    # SQLite 기본값 — 프로덕션에서는 PostgreSQL URL로 교체
    database_url: str = "sqlite:///./coverletter.db"

    # JWT 설정
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7일

    # 사용할 LLM 프로바이더 선택 — "claude" 또는 "openai"
    llm_provider: str = "openai"

    # 각 프로바이더별 API 키 — 사용하는 것만 .env에 입력하면 됨
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # 모델명 — 프로바이더 바꿀 때 여기도 같이 변경
    llm_model: str = "claude-sonnet-4-20250514"

    # CORS 허용 출처 — 쉼표로 구분해서 여러 개 입력 가능
    allowed_origins: str = "http://localhost:5173"

    class Config:
        # APP_ENV 값에 따라 .env 파일 선택
        # APP_ENV=development → .env.development
        # APP_ENV=production  → .env.production
        env = os.getenv("APP_ENV", "development")
        env_file = f".env.{env}"


# 전역 싱글톤 — 다른 모듈에서 from core.config import settings 로 사용
settings = Settings()