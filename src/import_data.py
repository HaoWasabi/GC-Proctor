import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Khởi tạo Firebase
cred = credentials.Certificate("D:\do_an\AI\GC-Proctor\src\configs\serviceAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_now():
    return datetime.now()

data_payload = {}  # Tạo payload tổng để chứa dữ liệu cho tất cả các bảng

# Data Payload chi tiết cho 10 bảng (mỗi bảng 10 records)
# data_payload = {
#     "USERS": [
#         {"_id": f"u{i:03}", "userCode": f"3122410{i:03}", "role": "student" if i < 9 else "admin", 
#          "fullName": f"User Name {i}", "email": f"user{i}@sgu.edu.vn", "authProvider": "google", "createdAt": get_now()}
#         for i in range(1, 11)
#     ],
#     "COURSES": [
#         {"_id": f"c{i:03}", "courseCode": f"84140{i}", "courseName": f"Mon hoc {i}", 
#          "faculty": "CNTT", "semester": "HK2-2025-2026", "createdAt": get_now()}
#         for i in range(1, 11)
#     ],
#     "EXAMS": [
#         {"_id": f"ex{i:03}", "courseId": f"c{i:03}", "examType": "Final" if i%2==0 else "Midterm", 
#          "durationMinutes": 90, "policyVersion": "v1.0", "createdAt": get_now()}
#         for i in range(1, 11)
#     ],
#     "EXAM_SCHEDULES": [
#         {"_id": f"s{i:03}", "examId": f"ex{i:03}", "studentId": "u003", "examDate": "2026-04-10", 
#          "startTime": "07:30", "room": f"C.E{400+i}", "status": "scheduled", "updatedAt": get_now()}
#         for i in range(1, 11)
#     ],
#     "REGULATIONS": [
#         {"_id": f"reg{i:03}", "regulationCode": f"REG-{i}", "title": f"Quy dinh thi so {i}", 
#          "version": "1.0", "effectiveDate": "2026-01-01", "sourceUrl": "http://sgu.edu.vn", "updatedAt": get_now()}
#         for i in range(1, 11)
#     ],
#     "DOCUMENTS": [
#         {"_id": f"doc{i:03}", "docType": "PDF", "title": f"Tai lieu {i}", "ownerType": "course", 
#          "ownerId": f"c{i:03}", "storagePath": f"gs://bucket/doc{i}.pdf", "language": "vi", "createdAt": get_now()}
#         for i in range(1, 11)
#     ],
#     "DOCUMENT_CHUNKS": [
#         {"_id": f"chk{i:03}", "documentId": "doc001", "chunkIndex": i, "content": f"Noi dung doan {i} cua tai lieu...", 
#          "embeddingId": f"vec_{i}", "scoreThreshold": 0.8, "createdAt": get_now()}
#         for i in range(1, 11)
#     ],
#     "CHAT_SESSIONS": [
#         {"_id": f"sess{i:03}", "userId": "u003", "channel": "web", "persona": "Assistant", 
#          "sessionStatus": "active", "startedAt": get_now()}
#         for i in range(1, 11)
#     ],
#     "CHAT_MESSAGES": [
#         {"_id": f"msg{i:03}", "sessionId": "sess001", "senderType": "user" if i%2!=0 else "bot", 
#          "intent": "ask_exam", "content": f"Cau hoi/Tra loi thu {i}", "citations": [], "entities": {}, "createdAt": get_now()}
#         for i in range(1, 11)
#     ],
#     "RETRIEVAL_LOGS": [
#         {"_id": f"log{i:03}", "messageId": "msg001", "chunkId": f"chk{i:03}", "similarity": 0.95 - (i*0.01), 
#          "retrieverVersion": "v1-rag", "createdAt": get_now()}
#         for i in range(1, 11)
#     ],
#     "FEEDBACKS": [
#         {"_id": f"fb{i:03}", "userId": "u003", "messageId": f"msg{i:03}", "rating": 5 if i%2==0 else 4, 
#          "comment": "Tot", "createdAt": get_now()}
#         for i in range(1, 11)
#     ],
#     "AUDIT_LOGS": [
#         {"_id": f"audit{i:03}", "actorUserId": "u003", "actionType": "QUERY", "targetCollection": "EXAMS", 
#          "targetId": "ex001", "metadata": {"ip": "127.0.0.1"}, "createdAt": get_now()}
#         for i in range(1, 11)
#     ]
# }

regulations_data = [
    {
        "_id": "reg001",
        "regulationCode": "258/QĐ-ĐHSG",
        "title": "Quy chế đào tạo trình độ đại học Trường Đại học Sài Gòn",
        "version": "2022",
        "effectiveDate": "2022-02-22",
        "sourceUrl": "https://daotao.sgu.edu.vn/images/pdf/quy_dinh/4.%20QuyCheDaoTaoDHSG%202021.pdf",
        "updatedAt": str(get_now())
    }
]

documents_data = [
    {
        "_id": "doc_258",
        "docType": "PDF",
        "title": "Toàn văn Quy chế đào tạo 258",
        "ownerType": "regulation",
        "ownerId": "reg_258",
        "storagePath": "gs://sgu-storage/4. QuyCheDaoTaoDHSG 2021.pdf",
        "language": "vi",
        "createdAt": str(get_now())
    }
]

document_chunks_data = [
    {
        "_id": "chk_258_001",
        "documentId": "doc_258",
        "chunkIndex": 0,
        "content": "Điều 2: Thời gian hoạt động giảng dạy từ 6 giờ đến 22 giờ hàng ngày. Thời gian cho 1 tiết học là 50 phút. Học kỳ chính có ít nhất 15 tuần thực học, học kỳ phụ có ít nhất 05 tuần thực học.",
        "embeddingId": "vec_001", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_258_002",
        "documentId": "doc_258",
        "chunkIndex": 1,
        "content": "Điều 6: Thời gian tối đa để sinh viên hoàn thành khóa học được quy định: Đối với khóa 4 năm là 8 năm (16 học kỳ chính); khóa 3.5 năm là 7 năm; khóa 3 năm là 6 năm.",
        "embeddingId": "vec_002", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_258_003",
        "documentId": "doc_258",
        "chunkIndex": 2,
        "content": "Điều 8: Đăng ký học phần. Sinh viên đăng ký tối thiểu 15 tín chỉ/học kỳ chính (trừ học kỳ cuối) và tối đa 25 tín chỉ/học kỳ chính. Với sinh viên học lực yếu, tối thiểu là 10 tín và tối đa là 14 tín.",
        "embeddingId": "vec_003", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_258_004",
        "documentId": "doc_258",
        "chunkIndex": 3,
        "content": "Điều 9: Đánh giá học phần. Điểm học phần bao gồm điểm quá trình (trọng số không dưới 40%) và điểm thi kết thúc học phần (trọng số từ 40% đến 60%).",
        "embeddingId": "vec_004", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_258_005",
        "documentId": "doc_258",
        "chunkIndex": 4,
        "content": "Điều 10: Phân loại học lực theo điểm trung bình tích lũy (thang 4): Xuất sắc: 3.60-4.00; Giỏi: 3.20-3.59; Khá: 2.50-3.19; Trung bình: 2.00-2.49; Yếu: 1.00-1.99; Kém: Dưới 1.00.",
        "embeddingId": "vec_005", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_258_006",
        "documentId": "doc_258",
        "chunkIndex": 5,
        "content": "Điều 11: Cảnh báo kết quả học tập. Sinh viên bị cảnh báo nếu: Điểm trung bình học kỳ < 0.8 (HK đầu), < 1.0 (HK tiếp theo); hoặc Điểm trung bình tích lũy < 1.2 (năm 1), < 1.4 (năm 2), < 1.6 (năm 3), < 1.8 (các năm tiếp theo).",
        "embeddingId": "vec_006", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_258_007",
        "documentId": "doc_258",
        "chunkIndex": 6,
        "content": "Điều 12: Buộc thôi học. Sinh viên bị buộc thôi học nếu: Đã bị cảnh báo học tập 02 lần liên tiếp; Vượt quá thời gian tối đa hoàn thành khóa học; Bị kỷ luật mức đuổi học.",
        "embeddingId": "vec_007", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_258_008",
        "documentId": "doc_258",
        "chunkIndex": 7,
        "content": "Điều 14: Sinh viên được quyền nghỉ học tạm thời và bảo lưu kết quả không quá 04 học kỳ chính (đối với khóa học 4 năm). Phải nộp đơn trước khi học kỳ bắt đầu.",
        "embeddingId": "vec_008", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_258_009",
        "documentId": "doc_258",
        "chunkIndex": 8,
        "content": "Điều 15: Chuyển ngành. Điều kiện: Không phải SV năm nhất hoặc năm cuối; Không bị kỷ luật; Đạt điểm trúng tuyển của ngành chuyển đến trong cùng năm tuyển sinh.",
        "embeddingId": "vec_009", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_258_010",
        "documentId": "doc_258",
        "chunkIndex": 9,
        "content": "Điều 16: Học cùng lúc hai chương trình (Song bằng). Điều kiện: SV đã kết thúc năm thứ nhất; Học lực tích lũy loại Khá trở lên; Không thuộc diện cảnh báo học tập.",
        "embeddingId": "vec_010", "scoreThreshold": 0.8, "createdAt": get_now()
    }
]

document_chunks_data = [
    # --- CHƯƠNG 1: QUY ĐỊNH CHUNG & CHƯƠNG TRÌNH ĐÀO TẠO ---
    {
        "_id": "chk_qc_001",
        "documentId": "doc_258",
        "chunkIndex": 0,
        "content": "Điều 1.1 & 1.2: Quy chế này cụ thể hóa Thông tư 08/2021/TT-BGDĐT, áp dụng cho người học, giảng viên và cán bộ tham gia đào tạo trình độ đại học tại Trường Đại học Sài Gòn.",
        "embeddingId": "vec_001", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_qc_002",
        "documentId": "doc_258",
        "chunkIndex": 1,
        "content": "Điều 2.1 & 2.2: Chương trình đào tạo (CTĐT) xây dựng theo tín chỉ, gồm các học phần bắt buộc và tự chọn. Chuẩn đầu ra áp dụng chung cho mọi hình thức đào tạo. Người đã tốt nghiệp trình độ khác có thể được công nhận hoặc chuyển đổi tín chỉ.",
        "embeddingId": "vec_002", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_qc_003",
        "documentId": "doc_258",
        "chunkIndex": 2,
        "content": "Điều 2.4.a: Thời gian học chuẩn (Chính quy): Cử nhân (120 tín chỉ): 4 năm; Kỹ sư (150 tín chỉ): 4.5 năm; Liên thông Trung cấp lên ĐH (85 tín): 2.5 năm; Liên thông Cao đẳng lên ĐH hoặc Bằng thứ hai (60 tín): 2.0 năm.",
        "embeddingId": "vec_003", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_qc_004",
        "documentId": "doc_258",
        "chunkIndex": 3,
        "content": "Điều 2.5: Thời gian tối đa hoàn thành khóa học không vượt quá 02 lần thời gian theo kế hoạch học tập chuẩn. Với hệ liên thông/văn bằng 2, thời gian tối đa giảm tương ứng với khối lượng tín chỉ được miễn trừ.",
        "embeddingId": "vec_004", "scoreThreshold": 0.8, "createdAt": get_now()
    },

    # --- HÌNH THỨC & KẾ HOẠCH ĐÀO TẠO ---
    {
        "_id": "chk_qc_005",
        "documentId": "doc_258",
        "chunkIndex": 4,
        "content": "Điều 3.2 & 3.3: Đào tạo theo tín chỉ cho phép cá nhân hóa kế hoạch học tập. Học phần bắt buộc không đạt phải học lại (hoặc học học phần tương đương/thay thế). Học phần tự chọn không đạt có thể học lại hoặc chọn học phần tự chọn khác.",
        "embeddingId": "vec_005", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_qc_006",
        "documentId": "doc_258",
        "chunkIndex": 5,
        "content": "Điều 4.1: Đào tạo chính quy tổ chức giảng dạy từ 06g00 đến 20g00 từ Thứ 2 đến Thứ 7 tại các cơ sở của Trường. Thực tập hoặc giảng dạy trực tuyến có thể thực hiện ngoài Trường.",
        "embeddingId": "vec_006", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_qc_007",
        "documentId": "doc_258",
        "chunkIndex": 6,
        "content": "Điều 6.1 & 6.2: Mỗi năm học có 02 học kỳ chính (tối thiểu 15 tuần thực học/kỳ, tổng 30 tuần/năm) và 01 học kỳ phụ (tối thiểu 05 tuần).",
        "embeddingId": "vec_007", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_qc_008",
        "documentId": "doc_258",
        "chunkIndex": 7,
        "content": "Điều 6.4: Thời khóa biểu bố trí đều các tuần. Trường hợp học tập trung, số giờ giảng không vượt quá 15 giờ/tuần và không quá 4 giờ/ngày.",
        "embeddingId": "vec_008", "scoreThreshold": 0.8, "createdAt": get_now()
    },

    # --- CHƯƠNG 2: ĐÁNH GIÁ KẾT QUẢ HỌC TẬP & ĐIỂM SỐ ---
    {
        "_id": "chk_qc_009",
        "documentId": "doc_258",
        "chunkIndex": 8,
        "content": "Điều 9.1: Mỗi học phần có ít nhất 2 điểm thành phần chấm theo thang điểm 10. Đánh giá trực tuyến (không quá 50% trọng số) yêu cầu tính trung thực, công bằng như trực tiếp.",
        "embeddingId": "vec_009", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_qc_010",
        "documentId": "doc_258",
        "chunkIndex": 9,
        "content": "Điều 9.2: Vắng thi không lý do chính đáng nhận điểm 0. Vắng thi có lý do chính đáng được dự thi đợt khác và tính điểm lần đầu.",
        "embeddingId": "vec_010", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_qc_011",
        "documentId": "doc_258",
        "chunkIndex": 10,
        "content": "Điều 9.3 (Xếp loại điểm chữ): Loại Đạt: A (8.5-10.0), B (7.0-8.4), C (5.5-6.9), D (4.0-5.4). Loại Không đạt: F (dưới 4.0). Điểm P dành cho học phần không tính trung bình học tập.",
        "embeddingId": "vec_011", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_qc_012",
        "documentId": "doc_258",
        "chunkIndex": 11,
        "content": "Điều 9.3.d (Ký hiệu đặc biệt): I (Hoãn thi/kiểm tra); X (Chưa đủ dữ liệu); R (Được miễn học và công nhận tín chỉ). Các ký hiệu này không tính vào điểm trung bình.",
        "embeddingId": "vec_012", "scoreThreshold": 0.8, "createdAt": get_now()
    },
    {
        "_id": "chk_qc_013",
        "documentId": "doc_258",
        "chunkIndex": 12,
        "content": "Điều 9.4: Học lại và Cải thiện: Điểm học phần không đạt (F) phải học lại. Người học đã đạt có thể đăng ký học lại để cải thiện điểm. Điểm chính thức là điểm cao nhất giữa các lần học.",
        "embeddingId": "vec_013", "scoreThreshold": 0.8, "createdAt": get_now()
    }
]

# Gán vào payload tổng
data_payload["regulations"] = regulations_data
data_payload["documents"] = documents_data
data_payload["document_chunks"] = document_chunks_data

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