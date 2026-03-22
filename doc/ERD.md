# GC-Proctor NoSQL ERD

## Muc tieu thiet ke
- Toi uu cho chatbot truy van nhanh, luu hoi thoai theo phien, va ho tro RAG.
- Ket hop quan he tham chieu (reference) va du lieu nhung (embedded) theo tung nghiep vu.
- Uu tien mo rong ngang va truy van theo user, mon hoc, ky thi, va nguon tai lieu.

## ERD theo huong NoSQL (Collection-centric)
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

## Quyet dinh mo hinh du lieu NoSQL
- `USERS`: thong tin danh tinh chuan hoa; profile mo rong co the nhung vao field `profile` neu can.
- `CHAT_SESSIONS` + `CHAT_MESSAGES`: tach rieng de tranh document vuot 16MB va de phan trang lich su chat.
- `DOCUMENTS` + `DOCUMENT_CHUNKS`: toi uu RAG, cho phep re-index theo tung document.
- `EXAM_SCHEDULES`: luu ban sao lich thi theo sinh vien de tra cuu nhanh theo `studentId`.
- `RETRIEVAL_LOGS`: theo doi chunk nao duoc goi, phuc vu danh gia accuracy va fallback.

## De xuat index chinh
- `USERS`: unique(`userCode`), unique(`email`).
- `COURSES`: unique(`courseCode`, `semester`).
- `EXAM_SCHEDULES`: index(`studentId`, `examDate`), index(`examId`).
- `DOCUMENT_CHUNKS`: index(`documentId`, `chunkIndex`), index(`embeddingId`).
- `CHAT_MESSAGES`: index(`sessionId`, `createdAt`), index(`intent`).
- `RETRIEVAL_LOGS`: index(`messageId`), index(`chunkId`, `similarity`).
- `FEEDBACKS`: index(`messageId`), index(`userId`, `createdAt`).

## Embedded vs Reference
- Nen embedded:
  - `CHAT_MESSAGES.entities` va `CHAT_MESSAGES.citations` (nho, di cung message).
  - metadata nho cua document trong `DOCUMENTS`.
- Nen reference:
  - `CHAT_SESSIONS` -> `CHAT_MESSAGES`.
  - `DOCUMENTS` -> `DOCUMENT_CHUNKS`.
  - `EXAMS` -> `EXAM_SCHEDULES`.

## Luu y mo rong
- Co the tach them collection `MODEL_CONFIGS` de quan ly prompt, retriever, fallback policy theo version.
- Co the bo sung `TENANTS` neu sau nay can ho tro da truong/da don vi.
