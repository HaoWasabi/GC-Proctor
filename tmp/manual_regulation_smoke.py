from datetime import date

from services.regulation_service import RegulationService
from models.document_model import DocumentModel
from models.document_chunk_model import DocumentChunkModel
from models.regulation_model import RegulationModel


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    today = date.today()

    regulations = [
        RegulationModel(
            id="reg_001",
            regulationCode="QC-EXAM",
            title="Quy che thi cu",
            version="2026.1",
            effectiveDate=today,
            sourceUrl="https://example.edu/reg-001.pdf",
            updatedAt=today,
            isActive=True,
        ),
        RegulationModel(
            id="reg_002",
            regulationCode="QC-OTHER",
            title="Quy che khac",
            version="2025.2",
            effectiveDate=today,
            sourceUrl="https://example.edu/reg-002.pdf",
            updatedAt=today,
            isActive=True,
        ),
    ]

    documents = [
        DocumentModel(
            id="doc_001",
            docType="pdf",
            title="QC-EXAM",
            ownerType="regulation",
            ownerId="reg_001",
            storagePath="/tmp/doc_001.pdf",
            language="vi",
            createdAt=today,
            isActive=True,
        ),
        DocumentModel(
            id="doc_002",
            docType="pdf",
            title="QC-OTHER",
            ownerType="regulation",
            ownerId="reg_002",
            storagePath="/tmp/doc_002.pdf",
            language="vi",
            createdAt=today,
            isActive=True,
        ),
    ]

    chunks = [
        DocumentChunkModel(
            id="chk_001",
            documentId="doc_001",
            chunkIndex=1,
            content="Dieu 12 Khoan 3: Sinh vien khong duoc mang dien thoai vao phong thi.",
            embeddingId="emb_001",
            scoreThreshold=0.1,
            createdAt=today,
            isActive=True,
        ),
        DocumentChunkModel(
            id="chk_002",
            documentId="doc_001",
            chunkIndex=2,
            content="Dieu 8 Khoan 1: Sinh vien phai co mat truoc gio thi 15 phut.",
            embeddingId="emb_002",
            scoreThreshold=0.1,
            createdAt=today,
            isActive=True,
        ),
        DocumentChunkModel(
            id="chk_003",
            documentId="doc_002",
            chunkIndex=1,
            content="Dieu 2 Khoan 1: Noi dung khong lien quan.",
            embeddingId="emb_003",
            scoreThreshold=0.1,
            createdAt=today,
            isActive=True,
        ),
    ]

    class FakeRegulationRepo:
        def get_all_regulations(self):
            return regulations

        def get_regulation(self, regulation_id):
            for regulation in regulations:
                if regulation.get_id() == regulation_id:
                    return regulation
            return None

    class FakeDocumentRepo:
        def get_all_documents(self):
            return documents

    class FakeChunkRepo:
        def get_all_document_chunks(self):
            return chunks

    service = RegulationService(
        regulation_repository=FakeRegulationRepo(),
        document_repository=FakeDocumentRepo(),
        chunk_repository=FakeChunkRepo(),
        model=None,
    )

    print("[1] query match case")
    result_match = service.query({"query": "Mang dien thoai vao phong thi co bi cam khong?", "topK": 2})
    assert_true(result_match["intent"] == "regulation", "intent must be regulation")
    assert_true(3 <= result_match["retrieval"]["topK"] <= 5, "topK must be normalized to 3..5")
    assert_true(len(result_match["citations"]) >= 1, "must return at least one citation for relevant query")
    assert_true(result_match["citations"][0]["regulationId"] == "reg_001", "first citation should prioritize matching regulation")

    print("[2] query no-match case")
    result_no_match = service.query({"query": "zzzz qqqq xxxx", "topK": 5})
    assert_true(result_no_match["citations"] == [], "no-match query should return empty citations")

    print("[3] get_clauses")
    clause_result = service.get_clauses("reg_001")
    assert_true(clause_result["regulationId"] == "reg_001", "get_clauses should return requested regulation")
    assert_true(len(clause_result["clauses"]) == 2, "reg_001 should have two clauses")

    print("[4] validate_answer")
    validation = service.validate_answer({
        "answer": "Theo Dieu 12 Khoan 3, khong duoc mang dien thoai vao phong thi.",
        "citations": [
            {
                "regulationId": "reg_001",
                "quote": "Dieu 12 Khoan 3: Sinh vien khong duoc mang dien thoai vao phong thi.",
            }
        ],
    })
    assert_true(validation["isValid"] is True, "validation should pass when answer and citation are present")

    print("SMOKE CHECK PASSED")


if __name__ == "__main__":
    main()
