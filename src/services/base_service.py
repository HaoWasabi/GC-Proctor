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

        self.model = genai.GenerativeModel(self._resolve_model_name())

    def _resolve_model_name(self) -> str:
        preferred_model = os.environ.get("GEMINI_MODEL")
        fallback_candidates = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash-latest",
            "gemini-1.5-pro-latest",
            "gemini-pro",
        ]

        try:
            available_models = {
                model.name.replace("models/", "")
                for model in genai.list_models()
                if "generateContent" in getattr(model, "supported_generation_methods", [])
            }
        except Exception:
            # Nếu không lấy được danh sách model, dùng cấu hình tĩnh để tránh chặn luồng.
            return preferred_model or fallback_candidates[0]

        if preferred_model and preferred_model in available_models:
            return preferred_model

        for candidate in fallback_candidates:
            if candidate in available_models:
                return candidate

        if preferred_model:
            return preferred_model

        return fallback_candidates[0]