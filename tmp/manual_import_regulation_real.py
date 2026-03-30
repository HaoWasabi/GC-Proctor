import json
from pathlib import Path

import httpx

PDF_URL = "https://daotao.sgu.edu.vn/images/pdf/quy_dinh/2022-2375-QyD%20Chuyen%20Chuong%20Trinh%20Dao%20Tao%20DoiVoiSinhVenDHCQ.pdf"
BASE_URL = "http://127.0.0.1:8000"


def main() -> int:
    tmp_dir = Path(__file__).resolve().parent
    pdf_path = tmp_dir / "sgu_regulation_2375.pdf"

    print(f"[INFO] Downloading PDF from: {PDF_URL}")
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        r = client.get(PDF_URL)
        r.raise_for_status()
        pdf_path.write_bytes(r.content)

    print(f"[INFO] Saved PDF: {pdf_path}")
    endpoint = f"{BASE_URL}/api/regulations/import-file"

    with httpx.Client(timeout=300.0) as client:
        with pdf_path.open("rb") as f:
            files = {
                "file": (pdf_path.name, f, "application/pdf"),
            }
            data = {
                "use_ai": "true",
                "default_version": "2022-2375",
                "default_source_url": PDF_URL,
            }
            response = client.post(endpoint, files=files, data=data)

    print(f"[INFO] HTTP {response.status_code}")
    try:
        body = response.json()
    except Exception:
        print(response.text)
        return 1

    print(json.dumps(body, ensure_ascii=False, indent=2))
    if response.status_code != 200:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
