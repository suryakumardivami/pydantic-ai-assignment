from fasthtml.common import *
from main import agent
import asyncio

app, routes = fast_app(
    hdrs=(
        Script(src="https://cdn.tailwindcss.com", pico=False),
    )
)

# Store message history for each session
message_histories = {}

class CardManager:
    """Manages card operations and storage."""
    
    def __init__(self):
        self.cards_storage = {}
        self.cart_storage = {}  # Track items added to cart
        self.color_map = {
            'yellow': 'bg-yellow-400', 'red': 'bg-red-500', 'green': 'bg-green-500',
            'blue': 'bg-blue-500', 'orange': 'bg-orange-500', 'purple': 'bg-purple-500',
            'pink': 'bg-pink-500', 'brown': 'bg-amber-700'
        }
        self.initial_inventory = {
            'banana': {'name': 'banana', 'color': 'yellow', 'quantity': 4, 'price': 50},
            'apple': {'name': 'apple', 'color': 'red', 'quantity': 5, 'price': 80},
            'orange': {'name': 'orange', 'color': 'orange', 'quantity': 3, 'price': 60},
            'grape': {'name': 'grape', 'color': 'purple', 'quantity': 6, 'price': 120}
        }
    
    def initialize_session(self, session_id: str):
        """Initialize a session with predefined inventory."""
        if session_id not in self.cards_storage:
            self.cards_storage[session_id] = {k: v.copy() for k, v in self.initial_inventory.items()}
        if session_id not in self.cart_storage:
            self.cart_storage[session_id] = {}
    
    def add_card(self, session_id: str, name: str, color: str, quantity: int = 1):
        """Add items to cart and decrease inventory."""
        self.initialize_session(session_id)
        name = name.lower()
        
        if name in self.cards_storage[session_id]:
            current_qty = self.cards_storage[session_id][name]['quantity']
            if quantity > current_qty:
                return f"Unable to add {quantity} {name}(s). Only {current_qty} available in stock."
            
            # Decrease inventory
            self.cards_storage[session_id][name]['quantity'] -= quantity
            
            # Add to cart
            if name in self.cart_storage[session_id]:
                self.cart_storage[session_id][name]['quantity'] += quantity
            else:
                item_data = self.cards_storage[session_id][name]
                self.cart_storage[session_id][name] = {
                    'name': name,
                    'color': item_data['color'],
                    'quantity': quantity,
                    'price': item_data['price']
                }
            return None
        else:
            return f"Unable to add {name}. Item not available in inventory."
    
    def remove_card(self, session_id: str, name: str, quantity: int = 1, remove_all: bool = False):
        """Remove items from cart and restore to inventory."""
        self.initialize_session(session_id)
        name = name.lower()
        
        if name in self.cart_storage[session_id]:
            cart_qty = self.cart_storage[session_id][name]['quantity']
            
            if remove_all:
                # Remove all from cart, restore to inventory
                self.cards_storage[session_id][name]['quantity'] += cart_qty
                del self.cart_storage[session_id][name]
            else:
                # Remove specified quantity
                if quantity >= cart_qty:
                    # Remove all if quantity >= cart quantity
                    self.cards_storage[session_id][name]['quantity'] += cart_qty
                    del self.cart_storage[session_id][name]
                else:
                    # Partial removal
                    self.cart_storage[session_id][name]['quantity'] -= quantity
                    self.cards_storage[session_id][name]['quantity'] += quantity
        else:
            return f"Unable to remove {name}. Item not in cart."
    
    def update_card(self, session_id: str, name: str, new_color: str = None, new_quantity: int = None):
        """Update card color or quantity."""
        if session_id not in self.cards_storage:
            return
        
        name = name.lower()
        if name in self.cards_storage[session_id]:
            if new_color:
                self.cards_storage[session_id][name]['color'] = new_color
            if new_quantity is not None:
                self.cards_storage[session_id][name]['quantity'] = new_quantity
    
    def create_card_element(self, name: str, color: str, quantity: int, card_id: str, price: float = 0.0, small: bool = False):
        """Create a single card HTML element."""
        color_class = self.color_map.get(color.lower(), 'bg-gray-500')
        if small:
            return Div(
                H4(name.title(), cls="text-sm font-bold text-black"),
                P(f"₹{price:.0f}", cls="text-xs font-semibold text-black mt-0.5"),
                P(f"Qty: {quantity}", cls="text-xs font-medium text-black mt-0.5"),
                cls=f"{color_class} p-2 rounded-lg shadow w-24 h-24 flex flex-col items-center justify-center",
                id=f"card-{card_id}"
            )
        return Div(
            H4(name.title(), cls="text-xl font-bold text-black"),
            P(f"₹{price:.0f}", cls="text-lg font-semibold text-black mt-1"),
            P(f"Qty: {quantity}", cls="text-sm font-medium text-black mt-1"),
            cls=f"{color_class} p-4 rounded-lg shadow-lg w-36 h-36 flex flex-col items-center justify-center",
            id=f"card-{card_id}"
        )
    
    def render_all_cards(self, session_id: str, small: bool = False):
        """Render all cards for a session."""
        self.initialize_session(session_id)
        
        if not self.cards_storage[session_id]:
            return Div(id="cards-container", cls="flex flex-wrap gap-4")
        
        cards = [
            self.create_card_element(data['name'], data['color'], data['quantity'], card_id, data.get('price', 0.0), small)
            for card_id, data in self.cards_storage[session_id].items()
        ]
        return Div(*cards, id="cards-container", cls="flex flex-wrap gap-2" if small else "flex flex-wrap gap-4")
    
    def render_cart(self, session_id: str):
        """Render cart items with total price."""
        self.initialize_session(session_id)
        
        if not self.cart_storage[session_id]:
            return Div(id="cart-container", cls="flex flex-wrap gap-3")
        
        cards = [
            self.create_card_element(
                data['name'], 
                data['color'], 
                data['quantity'], 
                card_id, 
                data.get('price', 0.0) * data['quantity']  # Total price
            )
            for card_id, data in self.cart_storage[session_id].items()
        ]
        return Div(*cards, id="cart-container", cls="flex flex-wrap gap-3")

card_manager = CardManager()

@routes("/")
def index():
    # Initialize cards with default inventory
    session_id = "default"
    card_manager.initialize_session(session_id)
    initial_cards = card_manager.render_all_cards(session_id, small=True)
    
    return Div(
        Div(
            H3("Available Items", cls="text-lg font-semibold mb-2 text-gray-700"),
            initial_cards,
            cls="px-4 py-3 bg-white border-b-2 border-gray-200"
        ),
        Div(
            H1("Hello, Customer!", 
               cls="text-6xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4"),
            P("This is a modern e-commerce application helper to make your shopping easier", 
              cls="text-xl text-gray-600 mb-8"),
            cls="text-center",
            id="welcome"
        ),
        Div(id="messages", cls="flex-1 overflow-y-auto px-6 py-4 space-y-4 hidden"),
        Div(
            H3("Your Cart", cls="text-lg font-semibold mb-2 text-gray-700"),
            Div(id="cart-container", cls="flex flex-wrap gap-3"),
            cls="px-4 py-3 bg-white border-t-2 border-gray-200"
        ),
        Form(
            Input(id="msg", name="msg", placeholder="Type your message...", autofocus=True, 
                  cls="flex-1 border-2 border-gray-300 focus:border-blue-500 focus:outline-none px-4 rounded-lg text-lg h-14"),
            Button("Send", 
                   cls="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 h-14 flex items-center justify-center"),
            id="form",
            cls="fixed bottom-0 left-0 right-0 bg-white shadow-2xl border-t-2 border-gray-200 p-6 flex gap-3 items-center",
            hx_post="/send",
            hx_target="#response",
            hx_swap="beforeend",
            hx_on__after_request="if(document.getElementById('welcome')) document.getElementById('welcome').classList.add('hidden'); this.reset();"
        ),
        Div(id="response", cls="flex-1 overflow-y-auto px-6 py-4 space-y-4"),
        cls="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-gray-100 pb-24"
    )

@routes('/send')
async def post(msg: str, session_id: str = "default"):
    if session_id not in message_histories:
        message_histories[session_id] = []
    
    card_manager.initialize_session(session_id)
    response = await agent.run(msg, message_history=message_histories[session_id])
    new_messages = response.new_messages()
    message_histories[session_id] = response.all_messages()
    
    # Process card operations (always render to show updated inventory)
    cards_updated = False
    error_message = None
    for message in new_messages:
        if hasattr(message, 'parts'):
            for part in message.parts:
                if hasattr(part, 'tool_name') and hasattr(part, 'args'):
                    
                    if part.tool_name == 'add_card':
                        result = card_manager.add_card(
                            session_id,
                            part.args.get('name', ''),
                            part.args.get('color', ''),
                            part.args.get('quantity', 1)
                        )
                        if result:  # Error message returned
                            error_message = result
                        else:
                            cards_updated = True
                    
                    elif part.tool_name == 'remove_card':
                        card_manager.remove_card(
                            session_id,
                            part.args.get('name', ''),
                            part.args.get('quantity', 1),
                            part.args.get('remove_all', False)
                        )
                        cards_updated = True
                    
                    elif part.tool_name == 'update_card':
                        card_manager.update_card(
                            session_id,
                            part.args.get('name', ''),
                            part.args.get('new_color'),
                            part.args.get('new_quantity')
                        )
                        cards_updated = True
    
    inventory_html = card_manager.render_all_cards(session_id, small=True) if cards_updated else ""
    cart_html = card_manager.render_cart(session_id) if cards_updated else ""
    
    # Prepare response output
    bot_response = error_message if error_message else response.output
    response_color = "bg-red-100 text-red-800" if error_message else "bg-gray-200 text-gray-800"
    
    chat_bubbles = Div(
        Div(Div(msg, cls="bg-blue-600 text-white px-4 py-3 rounded-lg rounded-tr-none max-w-md shadow-md"), cls="flex justify-end mb-2"),
        Div(Div(bot_response, cls=f"{response_color} px-4 py-3 rounded-lg rounded-tl-none max-w-md shadow-md"), cls="flex justify-start mb-4")
    )
    
    if inventory_html and cart_html:
        inventory_html.attrs['hx-swap-oob'] = 'outerHTML'
        cart_html.attrs['hx-swap-oob'] = 'outerHTML'
        return Div(chat_bubbles, inventory_html, cart_html)
    return chat_bubbles

serve(port=1234)