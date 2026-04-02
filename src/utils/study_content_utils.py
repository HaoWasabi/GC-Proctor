import base64
import json

import requests


def generate_mindmap_markdown(study_svc, prompt: str, context: str, chunks: list) -> str:
    """Generate Mermaid mindmap image markdown from study context."""
    if not chunks:
        return "⚠️ Úi, hệ thống chưa có tài liệu phần này nên mình không vẽ sơ đồ được. Bạn upload thêm nha!"

    map_prompt = (
        f"Vẽ sơ đồ (mindmap/graph) cho: {prompt}. "
        "BẮT BUỘC TRẢ VỀ CÚ PHÁP MERMAID JS BẮT ĐẦU BẰNG `graph TD` hoặc `mindmap`. "
        "KHÔNG bọc markdown.\n"
        f"NỘI DUNG:\n{context}"
    )

    try:
        mermaid_code = (
            study_svc.model.generate_content(map_prompt)
            .text.replace("```mermaid", "")
            .replace("```", "")
            .strip()
        )
        payload = {"code": mermaid_code, "mermaid": {"theme": "default"}}
        b64_payload = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
        img_url = f"https://mermaid.ink/img/{b64_payload}"
        res_img = requests.get(img_url, timeout=15)

        if res_img.status_code == 200:
            return f"🎉 **Tèn ten! Sơ đồ của bạn đây:**\n\n![Mindmap]({img_url})"

        return (
            f"⚠️ Lỗi vẽ ảnh (Code {res_img.status_code}). Cú pháp bị kẹt:\n"
            f"```mermaid\n{mermaid_code}\n```"
        )
    except Exception as e:
        return f"⚠️ Lỗi khi tạo sơ đồ Mermaid: {e}"


def generate_flashcards_markdown(study_svc, prompt: str) -> str:
    """Generate flashcards text markdown for study chat."""
    res = study_svc.generate_flashcards("ALL", prompt)
    flashcards = res.get("flashcards", []) if isinstance(res, dict) else []

    if flashcards:
        response = "**🎉 Ta-da! Bộ thẻ Flashcard cho bạn nè:**\n\n"
        for i, card in enumerate(flashcards, 1):
            response += (
                f"**Q{i}:** {card.get('question', '')}\n"
                f"> **A{i}:** {card.get('answer', '')}\n\n---\n"
            )
        return response

    return res.get("message") if isinstance(res, dict) and res.get("message") else "⚠️ Tiếc quá, mình không tìm thấy đủ dữ liệu để tạo flashcard. Bạn cho mình thêm tài liệu nha!"
