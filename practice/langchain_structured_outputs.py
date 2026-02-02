# TIER 7-8: LangChain & Structured Output Parsing
# =================================================

"""
SETUP: You'll need a Google API key in your .env file:
GOOGLE_API_KEY=your_api_key_here

Get one from: https://makersuite.google.com/app/apikey
"""

"""
EXERCISE 1: Basic LLM Call with Prompts
----------------------------------------
Create a simple character backstory generator:
- Use ChatGoogleGenerativeAI with gemini-2.0-flash-exp
- Create a ChatPromptTemplate with system and human messages
- System: "You are a fantasy character backstory writer"
- Human: "Create a backstory for a {character_class} named {name}"
- Call the LLM and print the response
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

# TODO: Create your character backstory generator
def generate_backstory(character_class: str, name: str) -> str:
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a fantasy character backstory writer"),
        ("human", "Create a backstory for a {character_class} named {name}"),
    ])
    
    message = template.format_messages(
        character_class=character_class,
        name=name
    )
    
    ai_msg = model.invoke(message)
    
    return ai_msg.content


# Test your code
if __name__ == "__main__":
    backstory = generate_backstory("wizard", "Gandalf")
    print(backstory)


"""
EXERCISE 2: Structured Output with Pydantic
--------------------------------------------
Create a loot drop generator that returns structured data:
- LootItem model: name (str), rarity (str), value (int)
- LootDrop model: items (List[LootItem]), total_value (int)
- Use PydanticOutputParser to parse the LLM response
- Prompt: "Generate a loot drop for defeating a {enemy_type}"
"""

# TODO: Create your Pydantic models
class LootItem(BaseModel):
    name: str = Field()
    rarity: str = Field()
    value: int

class LootDrop(BaseModel):
    items: list[LootItem] = Field(
        description="""
        A list of LootItem objects which have three fields: 
            1. name, which is the name of the item as a Python String.
            2. rarity, which is a Python String. Has four options: Common, Uncommon, Rare and Mythic Rare.
            3. value, which is the total value of the item as a Python Int.
        """)
    total_value: int = Field(description="The total value of all items as a Python Int.")

# TODO: Create your loot generator
def generate_loot(enemy_type: str) -> LootDrop:
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    
    parser = PydanticOutputParser(pydantic_object=LootDrop)
    
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a loot generator. {format_instructions}"),
        ("human", "Generate a loot drop for defeating a {enemy_type}. Output ONLY valid JSON, no extra text."),
    ])
    
    message = template.format_messages(
        format_instructions=parser.get_format_instructions(),
        enemy_type=enemy_type
    )
    
    ai_msg = model.invoke(message)
    
    return parser.parse(ai_msg.content)


# Test your code
if __name__ == "__main__":
    loot = generate_loot("dragon")
    print(f"Total value: {loot.total_value}")
    for item in loot.items:
        print(f"  - {item.name} ({item.rarity}): {item.value}g")


"""
EXERCISE 3: Complex Nested Structures (Mini Story Generator)
-------------------------------------------------------------
Create a simplified version of your story generator:
- StoryChoice model: text (str), outcome (str)
- StoryNode model: content (str), choices (List[StoryChoice])
- Use PydanticOutputParser to generate a 2-choice story node
- The LLM should return a complete StoryNode with 2 choices
"""

# TODO: Create your Pydantic models
class StoryChoice(BaseModel):
    text: str
    outcome: str

class StoryNode(BaseModel):
    contetn: str
    choices: list[StoryChoice]

# TODO: Create your story node generator
def generate_story_node(theme: str) -> StoryNode:
    pass


# Test your code
if __name__ == "__main__":
    node = generate_story_node("space adventure")
    print(f"Story: {node.content}")
    print("Choices:")
    for i, choice in enumerate(node.choices, 1):
        print(f"  {i}. {choice.text}")
        print(f"     Result: {choice.outcome}")


# ============================================================================
# SOLUTIONS (Don't peek until you've tried!)
# ============================================================================

"""
SOLUTION 1:
-----------
def generate_backstory(character_class: str, name: str) -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a fantasy character backstory writer. Create engaging backstories."),
        ("human", "Create a backstory for a {character_class} named {name}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"character_class": character_class, "name": name})
    
    return response.content


SOLUTION 2:
-----------
class LootItem(BaseModel):
    name: str = Field(description="The name of the item")
    rarity: str = Field(description="Rarity: common, uncommon, rare, epic, legendary")
    value: int = Field(description="Gold value of the item")

class LootDrop(BaseModel):
    items: List[LootItem] = Field(description="List of items in the loot drop")
    total_value: int = Field(description="Total gold value of all items")

def generate_loot(enemy_type: str) -> LootDrop:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.7)
    
    parser = PydanticOutputParser(pydantic_object=LootDrop)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a game loot generator. Generate appropriate loot drops."),
        ("human", "Generate a loot drop for defeating a {enemy_type}. {format_instructions}")
    ]).partial(format_instructions=parser.get_format_instructions())
    
    chain = prompt | llm
    response = chain.invoke({"enemy_type": enemy_type})
    
    return parser.parse(response.content)


SOLUTION 3:
-----------
class StoryChoice(BaseModel):
    text: str = Field(description="The text of the choice shown to the player")
    outcome: str = Field(description="What happens if the player chooses this")

class StoryNode(BaseModel):
    content: str = Field(description="The main story content")
    choices: List[StoryChoice] = Field(description="The choices available")

def generate_story_node(theme: str) -> StoryNode:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.7)
    
    parser = PydanticOutputParser(pydantic_object=StoryNode)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a creative story writer. Generate story nodes with choices."),
        ("human", '''Create a story node with a {theme} theme.
        Include:
        - A compelling situation (content)
        - Exactly 2 choices
        - Each choice should have clear outcomes
        
        {format_instructions}''')
    ]).partial(format_instructions=parser.get_format_instructions())
    
    chain = prompt | llm
    response = chain.invoke({"theme": theme})
    
    return parser.parse(response.content)
"""