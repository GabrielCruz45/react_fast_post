# TIER 2-3: Classes, Type Hints, and Object-Oriented Basics
# =============================================================

"""
EXERCISE 1: Create a Character Class
-------------------------------------
Create a Character class for an RPG game with:
- Instance attributes: name (str), health (int), level (int)
- Instance method: take_damage(amount: int) -> None
- Class method: create_warrior(name: str) -> Character (health=100, level=1)
- Class method: create_mage(name: str) -> Character (health=60, level=1)
"""

from typing import List, Optional, Dict

# TODO: Create your Character class here
class Character:
    def __init__(self, name: str, health: int, level: int):
        self.name = name
        self.health = health
        self.level = level
        
    def take_damage(self, amount: int) -> None:
        self.health = self.health - amount
        
    
    @classmethod
    def create_warrior(cls, name: str) -> 'Character':
        return cls(name, 100, 1)
    
    @classmethod
    def create_mage(cls, name: str) -> 'Character':
        return cls(name, 60, 1)
        
        
        


# Test your code
if __name__ == "__main__":
    # Create characters using class methods
    warrior = Character.create_warrior("Aragorn")
    mage = Character.create_mage("Gandalf")
    
    print(f"{warrior.name}: HP={warrior.health}")
    print(f"{mage.name}: HP={mage.health}")
    
    # Damage the warrior
    print(f"{warrior.name} before damage: HP={warrior.health}")
    warrior.take_damage(30)
    print(f"{warrior.name} after damage: HP={warrior.health}")





"""
EXERCISE 2: Type Hints & Inventory System
------------------------------------------
Create an inventory system with proper type hints:
- Inventory class with items: List[str]
- add_item(item: str) -> None
- remove_item(item: str) -> bool (True if removed, False if not found)
- get_items() -> List[str]
- find_item(search: str) -> Optional[str] (returns item if found, None otherwise)
"""

# TODO: Create your Inventory class here
class Inventory:
    def __init__(self):
        self.items: List[str] = []
    
    
    def add_item(self, item: str) -> None:
        self.items.append(item)
        return
        
    def get_items(self) -> List[str]:
        return self.items
    
    def find_item(self, item) -> str | None:
        if item in self.items:
            return item
        else:
            return None
    
    def remove_item(self, item) -> bool:
        if item in self.items:
            self.items.remove(item)
            return True
        else:
            return False



# Test your code
if __name__ == "__main__":
    inv = Inventory()
    inv.add_item("Sword")
    inv.add_item("Shield")
    inv.add_item("Potion")
    
    print(f"Items: {inv.get_items()}")
    
    found = inv.find_item("Shield")
    print(f"Found: {found}")
    
    removed = inv.remove_item("Shield")
    print(f"Removed Shield: {removed}")
    print(f"Items: {inv.get_items()}")


"""
EXERCISE 3: Inheritance & Method Types
---------------------------------------
Create a vehicle hierarchy:
- Base class Vehicle with: brand (str), speed (int)
- Instance method: accelerate(amount: int) -> None
- Class method: from_dict(data: Dict[str, any]) -> Vehicle
- Subclass Car that adds: num_doors (int)
- Subclass Motorcycle that adds: has_sidecar (bool)
"""

# TODO: Create your Vehicle hierarchy here
class Vehicle:
    def __init__(self, brand: str, speed: int, *args):
        self.brand = brand
        self.speed = speed
  
    def accelerate(self, amount: int) -> None:
        self.speed += amount
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Vehicle':
        return cls(data["brand"], data["speed"])



class Car(Vehicle):
    def __init__(self, brand: str, speed: int, num_doors: int):
        super().__init__(brand, speed)
        self.num_doors = num_doors
        
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Car':
        return cls(data["brand"], data["speed"], data["num_doors"])


class Motorcycle(Vehicle):
    def __init__(self, brand: str, speed: int, has_sidecar: bool):
        super().__init__(brand, speed)
        self.has_sidecar = has_sidecar
        
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Motorcycle':
        return cls(data["brand"], data["speed"], data["has_sidecar"])



# Test your code
if __name__ == "__main__":
    car_data = {"brand": "Toyota", "speed": 0, "num_doors": 4}
    car = Car.from_dict(car_data)
    print(f"{car.brand} with {car.num_doors} doors, speed: {car.speed}")
    
    car.accelerate(50)
    print(f"After acceleration: {car.speed}")


# ============================================================================
# SOLUTIONS (Don't peek until you've tried!)
# ============================================================================

"""
SOLUTION 1:
-----------
class Character:
    def __init__(self, name: str, health: int, level: int):
        self.name = name
        self.health = health
        self.level = level
    
    def take_damage(self, amount: int) -> None:
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    @classmethod
    def create_warrior(cls, name: str) -> 'Character':
        return cls(name, health=100, level=1)
    
    @classmethod
    def create_mage(cls, name: str) -> 'Character':
        return cls(name, health=60, level=1)


SOLUTION 2:
-----------
class Inventory:
    def __init__(self):
        self.items: List[str] = []
    
    def add_item(self, item: str) -> None:
        self.items.append(item)
    
    def remove_item(self, item: str) -> bool:
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def get_items(self) -> List[str]:
        return self.items.copy()
    
    def find_item(self, search: str) -> Optional[str]:
        for item in self.items:
            if search.lower() in item.lower():
                return item
        return None


SOLUTION 3:
-----------
class Vehicle:
    def __init__(self, brand: str, speed: int):
        self.brand = brand
        self.speed = speed
    
    def accelerate(self, amount: int) -> None:
        self.speed += amount
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Vehicle':
        return cls(brand=data["brand"], speed=data["speed"])

class Car(Vehicle):
    def __init__(self, brand: str, speed: int, num_doors: int):
        super().__init__(brand, speed)
        self.num_doors = num_doors
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Car':
        return cls(
            brand=data["brand"],
            speed=data["speed"],
            num_doors=data["num_doors"]
        )

class Motorcycle(Vehicle):
    def __init__(self, brand: str, speed: int, has_sidecar: bool):
        super().__init__(brand, speed)
        self.has_sidecar = has_sidecar
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Motorcycle':
        return cls(
            brand=data["brand"],
            speed=data["speed"],
            has_sidecar=data["has_sidecar"]
        )
"""