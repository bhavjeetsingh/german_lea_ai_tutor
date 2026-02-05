from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Server
    port: int = 8000
    environment: str = "development"
    
    # AI Provider
    ai_provider: Literal["openai", "gemini", "groq"] = "groq"
    
    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    
    # Google Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-pro"
    
    # Groq
    groq_api_key: str = ""
    groq_model: str = "llama-3.1-70b-versatile"
    
    # CORS
    cors_origin: str = "http://localhost:8501"
    
    # Data Storage
    data_dir: str = "./data"
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )


settings = Settings()