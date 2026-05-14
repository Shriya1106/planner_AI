"""Configuration management for Festiva Planner AI."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Festiva Planner AI"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # API Keys
    openai_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None
    
    # Database
    database_url: str = "sqlite:///./festiva.db"
    
    # Model Settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # RAG Settings
    vector_store_path: str = "./data/vector_store"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_results: int = 5
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
