#!/usr/bin/env python3
"""
Simple test script to verify core functionality
"""

import sys
import os
import asyncio

# Add the project directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Multi-Agent-deep-researcher-mcp-windows-linux'))

async def test_ollama_tool():
    """Test the Ollama tool."""
    print("Testing Ollama tool...")
    try:
        from agents.tools.ollama_tool import OllamaLLMTool
        
        ollama_tool = OllamaLLMTool()
        print(f"✅ Ollama tool created successfully")
        print(f"   Base URL: {ollama_tool.base_url}")
        print(f"   Model: {ollama_tool.model_name}")
        
        # Check model availability
        if ollama_tool.check_model_availability():
            print("✅ Model is available in Ollama")
        else:
            print("⚠️  Model not found in Ollama")
        
        return True
    except Exception as e:
        print(f"❌ Error testing Ollama tool: {e}")
        return False

async def test_linkup_tool():
    """Test the LinkUp tool."""
    print("\nTesting LinkUp tool...")
    try:
        from agents.tools.linkup_search import LinkUpSearchTool
        
        linkup_tool = LinkUpSearchTool()
        print("✅ LinkUp tool created successfully")
        
        # Test with a simple query (will fail without API key but shouldn't crash)
        result = linkup_tool._run("test query")
        print(f"✅ Search test completed (result length: {len(result)} chars)")
        
        return True
    except Exception as e:
        print(f"❌ Error testing LinkUp tool: {e}")
        return False

async def test_simple_crew():
    """Test creating a simple crew without full initialization."""
    print("\nTesting basic CrewAI setup...")
    try:
        from crewai import Agent
        
        # Try creating a simple agent without LLM first
        simple_agent = Agent(
            role='Test Agent',
            goal='Test basic functionality',
            backstory='A simple test agent',
            verbose=False,
            allow_delegation=False
        )
        print("✅ Simple CrewAI agent created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating simple agent: {e}")
        return False

async def main():
    """Run all tests."""
    print("Simple Component Tests")
    print("=" * 30)
    
    tests = [
        test_ollama_tool(),
        test_linkup_tool(),
        test_simple_crew()
    ]
    
    results = []
    for test in tests:
        result = await test
        results.append(result)
    
    print("\n" + "=" * 30)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All tests passed! ({passed}/{total})")
    else:
        print(f"⚠️  Some tests failed ({passed}/{total} passed)")
    
    return passed == total

if __name__ == "__main__":
    asyncio.run(main())