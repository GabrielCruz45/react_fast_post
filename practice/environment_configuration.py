# TIER 5: Environment Variables & Configuration
# ===============================================

"""
SETUP: Create a .env file in the same directory with this content:
-------
APP_NAME=MyGameServer
DEBUG=true
DATABASE_URL=postgresql://localhost/gamedb
MAX_PLAYERS=100
ADMIN_EMAILS=admin@game.com,mod@game.com,support@game.com
API_KEY=secret_key_12345
"""

"""
EXERCISE 1: Basic Environment Loading
--------------------------------------
Create a GameSettings class using Pydantic BaseSettings:
- app_name (str)
- debug (bool)
- database_url (str)
- max_players (int)
- Load from .env file automatically
"""
import os

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
from dotenv import load_dotenv

load_dotenv()

# TODO: Create your GameSettings class
class GameSettings(BaseSettings):
    app_name: str = os.getenv('APP_NAME')
    debug: bool = os.getenv('DEBUG')
    database_url: str = os.getenv('DATABASE_URL')
    max_players: str = os.getenv('MAX_PLAYERS')
    
    


# Test your code
if __name__ == "__main__":
    settings = GameSettings()
    print(f"App: {settings.app_name}")
    print(f"Debug: {settings.debug}")
    print(f"Max Players: {settings.max_players}")
    print("Hello")


"""
EXERCISE 2: CSV Parsing in Environment Variables
-------------------------------------------------
Extend GameSettings to include:
- admin_emails (str in .env, List[str] in Python)
- Use @field_validator to convert comma-separated string to list
- Handle the case_sensitive and env_file settings in Config class
"""

# TODO: Create your enhanced GameSettings class
class GameSettings(BaseSettings):
    app_name: str
    debug: bool
    database_url: str
    max_players: str
    admin_emails: str

    @field_validator('admin_emails')
    @classmethod
    def csv_to_list(cls, v: str) -> list:
        return v.split(",") if v else []
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False # controls whether environment variables must match exact casing
        extra = "ignore" # ignores any variable that's in the .env but not in outer class; api_key in this case
        


# Test your code
if __name__ == "__main__":
    settings = GameSettings()
    print(f"Admin emails: {settings.admin_emails}")
    print(f"Type: {type(settings.admin_emails)}")


"""
EXERCISE 3: Multiple Environment Files & Overrides
---------------------------------------------------
Create a flexible config system:
- AppConfig class that loads from .env
- Supports optional .env.local override file
- Has a get_api_key() method that returns the API key
- Has a is_production() method that returns True if debug=False
"""

import os

# TODO: Create your AppConfig class
class AppConfig(BaseSettings):
    app_name: str
    debug: bool
    database_url: str
    max_players: str
    admin_emails: str
    api_key: str
    
    class Config:
        env_file = [".env", ".env.local"]
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"
        

    def get_api_key(self) -> str:
        return self.api_key
    
    
    def is_production(self) -> bool:
        return not self.debug
        


# Test your code
if __name__ == "__main__":
    config = AppConfig()
    
    with open('.env.local', 'r') as f:
        print("Content of .env.local:")
        print(f.read())
        print("--- End of file ---")
    
    print(f"Is Production: {config.is_production()}")
    print(f"API Key: {config.get_api_key()}")
    
    # Test environment override
    os.environ["DEBUG"] = "false"
    config_prod = AppConfig()
    print(f"Is Production (after override): {config_prod.is_production()}")


# ============================================================================#
#               SOLUTIONS (Don't peek until you've tried!)                    #
# ============================================================================#

"""
SOLUTION 1:
-----------
class GameSettings(BaseSettings):
    app_name: str
    debug: bool
    database_url: str
    max_players: int
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


SOLUTION 2:
-----------
class GameSettings(BaseSettings):
    app_name: str
    debug: bool
    database_url: str
    max_players: int
    admin_emails: List[str]
    
    @field_validator('admin_emails', mode='before')
    @classmethod
    def parse_emails(cls, v):
        if isinstance(v, str):
            return [email.strip() for email in v.split(',') if email.strip()]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


SOLUTION 3:
-----------
class AppConfig(BaseSettings):
    app_name: str
    debug: bool
    database_url: str
    api_key: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def get_api_key(self) -> str:
        return self.api_key
    
    def is_production(self) -> bool:
        return not self.debug

# For .env.local support, you can do:
# class Config:
#     env_file = [".env", ".env.local"]
"""