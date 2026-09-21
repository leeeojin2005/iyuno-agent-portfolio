from pathlib import Path
from pypdf import PdfReader


# 프로젝트의 data/raw 폴더
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# 처리된 텍스트를 저장할 폴더
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


def load_pdf(pdf_path):
    """PDF 파일의 각 페이지에서 텍스트를 추출한다."""
    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append({
            "page": page_number,
            "text": text
        })

    return pages


def create_chunks(pages, chunk_size=800, overlap=100):
    """페이지 텍스트를 겹치는 작은 chunk로 나눈다."""
    chunks = []

    for page in pages:
        text = page["text"].replace("\n", " ").strip()

        if not text:
            continue

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append({
                "page": page["page"],
                "text": chunk_text
            })

            start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"PDF 파일이 없습니다: {RAW_DIR}")

    else:
        for pdf_file in pdf_files:
            pages = load_pdf(pdf_file)
            chunks = create_chunks(pages)

            print(f"\n파일: {pdf_file.name}")
            print(f"페이지 수: {len(pages)}")
            print(f"생성된 chunk 수: {len(chunks)}")

            if chunks:
                print("\n첫 번째 chunk:")
                print(chunks[0]["text"][:500])