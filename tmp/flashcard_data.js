window.externalFlashcards = [
  {
    "front": "Mục đích chính của \"Embedding Models\" trong ngữ cảnh LangChain là gì?",
    "back": "Chuyển đổi văn bản thô (câu, đoạn văn) thành một vector số có độ dài cố định nhằm nắm bắt ý nghĩa ngữ nghĩa của văn bản đó."
  },
  {
    "front": "Các vector embedding giúp ích như thế nào trong việc so sánh và tìm kiếm văn bản?",
    "back": "Các văn bản có ý tưởng tương đồng sẽ được đặt gần nhau trong không gian vector, cho phép máy tính so sánh và tìm kiếm văn bản dựa trên nội dung ngữ nghĩa thay vì chỉ dựa vào các từ ngữ chính xác."
  },
  {
    "front": "Mô hình embedding cụ thể nào được sử dụng với `HuggingFaceEndpointEmbeddings` trong đoạn code mẫu được cung cấp?",
    "back": "`sentence-transformers/all-MiniLM-L6-v2`."
  },
  {
    "front": "Kể tên ít nhất ba nhà cung cấp LLM (mô hình ngôn ngữ lớn) khác nhau được tích hợp với LangChain dựa trên các câu lệnh import trong tài liệu.",
    "back": "OpenAI (`ChatOpenAI`), Ollama (`ChatOllama`), Groq (`ChatGroq`), NVIDIA (`ChatNVIDIA`), HuggingFace (qua `ChatHuggingFace integration`). (Chỉ cần 3 trong số đó)."
  },
  {
    "front": "`Chroma` được sử dụng với mục đích gì trong đoạn mã đã cho liên quan đến LangChain?",
    "back": "Được sử dụng làm `vector_db` (cơ sở dữ liệu vector) để lưu trữ và quản lý dữ liệu embedding, ví dụ như `collection_name=\"schedule_eve\"`."
  },
  {
    "front": "Dựa vào ví dụ về `Calendar subagent` và các import liên quan, một SubAgent trong kiến trúc `DeepAgents` có thể bao gồm những thành phần nào?",
    "back": "Có thể bao gồm `prompts` (ví dụ: `CALENDAR_AGENT_PROMPT`) và `tools` (ví dụ: `get_calendar_tools`)."
  },
  {
    "front": "Chức năng của `load_dotenv()` trong các đoạn mã Python được cung cấp là gì?",
    "back": "Để tải các biến môi trường (như `HF_TOKEN`, `UNSTRUCTURED_API_KEY`) từ file `.env` vào môi trường chạy của script, giúp quản lý thông tin nhạy cảm an toàn."
  },
  {
    "front": "Module nào trong LangChain được sử dụng để định nghĩa các `tool` (công cụ) theo cú pháp `from langchain_core.tools import tool`?",
    "back": "`langchain_core`."
  },
  {
    "front": "Dựa trên câu lệnh import `from langchain_unstructured import UnstructuredLoader`, vai trò của `UnstructuredLoader` trong LangChain là gì?",
    "back": "Được sử dụng để tải và xử lý dữ liệu không có cấu trúc (unstructured data) từ các nguồn khác nhau."
  },
  {
    "front": "Ngoài `HuggingFaceEndpointEmbeddings`, LangChain còn hỗ trợ tích hợp HuggingFace cho mô hình chat thông qua phương thức nào khác?",
    "back": "Tích hợp `ChatHuggingFace` (như đã đề cập trong tài liệu tham khảo số 5: `ChatHuggingFace integration`)."
  }
];