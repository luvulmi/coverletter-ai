from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI 커버레터 생성기"
    debug: bool = False

    database_url: str = "sqlite:///./coverletter.db"

    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7일

    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-20250514"

    class Config:
        env_file = ".env"


settings = Settings()