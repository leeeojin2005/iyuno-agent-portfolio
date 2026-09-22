import os
import sys
import json
import time
from datetime import datetime

# src 폴더를 기준으로 프로젝트 경로 설정
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# agent.py에서 필요한 함수 가져오기
from agent import run_agent

# retriever에서 RAG 검색 함수 가져오기
from retriever import search_docs


# ==========================================
# 30개 평가 질문
# ==========================================

TEST_CASES = [
    {
        "id": "Q01",
        "question": "SQL Injection을 방지하려면 어떻게 해야 해?",
        "expected_source": "SQL_Injection_Prevention.txt"
    },
    {
        "id": "Q02",
        "question": "Parameterized Query가 왜 중요한가요?",
        "expected_source": "Query_Parameterization.txt"
    },
    {
        "id": "Q03",
        "question": "SQL 쿼리에 사용자 입력값을 직접 연결하면 왜 위험한가요?",
        "expected_source": "SQL_Injection_Prevention.txt"
    },
    {
        "id": "Q04",
        "question": "XSS 공격을 방지하려면 어떻게 해야 하나요?",
        "expected_source": "Cross_Site_Scripting.txt"
    },
    {
        "id": "Q05",
        "question": "Stored XSS와 Reflected XSS의 차이는 무엇인가요?",
        "expected_source": "Cross_Site_Scripting.txt"
    },
    {
        "id": "Q06",
        "question": "XSS 방지를 위한 출력 인코딩은 왜 필요한가요?",
        "expected_source": "Cross_Site_Scripting.txt"
    },
    {
        "id": "Q07",
        "question": "CSRF 공격을 방어하려면 어떻게 해야 하나요?",
        "expected_source": "Cross_Site_Request_Forgery.txt"
    },
    {
        "id": "Q08",
        "question": "CSRF Token은 어떤 역할을 하나요?",
        "expected_source": "Cross_Site_Request_Forgery.txt"
    },
    {
        "id": "Q09",
        "question": "CSRF와 XSS의 차이는 무엇인가요?",
        "expected_source": "Cross_Site_Request_Forgery.txt"
    },
    {
        "id": "Q10",
        "question": "비밀번호를 안전하게 저장하려면 어떻게 해야 하나요?",
        "expected_source": "Password_Storage.txt"
    },
    {
        "id": "Q11",
        "question": "비밀번호 해싱에서 Work Factor가 중요한 이유는 무엇인가요?",
        "expected_source": "Password_Storage.txt"
    },
    {
        "id": "Q12",
        "question": "비밀번호 저장에서 Pepper는 무엇인가요?",
        "expected_source": "Password_Storage.txt"
    },
    {
        "id": "Q13",
        "question": "Authentication과 Authorization의 차이는 무엇인가요?",
        "expected_source": "Authentication.txt"
    },
    {
        "id": "Q14",
        "question": "Authorization에서 권한 검사를 왜 해야 하나요?",
        "expected_source": "Authorization.txt"
    },
    {
        "id": "Q15",
        "question": "접근 제어 실패를 줄이려면 어떤 방법을 사용할 수 있나요?",
        "expected_source": "Authorization.txt"
    },
    {
        "id": "Q16",
        "question": "민감한 데이터를 암호화해서 저장해야 하는 이유는 무엇인가요?",
        "expected_source": "Cryptographic_Storage.txt"
    },
    {
        "id": "Q17",
        "question": "데이터베이스 보안을 강화하려면 어떻게 해야 하나요?",
        "expected_source": "Database_Security.txt"
    },
    {
        "id": "Q18",
        "question": "파일 업로드 기능을 안전하게 구현하려면 어떻게 해야 하나요?",
        "expected_source": "File_Upload.txt"
    },
    {
        "id": "Q19",
        "question": "HTTP Security Header는 왜 사용하나요?",
        "expected_source": "HTTP_Headers.txt"
    },
    {
        "id": "Q20",
        "question": "사용자 입력값을 검증하는 이유는 무엇인가요?",
        "expected_source": "Input_Validation.txt"
    },
    {
        "id": "Q21",
        "question": "JWT를 안전하게 사용하려면 무엇을 주의해야 하나요?",
        "expected_source": "JSON_Web_Token.txt"
    },
    {
        "id": "Q22",
        "question": "REST API를 안전하게 만들려면 어떻게 해야 하나요?",
        "expected_source": "REST_Security.txt"
    },
    {
        "id": "Q23",
        "question": "HTTPS와 TLS는 어떤 역할을 하나요?",
        "expected_source": "Transport_Layer_Security.txt"
    },
    {
        "id": "Q24",
        "question": "보안 관점에서 오류 메시지를 어떻게 처리해야 하나요?",
        "expected_source": "Error_Handling.txt"
    },
    {
        "id": "Q25",
        "question": "보안 로그를 기록하는 것이 왜 중요한가요?",
        "expected_source": "Logging.txt"
    },
    {
        "id": "Q26",
        "question": "API Key와 같은 비밀정보를 안전하게 관리하려면 어떻게 해야 하나요?",
        "expected_source": "Secrets_Management.txt"
    },
    {
        "id": "Q27",
        "question": "WAF만 사용하면 SQL Injection을 완전히 막을 수 있나요?",
        "expected_source": "SQL_Injection_Prevention.txt"
    },
    {
        "id": "Q28",
        "question": "Virtual Patching이란 무엇인가요?",
        "expected_source": "Virtual_Patching.txt"
    },
    {
        "id": "Q29",
        "question": "Threat Modeling이란 무엇인가요?",
        "expected_source": "Threat_Modeling.txt"
    },
    {
        "id": "Q30",
        "question": "2 + 3 * 4는 얼마인가요?",
        "expected_source": None
    }
]


# ==========================================
# RAG Recall@3 측정
# ==========================================

def calculate_recall_at_3(question, expected_source):
    """
    질문에 대해 ChromaDB에서 상위 3개 문서를 검색하고
    기대하는 문서가 포함되어 있는지 확인한다.
    """

    if expected_source is None:
        return None

    try:
        results = search_docs(question, n_results=3)

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        sources = []

        for metadata in metadatas:
            source = metadata.get("source", "")
            sources.append(source)

        hit = expected_source in sources

        return {
            "hit": hit,
            "sources": sources
        }

    except Exception as e:
        return {
            "hit": False,
            "sources": [],
            "error": str(e)
        }


# ==========================================
# 30개 질문 평가 실행
# ==========================================

def run_evaluation():

    results = []

    total = len(TEST_CASES)

    print()
    print("=" * 70)
    print("Iyuno AI Agent - 30개 질문 정량 평가")
    print("=" * 70)
    print()
    print("총 질문 수:", total)
    print()

    for index, test_case in enumerate(TEST_CASES, start=1):

        question_id = test_case["id"]
        question = test_case["question"]
        expected_source = test_case["expected_source"]

        print()
        print("-" * 70)
        print(f"[{index}/{total}] {question_id}")
        print("질문:", question)

        # ------------------------------
        # Recall@3 측정
        # ------------------------------

        recall_result = calculate_recall_at_3(
            question,
            expected_source
        )

        if recall_result is None:
            recall_hit = None
            retrieved_sources = []
        else:
            recall_hit = recall_result["hit"]
            retrieved_sources = recall_result["sources"]

        print("RAG 검색 결과:", retrieved_sources)

        # ------------------------------
        # Agent 응답 시간 측정
        # ------------------------------

        start_time = time.perf_counter()

        try:
            answer = run_agent(question)
            error = None

        except Exception as e:
            answer = ""
            error = str(e)

        end_time = time.perf_counter()

        latency = end_time - start_time

        # ------------------------------
        # Citation 여부 확인
        # ------------------------------

        if expected_source is None:
            citation_supported = True
        else:
            citation_supported = (
                expected_source in answer
            )

        # ------------------------------
        # 계산기 테스트
        # ------------------------------

        calculator_correct = None

        if question_id == "Q30":
            calculator_correct = "14" in answer

        # ------------------------------
        # 결과 출력
        # ------------------------------

        print("응답 시간:", round(latency, 2), "초")
        print("Citation:", citation_supported)

        if calculator_correct is not None:
            print("계산 결과:", calculator_correct)

        if error:
            print("오류:", error)

        # ------------------------------
        # 결과 저장
        # ------------------------------

        results.append({
            "id": question_id,
            "question": question,
            "expected_source": expected_source,
            "retrieved_sources": retrieved_sources,
            "recall_at_3": recall_hit,
            "citation_supported": citation_supported,
            "calculator_correct": calculator_correct,
            "latency_seconds": round(latency, 3),
            "answer": answer,
            "error": error
        })

    return results


# ==========================================
# Metrics 계산
# ==========================================

def calculate_metrics(results):

    rag_results = [
        r for r in results
        if r["expected_source"] is not None
    ]

    recall_hits = [
        r["recall_at_3"]
        for r in rag_results
        if r["recall_at_3"] is not None
    ]

    citation_results = [
        r["citation_supported"]
        for r in rag_results
    ]

    latencies = [
        r["latency_seconds"]
        for r in results
        if r["error"] is None
    ]

    if recall_hits:
        recall_at_3 = sum(recall_hits) / len(recall_hits)
    else:
        recall_at_3 = 0

    if citation_results:
        citation_supported_rate = (
            sum(citation_results) /
            len(citation_results)
        )
    else:
        citation_supported_rate = 0

    if latencies:
        average_latency = sum(latencies) / len(latencies)
        minimum_latency = min(latencies)
        maximum_latency = max(latencies)
    else:
        average_latency = 0
        minimum_latency = 0
        maximum_latency = 0

    calculator_results = [
        r["calculator_correct"]
        for r in results
        if r["calculator_correct"] is not None
    ]

    if calculator_results:
        calculator_accuracy = (
            sum(calculator_results) /
            len(calculator_results)
        )
    else:
        calculator_accuracy = None

    metrics = {
        "evaluation_date": datetime.now().isoformat(),
        "total_questions": len(results),
        "rag_questions": len(rag_results),
        "recall_at_3": round(recall_at_3, 4),
        "citation_supported_rate": round(
            citation_supported_rate,
            4
        ),
        "average_latency_seconds": round(
            average_latency,
            3
        ),
        "minimum_latency_seconds": round(
            minimum_latency,
            3
        ),
        "maximum_latency_seconds": round(
            maximum_latency,
            3
        ),
        "calculator_accuracy": calculator_accuracy,
        "faithfulness_note": (
            "현재 평가는 답변에 기대 문서 출처가 "
            "포함되었는지를 확인하는 citation-supported "
            "proxy를 사용한다. 의미 기반 faithfulness "
            "평가는 별도 단계에서 추가한다."
        )
    }

    return metrics


# ==========================================
# Markdown 결과 생성
# ==========================================

def create_markdown(results, metrics):

    lines = []

    lines.append("# 30개 질문 정량 평가 결과")
    lines.append("")
    lines.append(
        "Iyuno AI Agent Engineer 과제의 평가 요구사항에 따라 "
        "30개 질문을 실행하고 RAG 검색 및 응답 성능을 측정했다."
    )
    lines.append("")

    lines.append("## 1. 평가 지표")
    lines.append("")
    lines.append(
        f"- 전체 질문 수: {metrics['total_questions']}"
    )
    lines.append(
        f"- RAG 질문 수: {metrics['rag_questions']}"
    )
    lines.append(
        f"- Recall@3: {metrics['recall_at_3'] * 100:.2f}%"
    )
    lines.append(
        f"- Citation Supported Rate: "
        f"{metrics['citation_supported_rate'] * 100:.2f}%"
    )
    lines.append(
        f"- 평균 응답 시간: "
        f"{metrics['average_latency_seconds']:.3f}초"
    )
    lines.append(
        f"- 최소 응답 시간: "
        f"{metrics['minimum_latency_seconds']:.3f}초"
    )
    lines.append(
        f"- 최대 응답 시간: "
        f"{metrics['maximum_latency_seconds']:.3f}초"
    )

    if metrics["calculator_accuracy"] is not None:
        lines.append(
            f"- 계산기 테스트 정확도: "
            f"{metrics['calculator_accuracy'] * 100:.2f}%"
        )

    lines.append("")
    lines.append("## 2. 질문별 결과")
    lines.append("")
    lines.append(
        "| ID | 질문 | Recall@3 | Citation | Latency |"
    )
    lines.append(
        "|---|---|---:|---:|---:|"
    )

    for result in results:

        recall = result["recall_at_3"]

        if recall is None:
            recall_text = "-"
        else:
            recall_text = "PASS" if recall else "FAIL"

        citation_text = (
            "PASS"
            if result["citation_supported"]
            else "FAIL"
        )

        latency_text = (
            f"{result['latency_seconds']:.2f}s"
        )

        question_text = result["question"].replace(
            "|",
            "\\|"
        )

        lines.append(
            f"| {result['id']} | "
            f"{question_text} | "
            f"{recall_text} | "
            f"{citation_text} | "
            f"{latency_text} |"
        )

    lines.append("")
    lines.append("## 3. Faithfulness 측정 방법")
    lines.append("")
    lines.append(
        "현재 단계에서는 답변이 기대한 OWASP 문서의 "
        "출처를 실제로 인용했는지를 확인하는 "
        "citation-supported proxy를 사용했다."
    )
    lines.append("")
    lines.append(
        "이는 의미 기반 faithfulness와 동일하지 않으며, "
        "향후 별도의 평가 방법을 추가할 수 있다."
    )

    lines.append("")
    lines.append("## 4. 한계")
    lines.append("")
    lines.append(
        "- Gemini API 응답 시간은 네트워크 상태에 따라 달라질 수 있다."
    )
    lines.append(
        "- 무료 API 사용량 제한에 따라 일부 요청이 실패할 수 있다."
    )
    lines.append(
        "- 현재 faithfulness는 citation 기반 proxy이다."
    )
    lines.append(
        "- 현재 token cost는 별도로 측정하지 않았다."
    )

    return "\n".join(lines)


# ==========================================
# 파일 저장
# ==========================================

def save_results(results, metrics):

    evaluation_dir = os.path.join(
        PROJECT_ROOT,
        "evaluation"
    )

    os.makedirs(
        evaluation_dir,
        exist_ok=True
    )

    # metrics.json
    metrics_path = os.path.join(
        evaluation_dir,
        "metrics.json"
    )

    with open(
        metrics_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metrics,
            f,
            ensure_ascii=False,
            indent=2
        )

    # 30_question_results.md
    markdown_path = os.path.join(
        evaluation_dir,
        "30_question_results.md"
    )

    markdown = create_markdown(
        results,
        metrics
    )

    with open(
        markdown_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(markdown)

    # raw results
    raw_path = os.path.join(
        evaluation_dir,
        "30_question_raw.json"
    )

    with open(
        raw_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            ensure_ascii=False,
            indent=2
        )

    return (
        metrics_path,
        markdown_path,
        raw_path
    )


# ==========================================
# 프로그램 시작
# ==========================================

if __name__ == "__main__":

    results = run_evaluation()

    metrics = calculate_metrics(results)

    paths = save_results(
        results,
        metrics
    )

    print()
    print("=" * 70)
    print("평가 완료")
    print("=" * 70)
    print()

    print("Recall@3:",
          f"{metrics['recall_at_3'] * 100:.2f}%")

    print(
        "Citation Supported Rate:",
        f"{metrics['citation_supported_rate'] * 100:.2f}%"
    )

    print(
        "평균 응답 시간:",
        f"{metrics['average_latency_seconds']:.3f}초"
    )

    print()
    print("생성된 파일:")

    for path in paths:
        print(path)

    print()
    print("30개 질문 평가가 끝났습니다.")