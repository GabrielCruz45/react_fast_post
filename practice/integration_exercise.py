# TIER 10: Integration Exercise - All Concepts Together
# =======================================================

"""
MEGA EXERCISE: Build a Mini Quest Generator
--------------------------------------------
Combine all concepts from previous tiers:

1. Configuration (Tier 5):
   - Load GOOGLE_API_KEY from .env using BaseSettings

2. Pydantic Models (Tier 4):
   - Quest: title, description, difficulty, reward_gold
   - QuestObjective: description, completed (bool)
   - GeneratedQuest: quest info + objectives (List[QuestObjective])

3. SQLAlchemy (Tier 6):
   - Quest table
   - QuestObjective table with ForeignKey to Quest
   - Use flush() to get IDs before creating objectives

4. LangChain (Tier 7-8):
   - Generate quest data using LLM
   - Parse into structured GeneratedQuest model

5. Recursive Processing (Tier 9):
   - Create quest in database with its objectives

Create a QuestGenerator class that:
- Has a @classmethod generate_quest(db: Session, theme: str) -> Quest
- Uses LLM to generate quest data
- Saves to database with objectives
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, Session
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from typing import List
from dotenv import load_dotenv

load_dotenv()

# TODO 1: Create your config
class Config(BaseSettings):
    pass


# TODO 2: Create your Pydantic models for LLM output
class QuestObjectiveLLM(BaseModel):
    pass

class GeneratedQuestLLM(BaseModel):
    pass


# TODO 3: Create your SQLAlchemy models
Base = declarative_base()

class Quest(Base):
    __tablename__ = "quests"
    pass

class QuestObjective(Base):
    __tablename__ = "quest_objectives"
    pass


# TODO 4: Create your QuestGenerator class
class QuestGenerator:
    
    @classmethod
    def _get_llm(cls):
        pass
    
    @classmethod
    def generate_quest(cls, db: Session, theme: str) -> Quest:
        """
        Generate a quest using LLM and save to database.
        
        Steps:
        1. Get LLM instance
        2. Create PydanticOutputParser for GeneratedQuestLLM
        3. Create prompt template asking for quest with 2-3 objectives
        4. Invoke LLM and parse response
        5. Create Quest in database and flush
        6. Create QuestObjective entries using quest.id
        7. Commit and return
        """
        pass


# Test your code
if __name__ == "__main__":
    # Setup database
    engine = create_engine("sqlite:///quests.db", echo=False)
    Base.metadata.create_all(engine)
    session = Session(engine)
    
    # Generate quest
    print("Generating quest...")
    quest = QuestGenerator.generate_quest(session, "fantasy dungeon")
    
    print(f"\nQuest: {quest.title}")
    print(f"Description: {quest.description}")
    print(f"Difficulty: {quest.difficulty}")
    print(f"Reward: {quest.reward_gold} gold")
    print(f"\nObjectives:")
    for obj in quest.objectives:
        print(f"  - {obj.description}")
    
    session.close()


# ============================================================================
# SOLUTION (Don't peek until you've tried!)
# ============================================================================

"""
SOLUTION:
---------
class Config(BaseSettings):
    google_api_key: str
    
    class Config:
        env_file = ".env"


class QuestObjectiveLLM(BaseModel):
    description: str = Field(description="What the player needs to do")

class GeneratedQuestLLM(BaseModel):
    title: str = Field(description="Quest title")
    description: str = Field(description="Quest description")
    difficulty: str = Field(description="easy, medium, or hard")
    reward_gold: int = Field(description="Gold reward amount")
    objectives: List[QuestObjectiveLLM] = Field(description="List of 2-3 objectives")


class Quest(Base):
    __tablename__ = "quests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    difficulty = Column(String)
    reward_gold = Column(Integer)
    
    objectives = relationship("QuestObjective", back_populates="quest")

class QuestObjective(Base):
    __tablename__ = "quest_objectives"
    
    id = Column(Integer, primary_key=True, index=True)
    quest_id = Column(Integer, ForeignKey("quests.id"), index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    
    quest = relationship("Quest", back_populates="objectives")


class QuestGenerator:
    
    @classmethod
    def _get_llm(cls):
        return ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.7)
    
    @classmethod
    def generate_quest(cls, db: Session, theme: str) -> Quest:
        llm = cls._get_llm()
        
        parser = PydanticOutputParser(pydantic_object=GeneratedQuestLLM)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a quest generator for an RPG game."),
            ("human", '''Generate a {theme} quest with:
            - A compelling title and description
            - Difficulty level (easy, medium, or hard)
            - Appropriate gold reward (50-500)
            - 2-3 specific objectives
            
            {format_instructions}''')
        ]).partial(format_instructions=parser.get_format_instructions())
        
        response = llm.invoke(prompt.invoke({"theme": theme}))
        quest_data = parser.parse(response.content)
        
        # Create quest
        quest = Quest(
            title=quest_data.title,
            description=quest_data.description,
            difficulty=quest_data.difficulty,
            reward_gold=quest_data.reward_gold
        )
        db.add(quest)
        db.flush()  # Get quest.id
        
        # Create objectives
        for obj_data in quest_data.objectives:
            objective = QuestObjective(
                quest_id=quest.id,
                description=obj_data.description,
                completed=False
            )
            db.add(objective)
        
        db.commit()
        return quest
"""