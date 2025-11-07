#!/usr/bin/env python3
"""
Setup script for MCP Multi-Agent Deep Researcher

This script helps users set up the environment and check dependencies.
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.10 to 3.13."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10 or higher is required (for CrewAI compatibility)")
        return False
    if version.major > 3 or (version.major == 3 and version.minor > 13):
        print("⚠️  Python 3.13 or lower is recommended (for CrewAI compatibility)")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return True
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is supported")
    return True

def check_poetry():
    """Check if Poetry is installed."""
    try:
        result = subprocess.run(['poetry', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Poetry is installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Poetry is not installed")
    print("   Install Poetry from: https://python-poetry.org/")
    return False

def check_ollama():
    """Check if Ollama is running and accessible."""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running with {len(models)} models")
            
            # Check if phi3 model is available
            phi3_available = any('phi3' in model['name'] for model in models)
            if phi3_available:
                print("✅ phi3 model is available")
            else:
                print("⚠️  phi3 model not found. Run: ollama pull phi3")
            
            return True
    except Exception as e:
        pass
    
    print("❌ Ollama is not running or not accessible")
    print("   Install Ollama from: https://ollama.ai/")
    print("   Then run: ollama serve")
    return False

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("⚠️  .env file not found")
        print("   Copy .env.example to .env and configure your API keys")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    required_vars = ['LINKUP_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if var not in content or f"{var}=your_" in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing or unconfigured environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ .env file is configured")
    return True

def install_dependencies():
    """Install Python dependencies using Poetry."""
    try:
        print("Installing dependencies with Poetry...")
        result = subprocess.run(['poetry', 'install'], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    """Main setup function."""
    print("MCP Multi-Agent Deep Researcher Setup")
    print("=" * 40)
    
    checks = [
        check_python_version(),
        check_poetry(),
        check_ollama(),
        check_env_file()
    ]
    
    if all(checks):
        print("\n✅ All checks passed!")
        
        # Offer to install dependencies
        install = input("\nInstall dependencies now? (y/n): ").lower().strip()
        if install == 'y':
            install_dependencies()
        
        print("\nSetup complete! You can now run:")
        print("  poetry run python Multi-Agent-deep-researcher-mcp-windows-linux/server.py")
        print("  or")
        print("  poetry run python Multi-Agent-deep-researcher-mcp-windows-linux/http_server.py")
    else:
        print("\n❌ Some checks failed. Please address the issues above before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()