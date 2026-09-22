from pathlib import Path
import json


RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


def create_chunks(text, chunk_size=800, overlap=100):
    """긴 텍스트를 겹치는 작은 chunk로 나눈다."""

    chunks = []

    text = text.replace("\r", " ").replace("\n", " ").strip()

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(chunk_text)

        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    txt_files = list(RAW_DIR.glob("*.txt"))

    print(f"찾은 문서 수: {len(txt_files)}")

    all_chunks = []

    for txt_file in txt_files:

        text = txt_file.read_text(encoding="utf-8")

        chunks = create_chunks(text)

        print(f"{txt_file.name}: {len(chunks)}개 chunk")

        for i, chunk in enumerate(chunks):

            all_chunks.append({
                "id": f"{txt_file.stem}_{i}",
                "source": txt_file.name,
                "chunk_index": i,
                "text": chunk
            })

    output_path = PROCESSED_DIR / "chunks.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            all_chunks,
            f,
            ensure_ascii=False,
            indent=2
        )

    print()
    print(f"전체 chunk 수: {len(all_chunks)}")
    print(f"저장 위치: {output_path}")

    if all_chunks:
        print()
        print("첫 번째 chunk:")
        print(all_chunks[0]["text"][:500])