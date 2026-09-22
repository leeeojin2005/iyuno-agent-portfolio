# OWASP Security AI Agent

OWASP 보안 문서를 기반으로 사용자의 보안 질문에 답변하는 RAG 기반 AI Agent 프로젝트입니다.

사용자의 질문과 관련된 OWASP 문서를 검색하고, 검색된 문서를 Gemini 모델에 전달하여 근거 기반의 답변을 생성합니다.

---

## 1. 프로젝트 소개

본 프로젝트는 보안 관련 질문에 대해 OWASP 문서를 검색하고 이를 기반으로 답변을 생성하는 AI Agent를 구현하는 것을 목표로 합니다.

단순히 LLM의 사전 학습 지식만 사용하는 것이 아니라, OWASP 문서를 벡터 데이터베이스에 저장하고 질문과 관련된 문서를 검색한 후 Gemini 모델에 전달하는 RAG(Retrieval-Augmented Generation) 방식을 사용합니다.

또한 보안 질문 여부를 판단하는 Agent 로직과 간단한 계산 기능을 함께 구현했습니다.

---

## 2. 주요 기능

### OWASP 문서 기반 RAG

OWASP 보안 문서를 수집하고 문서를 작은 단위로 분할한 후 ChromaDB에 저장합니다.

사용자의 보안 질문이 입력되면 관련 문서를 검색하고 검색 결과를 Gemini 모델에 전달합니다.

### Gemini 기반 답변 생성

Gemini 모델을 사용하여 검색된 OWASP 문서를 참고한 자연어 답변을 생성합니다.

### 보안 질문 처리

다음과 같은 보안 주제에 대한 질문을 처리할 수 있습니다.

* SQL Injection
* Cross-Site Scripting (XSS)
* Cross-Site Request Forgery (CSRF)
* Password Storage
* Authentication
* Authorization
* Cryptographic Storage
* Database Security
* File Upload
* HTTP Security Headers
* Input Validation
* JWT
* REST Security
* TLS
* Error Handling
* Logging
* Secrets Management
* Virtual Patching
* Threat Modeling

### 계산 기능

간단한 수학 계산식을 입력하면 계산 결과를 반환합니다.

예:

```text
2 + 3 * 4
```

결과:

```text
14
```

계산 질문은 Agent가 계산기 함수를 직접 실행하도록 구현했습니다.

---

## 3. 시스템 구조

```text
사용자 질문
     ↓
    Agent
     ↓
질문 유형 판단
     ├───────────────┐
     ↓               ↓
계산 질문          보안 질문
     ↓               ↓
Calculator       OWASP 문서 검색
     ↓               ↓
   결과           ChromaDB
                     ↓
                 관련 문서 검색
                     ↓
              검색 결과 + 사용자 질문
                     ↓
                   Gemini
                     ↓
                  최종 답변
```

---

## 4. 사용 기술

| 기술            | 용도               |
| ------------- | ---------------- |
| Python        | 전체 애플리케이션 개발     |
| Gemini        | 자연어 답변 생성        |
| ChromaDB      | OWASP 문서 벡터 검색   |
| RAG           | 관련 문서 검색 및 답변 보강 |
| OWASP         | 보안 지식 문서         |
| python-dotenv | API Key 환경변수 관리  |
| Spyder        | 개발 및 실행 환경       |

---

## 5. 프로젝트 구조

```text
iyuno-agent-portfolio
│
├── .env
├── .gitignore
├── README.md
├── test_agent.py
│
├── data
│   ├── documents
│   ├── raw
│   └── chroma_db
│
├── evaluation
│   ├── metrics.json
│   ├── 30_question_results.md
│   └── 30_question_raw.json
│
└── src
    ├── agent.py
    ├── build_Vector_db.py
    ├── chunk_does.py
    ├── collect_docs.py
    ├── ingest.py
    ├── retriever.py
    ├── run_evaluation.py
    ├── test_api.py
    └── test_openai.py
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

Spyder를 사용하는 경우 `agent.py`를 열고 Run 기능으로 실행할 수 있습니다.

---

### 4) 평가 실행

30개 질문 정량 평가를 실행하려면 다음 파일을 실행합니다.

```text
src/run_evaluation.py
```

평가가 완료되면 다음 파일이 생성됩니다.

```text
evaluation/metrics.json
evaluation/30_question_results.md
evaluation/30_question_raw.json
```

---

## 7. 평가 결과

2026년 9월 22일에 30개 질문을 대상으로 1차 정량 평가를 수행했습니다.

| 평가 지표                   |       결과 |
| ----------------------- | -------: |
| 전체 질문 수                 |       30 |
| RAG 질문 수                |       29 |
| Recall@3                |   72.41% |
| Citation Supported Rate |    6.90% |
| 평균 응답 시간                | 133.374초 |
| 최소 응답 시간                |  13.882초 |
| 최대 응답 시간                | 180.007초 |
| 계산기 테스트 정확도             |    0.00% |

### 질문별 평가

30개 질문에 대해 SQL Injection, XSS, CSRF, Password Storage, Authentication, Authorization, 암호화, 데이터베이스 보안, 파일 업로드, JWT, TLS 등의 주제를 평가했습니다.

RAG 검색은 전체 29개의 RAG 질문에 대해 Recall@3 방식으로 측정했으며, 기대한 OWASP 문서가 상위 3개 검색 결과에 포함되는지를 기준으로 평가했습니다.

세부 질문별 결과는 다음 파일에서 확인할 수 있습니다.

```text
evaluation/30_question_results.md
```

원본 평가 데이터는 다음 파일에 저장했습니다.

```text
evaluation/30_question_raw.json
```

평가 지표는 다음 파일에서 확인할 수 있습니다.

```text
evaluation/metrics.json
```

---

## 8. 평가 방법 및 한계

### Recall@3

각 질문에 대해 ChromaDB에서 상위 3개의 문서를 검색하고, 사전에 지정한 기대 문서가 검색 결과에 포함되는지를 확인했습니다.

### Citation Supported Rate

Gemini 답변에 사전에 지정한 기대 OWASP 문서의 파일명이 포함되는지를 확인하는 방식으로 측정했습니다.

이 방식은 실제 의미 기반 인용 정확도나 답변의 모든 내용에 대한 사실성까지 평가하는 방식은 아니며, citation-supported proxy로 사용했습니다.

### 응답 시간

각 질문에 대한 Agent 응답 생성 시간을 측정했습니다.

응답 시간은 Gemini API, 네트워크 상태 및 API 사용 환경의 영향을 받을 수 있습니다.

### 계산기 평가

계산 질문인 `2 + 3 * 4`를 대상으로 결과가 `14`인지 확인했습니다.

30개 질문의 1차 평가 결과에서는 계산기 정확도가 0.00%로 측정되었으며, 이후 Agent 코드에서 계산 질문이 calculator 함수를 직접 사용하도록 개선했습니다.

---

## 9. 보안 관련 주의사항

`.env` 파일에는 Gemini API Key가 포함되어 있으므로 GitHub 등의 공개 저장소에 API Key를 업로드하지 않습니다.

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
7. Calculator Tool 구현
8. Agent 기능 테스트 및 정량 평가

이를 통해 외부 지식 문서를 활용하여 보안 질문에 대해 근거를 제공하는 RAG 기반 AI Agent를 구현했습니다.
