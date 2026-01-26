# TIER 4: Pydantic Data Validation
# ==================================

"""
EXERCISE 1: Basic Pydantic Models
----------------------------------
Create Pydantic models for a game quest system:
- QuestReward model: gold (int), items (List[str])
- Quest model: title (str), description (str), reward (QuestReward), completed (bool = False)

Test by creating a quest from a dictionary and accessing its properties.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

# TODO: Create your Pydantic models here
class QuestReward(BaseModel):
    gold: int
    items: List[str]

class Quest(BaseModel):
    title: str
    description: str
    reward: QuestReward
    completed: bool = False


# Test your code
if __name__ == "__main__":
    quest_data = {
        "title": "Slay the Dragon",
        "description": "Defeat the dragon in the mountain",
        "reward": {
            "gold": 1000,
            "items": ["Dragon Scale", "Legendary Sword"]
        }
    }
    
    quest = Quest(**quest_data)
    print(f"Quest: {quest.title}")
    print(f"Reward: {quest.reward.gold} gold")
    print(f"Items: {quest.reward.items}")


"""
EXERCISE 2: Field Validation and Defaults
------------------------------------------
Create a Player model with validation:
- username (str): must be 3-20 characters
- level (int): must be between 1 and 100, default=1
- email (str): add Field() with description
- experience (int): default=0, must be >= 0

Use @field_validator to enforce these rules.
"""

# TODO: Create your Player model with validation
class Player(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="The player's name.")
    level: int = Field(default=1, ge=1, le=100)
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    experience: int = Field(default=0, ge=0)


# Test your code
if __name__ == "__main__":
    # Valid player
    player1 = Player(username="Hero123", email="hero@game.com")
    print(f"Player: {player1.username}, Level: {player1.level}")
    
    # Test validation (these should raise errors - uncomment to test)
    # player2 = Player(username="ab", email="test@test.com")  # too short
    # player3 = Player(username="ValidName", email="test@test.com", level=101)  # level too high
    # player4 = Player(username="ValidName", email="test@test.com", experience=-10)  # negative XP


"""
EXERCISE 3: Model Validation and Conversion
--------------------------------------------
Create a configuration parser:
- ServerConfig model: host (str), port (int), debug (bool), allowed_ips (List[str])
- Add a @field_validator for allowed_ips that converts comma-separated string to list
  (Like the ALLOWED_ORIGINS validator in your config.py)
- Add .model_validate() to convert a dict to ServerConfig
"""

# TODO: Create your ServerConfig model
class ServerConfig(BaseModel):
    host: str
    port: int
    debug: bool
    allowed_ips: str
    
    @field_validator('allowed_ips')
    @classmethod
    def convert_csv_to_list(cls, v: str) -> list:
        return v.split(",") if v else []


# Test your code
if __name__ == "__main__":
    # Test with dict
    config_dict = {
        "host": "localhost",
        "port": 8000,
        "debug": True,
        "allowed_ips": "192.168.1.1,192.168.1.2,10.0.0.1"
    }
    
    config = ServerConfig.model_validate(config_dict)
    print(f"Host: {config.host}:{config.port}")
    print(f"Allowed IPs: {config.allowed_ips}")


# ============================================================================
# SOLUTIONS (Don't peek until you've tried!)
# ============================================================================

"""
SOLUTION 1:
-----------
class QuestReward(BaseModel):
    gold: int
    items: List[str]

class Quest(BaseModel):
    title: str
    description: str
    reward: QuestReward
    completed: bool = False


SOLUTION 2:
-----------
class Player(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    level: int = Field(default=1, ge=1, le=100)
    email: str = Field(..., description="Player's email address")
    experience: int = Field(default=0, ge=0)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not 3 <= len(v) <= 20:
            raise ValueError('Username must be 3-20 characters')
        return v
    
    @field_validator('level')
    @classmethod
    def validate_level(cls, v: int) -> int:
        if not 1 <= v <= 100:
            raise ValueError('Level must be between 1 and 100')
        return v


SOLUTION 3:
-----------
class ServerConfig(BaseModel):
    host: str
    port: int
    debug: bool
    allowed_ips: List[str]
    
    @field_validator('allowed_ips', mode='before')
    @classmethod
    def parse_allowed_ips(cls, v):
        if isinstance(v, str):
            return [ip.strip() for ip in v.split(',') if ip.strip()]
        return v

# Alternative way to use it:
# config = ServerConfig(**config_dict)
"""