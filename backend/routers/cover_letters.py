from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from core.security import get_current_user
from database import get_db
from models.cover_letter import CoverLetter, Resume
from models.user import User
from schemas.schemas import (
    CoverLetterResponse,
    CoverLetterSaveRequest,
    CoverLetterUpdate,
    GenerateRequest,
)
from services.llm_service import stream_cover_letter

router = APIRouter(prefix="/cover-letters", tags=["cover-letters"])


@router.post("/generate")
def generate(
    body: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    커버레터 스트리밍 생성 (SSE 방식)
    - resume_text가 없으면 저장된 이력서 사용
    - StreamingResponse로 Claude 응답을 실시간 전송
    - 프론트에서 EventSource 또는 fetch + ReadableStream으로 수신
    """
    # 이력서 텍스트 결정 — 직접 입력 > 저장된 이력서
    resume_text = body.resume_text
    if not resume_text:
        resume = db.query(Resume).filter(Resume.user_id == current_user.id).first()
        if not resume:
            raise HTTPException(status_code=400, detail="이력서를 먼저 저장해주세요")
        resume_text = resume.content

    def event_stream():
        """
        SSE(Server-Sent Events) 포맷으로 청크 전송
        - 포맷: "data: {텍스트}\n\n"
        - 프론트는 이 포맷을 파싱해서 실시간으로 화면에 출력
        - 완료 시 [DONE] 시그널 전송
        """
        try:
            for chunk in stream_cover_letter(
                company_name=body.company_name,
                position=body.position,
                jd_text=body.jd_text,
                resume_text=resume_text,
            ):
                # 줄바꿈을 특수 구분자로 치환
                safe_chunk = chunk.replace("\n", "\\n")
                yield f"data: {safe_chunk}\n\n"
        except Exception as e:
            # 에러 발생 시 클라이언트에 알림
            yield f"data: [ERROR] {str(e)}\n\n"
        finally:
            # 스트리밍 완료 시그널 — 프론트에서 연결 종료 트리거로 사용
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",        # 브라우저 캐싱 방지
            "X-Accel-Buffering": "no",           # nginx 버퍼링 비활성화
            "Connection": "keep-alive",          # 연결 유지
        },
    )


@router.post("/", response_model=CoverLetterResponse, status_code=201)
def save(
    body: CoverLetterSaveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    생성된 커버레터 저장
    - 스트리밍으로 생성 완료 후 프론트에서 전체 텍스트를 모아 저장 요청
    - generate와 save를 분리한 이유: 스트리밍 중엔 DB 저장 타이밍을 잡기 어려움
    """
    cover_letter = CoverLetter(
        user_id=current_user.id,
        company_name=body.company_name,
        position=body.position,
        jd_text=body.jd_text,
        content=body.content,
    )
    db.add(cover_letter)
    db.commit()
    db.refresh(cover_letter)
    return cover_letter


@router.get("/", response_model=List[CoverLetterResponse])
def list_cover_letters(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    내 커버레터 목록 조회
    - 최신순 정렬
    - 본인 것만 조회 (user_id 필터)
    """
    return (
        db.query(CoverLetter)
        .filter(CoverLetter.user_id == current_user.id)
        .order_by(CoverLetter.created_at.desc())
        .all()
    )


@router.get("/{cover_letter_id}", response_model=CoverLetterResponse)
def get_cover_letter(
    cover_letter_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    특정 커버레터 조회
    - cover_letter_id + user_id 동시 필터로 타인 접근 차단
    """
    cl = db.query(CoverLetter).filter(
        CoverLetter.id == cover_letter_id,
        CoverLetter.user_id == current_user.id,
    ).first()

    if not cl:
        raise HTTPException(status_code=404, detail="커버레터를 찾을 수 없습니다")
    return cl


@router.put("/{cover_letter_id}", response_model=CoverLetterResponse)
def update_cover_letter(
    cover_letter_id: int,
    body: CoverLetterUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """커버레터 내용 수정 — 생성 후 직접 편집 시 사용"""
    cl = db.query(CoverLetter).filter(
        CoverLetter.id == cover_letter_id,
        CoverLetter.user_id == current_user.id,
    ).first()

    if not cl:
        raise HTTPException(status_code=404, detail="커버레터를 찾을 수 없습니다")

    cl.content = body.content
    db.commit()
    db.refresh(cl)
    return cl


@router.delete("/{cover_letter_id}", status_code=204)
def delete_cover_letter(
    cover_letter_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    커버레터 삭제
    - 204 No Content 반환 (삭제 성공 시 본문 없음)
    """
    cl = db.query(CoverLetter).filter(
        CoverLetter.id == cover_letter_id,
        CoverLetter.user_id == current_user.id,
    ).first()

    if not cl:
        raise HTTPException(status_code=404, detail="커버레터를 찾을 수 없습니다")

    db.delete(cl)
    db.commit()