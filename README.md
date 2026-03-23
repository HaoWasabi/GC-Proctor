# GC-Proctor

## Introduction
* GC-Proctor is a next-generation AI Chatbot solution developed by the GCdev26 team from the Greencode community. The project was born with the mission to eliminate barriers of complex regulations, overlapping exam schedules, and revision pressure, helping students and lecturers optimize the examination experience.

* GC-Proctor là giải pháp Chatbot AI thế hệ mới được phát triển bởi tổ đội GCdev26 từ cộng đồng Greencode. Dự án ra đời với sứ mệnh xóa tan những rào cản về quy chế phức tạp, lịch thi chồng chéo và áp lực ôn tập, giúp sinh viên và giảng viên tối ưu hóa trải nghiệm khảo thí.

### Resources

* [Project Report](https://youtu.be/dQw4w9WgXcQ?si=hLIbE11aBkE04_ls)

* [Presentation Slides](https://youtu.be/dQw4w9WgXcQ?si=hLIbE11aBkE04_ls)

## Cấu trúc dự án hiện tại

```text
GC-Proctor/
├── README.md
├── requirements.txt
├── doc/
│   ├── ERD.md
│   └── PRD.md
└── src/
    ├── ai_models/
    └── app/
        ├── main.py
        ├── controllers/
        ├── dtos/
        ├── models/
        ├── services/
        └── views/
```

### Định nghĩa vai trò theo thư mục

- `README.md`: mô tả tổng quan dự án, tài nguyên, hướng dẫn sử dụng.
- `requirements.txt`: danh sách dependency Python của toàn bộ hệ thống.
- `doc/`: tài liệu phân tích và thiết kế.
  - `PRD.md`: mô tả yêu cầu sản phẩm và luồng nghiệp vụ chính.
  - `ERD.md`: thiết kế dữ liệu (NoSQL-centric) cho chatbot, lịch thi, và RAG.
- `src/`: mã nguồn chính.
  - `ai_models/`: nơi đặt các thành phần AI/ML (pipeline RAG, prompt, model adapters, embedding/retriever).
  - `app/`: tầng ứng dụng theo hướng module hóa.
    - `main.py`: entrypoint khởi chạy ứng dụng (hiện tại đang để trống, sẵn sàng triển khai).
    - `controllers/`: nhận request, điều phối use case, gọi service phù hợp.
    - `services/`: chứa business logic và tích hợp ngoài (LLM, vector DB, API lịch thi).
    - `models/`: định nghĩa entity/domain model dùng nội bộ.
    - `dtos/`: cấu trúc dữ liệu trao đổi giữa các tầng (request/response contract).
    - `views/`: chuẩn hóa dữ liệu trả về cho client/UI.

### Gợi ý quy ước phát triển

- Mỗi tính năng mới nên tách theo luồng: `model -> service -> controller -> view`.
- Giữ `controllers/` mỏng, không đặt nghiệp vụ phức tạp tại đây.
- Logic AI (prompt template, retriever config, guardrail) nên gom trong `ai_models/` hoặc service chuyên biệt để dễ kiểm thử.
- Khi bắt đầu implement, ưu tiên tạo thêm module theo domain: `exam`, `regulation`, `study_support`, `chat_session`.

---

*GCdev - Innovative technology, sustainable future*
