from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List
import asyncio  
import os
import logfire
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv(override=True)
logfire.configure()
logfire.instrument_pydantic_ai()

os.environ["GOOGLE_API_KEY"] = "AIzaSyCwo_fdDi7rJpPeqy9EMSMnIKvFrnG1eik"

SERP_API_KEY = os.getenv("SERP_API_KEY")

system_prompt = """
You are a Research Agent specialized in gathering, analyzing, and presenting factual information.

IMPORTANT: You MUST respond with structured data containing:
- summary: A concise summary of your research findings
- sources: A list of URLs or source names you used
- key_points: A list of 3-5 main findings or important facts
- confidence: Either "high", "medium", or "low" based on source reliability
- raw_text: The complete detailed research information

PRIMARY ROLE:
- Conduct thorough research using available tools.
- Produce structured, verifiable, and well-sourced summaries.
- Maintain high standards of accuracy, transparency, and methodological rigor.

RESEARCH METHODOLOGY:
- Always use tools for external knowledge. Never rely solely on internal model knowledge for current or factual information.
- Break complex queries into smaller, focused research tasks.
- Cross-reference information across at least 2-3 independent sources when possible.
- Prioritize primary and authoritative sources (government, academic, institutional, reputable news organizations).
- Search for the most recent, up-to-date information.

TOOL USAGE:
- Use search_web() for discovering current information and locating diverse sources.
- Use extract_content() to analyze specific documents, articles, or web pages.
- Use fact_check() to verify claims across multiple sources.
- Prefer tool calls over internal reasoning when external data is required.
- If a tool fails or lacks sufficient information, state the limitation clearly—never guess or fabricate.

SOURCE EVALUATION:
- Assess credibility (official/government sources > academic > established media > independent blogs).
- Check publication dates for relevance and potential outdatedness.
- Identify author bias, institutional incentives, or conflicts of interest.
- Distinguish verifiable facts, expert opinions, interpretations, and speculation.

OUTPUT REQUIREMENTS:
- Provide a concise summary in the 'summary' field
- List all sources used in the 'sources' field
- Extract 3-5 main findings or facts in the 'key_points' field
- Assign confidence level based on source quality and consensus
- Include complete research details in 'raw_text' field
- Cite sources explicitly with URLs when available

CONFIDENCE LEVELS:
- "high": Multiple authoritative sources agree, recent data, primary sources
- "medium": Some authoritative sources, minor inconsistencies, secondary sources
- "low": Limited sources, questionable reliability, outdated information

ERROR HANDLING:
- If the query is ambiguous, ask clarifying questions before proceeding.
- State clearly when information is unavailable, unverifiable, or contradictory.
- Never hallucinate or infer information without evidence.
- Acknowledge any limitations of tools, data availability, or domain expertise.

TOOL-CALL BEHAVIOR:
- When external data is required, respond with a tool call using the proper format.
- Avoid answering with internal knowledge if a tool is more appropriate.
- Combine multiple tool outputs into a unified, well-structured final answer.

Your goal is to provide reliable, verifiable, and transparent research that the user can independently confirm.
Your final output MUST follow the ResearchOutput schema exactly.
Use the results from the tools to populate each field.
"""

class ResearchOutput(BaseModel):
    summary: str
    sources: List[str]
    key_points: List[str]
    confidence: str  # "high", "medium", "low"
    raw_text: str = ""  # Full research text for reference

model = "google-gla:gemini-2.5-flash"
agent = Agent[None, ResearchOutput](
    model=model,
    system_prompt=system_prompt
)

@agent.tool_plain
async def search_web(query: str) -> str:
    print("[TOOL LOG] Searching the web for:", query)
    logfire.info("search_web called", query=query)
    """Search the web for current information on the given query using SerpAPI."""
    
    try:
        # Use SerpAPI for real Google search results
        print("[DEBUG] Using SerpAPI for Google search")
        search_params = {
            "q": query,
            "api_key": SERP_API_KEY,
            "num": 5,  # Get top 5 results
            "gl": "us",  # Country
            "hl": "en"   # Language
        }
        
        search = GoogleSearch(search_params)
        results = search.get_dict()
        
        # Extract and format search results
        result_parts = []
        
        # Check for direct answer box
        if "answer_box" in results:
            answer_box = results["answer_box"]
            if "answer" in answer_box:
                result_parts.append(f"Direct Answer: {answer_box['answer']}")
            elif "snippet" in answer_box:
                result_parts.append(f"Answer Box: {answer_box['snippet']}")
        
        # Check for knowledge graph
        if "knowledge_graph" in results:
            kg = results["knowledge_graph"]
            if "description" in kg:
                result_parts.append(f"Knowledge Graph: {kg['description']}")
        
        # Extract organic search results
        if "organic_results" in results:
            organic_results = []
            for result in results["organic_results"][:3]:  # Top 3 results
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                link = result.get("link", "")
                
                if title and snippet:
                    organic_results.append(f"• {title}\n  {snippet}\n  Source: {link}")
            
            if organic_results:
                result_parts.append("Search Results:\n" + "\n\n".join(organic_results))
        
        # Check for related questions
        if "related_questions" in results:
            questions = [q.get("question", "") for q in results["related_questions"][:2]]
            if questions:
                result_parts.append(f"Related Questions: {'; '.join(questions)}")
        
        if result_parts:
            return "\n\n".join(result_parts)
        else:
            return f"Search completed for '{query}' but no detailed results found. Please try different search terms."
            
    except Exception as e:
        logfire.error("search_web error", error=str(e))
        print(f"[DEBUG] Search exception: {e}")
        return f"Search error occurred: {str(e)}. Please try again with a different query."

@agent.tool_plain
async def extract_content(url: str) -> str:
    print("[TOOL LOG] Extracting content from:", url)
    logfire.info("extract_content called", url=url)
    """Extract content from the given URL using SerpAPI."""
    
    try:
        if SERP_API_KEY:
            print("[DEBUG] Using SerpAPI for content extraction")
            
            # Search for the specific URL to get its content
            search_params = {
                "q": f'"{url}"',
                "api_key": SERP_API_KEY,
                "num": 3
            }
            
            search = GoogleSearch(search_params)
            results = search.get_dict()
            
            if "organic_results" in results:
                for result in results["organic_results"]:
                    if url in result.get("link", ""):
                        title = result.get("title", "")
                        snippet = result.get("snippet", "")
                        if title and snippet:
                            return f"Page Title: {title}\n\nContent Summary: {snippet}\n\nSource: {url}"
            
            # If exact URL not found, try domain search
            domain = url.split("/")[2]
            fallback_params = {
                "q": f'site:{domain}',
                "api_key": SERP_API_KEY,
                "num": 2
            }
            
            fallback_search = GoogleSearch(fallback_params)
            fallback_results = fallback_search.get_dict()
            
            if "organic_results" in fallback_results and fallback_results["organic_results"]:
                result = fallback_results["organic_results"][0]
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                if title and snippet:
                    return f"Related Page: {title}\n\nContent: {snippet}\n\nNote: Exact URL content not found, showing related content from {domain}"
            
            return f"No content could be extracted from {url}"
        else:
            return f"SerpAPI key not configured. Cannot extract content from {url}"
                    
    except Exception as e:
        logfire.error("extract_content error", error=str(e), url=url)
        return f"Error extracting content from {url}: {str(e)}"

@agent.tool_plain
async def fact_check(claim: str) -> str:
    print("[TOOL LOG] Fact-checking claim:", claim)
    logfire.info("fact_check called", claim=claim)
    """Fact-check the given claim using multiple sources and verification strategies."""
    
    try:
        result_parts = []
        
        if SERP_API_KEY:
            print("[DEBUG] Using SerpAPI for comprehensive fact-checking")
            
            # Strategy 1: Search for fact-checking websites
            fact_check_queries = [
                f'"{claim}" site:snopes.com OR site:factcheck.org OR site:politifact.com',
                f'fact check "{claim}"',
                f'"{claim}" debunked OR verified OR false OR true'
            ]
            
            for i, query in enumerate(fact_check_queries, 1):
                try:
                    search_params = {
                        "q": query,
                        "api_key": SERP_API_KEY,
                        "num": 3,
                        "gl": "us",
                        "hl": "en"
                    }
                    
                    search = GoogleSearch(search_params)
                    results = search.get_dict()
                    
                    if "organic_results" in results and results["organic_results"]:
                        strategy_results = []
                        for result in results["organic_results"][:2]:
                            title = result.get("title", "")
                            snippet = result.get("snippet", "")
                            link = result.get("link", "")
                            
                            if title and snippet:
                                # Determine credibility based on domain
                                domain = link.split('/')[2] if '/' in link else link
                                credibility = "HIGH" if any(trusted in domain.lower() for trusted in 
                                    ['snopes.com', 'factcheck.org', 'politifact.com', 'reuters.com', 'bbc.com', 'gov']) else "MEDIUM"
                                
                                strategy_results.append(f"  • {title}\n    {snippet}\n    Source: {link} (Credibility: {credibility})")
                        
                        if strategy_results:
                            result_parts.append(f"Verification Strategy {i}:\n" + "\n\n".join(strategy_results))
                            
                    await asyncio.sleep(0.1)  # Rate limiting
                    
                except Exception as e:
                    print(f"[DEBUG] Fact-check strategy {i} failed: {e}")
                    continue
            
            # Strategy 2: Search for contradicting information
            try:
                contradiction_query = f'"{claim}" NOT true OR false OR incorrect OR myth'
                search_params = {
                    "q": contradiction_query,
                    "api_key": SERP_API_KEY,
                    "num": 2
                }
                
                search = GoogleSearch(search_params)
                results = search.get_dict()
                
                if "organic_results" in results and results["organic_results"]:
                    contradiction_results = []
                    for result in results["organic_results"]:
                        title = result.get("title", "")
                        snippet = result.get("snippet", "")
                        link = result.get("link", "")
                        
                        if title and snippet:
                            contradiction_results.append(f"  • {title}\n    {snippet}\n    Source: {link}")
                    
                    if contradiction_results:
                        result_parts.append("Potential Contradictions Found:\n" + "\n\n".join(contradiction_results))
            
            except Exception as e:
                print(f"[DEBUG] Contradiction search failed: {e}")
        
        else:
            # Fallback to basic search if no SerpAPI
            print("[DEBUG] Using basic search for fact-checking")
            search_query = f"fact check verify: {claim}"
            search_results = await search_web(search_query)
            result_parts.append(f"Basic Fact-Check Results:\n{search_results}")
        
        # Compile final response
        if result_parts:
            confidence_note = "\n\nCONFIDENCE ASSESSMENT:\n"
            confidence_note += "- HIGH: Information from established fact-checking organizations\n"
            confidence_note += "- MEDIUM: Information from reputable news sources\n"
            confidence_note += "- LOW: Information from unverified or biased sources\n\n"
            confidence_note += "RECOMMENDATION: Cross-reference these findings with multiple authoritative sources before making decisions."
            
            return f"FACT-CHECK ANALYSIS FOR: '{claim}'\n\n" + "\n\n".join(result_parts) + confidence_note
        else:
            return f"Fact-check for '{claim}': No specific verification results found. Please verify this claim through authoritative fact-checking websites or primary sources."
    
    except Exception as e:
        logfire.error("fact_check error", error=str(e), claim=claim)
        return f"Error during fact-checking: {str(e)}. Please try again or verify the claim manually through trusted sources."

async def main():
    message_history = []
    while True:
        message = input("You: ")
        if message.upper() in ["EXIT", "QUIT"]:
            break
        
        response = await agent.run(message, message_history=message_history)
        
        # Display structured output if available
        if hasattr(response, 'data') and response.data:
            print("\n📌 STRUCTURED OUTPUT")
            print("-" * 50)
            print(f"📋 Summary: {response.data.summary}")
            print(f"🎯 Confidence: {response.data.confidence.upper()}")
            print(f"📚 Sources ({len(response.data.sources)}): {', '.join(response.data.sources) if response.data.sources else 'None provided'}")
            
            # Display key points
            if response.data.key_points:
                print(f"🔑 Key Points ({len(response.data.key_points)}):")
                for i, point in enumerate(response.data.key_points, 1):
                    print(f"   {i}. {point}")
            else:
                print("🔑 Key Points: None provided")
            
            # Show first 300 characters of raw text
            if response.data.raw_text:
                raw_preview = response.data.raw_text[:300]
                if len(response.data.raw_text) > 300:
                    raw_preview += "..."
                print(f"📄 Raw Text Preview: {raw_preview}\n")
            
            print("-" * 50)
        else:
            # Fallback to regular output if structured data not available
            print("Agent: ", response.output)

        message_history = response.all_messages()

asyncio.run(main())