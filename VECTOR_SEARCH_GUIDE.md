# Vector Search Implementation Guide

## 📌 Overview

Hệ thống tra cứu quy chế giờ đã được triển khai **Vector Search** sử dụng:
- **FAISS**: Thư viện tìm kiếm similarity nhanh từ Meta
- **Sentence-Transformers**: Pre-trained embedding model để tạo embeddings
- **Fallback Keyword Matching**: Nếu vector search không khả dụng

## 🚀 Installation

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

Packages mới:
- `sentence-transformers>=2.6.1` - Embedding model (all-MiniLM-L6-v2, ~33MB)
- `numpy>=1.24.0` - Matrix operations

### 2. Chuẩn bị FAISS Index

FAISS index có thể từ:

#### Option A: Sử dụng FAISS file có sẵn
Nếu `tmp/vector_db/all_regulations.faiss` đã tồn tại, hệ thống sẽ tự động load.

#### Option B: Rebuild từ Firestore
Nếu Firestore có document chunks:
```bash
cd src
python utils/index_builder.py
```

Lúc này sẽ:
1. Fetch tất cả chunks từ Firestore
2. Generate embeddings (lần đầu sẽ download ~33MB model)
3. Build FAISS index và save vào `tmp/vector_db/`

#### Option C: Import từ PDF (Backend API)
Endpoint: `POST /api/regulations/import-file`
```bash
python tmp/manual_import_regulation_real.py
```

## 🧪 Testing

### Test 1: Vector Search Functionality
```bash
cd src
python tests/test_vector_search.py
```

Output:
```
TEST 1: VectorStoreService - Load FAISS Index
✅ Đã load FAISS index thành công
   - Số chunks: 15
   - Embedding dim: 384

[Testing RAG Response]
✅ Chunks tìm thấy
```

### Test 2: Streamlit App
```bash
streamlit run src/app.py
```

Vào **"💬 Hỏi đáp Quy chế"** và thử hỏi:
- "Sinh viên đi trễ bao lâu không được vào thi?"
- "Quy định về mang điện thoại vào phòng thi"
- "Khi nào được phép vào phòng thi?"

## 🔍 How It Works

### Flow Diagram
```
User Query
    ↓
RegulationService.answer_regulation_question()
    ↓
_retrieve_relevant_chunks()
    ├─→ [PRIMARY] Vector Search (FAISS)
    │   ├─ Encode query → embedding
    │   ├─ Search FAISS index
    │   ├─ Return top-5 similar chunks
    │   └─ Filter by threshold (0.3)
    │
    └─→ [FALLBACK] Keyword Matching
        ├─ If FAISS not available
        ├─ Match 30% query words
        └─ Return top-5 matching chunks
    ↓
LLM (Gemini) generates answer
    ↓
User Response
```

### Key Files

| File | Purpose |
|------|---------|
| `src/utils/vector_store_service.py` | VectorStoreService class - manages FAISS & embeddings |
| `src/utils/index_builder.py` | Rebuild FAISS index từ Firestore |
| `src/services/regulation_service.py` | Main RAG service (updated) |
| `src/tests/test_vector_search.py` | Test script |
| `tmp/vector_db/` | FAISS index files location |

## ⚙️ Configuration

### Embedding Model
Default: `all-MiniLM-L6-v2` (33M, tốc độ Vs accuracy cân bằng)

Options:
- `all-MiniLM-L6-v2`: 33M, ~38ms/query (khuyến nghị)
- `all-mpnet-base-v2`: 110M, ~100ms/query (chính xác hơn)
- `sentence-transformers/paraphrase-multilingual-mini-v1`: Multilingual

Thay đổi trong `vector_store_service.py`:
```python
self.model = SentenceTransformer("all-mpnet-base-v2")
```

### Similarity Threshold
Default: `0.3` (30% similarity được chấp nhận)

Điều chỉnh trong `regulation_service.py`:
```python
threshold = 0.3  # Tăng = strict hơn, giảm = lenient hơn
```

### Top-K Results
Default: `k=5` (trả về 5 chunks tương tự nhất)

## 📊 Performance

Trên máy CPU thường:
- Embed query: ~50ms
- Search FAISS: ~5ms
- Total retrieval: ~60ms

Trên GPU:
- ~10-20ms total

## ⚠️ Troubleshooting

### 1. "FAISS index không tìm thấy"
→ Rebuild từ Firestore:
```bash
python src/utils/index_builder.py
```

### 2. "Không tìm thấy quy định cụ thể" message
→ Kiểm tra:
- Chunks có trong Firestore?
- FAISS index có data?
- Query có phù hợp?

### 3. Import error: "sentence_transformers"
→ Cài lại: `pip install sentence-transformers`

### 4. Query quá chậm
→ Kiểm tra:
- Model size quá lớn? → Đổi sang MiniLM
- Firestore query chậm? → Check Firestore connection

## 🔄 Rebuild Workflow

Khi cập nhật quy chế:
1. Import PDF/Excel vào Firestore
2. Chunks được stored trong Firestore
3. Run index builder:
   ```bash
   python src/utils/index_builder.py
   ```
4. FAISS index được rebuild
5. Vector search sử dụng index mới

## 📝 Next Steps

1. **Fine-tune Threshold**: Điều chỉnh similarity threshold based on your data
2. **Monitor Performance**: Log search queries and results
3. **Add Caching**: Cache embeddings để tránh tính toán lại
4. **Batch Processing**: Support batch queries
5. **Multilingual**: Upgrade model để support Vietnamese tốt hơn

---

**Status**: ✅ Vector Search Implemented & Ready
