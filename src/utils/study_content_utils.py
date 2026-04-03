import json
from typing import Any, Dict
import re
from utils.mindmap_builder import generate_mindmap_js
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]


def _resolve_output_path(output_file: str) -> Path:
    normalized = (output_file or "").replace("\\", "/")
    target = Path(normalized)
    if target.is_absolute():
        return target
    return WORKSPACE_ROOT / target

def generate_mindmap_payload(study_svc, prompt: str, context: str, chunks: list, output_file: str = "tmp/data.js") -> Dict[str, Any]:
    """Generate mindmap nodes, persist as data.js and return payload for message entities."""
    if not chunks:
        return {
            "ok": False,
            "message": "⚠️ Úi, hệ thống chưa có tài liệu phần này nên mình không vẽ sơ đồ được. Bạn upload thêm nha!",
            "nodes": [],
            "output_file": output_file,
        }

    map_prompt = (
        "Bạn là trợ lý tạo sơ đồ tư duy học tập. "
        "Hãy trả về DUY NHẤT JSON hợp lệ dạng mảng node theo schema: "
        "[{\"id\": \"root\", \"text\": \"...\", \"parent_id\": null}, {\"id\": \"n1\", \"text\": \"...\", \"parent_id\": \"root\"}]. "
        "Không bọc markdown, không thêm giải thích, không thêm key ngoài id/text/parent_id. "
        "Node gốc phải có id='root' và parent_id=null.\n"
        f"Chủ đề: {prompt}\n"
        f"NỘI DUNG:\n{context}"
    )

    try:
        raw_json = study_svc.model.generate_content(map_prompt).text.strip()
        processed_nodes = generate_mindmap_js(raw_json, output_file=output_file)
        if not processed_nodes:
            return {
                "ok": False,
                "message": "⚠️ Mình chưa dựng được sơ đồ do dữ liệu đầu ra chưa đúng định dạng JSON node.",
                "nodes": [],
                "output_file": output_file,
            }

        return {
            "ok": True,
            "message": "🎉 Mình đã tạo sơ đồ tư duy theo định dạng mới. Bạn có thể bấm 'Xem sơ đồ' ở tin nhắn này để mở.",
            "nodes": processed_nodes,
            "output_file": output_file,
            "raw": raw_json,
        }
    except Exception as e:
        return {
            "ok": False,
            "message": f"⚠️ Lỗi khi tạo sơ đồ tư duy: {e}",
            "nodes": [],
            "output_file": output_file,
        }


def generate_mindmap_markdown(study_svc, prompt: str, context: str, chunks: list) -> str:
    """Backward-compatible wrapper for legacy call sites."""
    result = generate_mindmap_payload(study_svc, prompt, context, chunks)
    return result.get("message", "⚠️ Không thể tạo sơ đồ tư duy.")


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


def find_related_sources_markdown(kb_service, prompt: str, course_code: str = "ALL") -> str:
    """Find and display related document sources from knowledge base."""
    try:
        chunks = kb_service.retrieve_relevant_chunks(prompt, course_code)
        
        if not chunks:
            return "⚠️ Không tìm thấy tài liệu liên quan trong cơ sở dữ liệu. Vui lòng thử tìm kiếm lại!"
        
        response = "**🎯 Tìm thấy tài liệu liên quan:**\n\n"
        
        # Group chunks by source document
        sources_map = {}
        for chunk in chunks:
            source_id = chunk.get("document_id", "unknown")
            if source_id not in sources_map:
                sources_map[source_id] = {
                    "title": chunk.get("document_title", "Tài liệu không xác định"),
                    "chunks": []
                }
            sources_map[source_id]["chunks"].append(chunk.get("content", ""))
        
        # Format output
        for i, (source_id, source_info) in enumerate(sources_map.items(), 1):
            response += f"**{i}. {source_info['title']}**\n"
            response += f"> Mô tả: {source_info['chunks'][0][:200]}...\n\n"
        
        return response
    except Exception as e:
        return f"⚠️ Lỗi khi tìm kiếm tài liệu: {e}"

def generate_flashcards_payload(study_svc, prompt: str, output_file: str = "tmp/flashcard_data.js") -> Dict[str, Any]:
    """Sử dụng backend sinh flashcard có sẵn và lưu ra file JS để render 3D"""
    # 1. Gọi hàm backend CÓ SẴN của bạn (không chế prompt mới)
    res = study_svc.generate_flashcards("ALL", prompt)
    flashcards = res.get("flashcards", []) if isinstance(res, dict) else []

    if not flashcards:
        return {
            "ok": False,
            "message": res.get("message") if isinstance(res, dict) and res.get("message") else "⚠️ Không đủ dữ liệu tạo flashcard."
        }

    # 2. Đổi key 'question'/'answer' của bạn thành 'front'/'back' để giao diện HTML 3D hiểu
    cards_for_html = []
    for card in flashcards:
        cards_for_html.append({
            "front": card.get("question", ""),
            "back": card.get("answer", "")
        })

    # 3. Ghi ra file flashcard_data.js giống hệt cách Mindmap làm
    js_content = f"var externalFlashcards = {json.dumps(cards_for_html, ensure_ascii=False, indent=2)};"
    output_path = _resolve_output_path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    return {
        "ok": True,
        "message": "🎉 Ta-da! Mình đã soạn xong bộ Flashcard 3D. Bạn nhấn nút bên dưới để học nhé!",
        "cards": cards_for_html
    }


def generate_quiz_payload(
    study_svc,
    prompt: str,
    context: str,
    chunks: list,
    num_questions: int = 5,
) -> Dict[str, Any]:
    """Generate multiple-choice quiz questions from study context."""
    if not chunks:
        return {
            "ok": False,
            "message": "⚠️ Chưa có đủ tài liệu liên quan để tạo quiz.",
            "questions": [],
        }

    quiz_prompt = f"""
    Bạn là trợ lý tạo quiz ôn tập cho sinh viên.
    Dựa trên tài liệu bên dưới, hãy tạo {num_questions} câu hỏi trắc nghiệm (MCQ).

    BẮT BUỘC CHỈ TRẢ VỀ JSON HỢP LỆ, không markdown, không giải thích thêm.
    Định dạng JSON:
    [
      {{
        "question": "...",
        "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
        "answer": "A",
        "explanation": "..."
      }}
    ]

    Yêu cầu:
    - Mỗi câu có đúng 4 lựa chọn A/B/C/D.
    - Trường answer chỉ chứa 1 ký tự: A hoặc B hoặc C hoặc D.
    - Nội dung phải bám sát tài liệu, không bịa thêm kiến thức ngoài tài liệu.

    Chủ đề sinh viên hỏi: {prompt}
    TÀI LIỆU:
    {context}
    """

    try:
        raw_text = study_svc.model.generate_content(quiz_prompt).text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()

        parsed = json.loads(raw_text)
        if not isinstance(parsed, list):
            return {
                "ok": False,
                "message": "⚠️ Đầu ra quiz từ AI chưa đúng định dạng danh sách câu hỏi.",
                "questions": [],
            }

        normalized_questions = []
        for item in parsed:
            if not isinstance(item, dict):
                continue

            raw_options = item.get("options", [])
            if isinstance(raw_options, dict):
                raw_options = list(raw_options.values())
            if not isinstance(raw_options, list):
                raw_options = []

            options = [str(opt).strip() for opt in raw_options if str(opt).strip()]
            if len(options) < 2:
                continue

            normalized_questions.append(
                {
                    "question": str(item.get("question", "")).strip(),
                    "options": options[:4],
                    "answer": str(item.get("answer", "")).strip().upper()[:1],
                    "explanation": str(item.get("explanation", "")).strip(),
                }
            )

        if not normalized_questions:
            return {
                "ok": False,
                "message": "⚠️ Mình chưa tạo được bộ quiz hợp lệ từ tài liệu hiện có.",
                "questions": [],
            }

        return {
            "ok": True,
            "message": "🎯 Mình đã tạo xong bài quiz ôn tập. Bạn bấm nút 'Làm Quiz' để bắt đầu nhé!",
            "questions": normalized_questions,
        }
    except Exception as e:
        return {
            "ok": False,
            "message": f"⚠️ Lỗi khi tạo quiz: {e}",
            "questions": [],
        }