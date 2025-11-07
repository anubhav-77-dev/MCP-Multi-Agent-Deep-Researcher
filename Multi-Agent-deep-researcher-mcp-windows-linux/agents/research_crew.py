"""
Research Crew Implementation

This module implements the multi-agent research system using CrewAI.
It orchestrates three agents: Web searcher, Research analyst, and Technical writer.
"""

import os
import asyncio
import logging
from typing import Dict, Any, Optional

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from dotenv import load_dotenv

from .tools.linkup_search import LinkUpSearchTool
from .tools.ollama_tool import OllamaLLMTool

load_dotenv()
logger = logging.getLogger(__name__)

class ResearchCrew:
    """Multi-agent research crew using CrewAI."""
    
    def __init__(self):
        self.linkup_tool = LinkUpSearchTool()
        self.ollama_tool = OllamaLLMTool()
        self.crew = self._setup_crew()
    
    def _setup_crew(self) -> Crew:
        """Set up the research crew with agents and their tasks."""
        
        # Web Searcher Agent
        web_searcher = Agent(
            role='Web Research Specialist',
            goal='Find comprehensive and relevant information from the web using LinkUp API',
            backstory="""You are an expert web researcher who excels at finding relevant, 
            accurate, and comprehensive information from various online sources. You use 
            advanced search techniques to gather data from multiple perspectives.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.linkup_tool]
            # Note: LLM will be set via environment variables
        )
        
        # Research Analyst Agent
        research_analyst = Agent(
            role='Research Analyst',
            goal='Analyze and synthesize information to provide comprehensive insights',
            backstory="""You are a skilled research analyst with expertise in synthesizing 
            information from multiple sources. You excel at identifying key insights, 
            verifying facts, and organizing information in a logical manner.""",
            verbose=True,
            allow_delegation=False
            # Note: LLM will be set via environment variables
        )
        
        # Technical Writer Agent
        technical_writer = Agent(
            role='Technical Writer',
            goal='Create clear, comprehensive, and well-structured written content',
            backstory="""You are an expert technical writer who excels at creating 
            clear, comprehensive, and well-structured documents. You can transform 
            complex research into accessible and informative content.""",
            verbose=True,
            allow_delegation=False
            # Note: LLM will be set via environment variables
        )
        
        # Define tasks for each agent
        search_task = Task(
            description="""Search for comprehensive information about the given query: {query}
            
            Use the LinkUp search tool to gather information from multiple sources.
            Focus on finding:
            - Current and accurate information
            - Multiple perspectives on the topic
            - Relevant examples and case studies
            - Statistical data when available
            
            Provide a detailed summary of your findings.""",
            agent=web_searcher,
            expected_output="A comprehensive summary of web search results with sources"
        )
        
        analysis_task = Task(
            description="""Analyze the web search results and synthesize the information.
            
            Based on the web search results, provide:
            - Key insights and main points
            - Analysis of different perspectives
            - Identification of gaps or contradictions
            - Verification of important claims
            - Structured organization of information
            
            Focus on depth and accuracy in your analysis.""",
            agent=research_analyst,
            expected_output="A structured analysis with key insights and verified information",
            dependencies=[search_task]
        )
        
        writing_task = Task(
            description="""Create a comprehensive, well-structured written response.
            
            Based on the research and analysis, write a comprehensive answer that:
            - Directly addresses the original query: {query}
            - Is well-organized with clear sections
            - Includes relevant examples and data
            - Is written in clear, accessible language
            - Provides actionable insights where appropriate
            - Includes proper context and background
            
            Format the response in markdown for better readability.""",
            agent=technical_writer,
            expected_output="A comprehensive, well-formatted markdown document answering the query",
            dependencies=[analysis_task]
        )
        
        # Create and return crew
        crew = Crew(
            agents=[web_searcher, research_analyst, technical_writer],
            tasks=[search_task, analysis_task, writing_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew
    
    async def conduct_research(self, query: str) -> str:
        """Conduct comprehensive research using the multi-agent crew."""
        try:
            logger.info(f"Starting research process for query: {query}")
            
            # Run the crew asynchronously
            result = await asyncio.to_thread(
                self.crew.kickoff,
                inputs={'query': query}
            )
            
            logger.info("Research process completed successfully")
            return str(result)
            
        except Exception as e:
            logger.error(f"Error in research process: {str(e)}")
            return f"Error conducting research: {str(e)}"
    
    async def quick_search(self, query: str) -> str:
        """Perform a quick search using just the web searcher agent."""
        try:
            logger.info(f"Performing quick search for: {query}")
            
            # Use just the search tool directly for quick results
            search_results = await asyncio.to_thread(
                self.linkup_tool._run,
                query
            )
            
            return f"Quick search results for '{query}':\n\n{search_results}"
            
        except Exception as e:
            logger.error(f"Error in quick search: {str(e)}")
            return f"Error performing quick search: {str(e)}"