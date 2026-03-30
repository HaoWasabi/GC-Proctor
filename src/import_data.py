import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Khởi tạo Firebase
cred = credentials.Certificate("D:\do_an\AI\GC-Proctor\src\configs\serviceAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_now():
    return datetime.now()

# Data Payload chi tiết cho 10 bảng (mỗi bảng 10 records)
data_payload = {
    "USERS": [
        {"_id": f"u{i:03}", "userCode": f"3122410{i:03}", "role": "student" if i < 9 else "admin", 
         "fullName": f"User Name {i}", "email": f"user{i}@sgu.edu.vn", "authProvider": "google", "createdAt": get_now()}
        for i in range(1, 11)
    ],
    "COURSES": [
        {"_id": f"c{i:03}", "courseCode": f"84140{i}", "courseName": f"Mon hoc {i}", 
         "faculty": "CNTT", "semester": "HK2-2025-2026", "createdAt": get_now()}
        for i in range(1, 11)
    ],
    "EXAMS": [
        {"_id": f"ex{i:03}", "courseId": f"c{i:03}", "examType": "Final" if i%2==0 else "Midterm", 
         "durationMinutes": 90, "policyVersion": "v1.0", "createdAt": get_now()}
        for i in range(1, 11)
    ],
    "EXAM_SCHEDULES": [
        {"_id": f"s{i:03}", "examId": f"ex{i:03}", "studentId": "u003", "examDate": "2026-04-10", 
         "startTime": "07:30", "room": f"C.E{400+i}", "status": "scheduled", "updatedAt": get_now()}
        for i in range(1, 11)
    ],
    "REGULATIONS": [
        {"_id": f"reg{i:03}", "regulationCode": f"REG-{i}", "title": f"Quy dinh thi so {i}", 
         "version": "1.0", "effectiveDate": "2026-01-01", "sourceUrl": "http://sgu.edu.vn", "updatedAt": get_now()}
        for i in range(1, 11)
    ],
    "DOCUMENTS": [
        {"_id": f"doc{i:03}", "docType": "PDF", "title": f"Tai lieu {i}", "ownerType": "course", 
         "ownerId": f"c{i:03}", "storagePath": f"gs://bucket/doc{i}.pdf", "language": "vi", "createdAt": get_now()}
        for i in range(1, 11)
    ],
    "DOCUMENT_CHUNKS": [
        {"_id": f"chk{i:03}", "documentId": "doc001", "chunkIndex": i, "content": f"Noi dung doan {i} cua tai lieu...", 
         "embeddingId": f"vec_{i}", "scoreThreshold": 0.8, "createdAt": get_now()}
        for i in range(1, 11)
    ],
    "CHAT_SESSIONS": [
        {"_id": f"sess{i:03}", "userId": "u003", "channel": "web", "persona": "Assistant", 
         "sessionStatus": "active", "startedAt": get_now()}
        for i in range(1, 11)
    ],
    "CHAT_MESSAGES": [
        {"_id": f"msg{i:03}", "sessionId": "sess001", "senderType": "user" if i%2!=0 else "bot", 
         "intent": "ask_exam", "content": f"Cau hoi/Tra loi thu {i}", "citations": [], "entities": {}, "createdAt": get_now()}
        for i in range(1, 11)
    ],
    "RETRIEVAL_LOGS": [
        {"_id": f"log{i:03}", "messageId": "msg001", "chunkId": f"chk{i:03}", "similarity": 0.95 - (i*0.01), 
         "retrieverVersion": "v1-rag", "createdAt": get_now()}
        for i in range(1, 11)
    ],
    "FEEDBACKS": [
        {"_id": f"fb{i:03}", "userId": "u003", "messageId": f"msg{i:03}", "rating": 5 if i%2==0 else 4, 
         "comment": "Tot", "createdAt": get_now()}
        for i in range(1, 11)
    ],
    "AUDIT_LOGS": [
        {"_id": f"audit{i:03}", "actorUserId": "u003", "actionType": "QUERY", "targetCollection": "EXAMS", 
         "targetId": "ex001", "metadata": {"ip": "127.0.0.1"}, "createdAt": get_now()}
        for i in range(1, 11)
    ]
}

def run_import():
    """Thực hiện đẩy dữ liệu lên Firestore theo batch để tối ưu hiệu suất."""
    batch = db.batch()
    count = 0
    
    for coll_name, docs in data_payload.items():
        print(f"Dang chuan bi: {coll_name}")
        for d in docs:
            doc_id = d["_id"]
            data = {k: v for k, v in d.items() if k != "_id"}
            
            doc_ref = db.collection(coll_name).document(doc_id)
            batch.set(doc_ref, data)
            count += 1
            
            # Firestore batch gioi han 500 operations
            if count >= 400:
                batch.commit()
                batch = db.batch()
                count = 0
                
    batch.commit()
    print("\n>>> Da import thanh cong toan bo du lieu cho GC-Proctor!")

if __name__ == "__main__":
    run_import()