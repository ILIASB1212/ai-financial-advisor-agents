from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import yfinance as yf


class StockRetriverInput(BaseModel):
    """Input schema for the Stock Retriver Tool."""
    ticker: str = Field(description="The stock ticker symbol (e.g., 'AAPL', 'GOOGL') for the company to retrieve data for.")

# 2. Define the Tool class using the schema
class StockRetriverSchemaTool(BaseTool):
    name: str = "Stock Retriver Tool"
    description: str = "A tool to retrieve stock data using a ticker symbol."
    # Assign the Pydantic schema here
    args_schema: BaseModel = StockRetriverInput

    def _run(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            current_price = stock.history(period="1d")['Close'].iloc[-1]
            market_cap = stock.info.get('marketCap')
            return f"Price for {ticker}: ${current_price:,.2f}. Market Cap: ${market_cap:,.0f}."
        except Exception as e:
            return f"Error retrieving stock data for {ticker}: {e}"
