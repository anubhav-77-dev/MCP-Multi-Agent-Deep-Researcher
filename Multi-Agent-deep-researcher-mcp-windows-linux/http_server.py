#!/usr/bin/env python3
"""
FastAPI HTTP Server for MCP Multi-Agent Deep Researcher

Provides HTTP endpoints for direct access to research functionality.
"""

import asyncio
import logging
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

from agents.research_crew import ResearchCrew

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="MCP Multi-Agent Deep Researcher",
    description="Multi-agent research system with web search and AI synthesis",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize research crew
research_crew = ResearchCrew()

class ResearchRequest(BaseModel):
    """Request model for research queries."""
    query: str

class ResearchResponse(BaseModel):
    """Response model for research results."""
    result: str
    status: str = "success"

@app.post("/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest) -> ResearchResponse:
    """Conduct comprehensive research using the multi-agent workflow."""
    try:
        logger.info(f"Received research request: {request.query}")
        
        result = await research_crew.conduct_research(request.query)
        
        return ResearchResponse(result=result)
        
    except Exception as e:
        logger.error(f"Error in research endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=ResearchResponse)
async def quick_search(request: ResearchRequest) -> ResearchResponse:
    """Perform quick web search."""
    try:
        logger.info(f"Received search request: {request.query}")
        
        result = await research_crew.quick_search(request.query)
        
        return ResearchResponse(result=result)
        
    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "MCP Multi-Agent Deep Researcher"}

@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint with basic information."""
    return {
        "service": "MCP Multi-Agent Deep Researcher",
        "version": "0.1.0",
        "endpoints": {
            "research": "POST /research - Comprehensive research with multi-agent workflow",
            "search": "POST /search - Quick web search",
            "health": "GET /health - Health check"
        }
    }

if __name__ == "__main__":
    logger.info("Starting FastAPI server for MCP Multi-Agent Deep Researcher...")
    
    uvicorn.run(
        "http_server:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=True
    )