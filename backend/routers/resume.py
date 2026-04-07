from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.security import get_current_user
from database import get_db
from models.cover_letter import Resume
from models.user import User
from schemas.schemas import ResumeResponse, ResumeUpsert

router = APIRouter(prefix="/resume", tags=["resume"])


@router.get("/", response_model=ResumeResponse)
def get_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    저장된 이력서 조회
    - 사용자당 이력서는 1개만 존재 (upsert 방식)
    - 없으면 404 반환
    """
    resume = db.query(Resume).filter(Resume.user_id == current_user.id).first()

    if not resume:
        raise HTTPException(status_code=404, detail="저장된 이력서가 없습니다")

    return resume


@router.put("/", response_model=ResumeResponse)
def upsert_resume(
    body: ResumeUpsert,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    이력서 저장 / 수정 (upsert)
    - 이력서가 없으면 생성, 있으면 내용 업데이트
    - 사용자당 이력서는 1개만 유지
    """
    resume = db.query(Resume).filter(Resume.user_id == current_user.id).first()

    if resume:
        # 기존 이력서 업데이트
        resume.content = body.content
    else:
        # 최초 저장
        resume = Resume(user_id=current_user.id, content=body.content)
        db.add(resume)

    db.commit()
    db.refresh(resume)
    return resume