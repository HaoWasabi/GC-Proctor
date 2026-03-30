import os
import google.generativeai as genai

class BaseService(object):
    _instances = {}
    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(BaseService, class_).__new__(class_, *args, **kwargs)
        return class_._instances[class_]
    
    def __init__(self): 
        # Cấu hình Gemini
        api_key = os.environ.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')