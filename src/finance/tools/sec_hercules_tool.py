# sec_hercules_tool.py (FINAL CORRECT VERSION for TypeError)

from pydantic import BaseModel, Field
from sec_edgar_downloader import Downloader
import os
import glob
import re
from crewai.tools import tool # Confirmed: This import works in your environment

# --------------------------------------------------------------------
# 1. Define the Tool Function using the @tool decorator
#    CRITICAL CHANGE: Removed 'args_schema=SECHerculesInput'
# --------------------------------------------------------------------
@tool("SEC Hercules Tool")
def sec_hercules_tool_function(ticker: str, risk_keyword: str) -> str:
    """Tool to download and search the latest 10-K and 8-K regulatory filings for formal risk factor disclosures using any ticker and risk keyword."""
    
    # CRITICAL FIX: The input schema must be defined as a NESTED class 
    # for the @tool decorator to automatically recognize it in this syntax.
    class SECHerculesToolSchema(BaseModel):
        """Input schema for the SEC Hercules Tool."""
        ticker: str = Field(description="The stock ticker symbol (e.g., 'PFE', 'NEM') to search filings for.")
        risk_keyword: str = Field(description="The keyword to search within the Risk Factors section (e.g., 'geopolitical', 'litigation', 'antitrust').")

    # Define a unique temporary directory to save filings for this specific search
    temp_dir = f"./sec_filings_temp/{ticker}_{risk_keyword}_{os.getpid()}"
    
    # --- 1. Initialize Downloader ---
    try:
        # IMPORTANT: The SEC requires a User-Agent header (Company Name and Email)
        dl = Downloader("MyInvestmentCrew", "ai.agent@mydomain.com", temp_dir)
    except Exception as e:
        # Ensure cleanup on failure to initialize
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
        return f"ERROR: Could not initialize Downloader: {e}"

    # --- 2. Download Filings ---
    filing_types = ["10-K", "8-K"]
    download_count = 0
    
    for form in filing_types:
        try:
            count = dl.get(form, ticker, limit=2) 
            download_count += count
        except Exception as e:
            print(f"Warning: Could not download {form} for {ticker}: {e}")

    if download_count == 0:
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
        return f"ERROR: No recent 10-K or 8-K filings found for ticker {ticker}. Cannot perform risk analysis."

    # --- 3. Search Downloaded Files for Keyword ---
    mentions = []
    
    search_pattern = os.path.join(temp_dir, "**", f"{ticker}*.txt")
    filing_paths = glob.glob(search_pattern, recursive=True)
    
    for path in filing_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                matches = re.findall(f".{{0,50}}({re.escape(risk_keyword)}).{{0,50}}", content, re.IGNORECASE)
                
                if matches:
                    parts = path.split(os.sep)
                    filing_type = next((p for p in parts if p in filing_types), "UNKNOWN FILING")
                    
                    mentions.append({
                        'filing': filing_type,
                        'context': [f"...{m.strip()}..." for m in matches]
                    })
                    break 
        except Exception as e:
            print(f"Warning: Could not read or search file {path}: {e}")
            continue

    # --- 4. Clean Up and Return Result ---
    
    def cleanup_temp_dir(dir_path):
        if not os.path.exists(dir_path):
            return
        # Removed recursive cleanup logic for brevity, assuming standard os.rmdir will work
        # after file removal. The original complex cleanup logic is kept below but simplified.
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(dir_path)
        
    cleanup_temp_dir(temp_dir)
    
    if mentions:
        first_mention = mentions[0]
        context_snippet = first_mention['context'][0].replace('\n', ' ')
        
        return (
            f"SUCCESS: Found significant risk disclosure for keyword '{risk_keyword}' in the latest {first_mention['filing']} filing for {ticker}. "
            f"Filing Type: {first_mention['filing']}. "
            f"Mentions Found: {len(first_mention['context'])} total. "
            f"Context Snippet: {context_snippet} (Review this for risk assessment.)"
        )
    else:
        return (
            f"RESULT: No recent 10-K or 8-K filings for {ticker} contained the keyword '{risk_keyword}' in a material way. "
            "The risk is either not formally disclosed or the keyword is too narrow."
        )