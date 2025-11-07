"""
Ollama LLM Tool

This tool provides integration with Ollama for local LLM processing.
"""

import os
import requests
import logging
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)

class OllamaLLMTool:
    """Tool for interacting with Ollama local LLMs."""
    
    def __init__(self):
        self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model_name = os.getenv('MODEL_NAME', 'phi3:latest')
        self.headers = {'Content-Type': 'application/json'}
    
    def get_llm(self):
        """Get LLM configuration for CrewAI agents."""
        # Use string-based configuration which works with newer CrewAI versions
        return f"ollama/{self.model_name}"
    
    def _create_fallback_llm(self):
        """Create a fallback LLM configuration."""
        class FallbackLLM:
            def __init__(self, model_name: str, base_url: str):
                self.model_name = model_name
                self.base_url = base_url
            
            def generate(self, prompt: str) -> str:
                return self._call_ollama(prompt)
            
            def _call_ollama(self, prompt: str) -> str:
                try:
                    url = f"{self.base_url}/api/generate"
                    payload = {
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False
                    }
                    
                    response = requests.post(url, json=payload, timeout=120)
                    if response.status_code == 200:
                        return response.json().get('response', '')
                    else:
                        return f"Error: {response.status_code}"
                except Exception as e:
                    return f"Error calling Ollama: {str(e)}"
        
        return FallbackLLM(self.model_name, self.base_url)
    
    def check_model_availability(self) -> bool:
        """Check if the specified model is available in Ollama."""
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [model['name'] for model in models]
                return self.model_name in available_models
            else:
                logger.error(f"Failed to check Ollama models: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error checking Ollama model availability: {str(e)}")
            return False
    
    def pull_model(self) -> bool:
        """Pull the specified model if it's not available."""
        try:
            url = f"{self.base_url}/api/pull"
            payload = {"name": self.model_name}
            
            logger.info(f"Pulling model {self.model_name}...")
            response = requests.post(url, json=payload, timeout=300)
            
            if response.status_code == 200:
                logger.info(f"Model {self.model_name} pulled successfully")
                return True
            else:
                logger.error(f"Failed to pull model: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error pulling model: {str(e)}")
            return False
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using the Ollama model."""
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                **kwargs
            }
            
            response = requests.post(url, json=payload, timeout=120)
            
            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                logger.error(f"Ollama generation failed: {response.status_code}")
                return f"Error generating text: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return f"Error generating text: {str(e)}"