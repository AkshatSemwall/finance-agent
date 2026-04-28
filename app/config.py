from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    openai_api_key: str = "test"
    model: str = "gpt-4o-mini"
    memory_file: str = "data/memory.json"
    transactions_file: str = "data/transactions.json"
    
    model_config = ConfigDict(env_file=".env")

settings = Settings()