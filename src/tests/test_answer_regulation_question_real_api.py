import os
import unittest

from services.regulation_service import RegulationService


class TestAnswerRegulationQuestionRealAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.getenv("RUN_REAL_API_TESTS") != "1":
            raise unittest.SkipTest("Set RUN_REAL_API_TESTS=1 to run real API tests")

        if not os.getenv("GEMINI_API_KEY"):
            raise unittest.SkipTest("Missing GEMINI_API_KEY")

        firebase_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
        firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        if not firebase_json and not (firebase_path and os.path.exists(firebase_path)):
            raise unittest.SkipTest(
                "Missing Firebase credentials: set FIREBASE_CREDENTIALS_PATH or FIREBASE_CREDENTIALS_JSON"
            )

        cls.user_query = os.getenv(
            "REAL_TEST_REGULATION_QUERY",
            "Di tre 20 phut co duoc vao phong thi khong?",
        )
        cls.service = RegulationService()

    def test_answer_regulation_question_real_data(self):
        answer = self.service.answer_regulation_question(self.user_query)
        print("Answer from API:", answer)   
        self.assertIsInstance(answer, str)
        self.assertTrue(answer.strip(), "answer should not be empty")


if __name__ == "__main__":
    unittest.main()
