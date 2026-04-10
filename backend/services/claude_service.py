import anthropic

from core.config import settings

# Anthropic 클라이언트 초기화 — 모듈 로드 시 1회만 생성
client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

# Claude에게 전달할 시스템 프롬프트
# 역할, 작성 규칙, 출력 형식을 명확히 지정할수록 품질이 올라감
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
    """유저 프롬프트 조합 — 회사명, 포지션, JD, 이력서를 하나의 메시지로"""
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
    """
    Claude API 스트리밍 생성기
    - with 구문으로 스트림 자동 종료 보장
    - text_stream은 텍스트 청크를 순서대로 yield
    - 호출하는 쪽에서 for loop으로 청크 소비
    """
    with client.messages.stream(
        model=settings.claude_model,
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