# Finance Crew

Welcome to the Finance Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/finance/config/agents.yaml` to define your agents
- Modify `src/finance/config/tasks.yaml` to define your tasks
- Modify `src/finance/crew.py` to add your own logic, tools and specific args
- Modify `src/finance/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the finance Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The finance Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## 💰 Dynamic Finance Crew: Investment Strategy Generator
Welcome to the Dynamic Finance Crew project, a multi-agent system built with CrewAI designed to generate customized investment strategies based on dynamic client profiles (Growth, Defensive, Long-Term, Short-Term).

This project successfully transitioned from a static defensive model to a dynamic, goal-aligned engine by creating specialized agents and integrating external data APIs.

🚀 Key Features of this Project
Dynamic Client Profiling: The system adapts its filtering criteria (Beta, FCF, Revenue Growth) based on the client's stated risk tolerance (1-10) and primary goal (e.g., Aggressive Accumulation vs. Capital Preservation).

Specialized Toolset: Integration of multiple custom tools for precise financial analysis and risk vetting.

End-to-End Workflow: The crew handles intake, research, quantitative filtering, qualitative risk assessment, portfolio allocation, and final reporting.

Web Interface (Streamlit): Deployed via app.py for easy user input and visualization.

🛠️ Project Setup & Installation
This project requires external libraries and API keys to run effectively.

Prerequisites
Ensure you have Python >=3.10 and a modern dependency manager (uv or pip) installed.

1. Install Dependencies
Navigate to your project root (/boit finance/finance) and install the required packages:

pip install crewai crewai-tools pandas yfinance google-api-python-client python-dotenv streamlit

2. API Key Configuration (Crucial)
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

⚙️ Custom Tools Implemented
The following tools (defined as Python functions with the @tool decorator) are used by the agents:

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

🏃 Running the Application
There are two primary ways to run the crew:

Option A: Web Interface (Recommended)
Run the Streamlit application to use the interactive client form:

streamlit run app.py

Option B: Command Line Interface (CLI)
Run the full sequence using the CLI (for debugging the core workflow):

$ crewai run

⚠️ Known Mismatches & Solutions (For Developers)
The project required extensive debugging due to framework conflicts and initial data errors. These are the major breakthroughs achieved:

Tool Argument Error Fix: The TypeError: tool() got an unexpected keyword argument 'args_schema' was fixed by replacing the keyword with a nested BaseModel class inside each decorated tool function.

Context Mapping Fix: The AttributeError: 'str' object has no attribute 'get' was fixed by ensuring all task dependencies (context:) are defined using the correct YAML list syntax (- task_name) instead of string-based lists.

Data Persistence Fix (The $1M Problem): The code was successfully refactored from a rigid "defensive/short-term" strategy to a dynamic structure where agent roles and task filtering criteria adapt based on the client's risk score and timeline recorded in the initial client_profile_task output.

LLM Failure Fix: Resolved the litellm.AuthenticationError in the cloud by removing the redundant os.environ = os.getenv(...) line and relying on the st.secrets injection in app.py.

Let's create wonders together with the power and simplicity of crewAI.
