#!/usr/bin/env python3
"""
Example script to test the MCP Multi-Agent Deep Researcher
"""

import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.research_crew import ResearchCrew

async def test_research():
    """Test the research functionality."""
    crew = ResearchCrew()
    
    # Test query
    query = "What is agentic AI and how does it differ from traditional AI?"
    
    print(f"Testing research query: {query}")
    print("=" * 50)
    
    result = await crew.conduct_research(query)
    
    print("Research Result:")
    print("-" * 20)
    print(result)

async def test_quick_search():
    """Test the quick search functionality."""
    crew = ResearchCrew()
    
    # Test query
    query = "latest developments in artificial intelligence 2024"
    
    print(f"Testing quick search: {query}")
    print("=" * 50)
    
    result = await crew.quick_search(query)
    
    print("Quick Search Result:")
    print("-" * 20)
    print(result)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test MCP Research functionality")
    parser.add_argument("--mode", choices=["research", "search"], default="search",
                        help="Test mode: research (full workflow) or search (quick search)")
    parser.add_argument("--query", type=str, help="Custom query to test")
    
    args = parser.parse_args()
    
    if args.mode == "research":
        if args.query:
            # Custom research query
            async def custom_research():
                crew = ResearchCrew()
                result = await crew.conduct_research(args.query)
                print(f"Research Result for '{args.query}':")
                print("=" * 50)
                print(result)
            
            asyncio.run(custom_research())
        else:
            asyncio.run(test_research())
    else:
        if args.query:
            # Custom search query
            async def custom_search():
                crew = ResearchCrew()
                result = await crew.quick_search(args.query)
                print(f"Search Result for '{args.query}':")
                print("=" * 50)
                print(result)
            
            asyncio.run(custom_search())
        else:
            asyncio.run(test_quick_search())