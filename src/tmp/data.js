var externalData = [
  {
    "id": "root",
    "text": "LangChain Mindmap",
    "x": 520.0,
    "y": 280.0,
    "parentId": null
  },
  {
    "id": "n1",
    "text": "1. LLMs & Providers",
    "x": 770.0,
    "y": 130.0,
    "parentId": "root"
  },
  {
    "id": "n1_1",
    "text": "HuggingFaceEndpoint",
    "x": 1020.0,
    "y": 30.0,
    "parentId": "n1"
  },
  {
    "id": "n1_2",
    "text": "HuggingFacePipeline",
    "x": 1020.0,
    "y": 130.0,
    "parentId": "n1"
  },
  {
    "id": "n1_3",
    "text": "ChatNVIDIA",
    "x": 1020.0,
    "y": 230.0,
    "parentId": "n1"
  },
  {
    "id": "n1_3_1",
    "text": "Cách khai báo đối tượng",
    "x": 1270.0,
    "y": 180.0,
    "parentId": "n1_3"
  },
  {
    "id": "n1_3_2",
    "text": "Ví dụ: `ChatNVIDIA(model='nvidia/nemotron-3-super-120b-a12b')`",
    "x": 1520.0,
    "y": 180.0,
    "parentId": "n1_3_1"
  },
  {
    "id": "n1_3_3",
    "text": "API Key: NVIDIA",
    "x": 1270.0,
    "y": 280.0,
    "parentId": "n1_3"
  },
  {
    "id": "n2",
    "text": "2. Embedding Models",
    "x": 770.0,
    "y": 230.0,
    "parentId": "root"
  },
  {
    "id": "n2_1",
    "text": "Định nghĩa",
    "x": 1020.0,
    "y": 80.0,
    "parentId": "n2"
  },
  {
    "id": "n2_1_1",
    "text": "Chuyển văn bản thô thành vector số",
    "x": 1270.0,
    "y": -70.0,
    "parentId": "n2_1"
  },
  {
    "id": "n2_1_2",
    "text": "Nắm bắt ý nghĩa ngữ nghĩa",
    "x": 1270.0,
    "y": 30.0,
    "parentId": "n2_1"
  },
  {
    "id": "n2_1_3",
    "text": "Cho phép so sánh và tìm kiếm văn bản dựa trên nội dung",
    "x": 1270.0,
    "y": 130.0,
    "parentId": "n2_1"
  },
  {
    "id": "n2_1_4",
    "text": "Văn bản tương đồng được đặt gần nhau trong không gian vector",
    "x": 1270.0,
    "y": 230.0,
    "parentId": "n2_1"
  },
  {
    "id": "n2_2",
    "text": "Các phương thức chính",
    "x": 1020.0,
    "y": 180.0,
    "parentId": "n2"
  },
  {
    "id": "n2_2_1",
    "text": "embed_documents(texts: List[str])",
    "x": 1270.0,
    "y": 130.0,
    "parentId": "n2_2"
  },
  {
    "id": "n2_2_1_1",
    "text": "Chức năng: Vectơ hóa nhiều tài liệu nguồn",
    "x": 1520.0,
    "y": 80.0,
    "parentId": "n2_2_1"
  },
  {
    "id": "n2_2_1_2",
    "text": "Đầu ra: Danh sách các vectơ (List[float])",
    "x": 1520.0,
    "y": 180.0,
    "parentId": "n2_2_1"
  },
  {
    "id": "n2_2_2",
    "text": "embed_query(text: str)",
    "x": 1270.0,
    "y": 230.0,
    "parentId": "n2_2"
  },
  {
    "id": "n2_2_2_1",
    "text": "Chức năng: Vectơ hóa một câu truy vấn",
    "x": 1520.0,
    "y": 180.0,
    "parentId": "n2_2_2"
  },
  {
    "id": "n2_2_2_2",
    "text": "Đầu ra: Vectơ đơn lẻ (List[float])",
    "x": 1520.0,
    "y": 280.0,
    "parentId": "n2_2_2"
  },
  {
    "id": "n2_3",
    "text": "Lý do cần phân chia hai phương thức",
    "x": 1020.0,
    "y": 280.0,
    "parentId": "n2"
  },
  {
    "id": "n2_3_1",
    "text": "Tối ưu hóa cho kiến trúc tìm kiếm không đối xứng",
    "x": 1270.0,
    "y": 230.0,
    "parentId": "n2_3"
  },
  {
    "id": "n2_3_2",
    "text": "Mô hình yêu cầu xử lý khác nhau (ví dụ: thêm tiền tố)",
    "x": 1270.0,
    "y": 330.0,
    "parentId": "n2_3"
  },
  {
    "id": "n2_4",
    "text": "Thực hiện Embedding trong Hugging Face",
    "x": 1020.0,
    "y": 380.0,
    "parentId": "n2"
  },
  {
    "id": "n2_4_1",
    "text": "Bước 1: Cài đặt",
    "x": 1270.0,
    "y": 330.0,
    "parentId": "n2_4"
  },
  {
    "id": "n2_4_1_1",
    "text": "`pip install langchain-huggingface`",
    "x": 1520.0,
    "y": 330.0,
    "parentId": "n2_4_1"
  },
  {
    "id": "n2_4_2",
    "text": "Bước 2: Tìm Hugging Face API Token",
    "x": 1270.0,
    "y": 430.0,
    "parentId": "n2_4"
  },
  {
    "id": "n2_4_2_1",
    "text": "Tìm tại: https://huggingface.co/docs/hub/security-tokens",
    "x": 1520.0,
    "y": 380.0,
    "parentId": "n2_4_2"
  },
  {
    "id": "n2_4_2_2",
    "text": "Lưu vào biến môi trường `HUGGINGFACEHUB_API_TOKEN`",
    "x": 1520.0,
    "y": 480.0,
    "parentId": "n2_4_2"
  },
  {
    "id": "n3",
    "text": "3. LangGraph",
    "x": 770.0,
    "y": 330.0,
    "parentId": "root"
  },
  {
    "id": "n3_1",
    "text": "Giới thiệu",
    "x": 1020.0,
    "y": 230.0,
    "parentId": "n3"
  },
  {
    "id": "n3_1_1",
    "text": "Minh họa xây dựng AI Agent đơn giản",
    "x": 1270.0,
    "y": 180.0,
    "parentId": "n3_1"
  },
  {
    "id": "n3_1_2",
    "text": "Sử dụng Graph API",
    "x": 1270.0,
    "y": 280.0,
    "parentId": "n3_1"
  },
  {
    "id": "n3_2",
    "text": "Cài đặt",
    "x": 1020.0,
    "y": 330.0,
    "parentId": "n3"
  },
  {
    "id": "n3_2_1",
    "text": "`pip install -U langgraph`",
    "x": 1270.0,
    "y": 230.0,
    "parentId": "n3_2"
  },
  {
    "id": "n3_2_2",
    "text": "Cài đặt thư viện liên quan: `pip install langchain openai`",
    "x": 1270.0,
    "y": 330.0,
    "parentId": "n3_2"
  },
  {
    "id": "n3_2_3",
    "text": "Kiểm tra: `import langgraph`",
    "x": 1270.0,
    "y": 430.0,
    "parentId": "n3_2"
  },
  {
    "id": "n3_3",
    "text": "Minh họa sử dụng",
    "x": 1020.0,
    "y": 430.0,
    "parentId": "n3"
  },
  {
    "id": "n3_3_1",
    "text": "Ví dụ (Test_Agent.py)",
    "x": 1270.0,
    "y": 430.0,
    "parentId": "n3_3"
  },
  {
    "id": "n3_3_1_1",
    "text": "Khởi tạo ChatOllama",
    "x": 1520.0,
    "y": 280.0,
    "parentId": "n3_3_1"
  },
  {
    "id": "n3_3_1_2",
    "text": "Sử dụng `.bind_tools(tools)`",
    "x": 1520.0,
    "y": 380.0,
    "parentId": "n3_3_1"
  },
  {
    "id": "n3_3_1_3",
    "text": "Xây dựng agent bằng `build_agent`",
    "x": 1520.0,
    "y": 480.0,
    "parentId": "n3_3_1"
  },
  {
    "id": "n3_3_1_4",
    "text": "Gọi agent bằng `agent.invoke(state)`",
    "x": 1520.0,
    "y": 580.0,
    "parentId": "n3_3_1"
  },
  {
    "id": "n4",
    "text": "4. Môi trường & Cài đặt Chung",
    "x": 770.0,
    "y": 430.0,
    "parentId": "root"
  },
  {
    "id": "n4_1",
    "text": "Mục đích sử dụng LLM trong LangChain",
    "x": 1020.0,
    "y": 380.0,
    "parentId": "n4"
  },
  {
    "id": "n4_1_1",
    "text": "Phân tích yêu cầu của người dùng",
    "x": 1270.0,
    "y": 280.0,
    "parentId": "n4_1"
  },
  {
    "id": "n4_1_2",
    "text": "Xử lý ngôn ngữ tự nhiên",
    "x": 1270.0,
    "y": 380.0,
    "parentId": "n4_1"
  },
  {
    "id": "n4_1_3",
    "text": "Đề xuất lịch trình cá nhân phù hợp",
    "x": 1270.0,
    "y": 480.0,
    "parentId": "n4_1"
  },
  {
    "id": "n4_2",
    "text": "Chuẩn bị môi trường làm việc",
    "x": 1020.0,
    "y": 480.0,
    "parentId": "n4"
  },
  {
    "id": "n4_2_1",
    "text": "Ngôn ngữ lập trình: Python",
    "x": 1270.0,
    "y": 330.0,
    "parentId": "n4_2"
  },
  {
    "id": "n4_2_2",
    "text": "Trình quản lý gói: pip",
    "x": 1270.0,
    "y": 430.0,
    "parentId": "n4_2"
  },
  {
    "id": "n4_2_3",
    "text": "API Key: Hugging Face (tạo trên trang web)",
    "x": 1270.0,
    "y": 530.0,
    "parentId": "n4_2"
  },
  {
    "id": "n4_2_4",
    "text": "Thư viện/Framework cần thiết",
    "x": 1270.0,
    "y": 630.0,
    "parentId": "n4_2"
  },
  {
    "id": "n4_2_4_1",
    "text": "OpenAI (v2.17.0)",
    "x": 1520.0,
    "y": 480.0,
    "parentId": "n4_2_4"
  },
  {
    "id": "n4_2_4_2",
    "text": "Pandas (v3.0.0)",
    "x": 1520.0,
    "y": 580.0,
    "parentId": "n4_2_4"
  },
  {
    "id": "n4_2_4_3",
    "text": "Python-dotenv (v1.2.1)",
    "x": 1520.0,
    "y": 680.0,
    "parentId": "n4_2_4"
  },
  {
    "id": "n4_2_4_4",
    "text": "LangChain (cài đặt qua pip)",
    "x": 1520.0,
    "y": 780.0,
    "parentId": "n4_2_4"
  }
];