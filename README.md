# 🤖 Pydantic AI Agents Assignment

This repository contains two sophisticated AI-powered applications built using **Pydantic AI** and **Google's Gemini 2.5 Flash** model, demonstrating advanced agent capabilities with real-time web integration and stateful conversational interfaces.

## 📁 Project Structure

```
pydantic-ai-assignment/
├── Research-Agent-Task-1/          # Task 1: Web Research Agent
│   ├── agent.py                    # Research agent with SerpAPI integration
│   └── readme.md                   # Detailed task documentation
│
├── State-aware-UI-agent-Task-2/    # Task 2: E-Commerce Shopping Assistant
│   ├── main.py                     # Agent logic with cart management tools
│   ├── ui.py                       # FastHTML web interface
│   └── __pycache__/                # Python cache files
│
└── README.md                       # This file
```

---

## 🔍 Task 1: Research Agent with Live Web Search

An **intelligent research assistant** that performs live web searches, extracts content, fact-checks claims, and provides structured, sourced outputs with confidence ratings.

### 🎯 Key Features

- **🌐 Live Web Search**: Real-time Google search via SerpAPI integration
- **📄 Content Extraction**: Fetches and analyzes webpage content from URLs
- **✅ Multi-Source Fact-Checking**: Verifies claims across trusted sources (Snopes, FactCheck.org, PolitiFact)
- **📊 Structured Output**: Returns research with summary, key points, sources, and confidence scores
- **🔗 Source Attribution**: All findings include URLs and credibility ratings
- **💬 Interactive Chat**: Command-line interface with conversation history
- **📡 Logfire Monitoring**: Full observability and debugging instrumentation

### 🛠️ Tech Stack

- **Pydantic AI**: Agent framework with tool calling and structured outputs
- **Google Gemini 2.5 Flash**: LLM for natural language processing and analysis
- **SerpAPI**: Google search API integration for real-time web data
- **Logfire**: Observability, logging, and monitoring
- **Python-dotenv**: Environment variable management

### 📦 Installation

```bash
cd Research-Agent-Task-1
pip install pydantic-ai google-serpapi logfire python-dotenv
```

### 🔑 API Keys Required

Create a `.env` file in the `Research-Agent-Task-1` folder:

```env
SERP_API_KEY=your_serpapi_key_here
GOOGLE_API_KEY=your_google_ai_api_key_here
```

- **SerpAPI Key**: Sign up at [serpapi.com](https://serpapi.com/)
- **Google AI Key**: Get from [Google AI Studio](https://aistudio.google.com/apikey)

### 🚀 How to Run

```bash
python agent.py
```

Then ask research questions interactively. Type `EXIT` or `QUIT` to end the session.

### 💡 Example Queries

```
You: What are the latest developments in quantum computing?

📌 STRUCTURED OUTPUT
--------------------------------------------------
📋 Summary: Recent breakthroughs include IBM's 1000+ qubit processor...
🎯 Confidence: HIGH
📚 Sources (3): nature.com, ibm.com/quantum, arxiv.org
🔑 Key Points (4):
   1. IBM achieved 1000+ qubit processor in 2023
   2. Google's quantum error correction milestone
   3. New quantum algorithms for optimization
   4. Commercial applications in drug discovery
📄 Raw Text Preview: Quantum computing has seen significant...
--------------------------------------------------
```

**Other Example Queries:**
- "Fact-check: Does drinking 8 glasses of water daily improve health?"
- "What's the current state of renewable energy technology?"
- "Research the impact of AI on job markets"
- "Latest trends in cryptocurrency regulation"

### 📊 Research Output Schema

```python
class ResearchOutput(BaseModel):
    summary: str                    # Concise research summary
    sources: List[str]             # URLs and source names
    key_points: List[str]          # 3-5 main findings
    confidence: str                # "high", "medium", or "low"
    raw_text: str                  # Full research data
```

**Confidence Levels:**
- **High**: Multiple authoritative sources, recent data, primary sources
- **Medium**: Some authoritative sources, minor inconsistencies
- **Low**: Limited sources, questionable reliability, outdated info

### 🔧 Available Tools

1. **`search_web(query)`**: Live Google search with top 5 results, answer boxes, knowledge graphs
2. **`extract_content(url)`**: Extracts webpage content with titles and summaries
3. **`fact_check(claim)`**: Multi-source verification with credibility ratings

---

## 🛍️ Task 2: E-Commerce Shopping Assistant

A **modern web-based shopping assistant** with a ChatGPT-style interface that manages inventory, cart operations, and natural language shopping interactions.

### 🎯 Key Features

- **🗣️ Natural Language Shopping**: Add items using conversational commands
- **🛒 Smart Cart Management**: Add, remove, update items with real-time updates
- **📦 Inventory Tracking**: Live stock management with quantity limits
- **💰 Price Calculations**: Automatic total price computation
- **🔄 Session Persistence**: Cart and chat history preserved across refreshes (30-day cookies)
- **🎨 Modern UI**: Dark-themed, responsive ChatGPT-inspired interface
- **⚡ Real-time Updates**: HTMX for dynamic UI without page reloads
- **🔒 Input Locking**: Prevents duplicate submissions during processing
- **✨ Visual Feedback**: Typing indicators and smooth animations

### 🛠️ Tech Stack

- **Pydantic AI**: Agent framework with tool calling
- **FastHTML**: Modern Python web framework
- **Gemini 2.5 Flash**: Google's LLM for command understanding
- **HTMX**: Dynamic UI updates
- **Tailwind CSS**: Responsive styling
- **Logfire**: Monitoring and debugging

### 📦 Installation

```bash
cd State-aware-UI-agent-Task-2
pip install pydantic-ai python-fasthtml logfire python-dotenv
```

### 🔑 Environment Setup

Create a `.env` file in the `State-aware-UI-agent-Task-2` folder:

```env
GOOGLE_API_KEY=your_google_ai_api_key_here
```

### 🚀 How to Run

```bash
python ui.py
```

Then open your browser to `http://localhost:1234`

### 💡 Example Commands

**Adding Items:**
- "Add 2 apples to my cart"
- "Add 3 banana cards"
- "Add 1 orange card"

**Removing Items:**
- "Remove apple from cart"
- "Delete 2 bananas"
- "Remove all grapes"

**Updating Quantities:**
- "Update banana quantity to 5"
- "Change apple to 3"

**Stock Checking:**
- "What's available?"
- "Show me the inventory"

### 📦 Predefined Inventory

| Item   | Color  | Price (₹) | Initial Stock |
|--------|--------|-----------|---------------|
| Banana | Yellow | 50        | 4             |
| Apple  | Red    | 80        | 5             |
| Orange | Orange | 60        | 3             |
| Grape  | Purple | 120       | 6             |

### 🔧 Available Tools

1. **`add_card(name, color, quantity)`**: Adds items to cart, decreases inventory
2. **`remove_card(name, quantity, remove_all)`**: Removes items from cart, restores inventory
3. **`update_card(name, new_color, new_quantity)`**: Updates card properties

### 🎨 UI Components

- **Inventory Panel** (Top): Shows available items with prices and stock
- **Chat Interface** (Center): ChatGPT-style conversation view
- **Cart Panel** (Bottom): Real-time cart with total prices
- **Input Form** (Fixed Bottom): Message input with send button

### 🔄 State Management

- **Session-based Storage**: Each user gets unique session ID via cookies
- **In-memory Data**: Carts and message history stored per session
- **30-day Persistence**: Sessions expire after 30 days
- **Real-time Sync**: UI updates instantly on cart operations

---

## 🎯 Core Concepts Demonstrated

### 1. **Agent Tool Calling**
Both agents use `@agent.tool` and `@agent.tool_plain` decorators to register functions that the LLM can invoke dynamically based on user intent.

### 2. **Conversational Context**
Message history is maintained across interactions, enabling follow-up questions and context-aware responses.

### 3. **Structured Outputs**
Task 1 uses Pydantic models (`ResearchOutput`) for type-safe, consistent API responses.

### 4. **Session Management**
Task 2 implements per-user session storage using UUID-based cookies for cart and message persistence.

### 5. **Real-time Web Integration**
Task 1 demonstrates live API integration with SerpAPI for current, verifiable information.

### 6. **Error Handling**
Both applications gracefully handle API errors, quota limits, and edge cases.

### 7. **Observability**
Logfire integration provides full visibility into agent behavior, tool calls, and performance metrics.

---

## 📋 Setup Requirements

### System Requirements
- **Python**: 3.10 or higher
- **Internet**: Required for API calls
- **Browser**: Modern browser (Chrome, Firefox, Safari) for Task 2

### Install All Dependencies

```bash
# Core Pydantic AI
pip install pydantic-ai

# Task 1 Requirements
pip install google-serpapi logfire python-dotenv

# Task 2 Requirements
pip install python-fasthtml logfire python-dotenv
```

### Environment Variables

Both tasks require a `.env` file in their respective folders:

**Task 1 (Research-Agent-Task-1/.env):**
```env
SERP_API_KEY=your_serpapi_key_here
GOOGLE_API_KEY=your_google_ai_api_key_here
```

**Task 2 (State-aware-UI-agent-Task-2/.env):**
```env
GOOGLE_API_KEY=your_google_ai_api_key_here
```

---

## 🐛 Troubleshooting

### Common Issues

**"No module named 'pydantic_ai'"**
```bash
pip install pydantic-ai
```

**"Model authentication failed"**
- Verify your `GOOGLE_API_KEY` is correct in `.env`
- Check API key permissions at [Google AI Studio](https://aistudio.google.com/apikey)

**"Search error occurred" (Task 1)**
- Verify `SERP_API_KEY` in `.env`
- Check remaining credits at [SerpAPI Dashboard](https://serpapi.com/dashboard)

**"Session not persisting" (Task 2)**
- Ensure cookies are enabled in your browser
- Clear cache and reload if issues persist

**"Raw HTML showing instead of rendered page" (Task 2)**
- Ensure FastHTML is installed: `pip install python-fasthtml`
- Check that you're accessing `http://localhost:1234` not `file://`

### API Rate Limits

- **SerpAPI**: 100 searches/month on free plan
- **Google AI (Gemini)**: 15 requests/minute free tier
- Both agents include rate limiting to prevent quota exhaustion

---

## 📊 Monitoring & Debugging

### Logfire Integration

Both applications use Logfire for comprehensive observability:

```python
import logfire
logfire.configure()
logfire.instrument_pydantic_ai()
```

**What Gets Logged:**
- Tool invocations with parameters
- API request/response cycles
- Error conditions and stack traces
- Agent response times
- Message history flow

**Access Logs:**
- Console output during runtime
- Logfire dashboard (if configured with account)
- `.logfire/` directory in each task folder

### Console Output

- `[TOOL LOG]` - Tool call notifications
- `[DEBUG]` - Detailed debugging information
- Error messages with specific failure reasons

---

## 🚀 Future Enhancements

### Task 1 (Research Agent)
- PDF/Document analysis capabilities
- Academic paper search (arXiv, Google Scholar)
- Citation formatting (APA, MLA, Chicago)
- Export results to markdown/PDF
- Multi-language support
- Comparative analysis across multiple topics

### Task 2 (E-Commerce)
- Database persistence (PostgreSQL/SQLite)
- User authentication and profiles
- Payment gateway integration (Stripe, Razorpay)
- Order history and tracking
- Product recommendations using embeddings
- Search and filtering capabilities
- Wishlist functionality
- Multi-language support

---

## ⚠️ Important Notes

### Task 1 - Research Agent
- Requires active internet for web searches
- API keys must have sufficient credits/quota
- Search results reflect current web content (may vary)
- Always verify critical information through primary sources
- Fact-checking provides guidance but not absolute certainty

### Task 2 - Shopping Assistant
- Uses in-memory storage (data resets on server restart)
- Sessions expire after 30 days or when cookies cleared
- Cart operations validate against inventory stock
- Each browser/user gets unique session ID
- Not suitable for production without database backend

### Security Considerations
- **Never commit `.env` files** to version control
- API keys should be kept private and rotated regularly
- Consider adding `.env` to `.gitignore`
- Use environment-specific configurations for production

---

## 📚 Additional Resources

### Documentation
- [Pydantic AI Docs](https://ai.pydantic.dev/)
- [Google Gemini API Docs](https://ai.google.dev/)
- [SerpAPI Documentation](https://serpapi.com/docs)
- [FastHTML Guide](https://docs.fastht.ml/)
- [Logfire Documentation](https://logfire.pydantic.dev/)

### API Keys
- [Google AI Studio](https://aistudio.google.com/apikey) - Get Gemini API key
- [SerpAPI](https://serpapi.com/) - Sign up for search API access

### Learning Resources
- [Pydantic AI Examples](https://github.com/pydantic/pydantic-ai/tree/main/examples)
- [HTMX Documentation](https://htmx.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/feature-name`)
3. Commit your changes (`git commit -m 'Add feature name'`)
4. Push to the branch (`git push origin feature/feature-name`)
5. Open a Pull Request

---

## 📝 License

This project is created for educational purposes as part of a Pydantic AI assignment.

---

## 👤 Author

**Surya Kumar Divami**
- GitHub: [@suryakumardivami](https://github.com/suryakumardivami)
- Repository: [pydantic-ai-assignment](https://github.com/suryakumardivami/pydantic-ai-assignment)

## 📧 Support

If you encounter issues or have questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review task-specific README files in each folder
3. Open an issue on GitHub
4. Check API provider status pages

---

**Last Updated**: November 2025
