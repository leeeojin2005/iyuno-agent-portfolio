import json
import chromadb
from pathlib import Path

# 경로 설정
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
DB_DIR = Path(__file__).resolve().parent.parent / "data" / "chroma_db"

def build_vector_db():
    # 1. 분할된 청크 데이터 로드
    chunks_path = PROCESSED_DIR / "chunks.json"
    if not chunks_path.exists():
        print("chunks.json 파일을 찾을 수 없습니다.")
        return

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # 2. ChromaDB 클라이언트 설정 (로컬 폴더에 영구 저장)
    client = chromadb.PersistentClient(path=str(DB_DIR))
    
    # 3. 컬렉션 생성 (기본 제공되는 임베딩 함수 사용)
    collection = client.get_or_create_collection(name="security_docs")

    # 4. DB에 넣을 데이터 리스트 분리
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [{"source": chunk["source"], "page_or_index": chunk.get("chunk_index", chunk.get("page", 0))} for chunk in chunks]
    ids = [chunk["id"] if "id" in chunk else f"chunk_{i}" for i, chunk in enumerate(chunks)]

    print(f"총 {len(documents)}개의 청크를 임베딩하여 ChromaDB에 저장합니다...")
    
    # 5. DB에 데이터 추가 (자동으로 임베딩 진행됨)
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"완료! 벡터 DB 저장 위치: {DB_DIR}")

if __name__ == "__main__":
    DB_DIR.mkdir(parents=True, exist_ok=True)
    build_vector_db()