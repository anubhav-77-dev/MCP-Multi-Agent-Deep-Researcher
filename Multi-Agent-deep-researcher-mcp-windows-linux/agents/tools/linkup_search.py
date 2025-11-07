"""
LinkUp Search Tool

This tool implements web search functionality using the LinkUp API.
"""

import os
import requests
import logging
from typing import Any, Optional
from crewai.tools import BaseTool

logger = logging.getLogger(__name__)

class LinkUpSearchTool(BaseTool):
    """Tool for performing web searches using LinkUp API."""
    
    name: str = "LinkUp Web Search"
    description: str = "Search the web for current information using LinkUp API"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Store API configuration as instance attributes
        self._api_key = os.getenv('LINKUP_API_KEY')
        self._base_url = "https://api.linkup.so/v1/search"
        
        if not self._api_key:
            logger.warning("LinkUp API key not found. Web search may not work properly.")
    
    def _run(self, query: str) -> str:
        """Execute web search using LinkUp API."""
        if not self._api_key:
            return "Error: LinkUp API key not configured. Please set LINKUP_API_KEY environment variable."
        
        try:
            headers = {
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": query,
                "depth": "deep",
                "outputType": "searchResults"
            }
            
            logger.info(f"Searching LinkUp for: {query}")
            response = requests.post(self._base_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_search_results(data)
            else:
                logger.error(f"LinkUp API error: {response.status_code} - {response.text}")
                return f"Search failed with status {response.status_code}: {response.text}"
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during search: {str(e)}")
            return f"Network error during search: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error during search: {str(e)}")
            return f"Unexpected error during search: {str(e)}"
    
    def _format_search_results(self, data: dict) -> str:
        """Format search results into a readable string."""
        try:
            results = data.get('results', [])
            
            if not results:
                return "No search results found."
            
            formatted_results = []
            formatted_results.append(f"Web Search Results ({len(results)} results found):\n")
            
            for i, result in enumerate(results[:10], 1):  # Limit to top 10 results
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                snippet = result.get('content', result.get('snippet', 'No description available'))
                
                # Truncate snippet if too long
                if len(snippet) > 300:
                    snippet = snippet[:300] + "..."
                
                formatted_results.append(f"{i}. **{title}**")
                formatted_results.append(f"   URL: {url}")
                formatted_results.append(f"   Summary: {snippet}")
                formatted_results.append("")
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"Error formatting search results: {str(e)}")
            return f"Error formatting search results: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the search."""
        return self._run(query)