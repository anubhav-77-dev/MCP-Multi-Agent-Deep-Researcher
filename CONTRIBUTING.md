# 🤝 Contributing to MCP Multi-Agent Deep Researcher

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## 🚀 Quick Start for Contributors

### 1. Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/MCP-Multi-Agent-Deep-Researcher.git
cd MCP-Multi-Agent-Deep-Researcher

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies including dev tools
poetry install --with dev

# Setup pre-commit hooks
poetry run pre-commit install

# Run setup verification
python3 setup.py
```

### 2. Development Workflow
```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes...

# Run tests and linting
make test
poetry run black .
poetry run isort .
poetry run flake8 .

# Commit and push
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

## 📋 Development Guidelines

### Code Style
- **Python**: Follow PEP 8, use Black for formatting
- **Line Length**: 88 characters (Black default)
- **Imports**: Use isort for import ordering
- **Type Hints**: Use type hints for function parameters and returns
- **Docstrings**: Use Google-style docstrings

### Example Code Style
```python
from typing import Dict, List, Optional

class ExampleClass:
    """Example class with proper formatting.
    
    Args:
        param1: Description of parameter 1
        param2: Optional parameter with default
        
    Attributes:
        attribute1: Description of attribute
    """
    
    def __init__(
        self, 
        param1: str, 
        param2: Optional[int] = None
    ) -> None:
        self.attribute1 = param1
        self._param2 = param2
    
    def example_method(self, data: Dict[str, str]) -> List[str]:
        """Example method with type hints and docstring.
        
        Args:
            data: Dictionary of string key-value pairs
            
        Returns:
            List of processed strings
            
        Raises:
            ValueError: If data is empty
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        return [f"{k}: {v}" for k, v in data.items()]
```

### Commit Message Format
We use conventional commits:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add support for custom AI models
fix: resolve CORS issue in FastAPI server
docs: update installation instructions
refactor: improve error handling in research crew
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
make test

# Run specific test categories
poetry run python simple_test.py
poetry run python verify_installation.py

# Test the launcher
python3 launcher.py
# Then test web interface manually
```

### Writing Tests
- Add tests for new features in appropriate test files
- Include both positive and negative test cases
- Mock external API calls (LinkUp, Ollama) for unit tests
- Test error handling and edge cases

### Test Structure
```python
import pytest
from unittest.mock import Mock, patch

def test_feature_success():
    """Test successful feature operation."""
    # Arrange
    input_data = "test input"
    expected_result = "expected output"
    
    # Act
    result = your_function(input_data)
    
    # Assert
    assert result == expected_result

def test_feature_error_handling():
    """Test feature error handling."""
    with pytest.raises(ValueError, match="Expected error message"):
        your_function(invalid_input)
```

## 🎯 Areas for Contribution

### High Priority
- 🧪 **Test Coverage**: Add more comprehensive tests
- 📚 **Documentation**: Improve API docs and examples
- 🐛 **Bug Fixes**: Fix reported issues
- 🔧 **Performance**: Optimize agent workflows

### Medium Priority  
- 🎨 **Frontend**: UI/UX improvements
- 🔌 **Integrations**: New tools and APIs
- 🤖 **Agents**: New specialized agents
- 🌍 **i18n**: Internationalization support

### Good First Issues
- 📝 Fix typos in documentation
- 🎨 Improve CSS styling
- 🔧 Add configuration options
- 📋 Add example queries
- 🧪 Add simple test cases

## 🔧 Project Architecture

### Key Components
```
Multi-Agent-deep-researcher-mcp-windows-linux/
├── server.py              # MCP protocol server
├── http_server.py         # FastAPI REST API
└── agents/
    ├── research_crew.py   # CrewAI orchestration
    └── tools/
        ├── linkup_search.py   # Web search
        └── ollama_tool.py     # Local AI
```

### Adding New Features

#### 1. New Agent Tool
```python
# agents/tools/new_tool.py
from crewai.tools import BaseTool

class NewTool(BaseTool):
    name = "New Tool"
    description = "Description of what the tool does"
    
    def _run(self, query: str) -> str:
        # Implementation
        return result
```

#### 2. New Agent
```python
# In agents/research_crew.py
new_agent = Agent(
    role='Specialist Role',
    goal='Specific goal for the agent',
    backstory='Background context',
    tools=[new_tool],
    verbose=True
)
```

#### 3. New API Endpoint
```python
# In http_server.py
@app.post("/new-endpoint")
async def new_endpoint(request: RequestModel) -> ResponseModel:
    """New endpoint description."""
    result = await process_request(request)
    return ResponseModel(result=result)
```

## 📦 Dependencies

### Adding New Dependencies
```bash
# Add runtime dependency
poetry add new-package

# Add development dependency  
poetry add --group dev new-dev-package

# Update requirements.txt
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### Dependency Guidelines
- Minimize dependencies where possible
- Use well-maintained, popular packages
- Pin major versions to avoid breaking changes
- Document why each dependency is needed

## 🔍 Code Review Process

### Before Submitting PR
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts

### PR Review Criteria
- **Functionality**: Does it work as intended?
- **Code Quality**: Is it readable and maintainable?
- **Testing**: Are there adequate tests?
- **Documentation**: Is it properly documented?
- **Performance**: Does it impact performance?
- **Security**: Are there any security implications?

## 🆘 Getting Help

### Resources
- 📖 **Documentation**: Check README.md and docs/
- 🐛 **Issues**: Search existing GitHub issues
- 💬 **Discussions**: Use GitHub Discussions for questions
- 📧 **Contact**: Create an issue for specific problems

### Development Environment Issues
1. **Run diagnostics**: `python3 setup.py`
2. **Check dependencies**: `poetry install`
3. **Verify environment**: Check `.env` file
4. **Test components**: `python3 simple_test.py`

## 🎉 Recognition

Contributors will be:
- Added to the contributors section in README
- Mentioned in release notes for significant contributions
- Given credit in code comments for major features

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to MCP Multi-Agent Deep Researcher! 🚀