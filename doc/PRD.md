# GC-Proctor

## Sơ đồ Userflow tổng quát (Main Conversation Flow)
```mermaid
flowchart TD
    A[Người dùng mở Chatbot] --> B["Bot chào hỏi + Giới thiệu tính năng<br/>Persona thân thiện, hỗ trợ tiếng Việt"]

    B --> C{Bạn đã đăng nhập / xác thực chưa?}
    
    C -->|Có / Sinh viên/Giảng viên đã login| D[Nhập câu hỏi tự nhiên]
    C -->|Chưa / Anonymous| E["Yêu cầu login/SSO hoặc hỏi mã SV/môn học nếu cần<br/>cho lịch thi cá nhân"]

    D --> F["Phân loại Intent & Entity Extraction<br/>NLP: quy chế / lịch thi / ôn tập / khác"]

    F --> G{Loại Intent}

    G -->|1. Quy chế thi cử| H["RAG: Tìm kiếm ngữ nghĩa trong PDF quy chế<br/>Trích xuất điều khoản chính xác + trích dẫn Điều X, Khoản Y"]
    G -->|2. Lịch thi / Phòng thi| I["Kiểm tra xác thực / mã SV<br/>Nếu OK -> Query API hệ thống đào tạo<br/>Trả về lịch cá nhân hóa: ngày, giờ, phòng, môn"]
    G -->|3. Ôn tập kiến thức| J["RAG: Tìm kiếm trong tài liệu môn học / slide / ngân hàng câu hỏi<br/>Hỗ trợ: tóm tắt chương, flashcard, ví dụ, giải thích khái niệm<br/>Nếu user upload PDF -> chunking và tóm tắt"]
    G -->|4. Khác / Không rõ / Vượt thẩm quyền| K["Fallback: Xin lỗi + hướng dẫn hỏi lại<br/>Đề xuất liên hệ phòng giáo vụ / giảng viên<br/>Không bịa đặt thông tin"]

    H --> L["Tạo câu trả lời tự nhiên<br/>Tone persona + Trích dẫn nguồn rõ ràng<br/>Đề xuất hỏi thêm nếu cần"]
    I --> L
    J --> L
    K --> L

    L --> M{Còn câu hỏi nữa không?}
    M -->|Có| D
    M -->|Không / Kết thúc| N["Kết thúc phiên chat<br/>Bot chào tạm biệt + gợi ý feedback"]

    %% Nhánh Admin (riêng)
    O[Admin / Data Engineer] --> P["Quản lý Knowledge Base<br/>Upload / Update quy chế, slide, ngân hàng câu hỏi"]
    P --> Q["Tinh chỉnh mô hình / RAG pipeline<br/>Monitor accuracy và fallback rate"]
```
### Giải thích chi tiết các luồng chính

1. **Luồng chung (Onboarding & Conversation Loop)**
- Người dùng bắt đầu chat → Bot chào hỏi, giới thiệu khả năng (tra quy chế, lịch thi, ôn tập).
- Hỗ trợ anonymous cho quy chế và ôn tập chung; yêu cầu login/mã SV cho lịch thi cá nhân.
- Luôn loop lại để hỏi tiếp hoặc kết thúc.

2. **Luồng tra cứu Quy chế thi (Không cần login)**
- Câu hỏi ví dụ: "Đem điện thoại vào phòng thi có bị gì không?"
- Bot → Intent classification → RAG search → Trả lời chính xác 100% + trích dẫn điều khoản.

3. **Luồng tra cứu Lịch thi (Cá nhân hóa, cần xác thực)**
- Câu hỏi ví dụ: "Mai thi môn Nhập môn Kỹ thuật Phần mềm lúc mấy giờ, phòng nào?"
- Bot → Kiểm tra login/mã SV → Query API → Trả lịch cụ thể.

4. **Luồng Ôn tập kiến thức (Tutor mode)**
- Câu hỏi ví dụ: "Giải thích khái niệm Dependency Injection" hoặc "Tóm tắt chương 5 môn Cơ sở dữ liệu".
- Bot → RAG trên tài liệu môn học → Có thể generate flashcard, tóm tắt, ví dụ.
Hỗ trợ upload file PDF bài giảng để tóm tắt nhanh.

5. **Luồng Admin / Quản lý (riêng biệt, không nằm trong chat user)**
- Admin truy cập dashboard → Upload/update tài liệu → Chunking & embedding → Tinh chỉnh RAG.


### Lưu ý khi triển khai Userflow
- **Fallback handling:** Rất quan trọng để đảm bảo accuracy 100% cho quy chế & lịch thi (không hallucinate).
- **Persona:** Bot nên có giọng điệu thân thiện, hỗ trợ, đôi khi khuyến khích học tập (ví dụ: "Cố lên nhé, sắp thi rồi đó!").
- **Tích hợp:** Login/SSO → API hệ thống đào tạo → RAG pipeline (vector DB như Pinecone/Chroma).
- **Edge cases:** Hỏi vượt thẩm quyền (điểm số cá nhân, thông tin nhạy cảm) → redirect đến giáo vụ.