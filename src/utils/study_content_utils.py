import json
from typing import Any, Dict

from utils.mindmap_builder import generate_mindmap_js


def generate_mindmap_payload(study_svc, prompt: str, context: str, chunks: list, output_file: str = "src/tmp/data.js") -> Dict[str, Any]:
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
