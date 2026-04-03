var externalFlashcards = [
  {
    "front": "Theo tài liệu, LangChain tích hợp với các nhà cung cấp LLM nào?",
    "back": "LangChain tích hợp với ChatOpenAI, ChatOllama, ChatGroq, và ChatNVIDIA."
  },
  {
    "front": "Mô hình embedding có vai trò gì trong bối cảnh được mô tả?",
    "back": "Mô hình embedding chuyển đổi văn bản thô thành một vector số có độ dài cố định nhằm nắm bắt ý nghĩa ngữ nghĩa, cho phép máy tính so sánh và tìm kiếm văn bản dựa trên nội dung."
  },
  {
    "front": "Tên cụ thể của mô hình embedding được sử dụng trong đoạn code là gì?",
    "back": "Mô hình embedding được sử dụng là 'sentence-transformers/all-MiniLM-L6-v2' thông qua `HuggingFaceEndpointEmbeddings`."
  },
  {
    "front": "Cơ sở dữ liệu vector nào được sử dụng trong đoạn code để lưu trữ các sự kiện lịch trình?",
    "back": "Cơ sở dữ liệu vector được sử dụng là `Chroma`."
  },
  {
    "front": "Thư viện nào được sử dụng để tải dữ liệu phi cấu trúc trong đoạn code?",
    "back": "`langchain_unstructured` với `UnstructuredLoader`."
  },
  {
    "front": "`HF_TOKEN` trong file `.env` được dùng để làm gì trong đoạn code được cung cấp?",
    "back": "`HF_TOKEN` được sử dụng để xác thực (API token) cho các dịch vụ của Hugging Face, ví dụ như `HuggingFaceEndpointEmbeddings`."
  },
  {
    "front": "Theo tài liệu, có hai cách chính để khai báo đối tượng HuggingFace trong LangChain là gì?",
    "back": "Hai cách chính là `HuggingFaceEndpoint` hoặc `HuggingFacePipeline`."
  },
  {
    "front": "`ChatNVIDIA` được sử dụng để làm gì trong LangChain?",
    "back": "`ChatNVIDIA` được sử dụng để tương tác với các mô hình ngôn ngữ lớn (LLM) của NVIDIA, ví dụ như 'nvidia/nemotron-3-super-120b-a12b'."
  },
  {
    "front": "LangChain tích hợp với HuggingFace theo những cách nào được đề cập trong tài liệu?",
    "back": "LangChain tích hợp với HuggingFace thông qua `ChatHuggingFace integration` và sử dụng `HuggingFaceEndpointEmbeddings` cho các mô hình nhúng."
  },
  {
    "front": "Mục tiêu chính của việc chuyển đổi văn bản thành vector số (embedding) là gì?",
    "back": "Mục tiêu chính là cho phép máy tính so sánh và tìm kiếm văn bản dựa trên nội dung và ý nghĩa ngữ nghĩa của chúng, thay vì chỉ dựa vào các từ ngữ chính xác."
  }
];