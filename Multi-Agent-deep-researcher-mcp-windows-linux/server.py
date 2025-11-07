#!/usr/bin/env python3
"""
MCP Multi-Agent Deep Researcher Server

A Model Context Protocol server that implements a multi-agent research system
using CrewAI for agent orchestration, LinkUp for web search, and Ollama for AI processing.
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

from agents.research_crew import ResearchCrew

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPResearchServer:
    """MCP Server for multi-agent research functionality."""
    
    def __init__(self):
        self.server = Server("mcp-multi-agent-researcher")
        self.research_crew = ResearchCrew()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List available research tools."""
            tools = [
                Tool(
                    name="research_query",
                    description="Conduct comprehensive research on a topic using multi-agent system",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The research question or topic to investigate"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="quick_search",
                    description="Perform a quick web search for immediate information",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict
        ) -> CallToolResult:
            """Handle tool calls."""
            try:
                if name == "research_query":
                    query = arguments.get("query")
                    if not query:
                        return CallToolResult(
                            content=[TextContent(
                                type="text",
                                text="Error: Query parameter is required"
                            )],
                            isError=True
                        )
                    
                    logger.info(f"Starting research for query: {query}")
                    result = await self.research_crew.conduct_research(query)
                    
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=result
                        )]
                    )
                
                elif name == "quick_search":
                    query = arguments.get("query")
                    if not query:
                        return CallToolResult(
                            content=[TextContent(
                                type="text",
                                text="Error: Query parameter is required"
                            )],
                            isError=True
                        )
                    
                    logger.info(f"Performing quick search for: {query}")
                    result = await self.research_crew.quick_search(query)
                    
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=result
                        )]
                    )
                
                else:
                    return CallToolResult(
                        content=[TextContent(
                            type="text",
                            text=f"Unknown tool: {name}"
                        )],
                        isError=True
                    )
            
            except Exception as e:
                logger.error(f"Error in tool call {name}: {str(e)}")
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Error: {str(e)}"
                    )],
                    isError=True
                )

async def main():
    """Main server entry point."""
    server_instance = MCPResearchServer()
    
    # Check required environment variables
    if not os.getenv('LINKUP_API_KEY'):
        logger.warning("LINKUP_API_KEY not set. Web search functionality may be limited.")
    
    logger.info("Starting MCP Multi-Agent Deep Researcher Server...")
    
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-multi-agent-researcher",
                server_version="0.1.0",
                capabilities=server_instance.server.get_capabilities(),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())