from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import bcrypt

from core.security import create_access_token, get_current_user
from database import get_db
from models.user import User
from schemas.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse

# prefix: 이 라우터의 모든 엔드포인트 앞에 /auth가 붙음
# tags: Swagger 문서에서 그룹으로 묶임
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    """
    회원가입
    - 이메일 중복 확인
    - 비밀번호 bcrypt 해싱 후 저장
    - 가입 즉시 JWT 발급 (로그인 불필요)
    """
    # 이미 존재하는 이메일인지 확인
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다")

    # 비밀번호 단방향 해싱 — 원문은 DB에 저장하지 않음
    hashed = bcrypt.hashpw(
        body.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # 사용자 생성 및 저장
    user = User(email=body.email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)  # DB에서 생성된 id, created_at 등 갱신

    # 가입 즉시 토큰 발급
    return TokenResponse(access_token=create_access_token(user.id))


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    로그인
    - 이메일로 사용자 조회
    - bcrypt로 비밀번호 검증
    - 검증 성공 시 JWT 발급
    """
    # 이메일로 사용자 조회
    user = db.query(User).filter(User.email == body.email).first()

    # 사용자 없거나 비밀번호 불일치 — 보안상 동일한 메시지 반환
    if not user or not bcrypt.checkpw(
        body.password.encode("utf-8"),
        user.password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다")

    return TokenResponse(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    """
    내 정보 조회
    - JWT 토큰 검증은 get_current_user에서 처리
    - 검증 성공 시 현재 사용자 정보 반환
    """
    return current_user