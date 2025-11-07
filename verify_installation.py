#!/usr/bin/env python3
"""
Installation verification script

This script runs basic tests to ensure the MCP Multi-Agent Deep Researcher is working correctly.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'Multi-Agent-deep-researcher-mcp-windows-linux'))
        from agents.research_crew import ResearchCrew
        print("✅ ResearchCrew import successful")
    except ImportError as e:
        print(f"❌ Failed to import ResearchCrew: {e}")
        return False
    
    try:
        from agents.tools.linkup_search import LinkUpSearchTool
        print("✅ LinkUpSearchTool import successful")
    except ImportError as e:
        print(f"❌ Failed to import LinkUpSearchTool: {e}")
        return False
    
    try:
        from agents.tools.ollama_tool import OllamaLLMTool
        print("✅ OllamaLLMTool import successful")
    except ImportError as e:
        print(f"❌ Failed to import OllamaLLMTool: {e}")
        return False
    
    return True

async def test_ollama_connection():
    """Test connection to Ollama."""
    print("\nTesting Ollama connection...")
    
    try:
        from agents.tools.ollama_tool import OllamaLLMTool
        
        ollama_tool = OllamaLLMTool()
        
        # Check model availability
        if ollama_tool.check_model_availability():
            print("✅ Ollama model is available")
            return True
        else:
            print("⚠️  Ollama model not available")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return False

async def test_environment():
    """Test environment configuration."""
    print("\nTesting environment configuration...")
    
    # Check .env file
    env_path = Path('.env')
    if not env_path.exists():
        print("⚠️  .env file not found")
        return False
    
    # Check required environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    linkup_key = os.getenv('LINKUP_API_KEY')
    if not linkup_key or linkup_key == 'your_linkup_api_key_here':
        print("⚠️  LINKUP_API_KEY not configured")
        return False
    
    print("✅ Environment configuration looks good")
    return True

async def test_basic_functionality():
    """Test basic functionality without making external API calls."""
    print("\nTesting basic functionality...")
    
    try:
        from agents.research_crew import ResearchCrew
        
        # Just test that we can create the crew
        crew = ResearchCrew()
        print("✅ Research crew created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating research crew: {e}")
        return False

async def main():
    """Main test function."""
    print("MCP Multi-Agent Deep Researcher - Installation Verification")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports()),
        ("Environment Test", test_environment()),
        ("Ollama Connection Test", test_ollama_connection()),
        ("Basic Functionality Test", test_basic_functionality())
    ]
    
    results = []
    for test_name, test_coro in tests:
        print(f"\n{test_name}")
        print("-" * len(test_name))
        result = await test_coro
        results.append(result)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All tests passed! ({passed}/{total})")
        print("\nYour installation is ready to use!")
        print("\nNext steps:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Run the MCP server: poetry run python Multi-Agent-deep-researcher-mcp-windows-linux/server.py")
        print("3. Or run the HTTP server: poetry run python Multi-Agent-deep-researcher-mcp-windows-linux/http_server.py")
    else:
        print(f"❌ Some tests failed ({passed}/{total} passed)")
        print("\nPlease check the errors above and run setup.py to fix any issues.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())