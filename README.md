# Iyuno AI Agent Portfolio

실제 AI Agent Engineer 채용공고를 분석하고,
공개 기술 문서를 기반으로 질문에 답변하는
RAG 기반 AI Agent를 구현하는 프로젝트입니다.

## 1. 프로젝트 개요

본 프로젝트는 Iyuno의 AI Agent Engineer 채용공고를 참고하여
채용공고에서 요구하는 AI 기술을 실제 작동하는 프로젝트로 구현하는 것을 목표로 합니다.

## 2. 참고 채용공고

- 회사: Iyuno
- 직무: AI Agent Engineer
- 근무지: 서울
- 채용공고: https://iyuno.wd3.myworkdayjobs.com/careers/job/seoul/ai-agent-engineer_jr101122

## 3. 구현 목표

채용공고에서 확인한 다음 요구사항을 프로젝트에 반영합니다.

- LLM 기반 AI Agent
- RAG 검색 및 응답
- Tool Calling
- API 연동
- 다단계 Workflow
- 평가 및 피드백
- Latency / Cost / Reliability 측정

## 4. 주요 기능

### RAG
공개된 보안 및 기술 문서를 수집하고,
문서를 Chunk 단위로 분할한 뒤 Embedding과 Vector Search를 이용하여
사용자의 질문과 관련된 정보를 검색합니다.

### Citation
검색된 문서를 근거로 답변을 생성하고,
답변에 참고한 문서의 출처를 표시합니다.

### Tool Calling
계산기, 검색 및 정책 조회 등의 도구를 호출할 수 있도록 구현합니다.

### Evaluation
질문 30개 이상을 이용하여 시스템의 성능을 평가하고
Recall@k, Faithfulness, Latency 등의 지표를 기록합니다.

## 5. 프로젝트 진행 상황

- [ ] 공개 문서 20개 수집
- [ ] 문서 Chunking
- [ ] Embedding
- [ ] Vector Search
- [ ] RAG 답변 생성
- [ ] Citation
- [ ] Tool Calling
- [ ] Evaluation
- [ ] pytest 테스트
- [ ] FastAPI 또는 Streamlit Demo
- [ ] 최종 Demo 영상

## 6. 프로젝트 구조

```text
iyuno-agent-portfolio/
├── README.md
├── data/
├── src/
├── evaluation/
├── tests/
├── requirements.txt
└── .gitignore
