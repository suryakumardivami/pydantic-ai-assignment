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
                Div(
                    H4(name.title(), cls="text-xs font-bold text-gray-900 mb-1"),
                    Div(
                        P(f"₹{price:.0f}", cls="text-lg font-extrabold text-gray-900"),
                        P(f"Stock: {quantity}", cls="text-xs font-medium text-gray-700 mt-0.5"),
                        cls="text-center"
                    ),
                    cls="flex flex-col items-center justify-center h-full"
                ),
                cls=f"{color_class} rounded-xl shadow-md hover:shadow-xl transition-shadow duration-300 w-28 h-28 p-3 border-2 border-white",
                id=f"card-{card_id}"
            )
        return Div(
            Div(
                H3(name.title(), cls="text-2xl font-bold text-gray-900 mb-2"),
                Div(
                    P(f"₹{price:.0f}", cls="text-3xl font-extrabold text-gray-900"),
                    P(f"Qty: {quantity}", cls="text-base font-semibold text-gray-700 mt-2"),
                    cls="text-center"
                ),
                cls="flex flex-col items-center justify-center h-full"
            ),
            cls=f"{color_class} rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 w-44 h-44 p-5 border-4 border-white",
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
        # Header
        Div(
            H1("🛒 Smart Shopping Assistant", 
               cls="text-2xl font-bold text-white mb-1"),
            P("Your AI-powered shopping companion", 
              cls="text-sm text-blue-100"),
            cls="bg-gradient-to-r from-blue-600 via-blue-700 to-indigo-700 px-8 py-3 shadow-xl"
        ),
        
        # Available Items Section - Full Width
        Div(
            Div(
                Div(
                    H2("🏪 Available Items", cls="text-2xl font-bold text-gray-800 mb-1"),
                    P("Select items to add to your cart", cls="text-sm text-gray-600"),
                    cls="mb-4 text-center"
                ),
                Div(
                    initial_cards,
                    cls="flex justify-center"
                ),
                cls="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
            ),
            cls="px-8 py-6"
        ),
        
        # Split Layout - Chat and Cart Side by Side
        Div(
            # Left Side - Chat Section (Half)
            Div(
                # Welcome Message
                Div(
                    Div(
                        H2("👋 Welcome!", cls="text-2xl font-bold text-gray-800 mb-2"),
                        P("Ask me to add items to your cart, remove items, or update quantities!", 
                          cls="text-base text-gray-600 mb-1"),
                        P("Examples: 'Add 2 bananas', 'Remove 1 apple'",
                          cls="text-sm text-gray-500 italic"),
                        cls="text-center"
                    ),
                    id="welcome",
                    cls="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 mb-4 shadow-md border border-blue-100"
                ),
                
                # Chat Messages
                Div(id="response", cls="space-y-3"),
                
                cls="flex-1 overflow-y-auto px-4"
            ),
            
            # Right Side - Shopping Cart Section (Half)
            Div(
                Div(
                    Div(
                        H2("🛍️ Your Cart", cls="text-2xl font-bold text-gray-800 mb-1"),
                        P("Items ready for checkout", cls="text-sm text-gray-600"),
                        cls="mb-4"
                    ),
                    Div(id="cart-container", cls="flex flex-wrap gap-4 min-h-[100px]"),
                    cls="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
                ),
                cls="flex-1 overflow-y-auto px-4"
            ),
            
            cls="flex gap-4 px-4 mb-32 flex-1 overflow-hidden"
        ),
        
        # Fixed Input Form
        Form(
            Div(
                Input(
                    id="msg", 
                    name="msg", 
                    placeholder="💬 Type your message here... (e.g., 'Add 3 bananas to cart')", 
                    autofocus=True, 
                    cls="flex-1 border-2 border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none px-6 py-4 rounded-xl text-lg shadow-sm"
                ),
                Button(
                    "Send ✨", 
                    cls="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold px-10 py-4 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
                ),
                cls="flex gap-4 items-center max-w-5xl mx-auto"
            ),
            id="form",
            cls="fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-sm shadow-2xl border-t-2 border-gray-200 px-8 py-6",
            hx_post="/send",
            hx_target="#response",
            hx_swap="beforeend",
            hx_on__after_request="if(document.getElementById('welcome')) document.getElementById('welcome').classList.add('hidden'); this.reset();"
        ),
        
        cls="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50"
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
    response_color = "bg-red-50 border-l-4 border-red-500 text-red-800" if error_message else "bg-white border-l-4 border-blue-500 text-gray-800"
    
    chat_bubbles = Div(
        Div(
            Div(msg, cls="bg-gradient-to-r from-blue-600 to-blue-500 text-white px-6 py-3 rounded-2xl rounded-tr-sm shadow-lg max-w-xl"),
            cls="flex justify-end mb-3"
        ),
        Div(
            Div(bot_response, cls=f"{response_color} px-6 py-3 rounded-2xl rounded-tl-sm shadow-md max-w-xl"),
            cls="flex justify-start"
        )
    )
    
    if inventory_html and cart_html:
        inventory_html.attrs['hx-swap-oob'] = 'outerHTML'
        cart_html.attrs['hx-swap-oob'] = 'outerHTML'
        return Div(chat_bubbles, inventory_html, cart_html)
    return chat_bubbles

serve(port=1234)