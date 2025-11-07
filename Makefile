.PHONY: help install setup server http-server test clean

help: ## Show this help message
	@echo "MCP Multi-Agent Deep Researcher"
	@echo "================================"
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using Poetry
	poetry install

setup: ## Run setup script to check environment
	python setup.py

server: ## Start the MCP server
	poetry run python Multi-Agent-deep-researcher-mcp-windows-linux/server.py

http-server: ## Start the HTTP server
	poetry run python Multi-Agent-deep-researcher-mcp-windows-linux/http_server.py

test: ## Run basic functionality tests
	poetry run python Multi-Agent-deep-researcher-mcp-windows-linux/test_research.py

verify: ## Verify installation
	python verify_installation.py

clean: ## Clean up cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name ".DS_Store" -delete

dev-setup: install setup ## Complete development setup
	@echo "Development setup complete!"
	@echo "Next steps:"
	@echo "1. Configure your .env file with API keys"
	@echo "2. Start Ollama: ollama serve"
	@echo "3. Pull the model: ollama pull phi3"
	@echo "4. Run the server: make server"

quick-test: ## Run a quick search test
	poetry run python Multi-Agent-deep-researcher-mcp-windows-linux/test_research.py --mode search --query "artificial intelligence trends 2024"

start: ## Start both frontend and backend servers
	python3 launcher.py

launch: start ## Alias for start

demo: start ## Alias for start - launch demo