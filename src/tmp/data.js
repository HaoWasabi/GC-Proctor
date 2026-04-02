var externalData = [
  {
    "id": "root",
    "text": "AI Agent",
    "x": 520.0,
    "y": 280.0,
    "parentId": null
  },
  {
    "id": "dinh_nghia",
    "text": "Định nghĩa",
    "x": 770.0,
    "y": 80.0,
    "parentId": "root"
  },
  {
    "id": "d_khong_chatbot",
    "text": "Không chỉ là chatbot",
    "x": 1020.0,
    "y": -320.0,
    "parentId": "dinh_nghia"
  },
  {
    "id": "d_llm_reasoning",
    "text": "Sử dụng LLM làm cỗ máy suy luận (reasoning engine)",
    "x": 1020.0,
    "y": -220.0,
    "parentId": "dinh_nghia"
  },
  {
    "id": "d_chuoi_hanh_dong",
    "text": "Xác định chuỗi hành động cần thực hiện",
    "x": 1020.0,
    "y": -120.0,
    "parentId": "dinh_nghia"
  },
  {
    "id": "d_khac_chains",
    "text": "Khác Chains (luồng hard-coded)",
    "x": 1020.0,
    "y": -20.0,
    "parentId": "dinh_nghia"
  },
  {
    "id": "d_quyet_dinh_qua_llm",
    "text": "LLM quyết định hành động",
    "x": 1020.0,
    "y": 80.0,
    "parentId": "dinh_nghia"
  },
  {
    "id": "d_thuc_hien_qua_tools",
    "text": "Thực hiện qua Tools",
    "x": 1020.0,
    "y": 180.0,
    "parentId": "dinh_nghia"
  },
  {
    "id": "d_quan_sat_lap_lai",
    "text": "Quan sát kết quả và lặp lại quy trình",
    "x": 1020.0,
    "y": 280.0,
    "parentId": "dinh_nghia"
  },
  {
    "id": "d_muc_tieu",
    "text": "Đạt được mục tiêu",
    "x": 1020.0,
    "y": 380.0,
    "parentId": "dinh_nghia"
  },
  {
    "id": "d_react_agent_example",
    "text": "Ví dụ: ReAct Agent (LangGraph)",
    "x": 1020.0,
    "y": 480.0,
    "parentId": "dinh_nghia"
  },
  {
    "id": "vai_tro_llm",
    "text": "Vai trò của LLM trong Agent",
    "x": 770.0,
    "y": 180.0,
    "parentId": "root"
  },
  {
    "id": "v_cong_cu_manh_me",
    "text": "Công cụ AI mạnh mẽ",
    "x": 1020.0,
    "y": 30.0,
    "parentId": "vai_tro_llm"
  },
  {
    "id": "v_dien_giai_tao_vb",
    "text": "Diễn giải và tạo văn bản giống con người",
    "x": 1020.0,
    "y": 130.0,
    "parentId": "vai_tro_llm"
  },
  {
    "id": "v_linh_hoat",
    "text": "Linh hoạt: viết nội dung, dịch ngôn ngữ, tóm tắt, trả lời câu hỏi",
    "x": 1020.0,
    "y": 230.0,
    "parentId": "vai_tro_llm"
  },
  {
    "id": "v_dong_co_suy_luan",
    "text": "Hoạt động như bộ máy suy luận và điều khiển tác vụ agent",
    "x": 1020.0,
    "y": 330.0,
    "parentId": "vai_tro_llm"
  },
  {
    "id": "thanh_phan_chinh",
    "text": "Thành phần & Thư viện (LangChain/LangGraph)",
    "x": 770.0,
    "y": 280.0,
    "parentId": "root"
  },
  {
    "id": "tc_langchain",
    "text": "LangChain: Khung làm việc cho Agents",
    "x": 1020.0,
    "y": 180.0,
    "parentId": "thanh_phan_chinh"
  },
  {
    "id": "tc_langgraph",
    "text": "LangGraph: Tạo ReAct Agent",
    "x": 1020.0,
    "y": 280.0,
    "parentId": "thanh_phan_chinh"
  },
  {
    "id": "tc_create_react_agent",
    "text": "`create_react_agent`: Giúp AI quyết định trả lời hay gọi công cụ",
    "x": 1270.0,
    "y": 230.0,
    "parentId": "tc_langgraph"
  },
  {
    "id": "tc_memorysaver",
    "text": "`MemorySaver`: 'Trí nhớ ngắn hạn', giúp AI nhớ nội dung chat",
    "x": 1270.0,
    "y": 330.0,
    "parentId": "tc_langgraph"
  },
  {
    "id": "tc_tools",
    "text": "Tools: Công cụ để Agents thực hiện hành động",
    "x": 1020.0,
    "y": 380.0,
    "parentId": "thanh_phan_chinh"
  },
  {
    "id": "ung_dung_tiem_nang",
    "text": "Ứng dụng & Lĩnh vực tiềm năng",
    "x": 770.0,
    "y": 380.0,
    "parentId": "root"
  },
  {
    "id": "ua_du_lieu_rieng",
    "text": "Đưa dữ liệu riêng (PDF, SQL, Notion) vào AI để trả lời chính xác",
    "x": 1020.0,
    "y": 180.0,
    "parentId": "ung_dung_tiem_nang"
  },
  {
    "id": "ua_ca_nhan_hoa",
    "text": "Cá nhân hóa",
    "x": 1020.0,
    "y": 280.0,
    "parentId": "ung_dung_tiem_nang"
  },
  {
    "id": "ua_goi_y_sp",
    "text": "Gợi ý sản phẩm",
    "x": 1270.0,
    "y": 230.0,
    "parentId": "ua_ca_nhan_hoa"
  },
  {
    "id": "ua_tro_ly_ao",
    "text": "Trợ lý ảo thông minh tư vấn sản phẩm",
    "x": 1270.0,
    "y": 330.0,
    "parentId": "ua_ca_nhan_hoa"
  },
  {
    "id": "ua_phan_tich_quyet_dinh",
    "text": "Phân tích & quyết định",
    "x": 1020.0,
    "y": 380.0,
    "parentId": "ung_dung_tiem_nang"
  },
  {
    "id": "ua_khai_thac_du_lieu",
    "text": "Khai thác dữ liệu (văn bản, hình ảnh, âm thanh)",
    "x": 1270.0,
    "y": 330.0,
    "parentId": "ua_phan_tich_quyet_dinh"
  },
  {
    "id": "ua_rut_ra_insight",
    "text": "Rút ra insight",
    "x": 1270.0,
    "y": 430.0,
    "parentId": "ua_phan_tich_quyet_dinh"
  },
  {
    "id": "ua_dai_ly_tu_hanh",
    "text": "Đại lý AI tự hành (Autonomous Agents)",
    "x": 1020.0,
    "y": 480.0,
    "parentId": "ung_dung_tiem_nang"
  },
  {
    "id": "ua_tu_suy_luan",
    "text": "Tự suy luận",
    "x": 1270.0,
    "y": 380.0,
    "parentId": "ua_dai_ly_tu_hanh"
  },
  {
    "id": "ua_su_dung_cong_cu",
    "text": "Sử dụng công cụ (web, email, code)",
    "x": 1270.0,
    "y": 480.0,
    "parentId": "ua_dai_ly_tu_hanh"
  },
  {
    "id": "ua_hoan_thanh_muc_tieu",
    "text": "Hoàn thành mục tiêu",
    "x": 1270.0,
    "y": 580.0,
    "parentId": "ua_dai_ly_tu_hanh"
  },
  {
    "id": "ua_linh_vuc_cu_the",
    "text": "Lĩnh vực tiềm năng cụ thể",
    "x": 1020.0,
    "y": 580.0,
    "parentId": "ung_dung_tiem_nang"
  },
  {
    "id": "ua_cntt",
    "text": "CNTT: Phát triển ứng dụng và tính năng AI",
    "x": 1270.0,
    "y": 380.0,
    "parentId": "ua_linh_vuc_cu_the"
  },
  {
    "id": "ua_marketing_kinh_doanh",
    "text": "Marketing & Kinh doanh",
    "x": 1270.0,
    "y": 480.0,
    "parentId": "ua_linh_vuc_cu_the"
  },
  {
    "id": "ua_chatbot_moi",
    "text": "Chatbot thế hệ mới (truy cập lịch sử giao dịch, chính sách bảo hành)",
    "x": 1520.0,
    "y": 430.0,
    "parentId": "ua_marketing_kinh_doanh"
  },
  {
    "id": "ua_tu_van_sp_ca_nhan",
    "text": "Tư vấn sản phẩm (sở thích cá nhân, lịch sử truy cập)",
    "x": 1520.0,
    "y": 530.0,
    "parentId": "ua_marketing_kinh_doanh"
  },
  {
    "id": "ua_giao_duc",
    "text": "Giáo dục: Học tập cá nhân hóa, trợ giảng ảo",
    "x": 1270.0,
    "y": 580.0,
    "parentId": "ua_linh_vuc_cu_the"
  },
  {
    "id": "ua_phan_tich_du_lieu",
    "text": "Phân tích dữ liệu: Kết nối LLM với SQL DB (hỏi đáp ngôn ngữ tự nhiên)",
    "x": 1270.0,
    "y": 680.0,
    "parentId": "ua_linh_vuc_cu_the"
  },
  {
    "id": "ua_thuong_mai_dien_tu",
    "text": "Thương mại điện tử: Chatbot, gợi ý, mô tả",
    "x": 1270.0,
    "y": 780.0,
    "parentId": "ua_linh_vuc_cu_the"
  },
  {
    "id": "he_thong_da_tac_nhan",
    "text": "Hệ thống đa tác nhân (Multi-Agent System)",
    "x": 770.0,
    "y": 480.0,
    "parentId": "root"
  },
  {
    "id": "ht_khai_niem",
    "text": "Khái niệm: Xây dựng nhiều tác nhân tương tác",
    "x": 1020.0,
    "y": 380.0,
    "parentId": "he_thong_da_tac_nhan"
  },
  {
    "id": "ht_loai_su_dung",
    "text": "Loại thường dùng: Hierarchical Multi-Agent System (Phân cấp)",
    "x": 1020.0,
    "y": 480.0,
    "parentId": "he_thong_da_tac_nhan"
  },
  {
    "id": "ht_ly_do",
    "text": "Lý do: Xây dựng và giám sát các tác nhân hành động",
    "x": 1270.0,
    "y": 480.0,
    "parentId": "ht_loai_su_dung"
  },
  {
    "id": "ht_vi_du_lich_trinh",
    "text": "Ví dụ: Đề xuất lịch trình cá nhân",
    "x": 1020.0,
    "y": 580.0,
    "parentId": "he_thong_da_tac_nhan"
  },
  {
    "id": "ht_tac_nhan_con_1",
    "text": "Tác nhân con 1: Kiểm tra ràng buộc thời gian",
    "x": 1270.0,
    "y": 530.0,
    "parentId": "ht_vi_du_lich_trinh"
  },
  {
    "id": "ht_tac_nhan_con_2",
    "text": "Tác nhân con 2: Xử lý các nhiệm vụ khác",
    "x": 1270.0,
    "y": 630.0,
    "parentId": "ht_vi_du_lich_trinh"
  }
];