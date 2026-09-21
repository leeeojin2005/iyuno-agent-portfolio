
import chromadb
from pathlib import Path

# DB가 저장된 경로 설정
DB_DIR = Path(__file__).resolve().parent.parent / "data" / "chroma_db"

def search_docs(query, n_results=3):
    """사용자 질문을 바탕으로 ChromaDB에서 가장 관련성 높은 문서를 검색한다."""
    
    # 저장된 DB 연결
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_collection(name="security_docs")

    # 벡터 유사도 검색 (자동으로 질문을 임베딩하여 비교함)
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results

if __name__ == "__main__":
    # RAG Retriever 테스트
    test_query = "How to prevent SQL Injection?"
    print(f"사용자 질문: {test_query}\n")
    
    search_results = search_docs(test_query, n_results=3)
    
    # 검색된 문서와 출처(citation) 확인
    documents = search_results['documents'][0]
    metadatas = search_results['metadatas'][0]
    
    for i, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
        print(f"🔍 [검색 결과 {i}]")
        print(f"출처(Citation): {meta['source']}")
        print(f"내용: {doc[:300]}...\n")
        print("-" * 50)