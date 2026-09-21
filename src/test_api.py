from pathlib import Path
import os
from dotenv import load_dotenv
from google import genai

# 프로젝트 경로
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

print("프로젝트 경로:", PROJECT_ROOT)
print(".env 경로:", ENV_FILE)
print(".env 존재 여부:", ENV_FILE.exists())

# .env 불러오기
load_dotenv(ENV_FILE)

# Gemini API 키 확인
api_key = os.getenv("GEMINI_API_KEY")

print("Gemini API 키 로드 여부:", bool(api_key))

# Gemini 연결 테스트
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="안녕하세요. API 연결 테스트입니다. 한 문장으로 답해주세요."
)

print("Gemini 응답:")
print(response.text)