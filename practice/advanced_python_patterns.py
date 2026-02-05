# TIER 9: Advanced Python Patterns
# ==================================

# Recursion pattern

# def recursive_function(self, params):
#     # 1. BASE CASE(S) - when to stop recursing
#     if [some condition]:
#         return [base value]
    
#     # 2. RECURSIVE CASE - process current level
#     result = [do something with current node]
    
#     # 3. RECURSE - go deeper into structure
#     for child in self.children:
#         child_result = child.recursive_function(params)
#         [combine child_result with result]
    
#     # 4. RETURN - combined result
#     return result



"""
EXERCISE 1: Recursive Data Structures
--------------------------------------
Create a skill tree system using recursion:
- Skill class: name, level_required, prerequisites (List[Skill])
- has_skill(skill_name: str) -> bool (recursively searches tree)
- get_all_skills() -> List[str] (recursively collects all skill names)
- calculate_total_levels() -> int (recursively sums all level requirements)
"""

from typing import List, Optional, Dict, Any

class Skill:
    def __init__(self, name: str, level_required: int, prerequisites: List['Skill'] = None):
        self.name = name
        self.level_required = level_required
        self.prerequisites = prerequisites or []
    
    # TODO: Implement has_skill recursively
    def has_skill(self, skill_name: str) -> bool: 
        # First, check current
        if self.name == skill_name:
            return True
        
        
        # Then, recurse for further
        for skill in self.prerequisites:
            if skill.has_skill(skill_name):
                return True
        
         
        # If not found; deep in a Shinganshina basement
        return False
            
            
    
    # TODO: Implement get_all_skills recursively
    def get_all_skills(self) -> list[str]:
        skills = []
        skills.append(self.name) 
        
        for child in self.prerequisites:
            skill = child.get_all_skills()
            skills.extend(skill)

        return skills
   
    
    # TODO: Implement calculate_total_levels recursively
    def calculate_total_levels(self) -> int:
        sum = 0
        
        return sum


# Test your code
if __name__ == "__main__":
    # Build a skill tree
    fireball = Skill("Fireball", level_required=5)
    ice_blast = Skill("Ice Blast", level_required=5)
    
    meteor = Skill("Meteor", level_required=15, prerequisites=[fireball])
    blizzard = Skill("Blizzard", level_required=15, prerequisites=[ice_blast])
    
    ultimate = Skill("Elemental Mastery", level_required=30, prerequisites=[meteor, blizzard])
    
    print(f"Has Fireball: {ultimate.has_skill('Fireball')}")
    print(f"Has Lightning: {ultimate.has_skill('Lightning')}")
    print(f"All skills: {ultimate.get_all_skills()}")
    print(f"Total levels required: {ultimate.calculate_total_levels()}")


"""
EXERCISE 2: hasattr() and Dynamic Attributes
---------------------------------------------
Create a flexible data processor that handles both dict and object formats:
- process_character(data) that accepts either a dict or an object
- Should extract: name, level, class_type from either format
- Use hasattr() to detect which format it is
- Return a normalized dict
"""

class CharacterObject:
    def __init__(self, name: str, level: int, class_type: str):
        self.name = name
        self.level = level
        self.class_type = class_type

# TODO: Implement your flexible processor
def process_character(data) -> Dict[str, Any]:
    pass


# Test your code
if __name__ == "__main__":
    # Test with object
    char_obj = CharacterObject("Warrior", 10, "Fighter")
    result1 = process_character(char_obj)
    print(f"From object: {result1}")
    
    # Test with dict
    char_dict = {"name": "Mage", "level": 15, "class_type": "Wizard"}
    result2 = process_character(char_dict)
    print(f"From dict: {result2}")


"""
EXERCISE 3: Recursive Tree Building (Like Your Story Generator)
----------------------------------------------------------------
Recreate the story node processing logic:
- TreeNode class: value (str), children (List[TreeNode])
- build_tree(data: Dict) -> TreeNode that recursively builds a tree
  - data format: {"value": "root", "children": [{"value": "child1", "children": []}, ...]}
- print_tree(node: TreeNode, indent: int) that recursively prints the tree
"""

class TreeNode:
    def __init__(self, value: str):
        self.value = value
        self.children: List['TreeNode'] = []

# TODO: Implement recursive tree builder
def build_tree(data: Dict[str, Any]) -> TreeNode:
    pass

# TODO: Implement recursive tree printer
def print_tree(node: TreeNode, indent: int = 0):
    pass


# Test your code
if __name__ == "__main__":
    tree_data = {
        "value": "Start",
        "children": [
            {
                "value": "Go Left",
                "children": [
                    {"value": "Find Treasure", "children": []},
                    {"value": "Meet Dragon", "children": []}
                ]
            },
            {
                "value": "Go Right",
                "children": [
                    {"value": "Find Exit", "children": []}
                ]
            }
        ]
    }
    
    tree = build_tree(tree_data)
    print_tree(tree)


# ============================================================================
# SOLUTIONS (Don't peek until you've tried!)
# ============================================================================

"""
SOLUTION 1:
-----------
class Skill:
    def __init__(self, name: str, level_required: int, prerequisites: List['Skill'] = None):
        self.name = name
        self.level_required = level_required
        self.prerequisites = prerequisites or []
    
    def has_skill(self, skill_name: str) -> bool:
        if self.name == skill_name:
            return True
        
        for prereq in self.prerequisites:
            if prereq.has_skill(skill_name):
                return True
        
        return False
    
    def get_all_skills(self) -> List[str]:
        skills = [self.name]
        
        for prereq in self.prerequisites:
            skills.extend(prereq.get_all_skills())
        
        return skills
    
    def calculate_total_levels(self) -> int:
        total = self.level_required
        
        for prereq in self.prerequisites:
            total += prereq.calculate_total_levels()
        
        return total


SOLUTION 2:
-----------
def process_character(data) -> Dict[str, Any]:
    result = {}
    
    # Check if it's an object with attributes
    if hasattr(data, 'name'):
        result['name'] = data.name
        result['level'] = data.level
        result['class_type'] = data.class_type
    # Otherwise treat as dict
    else:
        result['name'] = data['name']
        result['level'] = data['level']
        result['class_type'] = data['class_type']
    
    return result


SOLUTION 3:
-----------
def build_tree(data: Dict[str, Any]) -> TreeNode:
    # Create the current node
    node = TreeNode(data['value'])
    
    # Recursively build children
    if 'children' in data:
        for child_data in data['children']:
            child_node = build_tree(child_data)
            node.children.append(child_node)
    
    return node

def print_tree(node: TreeNode, indent: int = 0):
    print("  " * indent + f"- {node.value}")
    
    for child in node.children:
        print_tree(child, indent + 1)
"""