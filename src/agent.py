import os
import re
from dotenv import load_dotenv
from google import genai

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

load_dotenv(ENV_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY를 찾을 수 없습니다. .env 파일을 확인하세요."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


MODEL_NAME = "gemini-3.6-flash"


def search_security_docs(query):

    print()
    print("[OWASP RAG 검색]")
    print("검색어:", query)

    try:

        from retriever import search_docs

        results = search_docs(
            query,
            n_results=3
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        if not documents:

            return "관련 OWASP 문서를 찾지 못했습니다."

        output = []

        for document, metadata in zip(
            documents,
            metadatas
        ):

            source = metadata.get(
                "source",
                "출처 정보 없음"
            )

            output.append(
                "[출처: "
                + source
                + "]\n"
                + document
            )

        return "\n\n".join(output)

    except Exception as e:

        return (
            "OWASP 문서 검색 중 오류가 발생했습니다.\n"
            + str(e)
        )


def calculator(expression):

    allowed_chars = "0123456789+-*/(). "

    for char in expression:

        if char not in allowed_chars:

            return "허용되지 않은 계산식입니다."

    try:

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:

        return "계산할 수 없는 식입니다."


def extract_calculation_expression(user_query):
    pattern = (
        r'^\s*'
        r'([0-9+\-*/().\s]+?)'
        r'\s*(?:는|은|=)?\s*'
        r'(?:얼마인가요|얼마야|계산해줘|계산해 주세요)?'
        r'\s*[?？]?\s*$'
    )

    match = re.match(pattern, user_query)

    if match:
        expression = match.group(1).strip()

        if expression and any(
            operator in expression
            for operator in ["+", "-", "*", "/"]
        ):
            return expression

    return None

def needs_security_search(user_query):

    keywords = [
        "OWASP",
        "SQL Injection",
        "SQL injection",
        "XSS",
        "CSRF",
        "인젝션",
        "보안",
        "취약점",
        "웹 보안",
        "인증",
        "권한",
        "접근 제어",
        "암호화",
        "세션"
    ]

    for keyword in keywords:

        if keyword in user_query:

            return True

    return False


def generate_answer(
    user_query,
    security_context
):

    system_prompt = """
너는 OWASP 보안 문서를 기반으로 답변하는 AI Agent이다.

규칙:

1. 사용자의 질문에 직접 답한다.
2. 제공된 OWASP 문서를 우선적으로 참고한다.
3. 문서에 없는 내용을 만들어내지 않는다.
4. OWASP 문서를 참고했다면 출처를 표시한다.
5. 한국어로 답변한다.
6. 이해하기 쉽게 설명한다.
7. 필요한 경우 간단한 예시를 제공한다.
8. 답변을 지나치게 길게 만들지 않는다.
"""

    if security_context:

        user_prompt = """
사용자 질문:

""" + user_query + """

다음은 OWASP RAG 검색 결과이다.

========== OWASP 검색 결과 ==========

""" + security_context + """

========== 검색 결과 끝 ==========

위 OWASP 자료를 참고하여 사용자의 질문에 답변해줘.
답변 마지막에는 참고한 OWASP 문서의 출처를 표시해줘.
"""

    else:

        user_prompt = """
사용자 질문:

""" + user_query + """

이 질문에는 OWASP RAG 검색 결과가 제공되지 않았다.
일반적인 지식을 바탕으로 정확하게 답변해줘.
"""

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=user_prompt,
        system_instruction=system_prompt
    )

    return interaction.output_text


def run_agent(user_query):
    print()
    print("=" * 60)
    print("사용자:", user_query)
    print("=" * 60)

    calculation_expression = extract_calculation_expression(
        user_query
    )

    if calculation_expression:
        print()
        print("[Calculator 실행]")
        print("계산식:", calculation_expression)

        return calculator(
            calculation_expression
        )

    security_context = ""

    if needs_security_search(user_query):
        security_context = search_security_docs(
            user_query
        )

    print()
    print("[Gemini 답변 생성 중...]")

    try:
        answer = generate_answer(
            user_query,
            security_context
        )

        if security_context:
            sources = re.findall(
                r"\[출처:\s*([^\]]+)\]",
                security_context
            )

            unique_sources = []

            for source in sources:
                if source not in unique_sources:
                    unique_sources.append(source)

            if unique_sources:
                answer = (
                    answer.rstrip()
                    + "\n\n"
                    + "참고 문서: "
                    + ", ".join(unique_sources)
                )

        return answer

    except Exception as e:
        return (
            "Gemini API 실행 중 오류가 발생했습니다.\n\n"
            "오류 종류: "
            + type(e).__name__
            + "\n\n"
            "오류 내용: "
            + str(e)
        )


if __name__ == "__main__":

    question = (
        "안전한 비밀번호 인증을 구현하려면 어떤 점을 고려해야 해?"
    )

    answer = run_agent(question)

    print()
    print("=" * 60)
    print("최종 답변")
    print("=" * 60)
    print(answer)