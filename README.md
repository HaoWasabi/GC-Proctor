# GC-Proctor

GC-Proctor là hệ thống chatbot hỗ trợ khảo thí và học tập, gồm các luồng chính:

- Tra cứu quy chế
- Tra cứu lịch thi
- Ôn tập theo tài liệu (mindmap, flashcard, quiz)
- Hỗ trợ sinh viên với luồng bot -> admin

## 1. Yêu cầu môi trường

- Python 3.10+ (khuyến nghị 3.11)
- Windows/Linux/macOS đều chạy được
- Có tài khoản Firebase service account
- Có API key cho Gemini

## 2. Cài đặt dự án

Tại thư mục gốc dự án:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## 3. Tạo configs

Tạo thư mục cấu hình nếu chưa có:

```bash
mkdir -p src/configs
```

Đặt file service account của Firebase tại:

- `src/configs/serviceAccount.json`

Luu y:

- Không commit file credentials thật lên Git.
- Nên thêm `src/configs/*.json` vào `.gitignore` nếu chưa có.

## 4. Tạo file .env

Tạo file `src/.env` với nội dung mẫu:

```env
# Bat buoc
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

# Chon 1 trong 2 cach cap Firebase credentials
# Cach 1 (de dung nhat): tro toi file json
FIREBASE_CREDENTIALS_PATH=src/configs/serviceAccount.json

# Cach 2: JSON credentials dang chuoi (neu deploy qua secret)
# FIREBASE_CREDENTIALS_JSON={"type":"service_account",...}

# Tuy chon cho real API tests
RUN_REAL_API_TESTS=0
REAL_TEST_STUDENT_ID=SV001
```

## 5. Chạy ứng dụng

Từ thư mục gốc dự án:

```bash
streamlit run src/app.py
```

Sau khi chạy, mở URL do Streamlit in ra (mặc định `http://localhost:8501`).

## 6. Chạy test

Test unit:

```bash
python -m unittest discover src/tests -v
```

Test gọi API thật (cần bật env):

```bash
# Windows PowerShell
$env:RUN_REAL_API_TESTS="1"
python -m unittest src/tests/test_answer_regulation_question_real_api.py -v
python -m unittest src/tests/test_answer_exam_question_real_api.py -v
```

## 7. Cấu trúc chính

```text
GC-Proctor/
├── README.md
├── requirements.txt
├── doc/
│   ├── PRD.md
│   ├── ERD.md
│   └── API_CONTRACT_P0.md
├── src/
│   ├── app.py
│   ├── configs/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── tests/
│   └── utils/
└── tmp/
```

## 8. Lưu ý vận hành

- Dự án hiện đã thống nhất dùng 1 thư mục tạm ở root: `tmp/`.
- Mindmap/Flashcard viewer và data files đều đọc/ghi trong `tmp/`.
- Nếu gặp lỗi không thấy file viewer hoặc data, kiểm tra các file sau có tồn tại:
  - `tmp/gc_mindmap.html`
  - `tmp/gc_flashcard.html`
  - `tmp/mindmap_data.js`
  - `tmp/flashcard_data.js`

## 9. Troubleshooting nhanh

- Lỗi `GEMINI_API_KEY environment variable not set`
  - Kiểm tra `src/.env` có `GEMINI_API_KEY`.

- Lỗi Firebase credentials
  - Kiểm tra `FIREBASE_CREDENTIALS_PATH` trỏ đúng file JSON.
  - Hoặc cung cấp `FIREBASE_CREDENTIALS_JSON` hợp lệ.

- Lỗi tìm đường dẫn tmp
  - Chạy app từ thư mục gốc bằng `streamlit run src/app.py`.
