# OWASP Security AI Agent

OWASP 보안 문서를 기반으로 사용자의 보안 질문에 답변하는 RAG 기반 AI Agent 프로젝트입니다.

사용자의 질문과 관련된 OWASP 문서를 검색하고, 검색된 문서를 Gemini에 전달하여 근거 기반의 답변을 생성합니다.

---

## 1. 프로젝트 소개

본 프로젝트는 보안 관련 질문에 대해 OWASP 문서를 검색하고 이를 기반으로 답변을 생성하는 AI Agent를 구현하는 것을 목표로 합니다.

단순히 LLM의 사전 학습 지식만 사용하는 것이 아니라, OWASP 문서를 벡터 데이터베이스에 저장하고 질문과 관련된 문서를 검색한 후 Gemini 모델에 전달하는 RAG(Retrieval-Augmented Generation) 방식을 사용합니다.

---

## 2. 주요 기능

### OWASP 문서 기반 RAG

OWASP 보안 문서를 수집하고 문서를 작은 단위로 분할한 후 ChromaDB에 저장합니다.

사용자의 보안 질문이 입력되면 관련 문서를 검색하고 검색 결과를 Gemini에 전달합니다.

### Gemini 기반 답변 생성

Gemini 3.6 Flash를 사용하여 검색된 OWASP 문서를 바탕으로 자연어 답변을 생성합니다.

### 보안 질문 처리

다음과 같은 보안 주제에 대한 질문을 처리할 수 있습니다.

* SQL Injection
* Cross-Site Scripting (XSS)
* Cross-Site Request Forgery (CSRF)
* Password Storage
* Authentication
* Access Control
* 기타 웹 보안 취약점

### 계산 기능

간단한 수학 계산식을 입력하면 계산 결과를 반환할 수 있습니다.

예:

```text
2 + 3 * 4
```

결과:

```text
14
```

---

## 3. 시스템 구조

```text
사용자 질문
     ↓
    Agent
     ↓
보안 관련 질문 판단
     ↓
OWASP 문서 검색
     ↓
ChromaDB
     ↓
관련 문서 검색
     ↓
검색 결과 + 사용자 질문
     ↓
Gemini 3.6 Flash
     ↓
최종 답변
```

---

## 4. 사용 기술

| 기술               | 용도               |
| ---------------- | ---------------- |
| Python           | 전체 애플리케이션 개발     |
| Gemini 3.6 Flash | 자연어 답변 생성        |
| ChromaDB         | OWASP 문서 벡터 검색   |
| RAG              | 관련 문서 검색 및 답변 보강 |
| OWASP            | 보안 지식 문서         |
| python-dotenv    | API Key 환경변수 관리  |
| Spyder           | 개발 및 실행 환경       |

---

## 5. 프로젝트 구조

```text
iyuno-agent-portfolio
│
├── .env
├── .gitignore
├── README.md
│
├── data
│   └── OWASP 문서
│
├── evaluation
│   └── test_results.md
│
└── src
    ├── agent.py
    ├── build_vector_db.py
    ├── chunk_docs.py
    ├── collect_docs.py
    ├── ingest.py
    ├── retriever.py
    └── test_api.py
```

---

## 6. 실행 방법

### 1) 환경 변수 설정

프로젝트 루트의 `.env` 파일에 Gemini API Key를 설정합니다.

```text
GEMINI_API_KEY=YOUR_API_KEY
```

API Key는 소스 코드에 직접 작성하지 않고 `.env` 파일을 통해 관리합니다.

---

### 2) 필요한 라이브러리 설치

```bash
pip install google-genai python-dotenv chromadb
```

---

### 3) Agent 실행

`src/agent.py`를 실행합니다.

```bash
python src/agent.py
```

Spyder를 사용하는 경우 `agent.py`를 열고 Run 버튼을 눌러 실행할 수 있습니다.

---

## 7. 테스트 결과

Agent의 주요 기능을 다음과 같이 테스트했습니다.

| 테스트                    | 결과   |
| ---------------------- | ---- |
| SQL Injection 관련 질문    | PASS |
| XSS 관련 질문              | PASS |
| CSRF 관련 질문             | PASS |
| 계산 질문                  | PASS |
| Password Storage 관련 질문 | PASS |

보안 관련 질문의 경우 관련 OWASP 문서가 검색되었으며, 검색된 문서를 기반으로 Gemini가 답변을 생성하는 것을 확인했습니다.

계산 테스트에서는 `2 + 3 * 4`에 대해 `14`를 정상적으로 반환했습니다.

자세한 테스트 결과는 `evaluation/test_results.md`에서 확인할 수 있습니다.

---

## 8. RAG 동작 예시

사용자가 다음과 같은 질문을 입력합니다.

```text
SQL Injection을 방지하려면 어떻게 해야 해?
OWASP 문서를 기반으로 설명해줘.
```

Agent는 질문과 관련된 OWASP 문서를 검색합니다.

검색된 문서 예시:

```text
SQL_Injection_Prevention.txt
```

검색된 문서를 Gemini에 전달하고, Gemini는 해당 자료를 기반으로 최종 답변을 생성합니다.

이를 통해 LLM의 일반적인 지식뿐만 아니라 프로젝트에 저장된 OWASP 문서를 답변 생성 과정에 활용할 수 있습니다.

---

## 9. 보안 관련 주의사항

`.env` 파일에는 API Key가 포함되어 있으므로 GitHub 등의 공개 저장소에 업로드하지 않습니다.

`.gitignore`를 통해 `.env`가 Git에 포함되지 않도록 관리합니다.

---

## 10. 프로젝트 목표

본 프로젝트를 통해 다음과 같은 AI Agent 개발 과정을 구현했습니다.

1. 보안 문서 수집
2. 문서 Chunking
3. 벡터 데이터베이스 구축
4. 관련 문서 검색
5. RAG 기반 정보 전달
6. Gemini를 이용한 답변 생성
7. Agent 기능 테스트 및 평가

이를 통해 외부 지식 문서를 활용하여 보다 근거 중심의 보안 질문 답변 시스템을 구현했습니다.
