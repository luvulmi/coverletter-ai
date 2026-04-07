# cover_letters / resumes 테이블 ORM 모델
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class CoverLetter(Base):
    """AI가 생성한 자기소개서 저장 테이블"""
    __tablename__ = "cover_letters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    jd_text = Column(Text, nullable=False)   # 채용 공고 원문
    content = Column(Text, nullable=False)   # 생성된 자기소개서 본문
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # 수정 시 자동 갱신

    user = relationship("User", back_populates="cover_letters")


class Resume(Base):
    """사용자 이력서 저장 테이블 — 유저당 1개 (upsert)"""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="resume")