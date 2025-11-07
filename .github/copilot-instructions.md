# MCP Multi-Agent Deep Researcher

This project implements a multi-agent research system built on the Model Context Protocol (MCP), using CrewAI for agent orchestration, LinkUp for deep web search, and the phi3 model (via Ollama) for synthesis and writing.

## Architecture

- **MCP Server**: Implements the Model Context Protocol for seamless integration
- **CrewAI Agents**: Three-agent workflow (Web Searcher → Analyst → Technical Writer)
- **LinkUp API**: For deep web search capabilities
- **Ollama phi3**: Local model for writing, synthesis, and reasoning

## Key Components

- `server.py`: Main MCP server implementation
- `agents/`: CrewAI agent definitions and workflows
- `pyproject.toml`: Poetry dependency management
- `.env`: Environment configuration (LinkUp API key)

## Development Guidelines

- Use Poetry for dependency management
- Follow MCP protocol specifications
- Implement proper error handling for API calls
- Ensure agents work in sequence: Web Searcher → Analyst → Writer
- Return structured, comprehensive research answers