import os
import sys


# 프로젝트의 src 폴더를 Python 경로에 추가
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SRC_DIR = os.path.join(
    PROJECT_ROOT,
    "src"
)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


from agent import calculator, needs_security_search
from retriever import search_docs


# ==========================================
# 테스트 1
# 계산기가 기본 계산을 정확하게 하는지 확인
# ==========================================

def test_calculator_basic():
    result = calculator("2 + 3 * 4")

    assert result == "14"


# ==========================================
# 테스트 2
# SQL Injection 질문을 보안 질문으로
# 제대로 판단하는지 확인
# ==========================================

def test_security_question_sql_injection():
    result = needs_security_search(
        "SQL Injection을 어떻게 방지하나요?"
    )

    assert result is True


# ==========================================
# 테스트 3
# XSS 질문을 보안 질문으로
# 제대로 판단하는지 확인
# ==========================================

def test_security_question_xss():
    result = needs_security_search(
        "XSS 공격을 방지하려면 어떻게 해야 하나요?"
    )

    assert result is True


# ==========================================
# 테스트 4
# 허용되지 않은 계산식을 차단하는지 확인
# ==========================================

def test_calculator_rejects_invalid_expression():
    result = calculator(
        "__import__('os').system('dir')"
    )

    assert result == "허용되지 않은 계산식입니다."


# ==========================================
# 테스트 5
# ChromaDB에서 OWASP 문서를 실제로
# 검색할 수 있는지 확인
# ==========================================

def test_rag_search_returns_documents():

    results = search_docs(
        "SQL Injection 방지 방법",
        n_results=3
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    assert len(documents) > 0