#!/usr/bin/env python
import warnings
from finance.crew import Finance
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from a .env file if present
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["AV_API_KEY"]= os.getenv("AV_API_KEY")
os.environ["GOOGLE_API_KEY"]= os.getenv("GOOGLE_API_KEY")

def run():
    """
    Run the research crew.
    """
    prompt= """
    I want to put 1 million dolar to invest in the stock market  using dolar codt avering for 3 yaers of puting  money
    and my goal for the next 15 years. I am looking for a diversified portfolio with a mix of growth and value and devident stocks,
    I am particularly interested in the technology and AI ,semiconductores sectors, i also want part to ETF .
    My risk tolerance is moderate to high, and I am looking for a balance between capital appreciation and income generation.
    Please provide a detailed investment strategy, including specific stock recommendations, allocation percentages, 
    and rationale for each choice. Additionally, please include any relevant market trends or economic factors 
    
    """
    inputs = {
        'goal': prompt,
    }

    # Create and run the crew
    result = Finance().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")
