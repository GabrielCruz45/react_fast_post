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

from sqlalchemy import Integer, String, DateTime, Numeric, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, Session, Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

# TODO: Create your Player model
class Player(Base):
    __tablename__ = "players"
    
    id:         Mapped[int]         = mapped_column(primary_key=True)
    username:   Mapped[str]         = mapped_column(String(32))
    level:      Mapped[int]         = mapped_column(default=1)
    created_at: Mapped[datetime]    = mapped_column(server_default=func.now())
     
    characters: Mapped[list["Character"]] = relationship(
        back_populates="player_from_character", 
        cascade="all, delete-orphan"
    )



# TODO: Create your Character model
class Character(Base):
    __tablename__ = "characters"
    
    id:         Mapped[int]         = mapped_column(primary_key=True)
    player_id:  Mapped[int]         = mapped_column(ForeignKey("players.id"), index=True)
    name:       Mapped[str]         = mapped_column(String(32))
    class_type: Mapped[str]         = mapped_column(String(32))
    
    player_from_character:     Mapped["Player"]    = relationship(back_populates="characters")
    
    
    


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

from decimal import Decimal

# TODO: Create your Item model
class Item(Base):
    __tablename__ = "items"
    
    id:         Mapped[int]             = mapped_column(primary_key=True)
    name:       Mapped[str]             = mapped_column(String(32))
    price:      Mapped[Decimal]         = mapped_column(Numeric(precision=10, scale=2))
    
    
# TODO: Create your PlayerInventory model  
class PlayerInventory(Base):
    __tablename__ = "player_inventory"
    
    id:         Mapped[int]             = mapped_column(primary_key=True)
    player_id:  Mapped[int]             = mapped_column(ForeignKey("players.id"), index=True)
    item_id:    Mapped[int]             = mapped_column(ForeignKey("items.id"), index=True)
    quantity:   Mapped[int]             = mapped_column(default=0)



# Test your code
if __name__ == "__main__":
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session = Session(engine)
    
    # TODO: Create player and add to session
    player = Player(username="gxbs_")
    session.add(player)
    session.flush() # get id?
    
    # TODO: Create items
    green_potion    = Item(name="Green Potion", price=1.35)
    red_potion      = Item(name="Red Potion", price=3.51)
    blue_potion     = Item(name="Blue Potion", price=5.13)
    
    session.add_all([green_potion, red_potion, blue_potion])
    session.flush() # get id?
    
    

    # TODO: Add items to player inventory
    inv_item_green  = PlayerInventory(player_id=player.id, item_id=green_potion.id, quantity=1)
    inv_item_red    = PlayerInventory(player_id=player.id, item_id=red_potion.id, quantity=1)
    inv_item_blue   = PlayerInventory(player_id=player.id, item_id=blue_potion.id, quantity=1)
    
    session.add_all([inv_item_green, inv_item_red, inv_item_blue])

    # TODO: Commit session
    session.commit()
    
    print(f"Player {player.username} inventory created with {session.query(PlayerInventory).count()} items")



"""
EXERCISE 3: JSON Column and Complex Relationships
--------------------------------------------------
Create a Quest system with JSON data:
- Quest model: id, title, description, rewards (JSON column)
- PlayerQuest model: id, player_id, quest_id, status, progress (JSON)
- Set up bidirectional relationships
"""

from typing import Any
from sqlalchemy import JSON, Boolean
from sqlalchemy.ext.mutable import MutableDict
# from sqlalchemy.dialects.postgresql import JSONB                                                              **for postgres!


# TODO: Create your Quest model
class Quest(Base):
    __tablename__ = "quests"
    
    id:             Mapped[int]                 = mapped_column(primary_key=True)
    title:          Mapped[str]                 = mapped_column(String(32))
    description:    Mapped[str]                 = mapped_column(String(256))
    rewards:        Mapped[dict[str, Any]]      = mapped_column(MutableDict.as_mutable(JSON))
    
    player_quests:  Mapped[list["PlayerQuest"]] = relationship(back_populates="quest")

# TODO: Create your PlayerQuest model
class PlayerQuest(Base):
    __tablename__ = "player_quests"
    
    id:             Mapped[int]                 = mapped_column(primary_key=True)
    player_id:      Mapped[int]                 = mapped_column(ForeignKey("players.id"), index=True)
    quest_id:       Mapped[int]                 = mapped_column(ForeignKey("quests.id"), index=True)
    status:         Mapped[str]                 = mapped_column(String(32))
    progress:       Mapped[dict[str, Any]]      = mapped_column(MutableDict.as_mutable(JSON))
    # progress:     Mapped[dict[str, Any]]      = mapped_column(JSONB)                                           **for posstgres!
    
    quest:          Mapped["Quest"]             = relationship(back_populates="player_quests")

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