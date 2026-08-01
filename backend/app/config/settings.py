from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")


settings = Settings()