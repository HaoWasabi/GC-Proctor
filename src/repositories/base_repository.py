import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
import logging
import os
import json

load_dotenv()
logger = logging.getLogger("repositories")

class BaseRepository:
    def __init__(self):
        # Lấy đường dẫn file credentials từ biến môi trường
        firebase_json = os.getenv("FIREBASE_CREDENTIALS_PATH")
        if not firebase_admin._apps:
            if firebase_json and os.path.exists(firebase_json):
                cred = credentials.Certificate(firebase_json)
            else:
                # Hoặc đọc JSON từ ENV (nếu lưu trực tiếp trong GitHub Secrets)
                cred_dict = json.loads(os.getenv("FIREBASE_CREDENTIALS_JSON"))
                cred = credentials.Certificate(cred_dict)

            firebase_admin.initialize_app(cred)
        self.db = firestore.client()