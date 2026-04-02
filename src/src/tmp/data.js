var externalData = [
  {
    "id": "root",
    "text": "LangGraph",
    "x": 520.0,
    "y": 280.0,
    "parentId": null
  },
  {
    "id": "c1",
    "text": "I. Các thành phần cốt lõi",
    "x": 770.0,
    "y": 180.0,
    "parentId": "root"
  },
  {
    "id": "c1.1",
    "text": "1. State (Trạng thái dùng chung)",
    "x": 1020.0,
    "y": 130.0,
    "parentId": "c1"
  },
  {
    "id": "c1.1.1",
    "text": "Vai trò: Bộ nhớ RAM dùng chung",
    "x": 1270.0,
    "y": -20.0,
    "parentId": "c1.1"
  },
  {
    "id": "c1.1.2",
    "text": "Chức năng: Lưu trữ mọi thông tin từ lúc chat đến khi lịch chốt",
    "x": 1270.0,
    "y": 80.0,
    "parentId": "c1.1"
  },
  {
    "id": "c1.1.3",
    "text": "Cơ chế: Mọi Node đọc và ghi dữ liệu vào State",
    "x": 1270.0,
    "y": 180.0,
    "parentId": "c1.1"
  },
  {
    "id": "c1.1.4",
    "text": "Ví dụ: SchedulingState (chứa messages, web_search_result, cal_search_result, final_plan, v.v.)",
    "x": 1270.0,
    "y": 280.0,
    "parentId": "c1.1"
  },
  {
    "id": "c1.2",
    "text": "2. Nodes/Edges (Các nút và cạnh điều hướng)",
    "x": 1020.0,
    "y": 230.0,
    "parentId": "c1"
  },
  {
    "id": "c1.2.1",
    "text": "Nodes (Nút): Các bước xử lý hoặc hàm trong đồ thị",
    "x": 1270.0,
    "y": 180.0,
    "parentId": "c1.2"
  },
  {
    "id": "c1.2.1.1",
    "text": "Ví dụ Nodes: router, info_checker, gather_info, supervisor, feedback_analyzer, executor",
    "x": 1520.0,
    "y": 180.0,
    "parentId": "c1.2.1"
  },
  {
    "id": "c1.2.2",
    "text": "Edges (Cạnh): Điều hướng luồng giữa các Nodes",
    "x": 1270.0,
    "y": 280.0,
    "parentId": "c1.2"
  },
  {
    "id": "c1.2.2.1",
    "text": "Các loại Edge: add_edge, add_conditional_edges",
    "x": 1520.0,
    "y": 230.0,
    "parentId": "c1.2.2"
  },
  {
    "id": "c1.2.2.2",
    "text": "Ví dụ Edges: START -> router, router (conditional), info_checker (conditional), gather_info -> supervisor, supervisor -> END, feedback_analyzer (conditional), executor -> END",
    "x": 1520.0,
    "y": 330.0,
    "parentId": "c1.2.2"
  },
  {
    "id": "c2",
    "text": "II. Tích hợp tính năng nâng cao",
    "x": 770.0,
    "y": 280.0,
    "parentId": "root"
  },
  {
    "id": "c2.1",
    "text": "1. Cơ chế Bộ nhớ Ngắn hạn (Conversational Memory với Checkpointer)",
    "x": 1020.0,
    "y": 280.0,
    "parentId": "c2"
  },
  {
    "id": "c2.1.1",
    "text": "Mục đích: Lưu lại mọi điểm kiểm soát (Checkpoints) của đồ thị",
    "x": 1270.0,
    "y": -120.0,
    "parentId": "c2.1"
  },
  {
    "id": "c2.1.2",
    "text": "Lớp lưu trữ bền bỉ: MemorySaver()",
    "x": 1270.0,
    "y": -20.0,
    "parentId": "c2.1"
  },
  {
    "id": "c2.1.3",
    "text": "Cơ chế lưu trữ: Thông qua các định danh thread_id",
    "x": 1270.0,
    "y": 80.0,
    "parentId": "c2.1"
  },
  {
    "id": "c2.1.4",
    "text": "Ví dụ: AI nhớ bản nháp lộ trình khi user nói \"Thôi tôi chỉ có 5 củ, làm lại đi\"",
    "x": 1270.0,
    "y": 180.0,
    "parentId": "c2.1"
  },
  {
    "id": "c2.1.5",
    "text": "Gói đi kèm: langgraph-checkpoint (chứa InMemorySaver cho dev/test)",
    "x": 1270.0,
    "y": 280.0,
    "parentId": "c2.1"
  },
  {
    "id": "c2.1.6",
    "text": "Gói tùy chọn (cho deploy): langgraph-checkpoint-sqlite, langgraph-checkpoint-postgres",
    "x": 1270.0,
    "y": 380.0,
    "parentId": "c2.1"
  },
  {
    "id": "c2.1.7",
    "text": "Cách hoạt động: Tạm dừng và chạy tiếp (resume) chính xác tại nơi dừng lại",
    "x": 1270.0,
    "y": 480.0,
    "parentId": "c2.1"
  },
  {
    "id": "c2.1.8",
    "text": "Ứng dụng thực tế",
    "x": 1270.0,
    "y": 580.0,
    "parentId": "c2.1"
  },
  {
    "id": "c2.1.8.1",
    "text": "Chờ con người can thiệp (Human-in-the-loop): Chatbot soạn xong email, chờ duyệt",
    "x": 1520.0,
    "y": 530.0,
    "parentId": "c2.1.8"
  },
  {
    "id": "c2.1.8.2",
    "text": "Chống đứt gánh giữa đường: Resume khi API timeout/mất mạng",
    "x": 1520.0,
    "y": 630.0,
    "parentId": "c2.1.8"
  },
  {
    "id": "c2.1.9",
    "text": "Lưu ý quan trọng: KHÔNG chạy tiếp từ dòng code bị dừng, mà chạy lại từ đầu của Node đó",
    "x": 1270.0,
    "y": 680.0,
    "parentId": "c2.1"
  },
  {
    "id": "c3",
    "text": "III. Tools (Công cụ)",
    "x": 770.0,
    "y": 380.0,
    "parentId": "root"
  },
  {
    "id": "c3.1",
    "text": "Định nghĩa: Hàm Python được đánh dấu @tool",
    "x": 1020.0,
    "y": 280.0,
    "parentId": "c3"
  },
  {
    "id": "c3.2",
    "text": "Ví dụ: add, multiply, divide",
    "x": 1020.0,
    "y": 380.0,
    "parentId": "c3"
  },
  {
    "id": "c3.3",
    "text": "Yêu cầu: Phải có biến tools_by_name",
    "x": 1020.0,
    "y": 480.0,
    "parentId": "c3"
  }
];