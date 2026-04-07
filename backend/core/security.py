# 인증 유틸리티
# - 비밀번호 bcrypt 해싱 / 검증
# - JWT 액세스 토큰 발급
# - FastAPI 의존성: 현재 로그인 사용자 조회
from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.config import settings
from database import get_db
from models.user import User

# Authorization: Bearer <token> 헤더를 파싱하는 스킴
bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    """비밀번호를 bcrypt로 해싱하여 반환"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """평문 비밀번호와 해시가 일치하는지 확인"""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(user_id: int) -> str:
    """user_id를 sub 클레임으로 담은 JWT 토큰 생성"""
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode(
        {"sub": str(user_id), "exp": expire},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    FastAPI 의존성 — Bearer 토큰을 검증하고 해당 User 객체를 반환.
    토큰이 없거나 유효하지 않으면 401 예외 발생.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 올바르지 않습니다",
    )
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user