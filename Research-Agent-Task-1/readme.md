# Research Agent — Intelligent Web Research with Pydantic-AI

This project implements an **Interactive Research Agent** using **Pydantic-AI** with real-time web search capabilities:

- **Live Web Search** using SerpAPI integration
- **Content Extraction** from web pages
- **Fact-Checking** across multiple sources
- **Structured Output** with confidence scoring
- **Interactive Chat Interface** with conversation history
- **Logfire Instrumentation** for monitoring and debugging
- **Source Attribution** and credibility assessment

This README explains installation, setup, API configuration, and how to run the interactive research agent.

---

## 📦 1. Project Setup

Create or clone your project folder:

```bash
git clone <your-repo-url>
cd your-project
```

---

## 🛠 2. Install Dependencies

Requires **Python 3.10+**

Install required packages:

```bash
pip install pydantic-ai google-serpapi logfire python-dotenv
```

**Key Dependencies:**
- `pydantic-ai` - AI agent framework with structured outputs
- `google-serpapi` - SerpAPI client for Google search integration
- `logfire` - Observability and monitoring
- `python-dotenv` - Environment variable management
---

## 🔧 3. API Keys & Environment Setup

### Required API Keys:

1. **SerpAPI Key** (Required for web search)
   - Sign up at [serpapi.com](https://serpapi.com/)
   - Get your API key from the dashboard

2. **Google AI API Key** (Required for Gemini model)
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create an API key

### Environment Configuration:

Create a `.env` file in the project root:

```env
SERP_API_KEY=your_serpapi_key_here
GOOGLE_API_KEY=your_google_ai_api_key_here
```

**⚠️ Important:** Without these API keys, the research agent cannot function. The web search and AI model require active API access.

The application loads environment variables using:
```python
from dotenv import load_dotenv
load_dotenv(override=True)
```

---

## 📘 4. Project Structure

```
Research-Agent-Task-1/
│── main.py              # Main application with interactive agent
│── readme.md           # This documentation
│── .env                # Environment variables (create this)
│── .gitignore          # Git ignore file (recommended)
```

**File Descriptions:**
- `main.py` - Contains the research agent, tools, and interactive chat interface
- `.env` - Stores your API keys (never commit to git)
- `readme.md` - Project documentation and setup instructions

---

## 🧩 5. Research Tools (Real Implementation)

### 🔍 `search_web(query: str)`
**Purpose:** Live Google search via SerpAPI
- Searches current web information using Google's search API
- Extracts multiple result types: direct answers, knowledge graphs, organic results
- Returns top 5 results with titles, snippets, and source URLs
- Includes related questions for comprehensive research
- **Error handling:** Graceful fallbacks and retry mechanisms

### 📄 `extract_content(url: str)`
**Purpose:** Extract and analyze webpage content
- Attempts to fetch content from specific URLs using SerpAPI
- Falls back to domain-level search if exact URL unavailable
- Returns structured content with titles, summaries, and source attribution
- **Credibility note:** Indicates when exact content isn't available

### ✔ `fact_check(claim: str)`
**Purpose:** Multi-source claim verification
- Searches fact-checking websites (Snopes, FactCheck.org, PolitiFact)
- Looks for contradictory information and debunking sources
- Assigns credibility ratings (HIGH/MEDIUM) based on source domains
- **Comprehensive approach:** Uses multiple verification strategies
- Provides detailed source analysis and confidence assessment

**Technical Implementation:**
- All tools use `@agent.tool_plain` decorator
- Integrated with Logfire for monitoring and debugging
- Rate-limited API calls to prevent quota exhaustion
- Structured error handling with fallback mechanisms

---

## 6. Structured Output Model

```python
from pydantic import BaseModel
from typing import List

class ResearchOutput(BaseModel):
    summary: str                    # Concise research summary
    sources: List[str]             # List of URLs and source names used
    key_points: List[str]          # 3-5 main findings or important facts
    confidence: str                # "high", "medium", or "low"
    raw_text: str = ""            # Complete detailed research information
```

**Field Descriptions:**
- **summary**: Concise overview of research findings
- **sources**: All URLs and source names referenced during research
- **key_points**: Bulleted list of 3-5 most important findings
- **confidence**: Quality assessment based on source reliability and consensus
- **raw_text**: Full detailed research data for reference

**Confidence Levels:**
- **"high"**: Multiple authoritative sources agree, recent data, primary sources
- **"medium"**: Some authoritative sources, minor inconsistencies, secondary sources  
- **"low"**: Limited sources, questionable reliability, outdated information

The agent **always** returns this structured format for consistent, parseable results.

---

## 🤖 7. Agent Configuration

### Core Setup:

```python
import asyncio
import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List

# Environment and monitoring setup
load_dotenv(override=True)
logfire.configure()
logfire.instrument_pydantic_ai()

# Model configuration
model = "google-gla:gemini-2.5-flash"

# Agent initialization
agent = Agent[None, ResearchOutput](
    model=model,
    system_prompt=system_prompt  # Detailed research methodology prompt
)
```

### Key Features:
- **Model**: Google Gemini 2.5 Flash via Google AI API
- **Monitoring**: Full Logfire instrumentation for debugging
- **Tools**: Three research tools registered with `@agent.tool_plain`
- **Output**: Structured `ResearchOutput` with confidence scoring
- **History**: Conversation memory for follow-up questions

---

## 8. Running the Interactive Agent

### Start the Research Agent:

```bash
python main.py
```

### Interactive Chat Interface:

The agent runs in an interactive loop where you can:
- Ask research questions
- Request fact-checking
- Get current information on any topic
- Build on previous conversations
- Type `EXIT` or `QUIT` to end the session

### Example Session:

```
You: What are the latest developments in quantum computing?

📌 STRUCTURED OUTPUT
--------------------------------------------------
📋 Summary: Recent breakthroughs in quantum computing include...
🎯 Confidence: HIGH
📚 Sources (3): nature.com, ibm.com/quantum, arxiv.org
🔑 Key Points (4):
   1. IBM achieved 1000+ qubit processor in 2023
   2. Google's quantum error correction milestone
   3. New quantum algorithms for optimization
   4. Commercial applications in drug discovery
📄 Raw Text Preview: Quantum computing has seen significant...
--------------------------------------------------

You: Can you fact-check the IBM claim?
```

### Output Format:
Each response includes:
- **Structured Summary** with key findings
- **Source Attribution** with URLs
- **Confidence Rating** based on source quality
- **Key Points** in bulleted format
- **Raw Research Data** preview

---

## 🧪 9. Example Research Questions

These questions showcase the agent's research capabilities:

### **Current Events & News:**
- "What are the latest developments in AI safety research?"
- "What's happening with climate change negotiations in 2024?"
- "Recent breakthroughs in renewable energy technology"

### **Fact-Checking:**
- "Fact-check: Does drinking 8 glasses of water daily improve health?"
- "Verify the claim that electric cars are better for the environment"
- "Is it true that humans only use 10% of their brain?"

### **Technical Research:**
- "Compare the latest smartphone processors from Apple and Qualcomm"
- "What are the pros and cons of different cloud storage providers?"
- "Explain quantum computing and its current limitations"

### **Market & Business:**
- "What's the current state of the cryptocurrency market?"
- "Research the impact of remote work on productivity"
- "Latest trends in sustainable investing"

Each question triggers:
- ✅ Live web search
- ✅ Multi-source verification
- ✅ Structured output with confidence scoring
- ✅ Source attribution
- ✅ Live web search
- ✅ Multi-source verification
- ✅ Structured output with confidence scoring
- ✅ Source attribution

---

## 🔧 10. Troubleshooting

### Common Issues:

**"Search error occurred"**
- Check your `SERP_API_KEY` in the `.env` file
- Verify your SerpAPI account has remaining credits
- Ensure internet connectivity

**"Model authentication failed"**
- Verify your `GOOGLE_API_KEY` is correct
- Check Google AI Studio for API key status
- Ensure the key has proper permissions

**"No structured output"**
- The agent always returns structured data
- Check for error messages in the console
- Review Logfire logs for debugging information

### Rate Limiting:
- SerpAPI has monthly query limits based on your plan
- The agent includes rate limiting (0.1s delays) to prevent quota exhaustion
- Monitor your API usage through SerpAPI dashboard

---

## 📊 11. Monitoring & Debugging

### Logfire Integration:
```python
logfire.configure()                    # Enable monitoring
logfire.instrument_pydantic_ai()       # Track AI interactions
```

**What gets logged:**
- Tool calls and responses
- Search queries and results
- Error conditions and exceptions
- Agent response times

### Console Output:
- `[TOOL LOG]` - Shows which tools are being called
- `[DEBUG]` - Detailed information for troubleshooting
- Error messages with specific failure reasons

---

## ⚠️ 12. Limitations & Considerations

### API Dependencies:
- **SerpAPI Required**: No fallback for web search without API key
- **Google AI Required**: Agent cannot function without Gemini access
- **Rate Limits**: Monthly query quotas on both APIs

### Data Quality:
- **Source Reliability**: Agent assesses credibility but cannot guarantee accuracy
- **Real-time Data**: Search results reflect current web content
- **Language**: Optimized for English-language sources

### Technical Constraints:
- **Memory**: Conversation history grows with session length
- **Network**: Requires stable internet for API calls
- **Processing**: Complex research queries may take 10-30 seconds

### Best Practices:
- Always verify critical information through primary sources
- Use fact-checking for important claims
- Consider source credibility ratings in decision-making
- Monitor API usage to avoid quota exhaustion

---