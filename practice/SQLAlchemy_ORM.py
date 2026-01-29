# TIER 6: SQLAlchemy Database ORM
# =================================

"""
SETUP: This uses SQLite (no installation needed)
You'll create an in-memory database for testing.
"""

"""
EXERCISE 1: Basic Models and Relationships
-------------------------------------------
Create a simple game database:
- Player model: id, username, level, created_at
- Character model: id, player_id (ForeignKey), name, class_type
- Set up relationship between Player and Character (one player has many characters)
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, Session, Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

# TODO: Create your Player model
class Player(Base):
    __tablename__ = "players"
    
    id:         Mapped[int]         = mapped_column(primary_key=True)
    username:   Mapped[str]         = mapped_column(String(30))
    level:      Mapped[int]         = mapped_column(default=1)
    created_at: Mapped[datetime]    = mapped_column(server_default=func.now())
    
    characters: Mapped[list["Character"]] = relationship(
        back_populates="player", cascade="all, delete-orphan"
    )

# TODO: Create your Character model
class Character(Base):
    __tablename__ = "characters"
    
    id:         Mapped[int]         = mapped_column(primary_key=True)
    player_id:  Mapped[int]         = mapped_column(ForeignKey("players.id"), index=True)
    name:       Mapped[str]         = mapped_column(String(30))
    class_type: Mapped[str]         = mapped_column(String(30))
    
    player:     Mapped["Player"]    = relationship(back_populates="characters")
    
    
    


# Test your code
if __name__ == "__main__":
    # Create in-memory database
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    
    # Create a session
    session = Session(engine)
    
    # Create player and characters
    player = Player(username="Hero123", level=10)
    session.add(player)
    session.flush()  # Get the player.id
    
    char1 = Character(player_id=player.id, name="Warrior", class_type="Fighter")
    char2 = Character(player_id=player.id, name="Mage", class_type="Wizard")
    
    session.add_all([char1, char2])
    session.commit()
    
    # Query back
    loaded_player = session.query(Player).filter_by(username="Hero123").first()
    print(f"Player: {loaded_player.username}, Characters: {len(loaded_player.characters)}")
    
    for char in loaded_player.characters:
        print(f"  - {char.name} ({char.class_type})")


"""
EXERCISE 2: Flush vs Commit and Auto-IDs
-----------------------------------------
Create an Inventory system that demonstrates flush() usage:
- Item model: id, name, price
- PlayerInventory model: id, player_id, item_id, quantity
- Create 3 items, flush to get IDs, then add them to a player's inventory
"""

# TODO: Create your Item model
class Item(Base):
    __tablename__ = "items"
    pass

# TODO: Create your PlayerInventory model  
class PlayerInventory(Base):
    __tablename__ = "player_inventory"
    pass



# Test your code
if __name__ == "__main__":
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session = Session(engine)
    
    # TODO: Create player and add to session

    
    # TODO: Create items


    # TODO: Add items to player inventory


    # TODO: Commit session
    
    print(f"Player {player.username} inventory created with {session.query(PlayerInventory).count()} items")



"""
EXERCISE 3: JSON Column and Complex Relationships
--------------------------------------------------
Create a Quest system with JSON data:
- Quest model: id, title, description, rewards (JSON column)
- PlayerQuest model: id, player_id, quest_id, status, progress (JSON)
- Set up bidirectional relationships
"""

from sqlalchemy import JSON, Boolean

# TODO: Create your Quest model
class Quest(Base):
    __tablename__ = "quests"
    pass

# TODO: Create your PlayerQuest model
class PlayerQuest(Base):
    __tablename__ = "player_quests"
    pass


# Test your code
if __name__ == "__main__":
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session = Session(engine)
    
    # Create quest with JSON rewards
    quest = Quest(
        title="Dragon Slayer",
        description="Defeat the ancient dragon",
        rewards={"gold": 1000, "items": ["Dragon Scale", "Legendary Sword"], "experience": 5000}
    )
    session.add(quest)
    session.flush()
    
    # Create player
    player = Player(username="DragonHunter", level=50)
    session.add(player)
    session.flush()
    
    # Assign quest to player with JSON progress
    player_quest = PlayerQuest(
        player_id=player.id,
        quest_id=quest.id,
        status="in_progress",
        progress={"dragons_killed": 0, "required": 1, "current_location": "Dragon's Lair"}
    )
    session.add(player_quest)
    session.commit()
    
    # Query back
    pq = session.query(PlayerQuest).first()
    print(f"Quest: {pq.quest.title}")
    print(f"Rewards: {pq.quest.rewards}")
    print(f"Progress: {pq.progress}")


# ============================================================================
# SOLUTIONS (Don't peek until you've tried!)
# ============================================================================

"""
SOLUTION 1:
-----------
class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    level = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    characters = relationship("Character", back_populates="player")

class Character(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    name = Column(String)
    class_type = Column(String)
    
    player = relationship("Player", back_populates="characters")


SOLUTION 2:
-----------
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)

class PlayerInventory(Base):
    __tablename__ = "player_inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, default=1)


SOLUTION 3:
-----------
class Quest(Base):
    __tablename__ = "quests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    rewards = Column(JSON)
    
    player_quests = relationship("PlayerQuest", back_populates="quest")

class PlayerQuest(Base):
    __tablename__ = "player_quests"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    quest_id = Column(Integer, ForeignKey("quests.id"), index=True)
    status = Column(String, default="not_started")
    progress = Column(JSON, default=dict)
    
    player = relationship("Player")
    quest = relationship("Quest", back_populates="player_quests")
"""