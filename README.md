# 💰 Dynamic Finance Crew: Investment Strategy Generator
Welcome to the Dynamic Finance Crew project, a multi-agent system built with CrewAI designed to generate customized investment strategies based on dynamic client profiles (Growth, Defensive, Long-Term, Short-Term).

This project successfully transitioned from a rigid, static model to a dynamic, goal-aligned engine by creating specialized agents and integrating external data APIs.

## 🚀 Key Features
Dynamic Client Profiling: The system adapts its filtering criteria (Beta, FCF, Revenue Growth) based on the client's stated risk tolerance (1-10) and primary goal (e.g., Aggressive Accumulation vs. Capital Preservation).

- Specialized Toolset: Integration of multiple custom tools for precise financial analysis and risk vetting.

- End-to-End Workflow: The crew handles intake, research, quantitative filtering, qualitative risk assessment, portfolio allocation, and final reporting.

- Web Interface (Streamlit): Deployed via app.py for easy user input and visualization.

## 🛠️ Project Setup & Installation
This project uses Python >=3.10 and requires external libraries and API keys to run effectively.

### 1. Install Dependencies
Navigate to your project root and install the required packages:

pip install crewai crewai-tools pandas yfinance google-api-python-client python-dotenv streamlit

### 2. API Key Configuration (Crucial)
Your agents rely on external services. You MUST define these keys securely.

Key Name

Service

Purpose

OPENAI_API_KEY

OpenAI (LLM)

Powers all agent reasoning and tool usage.

AV_API_KEY

Alpha Vantage

Provides financial metrics (FCF, P/E, SMA) via the Financial Scraper Tool.

GOOGLE_API_KEY

Google Cloud Console

Powers the custom Google Search Tool for qualitative news/context.

For Local Testing: Create a .env file in the root directory and add your keys.
For Streamlit Cloud: Add these keys to your Streamlit App Secrets ([secrets]).

## ⚙️ Custom Tools Implemented
The following highly specialized tools (defined as Python functions with the @tool decorator) are integrated into the workflow:

Agent

Tool

Description

Market Analyst

GoogleSearchTool

General web search for news, sentiment, and sector outlook.

Financial Analyst

FinancialScraperTool

Fetches specific financial metrics (e.g., price, volume, SMA) using Alpha Vantage.

Financial Analyst

HistoricalCorrelationTool

Calculates asset correlation for diversification metrics using YFinance/Pandas.

Risk Specialist

SECHerculesTool

Downloads and searches SEC 10-K/8-K filings for legal/geopolitical risk keywords (FREE via sec-edgar-downloader).

Report Generator

MarkdownGeneratorTool

Formats the final strategy into a readable Markdown report and saves the file.

## 🏃 Running the Application
Method

Command

Notes

Web Interface (Recommended)

streamlit run app.py

Launches the interactive client input form.

Command Line (CLI)

$ crewai run

Runs the full sequence for debugging and testing the core workflow.

## ⚠️ Known Mismatches & Solutions (For Developers)
- The project required extensive debugging due to framework conflicts and initial data errors. These are the major breakthroughs achieved:

-- Tool Argument Error Fix: Resolved TypeError: tool() got an unexpected keyword argument 'args_schema' by implementing the nested BaseModel class syntax inside each decorated tool function.

-- Context Mapping Fix: Resolved AttributeError: 'str' object has no attribute 'get' by ensuring all task dependencies (context:) are defined using the correct YAML list syntax (- task_name).

-- Data Persistence Fix (The $1M Problem): The code was successfully refactored to a dynamic structure where agent filtering criteria adapt based on the client's actual financial profile and timeline.

--LLM Failure Fix: Resolved the litellm.AuthenticationError in the cloud by relying on the st.secrets injection in app.py.

Let's create wonders together with the power and simplicity of crewAI.
