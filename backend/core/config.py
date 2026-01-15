from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

# you need to make sure the amount and name of the variables in the Settings class match with those present in .env
class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    DATABASE_URL: str
    ALLOWED_ORIGINS: str = ""
    OPENAI_API_KEY: str
    
    
    # .env files don't support python lists (only csv), so we convert that here
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
settings = Settings() # instantiate object from class