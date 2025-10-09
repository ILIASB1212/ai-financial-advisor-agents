# historical_correlation_tool.py (FINAL CORRECT VERSION for TypeError)

from pydantic import BaseModel, Field
from crewai.tools import tool # Confirmed: This import works in your environment
import yfinance as yf
import pandas as pd
from typing import Type # Not needed, but harmless if kept

# --------------------------------------------------------------------
# 1. Define the Tool Function using the @tool decorator
#    CRITICAL CHANGE: Removed 'args_schema=CorrelationInput'
# --------------------------------------------------------------------
@tool("Historical Correlation Tool")
def historical_correlation_tool_function(ticker_1: str, ticker_2: str, period: str) -> str:
    """Tool to calculate the historical correlation coefficient (rho) between two stock tickers' daily returns."""
    
    # CRITICAL FIX: The input schema must be defined as a NESTED class 
    # for the @tool decorator to automatically recognize it in this syntax.
    class HistoricalCorrelationToolSchema(BaseModel):
        """Input schema for the Historical Correlation Tool."""
        ticker_1: str = Field(description="The first stock ticker symbol (e.g., 'PG').")
        ticker_2: str = Field(description="The second stock ticker symbol (e.g., 'KO').")
        period: str = Field(description="The historical period for calculation (e.g., '1y', '3y').")
    
    try:
        # Download historical data
        data = yf.download([ticker_1, ticker_2], period=period, progress=False)
        
        # Calculate daily returns
        returns = data['Close'].pct_change().dropna()
        
        # Calculate the correlation matrix and extract the correlation value
        # Ensure that both tickers have enough data to calculate correlation
        if ticker_1 not in returns.columns or ticker_2 not in returns.columns or returns.empty:
             return f"Error: Could not retrieve sufficient data for one or both tickers ({ticker_1}, {ticker_2}) over the period {period}."
             
        correlation = returns.corr().loc[ticker_1, ticker_2]
        
        # A good diversification target is usually below 0.5
        conclusion = "Well-diversified (low correlation)." if correlation < 0.5 else "Highly correlated (less diversified benefit)."
        
        return f"Historical correlation (rho) between {ticker_1} and {ticker_2} over {period} is: {correlation:.2f}. Conclusion: {conclusion}"
    
    except Exception as e:
        return f"Error calculating correlation for {ticker_1} and {ticker_2}: {e}"