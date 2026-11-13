import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    def validate(self):
        missing = []
        if not self.GROQ_API_KEY: missing.append("GROQ_API_KEY")
        if not self.QDRANT_URL: missing.append("QDRANT_URL")
        if not self.QDRANT_API_KEY: missing.append("QDRANT_API_KEY")
        
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")
        return True

settings = Settings()