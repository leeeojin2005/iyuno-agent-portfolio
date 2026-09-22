import json
import chromadb
from pathlib import Path

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
DB_DIR = Path(__file__).resolve().parent.parent / "data" / "chroma_db"

def build_vector_db():

    chunks_path = PROCESSED_DIR / "chunks.json"
    if not chunks_path.exists():
        print("chunks.json 파일을 찾을 수 없습니다.")
        return

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    client = chromadb.PersistentClient(path=str(DB_DIR))
    
    collection = client.get_or_create_collection(name="security_docs")

    documents = [chunk["text"] for chunk in chunks]
    metadatas = [{"source": chunk["source"], "page_or_index": chunk.get("chunk_index", chunk.get("page", 0))} for chunk in chunks]
    ids = [chunk["id"] if "id" in chunk else f"chunk_{i}" for i, chunk in enumerate(chunks)]

    print(f"총 {len(documents)}개의 청크를 임베딩하여 ChromaDB에 저장합니다...")
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"완료! 벡터 DB 저장 위치: {DB_DIR}")

if __name__ == "__main__":
    DB_DIR.mkdir(parents=True, exist_ok=True)
    build_vector_db()