from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from .tools.custom_tool import StockRetriverSchemaTool
from .tools.financial_scraper_tool import financial_scraper_tool_function
from .tools.google_search_tool import google_search_tool_function
from .tools.sec_hercules_tool import sec_hercules_tool_function
from .tools.markdown_generator_tool import markdown_generator_tool_function
from .tools.historical_correlation_tool import historical_correlation_tool_function

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from a .env file if present
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
@CrewBase
class Finance():
    """Finance crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def Client_Profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['Client_Profiler'], # type: ignore[index]
            verbose=True
        )

    @agent
    def Market_Research_Analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['Market_Research_Analyst'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool(),google_search_tool_function,StockRetriverSchemaTool()]
        )
    
    @agent
    def Financial_Data_Analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['Financial_Data_Analyst'], # type: ignore[index]
            verbose=True,
            tools=[financial_scraper_tool_function,historical_correlation_tool_function,google_search_tool_function,StockRetriverSchemaTool()]
        )
    @agent
    def Risk_Management_Specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['Risk_Management_Specialist'], # type: ignore[index]
            verbose=True,
            tools=[sec_hercules_tool_function,google_search_tool_function,StockRetriverSchemaTool()]
        )
    @agent
    def Investment_Strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['Investment_Strategist'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool(),google_search_tool_function,StockRetriverSchemaTool(),
                   financial_scraper_tool_function,historical_correlation_tool_function]
        )
    @agent
    def Final_Report_Generator(self) -> Agent:
        return Agent(
            config=self.agents_config['Final_Report_Generator'], # type: ignore[index]
            verbose=True,
            tools=[markdown_generator_tool_function]
        )
    
    #TASK-------------------------------------------------------

    @task
    def client_profile_task(self) -> Task:
        return Task(
            config=self.tasks_config['client_profile_task'], # type: ignore[index]
            output_file='output/compliance_report.md'
        )
    
    @task
    def market_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_research_task'], # type: ignore[index]
            output_file='output/market_research_report.md'
        )
    @task
    def Quantitative_Defensive_Stock_Filtering(self) -> Task:
        return Task(
            config=self.tasks_config['Quantitative_Defensive_Stock_Filtering'], # type: ignore[index]
            output_file='output/quantitative_stock_filtering_report.md'
        )
    
    @task
    def Qualitative_and_External_Risk_Assessment(self) -> Task:
        return Task(
            config=self.tasks_config['Qualitative_and_External_Risk_Assessment'], # type: ignore[index]
            output_file='output/risk_assessment_report.md'
        )
    
    @task
    def Portfolio_Allocation_Task(self) -> Task:
        return Task(
            config=self.tasks_config['Portfolio_Allocation_Task'], # type: ignore[index]
            output_file='output/portfolio_allocation_report.md'
        )
    
    @task
    def Final_Report_Task(self) -> Task:
        return Task(
            config=self.tasks_config['Final_Report_Task'], # type: ignore[index]
            output_file='output/final_report.md'
        )

    

    @crew
    def crew(self) -> Crew:
        """Creates the Finance crew"""
       
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            manager_llm="openai/gpt-4o-mini",
        )
