from typing import Generator
import anthropic
from openai import OpenAI

from core.config import settings

# 각 프로바이더 클라이언트 — 설정된 것만 초기화
# API 키가 없는 쪽은 실제로 호출되지 않으므로 빈 문자열이어도 무방
_claude_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
_openai_client = OpenAI(api_key=settings.openai_api_key or "dummy")

SYSTEM_PROMPT = """당신은 10년 경력의 전문 커리어 컨설턴트입니다.
지원자의 이력서와 채용공고(JD)를 분석하여 맞춤형 커버레터를 작성합니다.

작성 규칙:
- 이력서의 실제 경험과 스킬만 사용 (없는 내용 추가 금지)
- JD의 핵심 키워드와 요구사항을 자연스럽게 반영
- 800~1000자 분량의 한국어로 작성
- 구성: 도입(지원 동기) → 핵심 경험 → 기술 스택 연관성 → 입사 후 포부
- 딱딱하지 않고 진솔한 톤으로 작성
- 불필요한 미사여구 없이 임팩트 있게
- 지원자이름이나 회사이름 언급하지 않기
"""


def build_prompt(company_name: str, position: str, jd_text: str, resume_text: str) -> str:
    """유저 프롬프트 조합 — 프로바이더 무관하게 동일한 포맷 사용"""
    return f"""## 지원 회사 / 포지션
{company_name} / {position}

## 내 이력서
{resume_text}

## 채용공고 (JD)
{jd_text}

위 정보를 바탕으로 커버레터를 작성해주세요."""


def _stream_claude(company_name: str, position: str, jd_text: str, resume_text: str) -> Generator:
    """Claude API 스트리밍 — system 파라미터가 messages 밖에 위치하는 Claude 전용 구조"""
    with _claude_client.messages.stream(
        model=settings.llm_model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": build_prompt(company_name, position, jd_text, resume_text),
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            yield text


def _stream_openai(company_name: str, position: str, jd_text: str, resume_text: str) -> Generator:
    """OpenAI API 스트리밍 — system이 messages 안에 포함되는 OpenAI 전용 구조"""
    stream = _openai_client.chat.completions.create(
        model=settings.llm_model,
        max_tokens=2048,
        stream=True,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_prompt(company_name, position, jd_text, resume_text),
            },
        ],
    )
    for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        if text:
            yield text


def stream_cover_letter(
    company_name: str,
    position: str,
    jd_text: str,
    resume_text: str,
) -> Generator:
    """
    LLM 스트리밍 진입점 — 라우터는 이 함수만 호출
    llm_provider 설정값에 따라 내부적으로 Claude 또는 OpenAI로 분기
    """
    if settings.llm_provider == "claude":
        yield from _stream_claude(company_name, position, jd_text, resume_text)
    elif settings.llm_provider == "openai":
        yield from _stream_openai(company_name, position, jd_text, resume_text)
    else:
        raise ValueError(f"지원하지 않는 LLM 프로바이더: {settings.llm_provider}")