from pydantic_ai import Agent, RunContext
import asyncio  
import os
import logfire
from dotenv import load_dotenv
import time
from pydantic import BaseModel

load_dotenv(override=True)
logfire.configure()
logfire.instrument_pydantic_ai()

os.environ["GOOGLE_API_KEY"] = "AIzaSyCwo_fdDi7rJpPeqy9EMSMnIKvFrnG1eik"

model = "google-gla:gemini-2.5-flash"

class CardData(BaseModel):
    name: str
    color: str
    description: str

agent = Agent(model)

@agent.tool
def add_card(ctx: RunContext, name: str, color: str, quantity: int = 1) -> dict:
    """Add a card for the specified item. Determine the color based on the natural color of the fruit/item.
    For example: banana is yellow, apple is red, orange is orange, grape is purple, lime is green, etc.
    
    Args:
        name: The name of the item (e.g., 'banana', 'apple', 'grape')
        color: The natural color of the item (e.g., 'yellow', 'red', 'orange', 'purple', 'green', 'blue', 'pink', 'brown')
        quantity: The quantity of the item (default is 1)
    
    Returns:
        A dictionary with card creation status including the name, color, and quantity
    """
    return {
        "action": "add_card",
        "name": name,
        "color": color,
        "quantity": quantity
    }

@agent.tool
def remove_card(ctx: RunContext, name: str, quantity: int = 1, remove_all: bool = False) -> dict:
    """Remove cards with the specified name.
    
    Args:
        name: The name of the card to remove (e.g., 'banana', 'apple')
        quantity: How many to remove (default is 1). Use when user specifies a number.
        remove_all: Set to True if user says 'all' or 'remove all' (default is False)
    
    Returns:
        A dictionary with card removal status
    """
    return {
        "action": "remove_card",
        "name": name,
        "quantity": quantity,
        "remove_all": remove_all
    }

@agent.tool
def update_card(ctx: RunContext, name: str, new_color: str = None, new_quantity: int = None) -> dict:
    """Update the color and/or quantity of an existing card.
    
    Args:
        name: The name of the card to update (e.g., 'banana', 'apple')
        new_color: The new color for the card (optional, e.g., 'yellow', 'red', 'orange', 'purple', 'green', 'blue', 'pink', 'brown')
        new_quantity: The new quantity for the card (optional)
    
    Returns:
        A dictionary with card update status
    """
    result = {
        "action": "update_card",
        "name": name
    }
    if new_color:
        result["color"] = new_color
    if new_quantity is not None:
        result["quantity"] = new_quantity
    return result

time.sleep(2)  

async def main():
    message_history = []
    while True:
        message = input("You: ")
        if message.upper() in ["EXIT", "QUIT"]:
            break
        response = await agent.run(message, message_history=message_history)
        print("Agent: ", response.output)

        message_history = response.all_messages()

if __name__ == "__main__":
    asyncio.run(main())