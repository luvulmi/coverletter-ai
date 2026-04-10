from openai import OpenAI
from core.config import settings

client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """당신은 10년 경력의 전문 커리어 컨설턴트입니다.
지원자의 이력서와 채용공고(JD)를 분석하여 맞춤형 커버레터를 작성합니다.

작성 규칙:
- 이력서의 실제 경험과 스킬만 사용 (없는 내용 추가 금지)
- JD의 핵심 키워드와 요구사항을 자연스럽게 반영
- 800~1000자 분량의 한국어로 작성
- 구성: 도입(지원 동기) → 핵심 경험 → 기술 스택 연관성 → 입사 후 포부
- 딱딱하지 않고 진솔한 톤으로 작성
- 불필요한 미사여구 없이 임팩트 있게"""


def build_prompt(company_name: str, position: str, jd_text: str, resume_text: str) -> str:
    """유저 프롬프트 조합"""
    return f"""## 지원 회사 / 포지션
{company_name} / {position}

## 내 이력서
{resume_text}

## 채용공고 (JD)
{jd_text}

위 정보를 바탕으로 커버레터를 작성해주세요."""


def stream_cover_letter(
    company_name: str,
    position: str,
    jd_text: str,
    resume_text: str,
):
    """OpenAI API 스트리밍 생성기"""
    stream = client.chat.completions.create(
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
        # OpenAI는 delta.content로 청크 텍스트 접근
        # 스트림 시작/끝엔 None이 올 수 있어서 or "" 처리
        text = chunk.choices[0].delta.content or ""
        if text:
            yield text