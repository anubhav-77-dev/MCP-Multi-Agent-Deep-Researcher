# 🚀 Quick Start Guide

## One-Command Launch

Start both frontend and backend servers with a single command:

```bash
python3 launcher.py
```

Or use the convenience scripts:

```bash
# Using the shell script
./start.sh

# Using make
make start
# or
make launch
# or  
make demo
```

## What the launcher does:

✅ **Checks all dependencies** (Poetry, Ollama, phi3 model)  
✅ **Starts backend API server** on http://localhost:8080  
✅ **Starts frontend web server** on http://localhost:3000  
✅ **Opens your browser** automatically  
✅ **Monitors both servers** and shows logs  
✅ **Handles cleanup** when you press Ctrl+C  

## Access Points:

- **🌐 Web Interface**: http://localhost:3000/frontend.html
- **🔌 API Endpoint**: http://localhost:8080
- **📚 API Documentation**: http://localhost:8080/docs

## Stopping the servers:

Press `Ctrl+C` in the terminal and the launcher will cleanly shut down both servers.

## Troubleshooting:

If the launcher fails to start:

1. Make sure Ollama is running: `ollama serve`
2. Ensure phi3 model is available: `ollama list`
3. Check your .env file has the LinkUp API key
4. Try running `poetry install` to ensure dependencies are current

The launcher provides detailed error messages to help diagnose any issues.