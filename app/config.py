import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Default fallback
    DEBUG = True  # Set False in production
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    @staticmethod
    def init_app(app):
        """Additional app configurations if needed."""
        pass
