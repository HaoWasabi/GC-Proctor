import unicodedata
from repositories.document_chunk_repository import DocumentChunkRepository


def normalize_text(text: str) -> str:
    nfd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def run() -> None:
    repo = DocumentChunkRepository()
    chunks = repo.get_all_document_chunks()
    print(f"chunks={len(chunks)}")

    queries = [
        "Sinh vien di tre bao lau khong duoc vao thi?",
        "Sinh viên đi trễ bao lâu không được vào thi?",
        "quy chế học vụ",
        "cảnh cáo học vụ là gì",
        "điều kiện dự thi",
    ]

    for q in queries:
        query_words = [
            normalize_text(w.lower().strip(".,?!:;\"'"))
            for w in q.split()
            if w.strip()
        ]
        ranked = []
        for ch in chunks:
            content = normalize_text(ch.get_content().lower())
            match_count = sum(1 for w in query_words if w and w in content)
            if match_count >= 1:
                ranked.append((match_count, ch.get_content()))
        ranked.sort(key=lambda x: x[0], reverse=True)

        print("---")
        print(q)
        print(f"matched_docs={len(ranked)}")
        for score, text in ranked[:3]:
            preview = text.replace("\n", " ")[:180]
            print(f"score={score} | {preview}")


if __name__ == "__main__":
    run()
