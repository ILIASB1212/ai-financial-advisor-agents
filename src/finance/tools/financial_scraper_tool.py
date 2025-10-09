# financial_scraper_tool.py (FINAL CORRECT VERSION)

from pydantic import BaseModel, Field
from crewai.tools import tool # Confirmed: This import works in your environment
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.foreignexchange import ForeignExchange
import json
import os
from typing import Type # Not needed, but harmless if kept

# API Key setup: Assuming environment variable is set.
# os.environ["AV_API_KEY"] = os.getenv("AV_API_KEY") 

# --------------------------------------------------------------------
# 1. Define the Tool Function using the @tool decorator
#    CRITICAL CHANGE: Removed 'args_schema' from the decorator call.
# --------------------------------------------------------------------
@tool("Alpha Vantage Financial Tool") 
def financial_scraper_tool_function(ticker: str, data_point: str) -> str:
    """A tool to retrieve specific supplementary financial data points 
    like current price, volume, or technical indicators using Alpha Vantage."""
    
    # CRITICAL FIX: The input schema must be defined as a NESTED class 
    # for the @tool decorator to automatically recognize it in this syntax.
    class FinancialScraperToolSchema(BaseModel):
        ticker: str = Field(description="The stock ticker symbol (e.g., 'PG', 'UNH') to retrieve data for.")
        data_point: str = Field(description="The specific data point to retrieve (e.g., 'price', 'volume', '50day SMA').")

    # Initialize the Alpha Vantage TimeSeries client
    try:
        ts = TimeSeries(output_format='json')
        ti = TechIndicators(output_format='json')
    except Exception as e:
        return f"ERROR: Alpha Vantage API initialization failed. Check your API key or connection. {e}"

    data_point_lower = data_point.lower().replace(" ", "_")
    
    try:
        # --- 1. Handle Simple Price/Quote Data (Daily/Intraday) ---
        if data_point_lower in ["price", "close", "open", "volume"]:
            
            data, meta_data = ts.get_quote_endpoint(symbol=ticker)
            
            if not data:
                return f"ERROR: Could not find quote data for ticker {ticker}. API returned empty response."

            if data_point_lower == "price" or data_point_lower == "close":
                value = data.get('05. price', 'N/A')
                return f"Latest closing price for {ticker}: ${value}"
            elif data_point_lower == "open":
                value = data.get('02. open', 'N/A')
                return f"Today's opening price for {ticker}: ${value}"
            elif data_point_lower == "volume":
                value = data.get('06. volume', 'N/A')
                return f"Latest trading volume for {ticker}: {value}"
            
        # --- 2. Handle Technical Indicators (e.g., 50-day SMA) ---
        elif "sma" in data_point_lower:
            data, meta_data = ti.get_sma(symbol=ticker, interval='daily', time_period=50, series_type='close')
            
            latest_timestamp = next(iter(data.values()))
            sma_value = data[latest_timestamp]['SMA']
            
            return f"The 50-day Simple Moving Average (SMA) for {ticker} is: ${sma_value}"
            
        # --- 3. Default/Fallback ---
        else:
            return f"Alpha Vantage cannot retrieve '{data_point}' directly. Please request a common metric like 'price' or 'volume' or a technical indicator like 'SMA' for ticker {ticker}."

    except Exception as e:
        return f"API ERROR: Failed to retrieve data for {ticker} and {data_point}. Reason: {e}. Check Alpha Vantage daily limits (25/day)."