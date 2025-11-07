#!/bin/bash

# GitHub Repository Setup Script
# This script initializes the git repository and prepares it for GitHub

echo "🚀 MCP Multi-Agent Deep Researcher - GitHub Setup"
echo "=================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're already in a git repository
if [ -d ".git" ]; then
    echo "⚠️  Git repository already exists."
    read -p "Do you want to continue? This will add files to the existing repo. (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    # Initialize git repository
    echo "📁 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ .env file created. Please edit it with your API keys."
    else
        echo "⚠️  .env.example not found. Please create .env file manually."
    fi
fi

# Add all files to git
echo "📋 Adding files to git..."
git add .

# Check git status
echo "📊 Git status:"
git status --short

# Create initial commit
echo "💾 Creating initial commit..."
if git diff --cached --quiet; then
    echo "⚠️  No changes to commit."
else
    git commit -m "feat: initial commit - MCP Multi-Agent Deep Researcher

- Complete multi-agent research system
- Web interface with beautiful UI
- FastAPI backend with CORS support
- MCP protocol compliance
- One-command launcher
- Comprehensive documentation
- CI/CD pipeline setup"
    echo "✅ Initial commit created"
fi

# Prompt for GitHub repository creation
echo ""
echo "🌐 Next steps for GitHub:"
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: MCP-Multi-Agent-Deep-Researcher"
echo "   - Description: Multi-agent research system with web interface and local AI processing"
echo "   - Make it Public (recommended) or Private"
echo "   - DO NOT initialize with README, .gitignore, or license (we have them)"
echo ""
echo "2. After creating the repository, run these commands:"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/YOUR_USERNAME/MCP-Multi-Agent-Deep-Researcher.git"
echo "   git push -u origin main"
echo ""

# Prompt to continue with GitHub setup
read -p "📤 Do you want to set up the GitHub remote now? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "📝 Enter your GitHub username: " github_username
    
    if [ -z "$github_username" ]; then
        echo "❌ GitHub username cannot be empty."
        exit 1
    fi
    
    # Set up remote
    echo "🔗 Setting up GitHub remote..."
    git branch -M main
    git remote add origin "https://github.com/$github_username/MCP-Multi-Agent-Deep-Researcher.git"
    
    echo "📤 Pushing to GitHub..."
    echo "Note: You may be prompted for your GitHub credentials."
    
    if git push -u origin main; then
        echo "🎉 Successfully pushed to GitHub!"
        echo "🌐 Your repository is now available at:"
        echo "   https://github.com/$github_username/MCP-Multi-Agent-Deep-Researcher"
        echo ""
        echo "📝 Don't forget to:"
        echo "   1. Update the README.md with your actual GitHub username"
        echo "   2. Add your LinkUp API key to the repository secrets (for CI/CD)"
        echo "   3. Enable GitHub Pages if you want to host the frontend"
    else
        echo "❌ Failed to push to GitHub."
        echo "   Make sure:"
        echo "   1. The repository exists on GitHub"
        echo "   2. You have the correct permissions"
        echo "   3. Your GitHub credentials are correct"
    fi
else
    echo "⏭️  Skipping GitHub setup. You can do this manually later."
fi

echo ""
echo "🎯 Repository is ready!"
echo "💡 Quick commands:"
echo "   python3 launcher.py  # Start the application"
echo "   make start           # Alternative launcher"
echo "   git status           # Check repository status"
echo "   git log --oneline    # View commit history"