# GC-Proctor API Contract (P0)

## 1. Scope
Tai lieu nay mo ta chi tiet API contract cho toan bo nhom P0 de team backend implement truc tiep.

P0 domains:
- Auth + identity
- Chat orchestration
- Regulation RAG query
- Personalized exam schedule
- Safety + fallback

Base URL:
- `/api`

Content type:
- Request body: `application/json`
- Response body: `application/json`

Datetime format:
- ISO 8601 UTC, vi du: `2026-03-25T10:30:00Z`

## 2. Common Conventions

### 2.1 Authentication
- Dung JWT Bearer token trong header:
  - `Authorization: Bearer <access_token>`
- Endpoint anonymous duoc danh dau ro trong tung API.

### 2.2 Standard Success Envelope
Tat ca response thanh cong nen theo format:

```json
{
  "success": true,
  "data": {},
  "meta": {
    "requestId": "req_01JXYZ...",
    "timestamp": "2026-03-25T10:30:00Z"
  }
}
```

### 2.3 Standard Error Envelope
Tat ca loi nen theo format:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Field 'question' is required",
    "details": {
      "field": "question"
    }
  },
  "meta": {
    "requestId": "req_01JXYZ...",
    "timestamp": "2026-03-25T10:30:00Z"
  }
}
```

### 2.4 Error Codes (recommended)
- `INVALID_INPUT` -> 400
- `UNAUTHENTICATED` -> 401
- `FORBIDDEN` -> 403
- `NOT_FOUND` -> 404
- `CONFLICT` -> 409
- `RATE_LIMITED` -> 429
- `UPSTREAM_UNAVAILABLE` -> 503
- `INTERNAL_ERROR` -> 500

### 2.5 Idempotency
Cho cac API co side-effect (chat ask, login, verify, fallback), khuyen nghi ho tro:
- Header: `Idempotency-Key: <uuid>`

Neu trung key trong vong 24h, tra lai ket qua da ghi nhan truoc do.

## 3. Auth + Identity (P0)

## 3.1 POST /auth/login
Muc dich:
- Dang nhap bang account noi bo hoac SSO bridge.

Auth:
- Anonymous

Request:

```json
{
  "provider": "local",
  "identifier": "sv00123",
  "password": "secret",
  "device": {
    "ip": "203.0.113.10",
    "userAgent": "Mozilla/5.0"
  }
}
```

Validation:
- `provider`: required, enum: `local|sso`
- `identifier`: required, max 100
- `password`: required neu `provider=local`

Response 200:

```json
{
  "success": true,
  "data": {
    "accessToken": "eyJ...",
    "refreshToken": "eyJ...",
    "expiresIn": 3600,
    "tokenType": "Bearer",
    "user": {
      "id": "usr_001",
      "userCode": "SV00123",
      "role": "student",
      "fullName": "Nguyen Van A",
      "email": "a@example.edu",
      "authProvider": "local",
      "isActive": true
    }
  },
  "meta": {
    "requestId": "req_login_001",
    "timestamp": "2026-03-25T10:30:00Z"
  }
}
```

Status codes:
- 200 login thanh cong
- 400 payload khong hop le
- 401 sai thong tin dang nhap
- 423 tai khoan bi khoa
- 500 loi he thong

## 3.2 POST /auth/refresh
Muc dich:
- Cap moi access token.

Auth:
- Anonymous (dua tren refresh token)

Request:

```json
{
  "refreshToken": "eyJ..."
}
```

Response 200:

```json
{
  "success": true,
  "data": {
    "accessToken": "eyJ_new...",
    "expiresIn": 3600,
    "tokenType": "Bearer"
  },
  "meta": {
    "requestId": "req_refresh_001",
    "timestamp": "2026-03-25T10:31:00Z"
  }
}
```

Status codes:
- 200 thanh cong
- 401 refresh token het han/khong hop le
- 500 loi he thong

## 3.3 GET /auth/me
Muc dich:
- Lay thong tin user dang dang nhap.

Auth:
- Required

Response 200:

```json
{
  "success": true,
  "data": {
    "id": "usr_001",
    "userCode": "SV00123",
    "role": "student",
    "fullName": "Nguyen Van A",
    "email": "a@example.edu",
    "authProvider": "local",
    "createdAt": "2026-01-02T10:00:00Z",
    "updatedAt": "2026-03-10T07:30:00Z",
    "isActive": true
  },
  "meta": {
    "requestId": "req_me_001",
    "timestamp": "2026-03-25T10:32:00Z"
  }
}
```

Status codes:
- 200 thanh cong
- 401 chua dang nhap/token loi

## 3.4 POST /auth/verify-student
Muc dich:
- Verify nhanh student identity cho use case lich thi ca nhan (neu chua SSO day du).

Auth:
- Optional token (cho phep anonymous + thong tin doi chieu)

Request:

```json
{
  "studentCode": "SV00123",
  "birthDate": "2004-08-10",
  "courseCode": "SE101"
}
```

Response 200:

```json
{
  "success": true,
  "data": {
    "verified": true,
    "studentId": "stu_001",
    "fullName": "Nguyen Van A",
    "verificationLevel": "basic"
  },
  "meta": {
    "requestId": "req_verify_001",
    "timestamp": "2026-03-25T10:33:00Z"
  }
}
```

Status codes:
- 200 verify thanh cong
- 400 payload sai
- 401 khong verify duoc
- 429 qua tan suat

## 4. Chat Orchestration (P0)

## 4.1 POST /chat/ask
Muc dich:
- API trung tam cho chatbot: classify intent, route nghiep vu, truy van RAG/API ngoai, tra loi + citation.

Auth:
- Optional
- Rule:
  - `regulation` va `study_support`: cho phep anonymous
  - `exam_schedule`: bat buoc xac thuc hoac verify student

Request:

```json
{
  "sessionId": "ses_001",
  "question": "Mai minh thi mon Nhap mon Ky thuat phan mem luc may gio?",
  "context": {
    "channel": "web",
    "locale": "vi-VN",
    "persona": "friendly"
  },
  "user": {
    "studentCode": "SV00123"
  }
}
```

Validation:
- `question`: required, 1..4000 ky tu
- `sessionId`: optional; neu null backend tao moi

Response 200:

```json
{
  "success": true,
  "data": {
    "sessionId": "ses_001",
    "messageId": "msg_bot_001",
    "intent": {
      "name": "exam_schedule",
      "confidence": 0.94
    },
    "answer": {
      "text": "Ban co lich thi luc 09:00 ngay 2026-03-26 tai phong A2.302.",
      "tone": "friendly",
      "requiresFollowUp": false
    },
    "citations": [
      {
        "type": "system_api",
        "source": "training_system_exam_schedule",
        "ref": "exam_schedule:sch_123"
      }
    ],
    "entities": {
      "courseName": "Nhap mon Ky thuat phan mem",
      "date": "2026-03-26"
    },
    "fallback": {
      "triggered": false,
      "reason": null
    }
  },
  "meta": {
    "requestId": "req_chat_001",
    "timestamp": "2026-03-25T10:35:00Z"
  }
}
```

Status codes:
- 200 thanh cong
- 400 payload sai
- 401 intent can auth nhung chua auth
- 422 khong trich xuat du entity toi thieu
- 429 qua tan suat
- 503 dependency (LLM/vector db/upstream exam API) tam thoi unavailable

## 4.2 POST /chat/sessions/{sessionId}/end
Muc dich:
- Ket thuc phien chat, cap nhat `sessionStatus=closed`, `endedAt`.

Auth:
- Required (hoac anonymous token lien ket session)

Path params:
- `sessionId`: required

Response 200:

```json
{
  "success": true,
  "data": {
    "sessionId": "ses_001",
    "sessionStatus": "closed",
    "endedAt": "2026-03-25T10:40:00Z"
  },
  "meta": {
    "requestId": "req_end_001",
    "timestamp": "2026-03-25T10:40:00Z"
  }
}
```

Status codes:
- 200 thanh cong
- 401 chua dang nhap/khong co quyen
- 404 khong tim thay session
- 409 session da dong

## 4.3 GET /chat/sessions/{sessionId}/context
Muc dich:
- Lay context conversation de UI render va phuc vu multi-turn.

Auth:
- Required (hoac token anonymous dung session)

Query params:
- `limit` (optional, default 20, max 100)
- `beforeMessageId` (optional)

Response 200:

```json
{
  "success": true,
  "data": {
    "session": {
      "id": "ses_001",
      "userId": "usr_001",
      "channel": "web",
      "persona": "friendly",
      "sessionStatus": "active",
      "startedAt": "2026-03-25T10:00:00Z",
      "endedAt": null,
      "isActive": true
    },
    "messages": [
      {
        "id": "msg_user_001",
        "senderType": "user",
        "intent": "unknown",
        "content": "Cho minh hoi...",
        "citations": [],
        "entities": {},
        "createdAt": "2026-03-25T10:01:00Z",
        "isActive": true
      }
    ]
  },
  "meta": {
    "requestId": "req_ctx_001",
    "timestamp": "2026-03-25T10:41:00Z"
  }
}
```

Status codes:
- 200 thanh cong
- 401 khong hop le
- 404 khong tim thay session

## 5. Regulation RAG (P0)

## 5.1 POST /regulations/query
Muc dich:
- Semantic retrieval tren quy che + answer co trich dan dieu/khoan.

Auth:
- Anonymous allowed

Request:

```json
{
  "query": "Dem dien thoai vao phong thi bi xu ly sao?",
  "topK": 5,
  "regulationVersion": "2026.1",
  "locale": "vi-VN"
}
```

Validation:
- `query`: required, 3..2000
- `topK`: optional, default 5, max 10

Response 200:

```json
{
  "success": true,
  "data": {
    "answer": "Theo Dieu 12, Khoan 3, sinh vien mang dien thoai vao phong thi co the bi lap bien ban...",
    "citations": [
      {
        "regulationId": "reg_001",
        "regulationCode": "QC-EXAM",
        "version": "2026.1",
        "article": "12",
        "clause": "3",
        "chunkId": "chk_991",
        "quote": "Sinh vien khong duoc mang thiet bi thu phat...",
        "sourceUrl": "https://example.edu/regulation.pdf"
      }
    ],
    "retrieval": {
      "topK": 5,
      "latencyMs": 182,
      "modelVersion": "rag-v1"
    }
  },
  "meta": {
    "requestId": "req_reg_001",
    "timestamp": "2026-03-25T10:45:00Z"
  }
}
```

Status codes:
- 200 thanh cong
- 400 query khong hop le
- 404 khong tim thay nguon quy che phu hop
- 422 ket qua retrieval confidence thap (buoc vao fallback)
- 503 vector store/LLM unavailable

## 6. Personalized Exam Schedule (P0)

## 6.1 GET /me/exam-schedules/upcoming
Muc dich:
- Lay danh sach lich thi sap toi cua user dang dang nhap.

Auth:
- Required

Query params:
- `days` (optional, default 14, max 60)
- `status` (optional: `scheduled|rescheduled|cancelled`)

Response 200:

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "sch_123",
        "examId": "ex_001",
        "studentId": "stu_001",
        "examDate": "2026-03-26",
        "startTime": "2026-03-26T09:00:00Z",
        "room": "A2.302",
        "status": "scheduled",
        "updatedAt": "2026-03-24T04:00:00Z",
        "isActive": true,
        "course": {
          "courseCode": "SE101",
          "courseName": "Nhap mon Ky thuat phan mem"
        }
      }
    ],
    "total": 1
  },
  "meta": {
    "requestId": "req_upcoming_001",
    "timestamp": "2026-03-25T10:50:00Z"
  }
}
```

Status codes:
- 200 thanh cong
- 401 chua dang nhap
- 404 khong tim thay du lieu lich thi
- 503 upstream he thong dao tao unavailable

## 6.2 GET /me/exam-schedules/today
Muc dich:
- Lay lich thi trong ngay cua user.

Auth:
- Required

Response 200:
- Tuong tu `/me/exam-schedules/upcoming` nhung da filter theo ngay hien tai.

Status codes:
- 200, 401, 503

## 6.3 GET /me/exam-schedules
Muc dich:
- Tim lich thi theo khoang ngay/mon hoc.

Auth:
- Required

Query params:
- `fromDate` (required, YYYY-MM-DD)
- `toDate` (required, YYYY-MM-DD)
- `courseCode` (optional)
- `status` (optional)

Response 200:
- Giong contract list o endpoint upcoming.

Status codes:
- 200 thanh cong
- 400 date range khong hop le
- 401 chua dang nhap
- 503 upstream unavailable

## 6.4 GET /me/exams/next
Muc dich:
- Lay ky thi gan nhat tiep theo.

Auth:
- Required

Response 200:

```json
{
  "success": true,
  "data": {
    "nextExam": {
      "id": "sch_123",
      "examId": "ex_001",
      "examDate": "2026-03-26",
      "startTime": "2026-03-26T09:00:00Z",
      "room": "A2.302",
      "status": "scheduled",
      "course": {
        "courseCode": "SE101",
        "courseName": "Nhap mon Ky thuat phan mem"
      }
    }
  },
  "meta": {
    "requestId": "req_next_exam_001",
    "timestamp": "2026-03-25T10:52:00Z"
  }
}
```

Status codes:
- 200 thanh cong
- 204 khong co lich thi sap toi
- 401 chua dang nhap
- 503 upstream unavailable

## 7. Safety + Fallback (P0)

## 7.1 POST /safety/check-query
Muc dich:
- Danh gia query co nhay cam/vuot tham quyen/yeu cau du lieu ca nhan hay khong.

Auth:
- Anonymous allowed

Request:

```json
{
  "query": "Cho toi diem thi cua ban Nguyen Van B",
  "context": {
    "intent": "unknown",
    "userRole": "student"
  }
}
```

Response 200:

```json
{
  "success": true,
  "data": {
    "allowed": false,
    "riskLevel": "high",
    "categories": ["privacy", "out_of_scope"],
    "action": "fallback",
    "reason": "requests_personal_sensitive_data"
  },
  "meta": {
    "requestId": "req_safety_001",
    "timestamp": "2026-03-25T10:55:00Z"
  }
}
```

Status codes:
- 200 thanh cong
- 400 payload sai
- 429 qua tan suat

## 7.2 POST /fallback/respond
Muc dich:
- Tra thong diep fallback chuan hoa, khong hallucinate, co huong dan hoi lai.

Auth:
- Anonymous allowed

Request:

```json
{
  "reason": "insufficient_evidence",
  "originalQuestion": "Diem so chi tiet cua ban X la bao nhieu?",
  "intent": "unknown",
  "locale": "vi-VN"
}
```

Response 200:

```json
{
  "success": true,
  "data": {
    "message": "Minh chua du co so de tra loi chinh xac cau hoi nay. Ban co the cung cap them mon hoc/ma sinh vien hoac lien he phong giao vu.",
    "suggestions": [
      "Ban co the hoi lai theo dinh dang: lich thi + ngay + mon hoc",
      "Neu can thong tin ca nhan, vui long dang nhap"
    ],
    "contact": {
      "unit": "Phong giao vu",
      "email": "giaovu@example.edu",
      "phone": "028-1234-5678"
    }
  },
  "meta": {
    "requestId": "req_fallback_001",
    "timestamp": "2026-03-25T10:56:00Z"
  }
}
```

Status codes:
- 200 thanh cong
- 400 payload sai

## 7.3 GET /escalation/contacts
Muc dich:
- Tra ve danh sach don vi lien he khi can escalate.

Auth:
- Anonymous allowed

Response 200:

```json
{
  "success": true,
  "data": {
    "contacts": [
      {
        "unit": "Phong giao vu",
        "email": "giaovu@example.edu",
        "phone": "028-1234-5678",
        "hours": "08:00-17:00"
      }
    ]
  },
  "meta": {
    "requestId": "req_contact_001",
    "timestamp": "2026-03-25T10:57:00Z"
  }
}
```

Status codes:
- 200 thanh cong

## 8. Non-Functional Acceptance (P0)

## 8.1 Performance SLO
- `/chat/ask` p95 <= 3.5s (khong stream)
- `/regulations/query` p95 <= 2.0s
- `/me/exam-schedules/*` p95 <= 1.5s (khong tinh downtime upstream)

## 8.2 Reliability
- Tat ca endpoint phai tra `requestId` de trace.
- Co retry policy cho upstream exam API (toi da 2 lan, exponential backoff).
- Khi upstream loi, tra 503 + message ro rang.

## 8.3 Security
- Mask du lieu nhay cam trong log (`password`, token, pii).
- Rate limit toi thieu cho endpoint anonymous: 60 req/phut/ip.
- Kiem soat RBAC cho endpoint can auth.

## 9. OpenAPI Tag Mapping (recommended)
- `Auth`: `/auth/*`
- `Chat`: `/chat/*`
- `Regulations`: `/regulations/query`
- `ExamSchedule`: `/me/exam-schedules/*`, `/me/exams/next`
- `Safety`: `/safety/check-query`, `/fallback/respond`, `/escalation/contacts`

## 10. Minimum Implementation Checklist
- [ ] Implement full request validation cho tat ca endpoint P0
- [ ] Implement success/error envelope dong nhat
- [ ] Implement JWT auth middleware + RBAC co ban
- [ ] Implement audit log cho endpoint co side-effect
- [ ] Implement contract tests (happy path + error path) cho moi endpoint P0
