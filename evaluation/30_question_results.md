# 30개 질문 정량 평가 결과

Iyuno AI Agent Engineer 과제의 평가 요구사항에 따라 30개 질문을 실행하고 RAG 검색 및 응답 성능을 측정했다.

## 1. 평가 지표

- 전체 질문 수: 30
- RAG 질문 수: 29
- Recall@3: 72.41%
- Citation Supported Rate: 6.90%
- 평균 응답 시간: 133.374초
- 최소 응답 시간: 13.882초
- 최대 응답 시간: 180.007초
- 계산기 테스트 정확도: 0.00%

## 2. 질문별 결과

| ID | 질문 | Recall@3 | Citation | Latency |
|---|---|---:|---:|---:|
| Q01 | SQL Injection을 방지하려면 어떻게 해야 해? | PASS | PASS | 60.03s |
| Q02 | Parameterized Query가 왜 중요한가요? | PASS | FAIL | 13.88s |
| Q03 | SQL 쿼리에 사용자 입력값을 직접 연결하면 왜 위험한가요? | PASS | FAIL | 93.65s |
| Q04 | XSS 공격을 방지하려면 어떻게 해야 하나요? | PASS | FAIL | 179.03s |
| Q05 | Stored XSS와 Reflected XSS의 차이는 무엇인가요? | PASS | PASS | 133.85s |
| Q06 | XSS 방지를 위한 출력 인코딩은 왜 필요한가요? | PASS | FAIL | 166.39s |
| Q07 | CSRF 공격을 방어하려면 어떻게 해야 하나요? | PASS | FAIL | 149.86s |
| Q08 | CSRF Token은 어떤 역할을 하나요? | PASS | FAIL | 155.16s |
| Q09 | CSRF와 XSS의 차이는 무엇인가요? | PASS | FAIL | 113.70s |
| Q10 | 비밀번호를 안전하게 저장하려면 어떻게 해야 하나요? | FAIL | FAIL | 179.58s |
| Q11 | 비밀번호 해싱에서 Work Factor가 중요한 이유는 무엇인가요? | PASS | FAIL | 179.96s |
| Q12 | 비밀번호 저장에서 Pepper는 무엇인가요? | PASS | FAIL | 180.01s |
| Q13 | Authentication과 Authorization의 차이는 무엇인가요? | PASS | FAIL | 179.66s |
| Q14 | Authorization에서 권한 검사를 왜 해야 하나요? | PASS | FAIL | 119.79s |
| Q15 | 접근 제어 실패를 줄이려면 어떤 방법을 사용할 수 있나요? | FAIL | FAIL | 150.09s |
| Q16 | 민감한 데이터를 암호화해서 저장해야 하는 이유는 무엇인가요? | FAIL | FAIL | 119.76s |
| Q17 | 데이터베이스 보안을 강화하려면 어떻게 해야 하나요? | FAIL | FAIL | 119.80s |
| Q18 | 파일 업로드 기능을 안전하게 구현하려면 어떻게 해야 하나요? | FAIL | FAIL | 89.69s |
| Q19 | HTTP Security Header는 왜 사용하나요? | PASS | FAIL | 119.50s |
| Q20 | 사용자 입력값을 검증하는 이유는 무엇인가요? | FAIL | FAIL | 179.50s |
| Q21 | JWT를 안전하게 사용하려면 무엇을 주의해야 하나요? | PASS | FAIL | 150.22s |
| Q22 | REST API를 안전하게 만들려면 어떻게 해야 하나요? | PASS | FAIL | 89.60s |
| Q23 | HTTPS와 TLS는 어떤 역할을 하나요? | PASS | FAIL | 179.75s |
| Q24 | 보안 관점에서 오류 메시지를 어떻게 처리해야 하나요? | FAIL | FAIL | 120.03s |
| Q25 | 보안 로그를 기록하는 것이 왜 중요한가요? | FAIL | FAIL | 119.33s |
| Q26 | API Key와 같은 비밀정보를 안전하게 관리하려면 어떻게 해야 하나요? | PASS | FAIL | 150.57s |
| Q27 | WAF만 사용하면 SQL Injection을 완전히 막을 수 있나요? | PASS | FAIL | 119.61s |
| Q28 | Virtual Patching이란 무엇인가요? | PASS | FAIL | 119.84s |
| Q29 | Threat Modeling이란 무엇인가요? | PASS | FAIL | 89.57s |
| Q30 | 2 + 3 * 4는 얼마인가요? | - | PASS | 179.79s |

## 3. Faithfulness 측정 방법

현재 단계에서는 답변이 기대한 OWASP 문서의 출처를 실제로 인용했는지를 확인하는 citation-supported proxy를 사용했다.

이는 의미 기반 faithfulness와 동일하지 않으며, 향후 별도의 평가 방법을 추가할 수 있다.

## 4. 한계

- Gemini API 응답 시간은 네트워크 상태에 따라 달라질 수 있다.
- 무료 API 사용량 제한에 따라 일부 요청이 실패할 수 있다.
- 현재 faithfulness는 citation 기반 proxy이다.
- 현재 token cost는 별도로 측정하지 않았다.