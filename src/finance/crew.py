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
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from dotenv import load_dotenv
import os


load_dotenv()  
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
@CrewBase
class Finance():
    """Finance crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def Client_Profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['Client_Profiler'], 
            verbose=True,
            memory=True
        )

    @agent
    def Market_Research_Analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['Market_Research_Analyst'], 
            verbose=True,
            tools=[SerperDevTool(),google_search_tool_function,StockRetriverSchemaTool()],
            memory=True
        )
    
    @agent
    def Financial_Data_Analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['Financial_Data_Analyst'], 
            verbose=True,
            tools=[financial_scraper_tool_function,historical_correlation_tool_function,google_search_tool_function,StockRetriverSchemaTool()],
            memory=True
        )
    @agent
    def Risk_Management_Specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['Risk_Management_Specialist'], 
            verbose=True,
            tools=[sec_hercules_tool_function,google_search_tool_function,StockRetriverSchemaTool()],
            memory=True
        )
    @agent
    def Investment_Strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['Investment_Strategist'], 
            verbose=True,
            tools=[SerperDevTool(),google_search_tool_function,StockRetriverSchemaTool(),
                   financial_scraper_tool_function,historical_correlation_tool_function],
                   memory=True
        )
    @agent
    def Final_Report_Generator(self) -> Agent:
        return Agent(
            config=self.agents_config['Final_Report_Generator'], 
            verbose=True,
            tools=[markdown_generator_tool_function],
            memory=True
        )
    
    #TASK-------------------------------------------------------

    @task
    def client_profile_task(self) -> Task:
        return Task(
            config=self.tasks_config['client_profile_task'], 
            output_file='output/compliance_report.md'
        )
    
    @task
    def market_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_research_task'], 
            output_file='output/market_research_report.md'
        )
    @task
    def Quantitative_Defensive_Stock_Filtering(self) -> Task:
        return Task(
            config=self.tasks_config['Quantitative_Defensive_Stock_Filtering'], 
            output_file='output/quantitative_stock_filtering_report.md'
        )
    
    @task
    def Qualitative_and_External_Risk_Assessment(self) -> Task:
        return Task(
            config=self.tasks_config['Qualitative_and_External_Risk_Assessment'], 
            output_file='output/risk_assessment_report.md'
        )
    
    @task
    def Portfolio_Allocation_Task(self) -> Task:
        return Task(
            config=self.tasks_config['Portfolio_Allocation_Task'], 
            output_file='output/portfolio_allocation_report.md'
        )
    
    @task
    def Final_Report_Task(self) -> Task:
        return Task(
            config=self.tasks_config['Final_Report_Task'], 
            output_file='output/final_report.md'
        )

    

    @crew
    def crew(self) -> Crew:
        """Creates the Finance crew"""
       
        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            manager_llm="openai/gpt-4o-mini",
            memory=True,
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/long_term_memory_storage.db"
                )
            ),
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                        embedder_config={
                            "provider": "openai",
                            "config": {
                                "model": 'text-embedding-3-small'
                            }
                        },
                        type="short_term",
                        path="./memory/"
                    )
                ),   
            entity_memory = EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="./memory/"
                )
            )
        )