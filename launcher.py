#!/usr/bin/env python3
"""
MCP Multi-Agent Deep Researcher Launcher

This script starts both the backend API server and frontend HTTP server
in a single command for easy development and usage.
"""

import os
import sys
import time
import signal
import subprocess
import threading
import webbrowser
from pathlib import Path

class MCPLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def check_dependencies(self):
        """Check if all required dependencies are available."""
        print("🔍 Checking dependencies...")
        
        # Check if Poetry is available
        try:
            subprocess.run(['poetry', '--version'], capture_output=True, check=True)
            print("✅ Poetry is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Poetry not found. Please install Poetry first.")
            return False
        
        # Check if .env file exists
        env_file = self.project_root / '.env'
        if not env_file.exists():
            print("⚠️  .env file not found. Creating from template...")
            env_example = self.project_root / '.env.example'
            if env_example.exists():
                import shutil
                shutil.copy(env_example, env_file)
                print("✅ .env file created. Please configure your API keys.")
            else:
                print("❌ .env.example not found. Please create .env file manually.")
                return False
        else:
            print("✅ .env file found")
        
        # Check if Ollama is running
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Ollama is running")
                # Check if phi3 model is available
                if 'phi3' in result.stdout:
                    print("✅ phi3 model is available")
                else:
                    print("⚠️  phi3 model not found. Will try to pull it...")
                    try:
                        subprocess.run(['ollama', 'pull', 'phi3'], check=True)
                        print("✅ phi3 model pulled successfully")
                    except subprocess.CalledProcessError:
                        print("❌ Failed to pull phi3 model")
                        return False
            else:
                print("❌ Ollama is not running. Please start Ollama first.")
                return False
        except FileNotFoundError:
            print("❌ Ollama not found. Please install Ollama first.")
            return False
        
        return True
    
    def start_backend(self):
        """Start the backend API server."""
        print("🚀 Starting backend API server...")
        
        backend_dir = self.project_root / "Multi-Agent-deep-researcher-mcp-windows-linux"
        server_script = backend_dir / "http_server.py"
        
        if not server_script.exists():
            print(f"❌ Backend server script not found: {server_script}")
            return False
        
        # Set environment variables for the backend
        env = os.environ.copy()
        env.update({
            'OPENAI_API_KEY': 'ollama',
            'OPENAI_API_BASE': 'http://localhost:11434/v1',
        })
        
        try:
            self.backend_process = subprocess.Popen(
                ['poetry', 'run', 'python', str(server_script)],
                cwd=str(self.project_root),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Wait a bit for the process to start
            time.sleep(3)
            
            # Monitor backend startup
            backend_ready = False
            for i in range(15):  # Wait up to 15 seconds
                if self.backend_process.poll() is not None:
                    # Process exited, get the error
                    stdout, stderr = self.backend_process.communicate()
                    print(f"❌ Backend server failed to start:")
                    if stdout:
                        print(f"   Output: {stdout}")
                    if stderr:
                        print(f"   Error: {stderr}")
                    return False
                
                try:
                    # Try to connect to the health endpoint
                    import urllib.request
                    with urllib.request.urlopen('http://localhost:8080/health', timeout=1) as response:
                        if response.status == 200:
                            backend_ready = True
                            break
                except Exception:
                    pass
                
                time.sleep(1)
            
            if backend_ready:
                print("✅ Backend API server is running on http://localhost:8080")
                return True
            else:
                print("⚠️  Backend server started but health check failed")
                return True  # Continue anyway
                
        except Exception as e:
            print(f"❌ Failed to start backend server: {e}")
            return False
    
    def start_frontend(self):
        """Start the frontend HTTP server."""
        print("🌐 Starting frontend HTTP server...")
        
        try:
            self.frontend_process = subprocess.Popen(
                [sys.executable, '-m', 'http.server', '3000'],
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Wait a moment for the server to start
            time.sleep(2)
            
            if self.frontend_process.poll() is None:
                print("✅ Frontend HTTP server is running on http://localhost:3000")
                return True
            else:
                print("❌ Frontend server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start frontend server: {e}")
            return False
    
    def monitor_processes(self):
        """Monitor both processes and restart if needed."""
        def monitor_backend():
            if self.backend_process:
                for line in self.backend_process.stdout:
                    if self.running:
                        print(f"[Backend] {line.strip()}")
        
        def monitor_frontend():
            if self.frontend_process:
                for line in self.frontend_process.stdout:
                    if self.running:
                        print(f"[Frontend] {line.strip()}")
        
        if self.backend_process:
            threading.Thread(target=monitor_backend, daemon=True).start()
        
        if self.frontend_process:
            threading.Thread(target=monitor_frontend, daemon=True).start()
    
    def open_browser(self):
        """Open the frontend in the default browser."""
        print("🌍 Opening browser...")
        try:
            webbrowser.open('http://localhost:3000/frontend.html')
            print("✅ Browser opened to http://localhost:3000/frontend.html")
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")
            print("   Please manually open: http://localhost:3000/frontend.html")
    
    def cleanup(self):
        """Clean up processes on exit."""
        print("\n🛑 Shutting down servers...")
        self.running = False
        
        if self.backend_process:
            print("   Stopping backend server...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
        
        if self.frontend_process:
            print("   Stopping frontend server...")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
        
        print("✅ Cleanup complete")
    
    def signal_handler(self, signum, frame):
        """Handle interrupt signals."""
        self.cleanup()
        sys.exit(0)
    
    def run(self):
        """Main launcher function."""
        print("=" * 60)
        print("🤖 MCP Multi-Agent Deep Researcher Launcher")
        print("=" * 60)
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Check dependencies
            if not self.check_dependencies():
                print("\n❌ Dependency check failed. Please fix the issues above.")
                return 1
            
            print("\n" + "=" * 60)
            
            # Start backend
            if not self.start_backend():
                print("❌ Failed to start backend. Exiting.")
                return 1
            
            # Start frontend
            if not self.start_frontend():
                print("❌ Failed to start frontend. Exiting.")
                self.cleanup()
                return 1
            
            # Start monitoring
            self.monitor_processes()
            
            print("\n" + "=" * 60)
            print("🎉 Both servers are running!")
            print("📱 Frontend: http://localhost:3000/frontend.html")
            print("🔌 Backend API: http://localhost:8080")
            print("📚 API Docs: http://localhost:8080/docs")
            print("\n💡 Try these sample queries:")
            print("   • What are the latest AI trends in 2024?")
            print("   • How does quantum computing work?")
            print("   • Environmental impacts of cryptocurrency mining")
            print("\n⌨️  Press Ctrl+C to stop both servers")
            print("=" * 60)
            
            # Open browser after a short delay
            time.sleep(2)
            self.open_browser()
            
            # Keep the main thread alive
            try:
                while self.running:
                    time.sleep(1)
                    
                    # Check if processes are still running
                    if self.backend_process and self.backend_process.poll() is not None:
                        print("⚠️  Backend process stopped unexpectedly")
                        break
                    
                    if self.frontend_process and self.frontend_process.poll() is not None:
                        print("⚠️  Frontend process stopped unexpectedly")
                        break
                        
            except KeyboardInterrupt:
                pass
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return 1
        
        finally:
            self.cleanup()
        
        return 0

def main():
    """Entry point."""
    launcher = MCPLauncher()
    return launcher.run()

if __name__ == "__main__":
    sys.exit(main())