from pathlib import Path
import requests
from bs4 import BeautifulSoup


RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


DOCUMENTS = [
    ("Authentication", "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html"),
    ("Authorization", "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html"),
    ("Cross_Site_Request_Forgery", "https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html"),
    ("Cross_Site_Scripting", "https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html"),
    ("Cryptographic_Storage", "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html"),
    ("Database_Security", "https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html"),
    ("Error_Handling", "https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html"),
    ("File_Upload", "https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html"),
    ("HTTP_Headers", "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html"),
    ("Input_Validation", "https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html"),
    ("JSON_Web_Token", "https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html"),
    ("Logging", "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html"),
    ("Password_Storage", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"),
    ("Query_Parameterization", "https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html"),
    ("REST_Security", "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html"),
    ("Secrets_Management", "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"),
    ("SQL_Injection_Prevention", "https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html"),
    ("Threat_Modeling", "https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html"),
    ("Transport_Layer_Security", "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html"),
    ("Virtual_Patching", "https://cheatsheetseries.owasp.org/cheatsheets/Virtual_Patching_Cheat_Sheet.html"),
]


def download_document(name, url):
    """웹 문서를 받아서 텍스트 파일로 저장한다."""

    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "iyuno-agent-portfolio/1.0"}
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    text = soup.get_text("\n")

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    clean_text = "\n".join(lines)

    output_path = RAW_DIR / f"{name}.txt"
    output_path.write_text(clean_text, encoding="utf-8")

    return output_path


if __name__ == "__main__":

    print(f"문서 저장 위치: {RAW_DIR}")
    print(f"수집할 문서 수: {len(DOCUMENTS)}")
    print()

    success = 0

    for name, url in DOCUMENTS:

        try:
            path = download_document(name, url)

            print(f"[OK] {name}")
            print(f"     → {path.name}")

            success += 1

        except Exception as e:
            print(f"[ERROR] {name}")
            print(f"        {e}")

    print()
    print(f"수집 완료: {success}/{len(DOCUMENTS)}")

