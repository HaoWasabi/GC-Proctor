import json
from services.base_service import BaseService
from services.kb_service import KBService
from repositories.study_repository import StudyRepository # Bổ sung import
from bs4 import BeautifulSoup
import requests

class StudyService(BaseService):
    """CLEAN Study Service - handles RAG + LLM for study support using Real API"""

    def __init__(self):
        super().__init__()
        self.kb_service = KBService()
        self.study_repo = StudyRepository() # Khởi tạo repository để dùng cho get_recommendations

    def process_study_workflow(self, question: str, user_info: dict, upcoming_exams: list) -> dict:
        # ... [Giữ nguyên nội dung hàm process_study_workflow tôi đã cung cấp ở câu trả lời trước] ...
        pass

    def get_recommendations(self, course_code: str) -> list:
        """
        Lấy tài liệu đề xuất: 
        1. Tìm trong Firebase trước.
        2. Nếu không có, tự động crawl từ tailieuhust.com.
        """
        mats = []
        
        # --- 1. TÌM TRONG FIREBASE TRƯỚC ---
        try:
            # Gọi thẳng Repository để quét toàn bộ documents
            # (Bạn cần import DocumentRepository vào __init__ của class này nếu chưa có)
            from repositories.document_repository import DocumentRepository
            doc_repo = DocumentRepository()
            
            all_docs = doc_repo.get_all_documents_by_ownerType("course")
            for d in all_docs:
                # Kiểm tra đúng môn học. Chấp nhận cả "study_material" (file sinh viên tự up)
                if d.get_ownerId() == course_code.upper():
                    mats.append({
                        "title": d.get_title(),
                        # Trả về link hoặc tên file để hiển thị
                        "url": d.get_storagePath() if str(d.get_storagePath()).startswith("http") else "#"
                    })
        except Exception as e:
            print(f"[StudyService] Lỗi khi quét Firebase: {e}")

        # Nếu Firebase CÓ dữ liệu, trả về luôn không cần đi crawl mạng
        if len(mats) > 0:
            return mats

        # --- 2. NẾU FIREBASE RỖNG -> CRAWL TỪ TAILIEUHUST.COM ---
        print(f"[StudyService] Không thấy tài liệu trên Firebase, đang Crawl TailieuHUST cho môn: {course_code}...")
        return self._crawl_tailieuhust(course_code)

    def _crawl_tailieuhust(self, course_code: str) -> list:
        """Hàm phụ: Cào dữ liệu bài viết từ tailieuhust.com"""
        crawled_mats = []
        try:
            # Cú pháp search của WordPress: domain.com/?s=keyword
            search_url = f"https://tailieuhust.com/?s={course_code}"
            
            # Cần giả lập User-Agent của trình duyệt để web không chặn (chống bot)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Trên TailieuHUST, tiêu đề bài viết thường nằm trong thẻ <h2 class="entry-title">
                titles = soup.find_all('h2', class_='entry-title')
                
                # Fallback: Nếu giao diện web đổi, thử tìm thẻ h3
                if not titles:
                    titles = soup.find_all('h3', class_='entry-title')
                    
                # Lặp qua các bài viết tìm được để lấy Link và Tên
                for t in titles:
                    a_tag = t.find('a')
                    if a_tag:
                        crawled_mats.append({
                            "title": f"[Tài liệu HUST] {a_tag.text.strip()}",
                            "url": a_tag['href']
                        })
                        
                # Giới hạn lấy 5 kết quả đầu tiên cho đẹp giao diện
                return crawled_mats[:5]
            else:
                print(f"[StudyService] Web TailieuHUST báo lỗi: {response.status_code}")
                
        except Exception as e:
            print(f"[StudyService] Lỗi khi crawl mạng: {e}")
            
        return crawled_mats

    def generate_flashcards(self, course_code: str, topic: str, num_cards: int = 10) -> dict:
        """Standalone flashcard generator"""
        chunks = self.kb_service.retrieve_relevant_chunks(topic, course_code)

        if not chunks:
            # SỬA Ở ĐÂY: Thêm status và message
            return {"status": "error", "flashcards": [], "message": "Không tìm thấy tài liệu phù hợp để tạo flashcards."}

        context = "\n".join([c.get("content", "") for c in chunks])

        prompt = f"""
        Tạo {num_cards} flashcard về chủ đề: {topic}
        Dựa trên tài liệu:
        {context}
        Format: TRẢ VỀ CHỈ MỘT CHUỖI JSON HỢP LỆ với các object có cấu trúc {{"question": "...", "answer": "..."}}
        """

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```"):
                response_text = response_text[3:-3].strip()
            flashcards_data = json.loads(response_text)
            
            # Đảm bảo flashcards_data là một list
            final_cards = flashcards_data if isinstance(flashcards_data, list) else flashcards_data.get("flashcards", [])
            
            # SỬA Ở ĐÂY: Trả về trạng thái thành công
            return {
                "status": "success",
                "flashcards": final_cards
            }
            
        except Exception as e:
            print(f"[DEBUG] Error parsing flashcards JSON: {e}")
            # SỬA Ở ĐÂY: Trả về trạng thái lỗi nếu quá trình AI parse gặp sự cố
            return {
                "status": "error",
                "flashcards": [],
                "message": f"Lỗi trong quá trình tạo flashcards từ AI."
            }

    def summarize_material(self, course_code: str, length: str = "short") -> dict:
        """Generate course summary"""
        chunks = self.kb_service.retrieve_relevant_chunks(f"Tóm tắt {course_code}", course_code)
        context = "\n".join([c.get("content", "") for c in chunks])

        length_guide = {
            "short": "100-200 từ",
            "medium": "300-500 từ",
            "long": "800+ từ"
        }

        prompt = f"""
        Tóm tắt tài liệu của môn {course_code} trong khoảng {length_guide.get(length, length_guide['short'])}:
        TÀI LIỆU:
        {context}
        """

        response = self.model.generate_content(prompt)
        return {"summary": response.text, "length": length}

