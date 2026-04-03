var externalData = [
  {
    "id": "root",
    "text": "mindmap",
    "x": 520,
    "y": 280,
    "parentId": null
  },
  {
    "id": "n1",
    "text": "LangGraph Workflow & Kết Nối",
    "x": 770,
    "y": -70.0,
    "parentId": "root"
  },
  {
    "id": "n1_1",
    "text": "Các cạnh (Edges) trong Workflow",
    "x": 1020,
    "y": -70.0,
    "parentId": "n1"
  },
  {
    "id": "n1_1_1",
    "text": "workflow.add_edge(START, 'router')",
    "x": 1270,
    "y": -370.0,
    "parentId": "n1_1"
  },
  {
    "id": "n1_1_2",
    "text": "workflow.add_conditional_edges('router', route_from_router)",
    "x": 1270,
    "y": -270.0,
    "parentId": "n1_1"
  },
  {
    "id": "n1_1_3",
    "text": "workflow.add_conditional_edges('info_checker', route_from_checker)",
    "x": 1270,
    "y": -170.0,
    "parentId": "n1_1"
  },
  {
    "id": "n1_1_4",
    "text": "workflow.add_edge('gather_info', 'supervisor')",
    "x": 1270,
    "y": -70.0,
    "parentId": "n1_1"
  },
  {
    "id": "n1_1_5",
    "text": "workflow.add_edge('supervisor', END) (Xong nháp)",
    "x": 1270,
    "y": 30.0,
    "parentId": "n1_1"
  },
  {
    "id": "n1_1_6",
    "text": "workflow.add_conditional_edges('feedback_analyzer', route_feedback)",
    "x": 1270,
    "y": 130.0,
    "parentId": "n1_1"
  },
  {
    "id": "n1_1_7",
    "text": "workflow.add_edge('executor', END)",
    "x": 1270,
    "y": 230.0,
    "parentId": "n1_1"
  },
  {
    "id": "n2",
    "text": "Tính năng nâng cao LangGraph",
    "x": 770,
    "y": 30.0,
    "parentId": "root"
  },
  {
    "id": "n2_1",
    "text": "Cơ chế Bộ nhớ Ngắn hạn (Conversational Memory)",
    "x": 1020,
    "y": 30.0,
    "parentId": "n2"
  },
  {
    "id": "n2_1_1",
    "text": "Với Checkpointer",
    "x": 1270,
    "y": -270.0,
    "parentId": "n2_1"
  },
  {
    "id": "n2_1_2",
    "text": "Sử dụng lớp lưu trữ bền bỉ MemorySaver()",
    "x": 1270,
    "y": -170.0,
    "parentId": "n2_1"
  },
  {
    "id": "n2_1_3",
    "text": "Lưu lại Checkpoints qua thread_id",
    "x": 1270,
    "y": -70.0,
    "parentId": "n2_1"
  },
  {
    "id": "n2_1_4",
    "text": "Ví dụ: AI nhớ bản nháp cũ khi user thay đổi yêu cầu",
    "x": 1270,
    "y": 30.0,
    "parentId": "n2_1"
  },
  {
    "id": "n2_1_5",
    "text": "Cấu hình: .compile(checkpointer=checkpointer)",
    "x": 1270,
    "y": 130.0,
    "parentId": "n2_1"
  },
  {
    "id": "n2_1_6",
    "text": "Cấu hình: config = {\"configurable\": {\"thread_id\": uuid.uuid4()}}",
    "x": 1270,
    "y": 230.0,
    "parentId": "n2_1"
  },
  {
    "id": "n2_1_7",
    "text": "Gọi graph: graph.invoke({\"url\": \"https://www.example.com\"}, config)",
    "x": 1270,
    "y": 330.0,
    "parentId": "n2_1"
  },
  {
    "id": "n3",
    "text": "Deep Agents",
    "x": 770,
    "y": 130.0,
    "parentId": "root"
  },
  {
    "id": "n3_1",
    "text": "Tổng quan",
    "x": 1020,
    "y": 80.0,
    "parentId": "n3"
  },
  {
    "id": "n3_2",
    "text": "Kiến trúc Deep Agents",
    "x": 1020,
    "y": 180.0,
    "parentId": "n3"
  },
  {
    "id": "n3_2_1",
    "text": "Thành phần kết hợp",
    "x": 1270,
    "y": 80.0,
    "parentId": "n3_2"
  },
  {
    "id": "n3_2_1_1",
    "text": "System prompt chi tiết",
    "x": 1520,
    "y": -70.0,
    "parentId": "n3_2_1"
  },
  {
    "id": "n3_2_1_2",
    "text": "Công cụ lập kế hoạch",
    "x": 1520,
    "y": 30.0,
    "parentId": "n3_2_1"
  },
  {
    "id": "n3_2_1_3",
    "text": "Sub-agent",
    "x": 1520,
    "y": 130.0,
    "parentId": "n3_2_1"
  },
  {
    "id": "n3_2_1_4",
    "text": "Hệ thống tệp",
    "x": 1520,
    "y": 230.0,
    "parentId": "n3_2_1"
  },
  {
    "id": "n3_2_2",
    "text": "Khả năng",
    "x": 1270,
    "y": 180.0,
    "parentId": "n3_2"
  },
  {
    "id": "n3_2_2_1",
    "text": "Xử lý nhiệm vụ phức tạp, nhiều bước",
    "x": 1520,
    "y": 30.0,
    "parentId": "n3_2_2"
  },
  {
    "id": "n3_2_2_2",
    "text": "Suy luận liên tục",
    "x": 1520,
    "y": 130.0,
    "parentId": "n3_2_2"
  },
  {
    "id": "n3_2_2_3",
    "text": "Sử dụng công cụ",
    "x": 1520,
    "y": 230.0,
    "parentId": "n3_2_2"
  },
  {
    "id": "n3_2_2_4",
    "text": "Ghi nhớ",
    "x": 1520,
    "y": 330.0,
    "parentId": "n3_2_2"
  },
  {
    "id": "n3_2_3",
    "text": "Điểm khác biệt so với Agent truyền thống",
    "x": 1270,
    "y": 280.0,
    "parentId": "n3_2"
  },
  {
    "id": "n3_2_3_1",
    "text": "Lập kế hoạch hành động",
    "x": 1520,
    "y": 230.0,
    "parentId": "n3_2_3"
  },
  {
    "id": "n3_2_3_2",
    "text": "Quản lý ngữ cảnh",
    "x": 1520,
    "y": 330.0,
    "parentId": "n3_2_3"
  },
  {
    "id": "n4",
    "text": "Cài đặt & Chuẩn bị Dự án",
    "x": 770,
    "y": 230.0,
    "parentId": "root"
  },
  {
    "id": "n4_1",
    "text": "Ngôn ngữ lập trình",
    "x": 1020,
    "y": 30.0,
    "parentId": "n4"
  },
  {
    "id": "n4_2",
    "text": "API Keys (OpenAI / Gemini / Hugging Face)",
    "x": 1020,
    "y": 130.0,
    "parentId": "n4"
  },
  {
    "id": "n4_3",
    "text": "Cài đặt",
    "x": 1020,
    "y": 230.0,
    "parentId": "n4"
  },
  {
    "id": "n4_4",
    "text": "Thiết kế Luồng dữ liệu / Quy trình",
    "x": 1020,
    "y": 330.0,
    "parentId": "n4"
  },
  {
    "id": "n4_5",
    "text": "Bài tập ứng dụng (Khởi tạo)",
    "x": 1020,
    "y": 430.0,
    "parentId": "n4"
  },
  {
    "id": "n5",
    "text": "Khái niệm cơ bản & Code minh họa",
    "x": 770,
    "y": 330.0,
    "parentId": "root"
  },
  {
    "id": "n5_1",
    "text": "Lý thuyết và minh họa",
    "x": 1020,
    "y": 280.0,
    "parentId": "n5"
  },
  {
    "id": "n5_2",
    "text": "Code minh họa Agent lập lịch cơ bản",
    "x": 1020,
    "y": 380.0,
    "parentId": "n5"
  },
  {
    "id": "n5_2_1",
    "text": "Sử dụng Agents",
    "x": 1270,
    "y": 280.0,
    "parentId": "n5_2"
  },
  {
    "id": "n5_2_2",
    "text": "Sử dụng Tools",
    "x": 1270,
    "y": 380.0,
    "parentId": "n5_2"
  },
  {
    "id": "n5_2_3",
    "text": "Sử dụng Models",
    "x": 1270,
    "y": 480.0,
    "parentId": "n5_2"
  },
  {
    "id": "n6",
    "text": "Quản lý trạng thái với SchedulingState",
    "x": 770,
    "y": 430.0,
    "parentId": "root"
  },
  {
    "id": "n6_1",
    "text": "Định nghĩa (TypedDict, Annotated)",
    "x": 1020,
    "y": 330.0,
    "parentId": "n6"
  },
  {
    "id": "n6_2",
    "text": "Các trường dữ liệu chính",
    "x": 1020,
    "y": 430.0,
    "parentId": "n6"
  },
  {
    "id": "n6_2_1",
    "text": "messages: Annotated[List[BaseMessage], add_messages]",
    "x": 1270,
    "y": 30.0,
    "parentId": "n6_2"
  },
  {
    "id": "n6_2_2",
    "text": "intent (Phân loại luồng hội thoại)",
    "x": 1270,
    "y": 130.0,
    "parentId": "n6_2"
  },
  {
    "id": "n6_2_2_1",
    "text": "'greeting'",
    "x": 1520,
    "y": -120.0,
    "parentId": "n6_2_2"
  },
  {
    "id": "n6_2_2_2",
    "text": "'off_topic'",
    "x": 1520,
    "y": -20.0,
    "parentId": "n6_2_2"
  },
  {
    "id": "n6_2_2_3",
    "text": "'schedule'",
    "x": 1520,
    "y": 80.0,
    "parentId": "n6_2_2"
  },
  {
    "id": "n6_2_2_4",
    "text": "'roadmap'",
    "x": 1520,
    "y": 180.0,
    "parentId": "n6_2_2"
  },
  {
    "id": "n6_2_2_5",
    "text": "'feedback'",
    "x": 1520,
    "y": 280.0,
    "parentId": "n6_2_2"
  },
  {
    "id": "n6_2_2_6",
    "text": "'providing_info'",
    "x": 1520,
    "y": 380.0,
    "parentId": "n6_2_2"
  },
  {
    "id": "n6_2_3",
    "text": "missing_info (Thông tin user cần cung cấp thêm)",
    "x": 1270,
    "y": 230.0,
    "parentId": "n6_2"
  },
  {
    "id": "n6_2_4",
    "text": "user_profile (Kết quả từ Agent 1: PDF RAG)",
    "x": 1270,
    "y": 330.0,
    "parentId": "n6_2"
  },
  {
    "id": "n6_2_5",
    "text": "research_data (Kết quả từ Agent 2: Web Search)",
    "x": 1270,
    "y": 430.0,
    "parentId": "n6_2"
  },
  {
    "id": "n6_2_6",
    "text": "calendar_slots (Kết quả từ Agent 3: Calendar Check)",
    "x": 1270,
    "y": 530.0,
    "parentId": "n6_2"
  },
  {
    "id": "n6_2_7",
    "text": "current_draft (Bản nháp lịch trình/lộ trình Supervisor)",
    "x": 1270,
    "y": 630.0,
    "parentId": "n6_2"
  },
  {
    "id": "n6_2_8",
    "text": "is_approved (Người dùng đồng ý nháp không?)",
    "x": 1270,
    "y": 730.0,
    "parentId": "n6_2"
  },
  {
    "id": "n6_2_9",
    "text": "user_feedback (Lý do người dùng từ chối)",
    "x": 1270,
    "y": 830.0,
    "parentId": "n6_2"
  },
  {
    "id": "n6_3",
    "text": "Mục đích: Giúp hệ thống tránh lỗi",
    "x": 1020,
    "y": 530.0,
    "parentId": "n6"
  },
  {
    "id": "n7",
    "text": "Xây dựng Agent với StateGraph (agent_builder.py)",
    "x": 770,
    "y": 530.0,
    "parentId": "root"
  },
  {
    "id": "n7_1",
    "text": "Khởi tạo StateGraph(MessagesState)",
    "x": 1020,
    "y": 430.0,
    "parentId": "n7"
  },
  {
    "id": "n7_2",
    "text": "Thêm nodes: 'llm_call', 'tool_node'",
    "x": 1020,
    "y": 530.0,
    "parentId": "n7"
  },
  {
    "id": "n7_3",
    "text": "Định nghĩa luồng",
    "x": 1020,
    "y": 630.0,
    "parentId": "n7"
  },
  {
    "id": "n7_3_1",
    "text": "add_edge(START, 'llm_call')",
    "x": 1270,
    "y": 480.0,
    "parentId": "n7_3"
  },
  {
    "id": "n7_3_2",
    "text": "Hàm should_continue (Logic conditional)",
    "x": 1270,
    "y": 580.0,
    "parentId": "n7_3"
  },
  {
    "id": "n7_3_2_1",
    "text": "Kiểm tra last_message.tool_calls",
    "x": 1520,
    "y": 530.0,
    "parentId": "n7_3_2"
  },
  {
    "id": "n7_3_2_2",
    "text": "Trả về 'tool_node' hoặc END",
    "x": 1520,
    "y": 630.0,
    "parentId": "n7_3_2"
  },
  {
    "id": "n7_3_3",
    "text": "add_conditional_edges('llm_call', should_continue, ['tool_node', END])",
    "x": 1270,
    "y": 680.0,
    "parentId": "n7_3"
  },
  {
    "id": "n7_3_4",
    "text": "add_edge('tool_node', 'llm_call')",
    "x": 1270,
    "y": 780.0,
    "parentId": "n7_3"
  },
  {
    "id": "n8",
    "text": "Xử lý Phản hồi & Lặp lại",
    "x": 770,
    "y": 630.0,
    "parentId": "root"
  },
  {
    "id": "n8_1",
    "text": "Từ chối -> Thu thập lại (web/cal) với feedback mới",
    "x": 1020,
    "y": 530.0,
    "parentId": "n8"
  },
  {
    "id": "n8_2",
    "text": "Làm nháp mới",
    "x": 1020,
    "y": 630.0,
    "parentId": "n8"
  },
  {
    "id": "n8_3",
    "text": "Liên quan đến user_feedback trong SchedulingState",
    "x": 1020,
    "y": 730.0,
    "parentId": "n8"
  }
];