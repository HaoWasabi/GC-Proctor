import unittest
from unittest.mock import MagicMock, patch
from services.regulation_service import RegulationService
from models.document_chunk_model import DocumentChunkModel

class TestRegulationService(unittest.TestCase):

    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def setUp(self, mock_model, mock_configure):
        # Mock repositories
        self.patcher_reg_repo = patch('services.regulation_service.RegulationRepository')
        self.patcher_chunk_repo = patch('services.regulation_service.DocumentChunkRepository')
        
        self.mock_reg_repo = self.patcher_reg_repo.start()
        self.mock_chunk_repo = self.patcher_chunk_repo.start()
        
        self.service = RegulationService()
        self.mock_gemini = MagicMock()
        self.service.model = self.mock_gemini

    def tearDown(self):
        self.patcher_reg_repo.stop()
        self.patcher_chunk_repo.stop()

    def test_answer_regulation_question_found(self):
        # Giả lập dữ liệu chunk quy chế
        mock_chunk = MagicMock(spec=DocumentChunkModel)
        mock_chunk.get_content.return_value = "Điều 15: Sinh viên đi trễ quá 15 phút không được vào phòng thi."
        
        self.mock_chunk_repo.return_value.get_document_chunks_by_owner_type.return_value = [mock_chunk]
        
        # Mock Gemini response
        mock_res = MagicMock()
        mock_res.text = "Theo Điều 15, nếu bạn đi trễ quá 15 phút thì sẽ không được phép vào thi nhé."
        self.mock_gemini.generate_content.return_value = mock_res

        result = self.service.answer_regulation_question("Đi trễ 20 phút có được thi không?")
        print("Câu trả lời:", result)
        self.assertIn("Điều 15", result)
        self.mock_gemini.generate_content.assert_called_once()
        print("Test Regulation: AI trả lời đúng dựa trên chunk được cung cấp.")

if __name__ == '__main__':
    unittest.main()