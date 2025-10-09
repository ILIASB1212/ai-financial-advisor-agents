# google_search_tool.py (FINAL CORRECT VERSION for TypeError)

from pydantic import BaseModel, Field
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from crewai.tools import tool # Confirmed: This import works in your environment

# **IMPORTANT: This CX ID will be used for your Google Custom Search.**
CUSTOM_SEARCH_ENGINE_ID = "42389273c2ea947a1" 

# --------------------------------------------------------------------
# 1. Define the Tool Function using the @tool decorator
#    CRITICAL CHANGE: Removed 'args_schema=GoogleSearchInput'
# --------------------------------------------------------------------
@tool("Google Search Tool") 
def google_search_tool_function(query: str) -> str:
    """A general web search tool to find recent news, sentiment, and broad market trends for any query."""
    
    # CRITICAL FIX: The input schema must be defined as a NESTED class 
    # for the @tool decorator to automatically recognize it in this syntax.
    class GoogleSearchToolSchema(BaseModel):
        """Input schema for the Google Search Tool."""
        query: str = Field(description="The search query to execute (e.g., 'latest market sentiment Consumer Staples 2025').")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "ERROR: GOOGLE_API_KEY is not set in environment variables."
        
    if CUSTOM_SEARCH_ENGINE_ID == "YOUR_CUSTOM_SEARCH_ID_HERE":
         return "ERROR: CUSTOM_SEARCH_ENGINE_ID (CX) is a placeholder. Please replace it with your actual ID."


    # --- 2. Initialize the Google Custom Search Service ---
    try:
        service = build("customsearch", "v1", developerKey=api_key)
    except Exception as e:
        return f"ERROR: Could not initialize Google Search service: {e}"

    # --- 3. Execute the Search and Retrieve Results ---
    try:
        result = service.cse().list(
            q=query,
            cx=CUSTOM_SEARCH_ENGINE_ID,
            num=5 # Number of results to return (max is 10)
        ).execute()
    
    except HttpError as e:
        return f"ERROR: Google Search API returned an HTTP error. Check daily quota (100 free per day). Error: {e}"
    except Exception as e:
        return f"ERROR: An unexpected error occurred during search execution: {e}"


    # --- 4. Format Output for the LLM Agent ---
    search_results_markdown = f"**Search Results for: '{query}'**\n"
    items = result.get('items', [])
    
    if not items:
        return f"Search for '{query}' returned no relevant results."

    for i, item in enumerate(items, 1):
        title = item.get('title', 'No Title')
        snippet = item.get('snippet', 'No Snippet')
        link = item.get('link', '#')
        
        # Formatting the result as a list of summaries
        search_results_markdown += (
            f"\n**{i}. {title}**\n"
            f"   *Snippet*: {snippet}\n"
            f"   *Source*: {link}\n"
        )
        
    # The agent receives this structured text, which it can summarize
    return (
        "General web search completed. The following relevant public articles and their summaries "
        "have been retrieved to provide context and current events:\n\n"
        f"{search_results_markdown}"
    )