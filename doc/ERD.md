# GC-Proctor NoSQL ERD

## Mục tiêu thiết kế
- Tối ưu cho chatbot truy vấn nhanh, lưu hội thoại theo phiên, và hỗ trợ RAG.
- Kết hợp quan hệ tham chiếu (reference) và dữ liệu nhúng (embedded) theo từng nghiệp vụ.
- Ưu tiên mở rộng ngang và truy vấn theo user, môn học, kỳ thi, và nguồn tài liệu.

## ERD theo hướng NoSQL (Collection-centric)
```mermaid
erDiagram
    USERS {
      string _id PK
      string userCode
      string role
      string fullName
      string email
      string authProvider
      date createdAt
      date updatedAt
    }

    COURSES {
      string _id PK
      string courseCode
      string courseName
      string faculty
      string semester
      date createdAt
    }

    EXAMS {
      string _id PK
      string courseId FK
      string examType
      int durationMinutes
      string policyVersion
      date createdAt
    }

    EXAM_SCHEDULES {
      string _id PK
      string examId FK
      string studentId FK
      date examDate
      string startTime
      string room
      string status
      date updatedAt
    }

    REGULATIONS {
      string _id PK
      string regulationCode
      string title
      string version
      date effectiveDate
      string sourceUrl
      date updatedAt
    }

    DOCUMENTS {
      string _id PK
      string docType
      string title
      string ownerType
      string ownerId
      string storagePath
      string language
      date createdAt
    }

    DOCUMENT_CHUNKS {
      string _id PK
      string documentId FK
      int chunkIndex
      string content
      string embeddingId
      float scoreThreshold
      date createdAt
    }

    CHAT_SESSIONS {
      string _id PK
      string userId FK
      string channel
      string persona
      string sessionStatus
      date startedAt
      date endedAt
    }

    CHAT_MESSAGES {
      string _id PK
      string sessionId FK
      string senderType
      string intent
      string content
      json citations
      json entities
      date createdAt
    }

    RETRIEVAL_LOGS {
      string _id PK
      string messageId FK
      string chunkId FK
      float similarity
      string retrieverVersion
      date createdAt
    }

    FEEDBACKS {
      string _id PK
      string userId FK
      string messageId FK
      int rating
      string comment
      date createdAt
    }

    AUDIT_LOGS {
      string _id PK
      string actorUserId FK
      string actionType
      string targetCollection
      string targetId
      json metadata
      date createdAt
    }

    USERS ||--o{ CHAT_SESSIONS : owns
    CHAT_SESSIONS ||--o{ CHAT_MESSAGES : contains
    CHAT_MESSAGES ||--o{ RETRIEVAL_LOGS : triggers
    DOCUMENT_CHUNKS ||--o{ RETRIEVAL_LOGS : retrieved_from

    USERS ||--o{ EXAM_SCHEDULES : attends
    EXAMS ||--o{ EXAM_SCHEDULES : has
    COURSES ||--o{ EXAMS : defines

    REGULATIONS ||--o{ DOCUMENTS : represented_by
    COURSES ||--o{ DOCUMENTS : learning_material
    DOCUMENTS ||--o{ DOCUMENT_CHUNKS : chunked_into

    USERS ||--o{ FEEDBACKS : submits
    CHAT_MESSAGES ||--o{ FEEDBACKS : rated_on

    USERS ||--o{ AUDIT_LOGS : acts
```

## Quyết định mô hình dữ liệu NoSQL
- `USERS`: thông tin danh tính chuẩn hóa; profile mở rộng có thể nhúng vào field `profile` nếu cần.
- `CHAT_SESSIONS` + `CHAT_MESSAGES`: tách riêng để tránh document vượt 16MB và để phân trang lịch sử chat.
- `DOCUMENTS` + `DOCUMENT_CHUNKS`: tối ưu RAG, cho phép re-index theo từng document.
- `EXAM_SCHEDULES`: lưu bản sao lịch thi theo sinh viên để tra cứu nhanh theo `studentId`.
- `RETRIEVAL_LOGS`: theo dõi chunk nào được gọi, phục vụ đánh giá accuracy và fallback.

## Đề xuất index chính
- `USERS`: unique(`userCode`), unique(`email`).
- `COURSES`: unique(`courseCode`, `semester`).
- `EXAM_SCHEDULES`: index(`studentId`, `examDate`), index(`examId`).
- `DOCUMENT_CHUNKS`: index(`documentId`, `chunkIndex`), index(`embeddingId`).
- `CHAT_MESSAGES`: index(`sessionId`, `createdAt`), index(`intent`).
- `RETRIEVAL_LOGS`: index(`messageId`), index(`chunkId`, `similarity`).
- `FEEDBACKS`: index(`messageId`), index(`userId`, `createdAt`).

## Embedded vs Reference
- Nên embedded:
  - `CHAT_MESSAGES.entities` và `CHAT_MESSAGES.citations` (nhỏ, đi cùng message).
  - metadata nhỏ của document trong `DOCUMENTS`.
- Nên reference:
  - `CHAT_SESSIONS` -> `CHAT_MESSAGES`.
  - `DOCUMENTS` -> `DOCUMENT_CHUNKS`.
  - `EXAMS` -> `EXAM_SCHEDULES`.

## Lưu ý mở rộng
- Có thể tách thêm collection `MODEL_CONFIGS` để quản lý prompt, retriever, fallback policy theo version.
- Có thể bổ sung `TENANTS` nếu sau này cần hỗ trợ đa trường/đa đơn vị.
