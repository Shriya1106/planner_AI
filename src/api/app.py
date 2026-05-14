"""FastAPI application."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Dict
import logging
from pathlib import Path

from ..models import EventRequest, EventPlan, KnowledgeQuery, KnowledgeResponse
from ..agents import AgentOrchestrator
from ..rag import RAGSystem, KnowledgeBase
from ..ml import BudgetPredictor
from ..config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI-powered event planning assistant"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount static files
    static_path = Path(__file__).parent.parent.parent / "static"
    if static_path.exists():
        app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    
    # Initialize components
    knowledge_base = KnowledgeBase()
    rag_system = RAGSystem(knowledge_base)
    ml_model = BudgetPredictor()
    orchestrator = AgentOrchestrator(rag_system, ml_model)
    
    @app.get("/")
    async def root():
        """Serve the main UI."""
        static_file = static_path / "index.html"
        if static_file.exists():
            return FileResponse(static_file)
        return {
            "message": "Welcome to Festiva Planner AI",
            "version": settings.app_version,
            "endpoints": {
                "plan_event": "/api/v1/plan",
                "query_knowledge": "/api/v1/knowledge/query",
                "health": "/health"
            }
        }
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version
        }
    
    @app.post("/api/v1/plan", response_model=EventPlan)
    async def plan_event(event_request: EventRequest):
        """Create event plan.
        
        Args:
            event_request: Event planning request
            
        Returns:
            Complete event plan
        """
        try:
            logger.info(f"Received event planning request: {event_request.event_type} in {event_request.city}")
            event_plan = await orchestrator.create_event_plan(event_request)
            return event_plan
        except Exception as e:
            logger.error(f"Error creating event plan: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/v1/knowledge/query", response_model=KnowledgeResponse)
    async def query_knowledge(query: KnowledgeQuery):
        """Query event planning knowledge.
        
        Args:
            query: Knowledge query
            
        Returns:
            Answer with sources
        """
        try:
            logger.info(f"Knowledge query: {query.query}")
            result = await rag_system.query(
                query.query,
                query.event_type,
                query.top_k
            )
            return KnowledgeResponse(**result)
        except Exception as e:
            logger.error(f"Error querying knowledge: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/v1/event-types")
    async def get_event_types():
        """Get supported event types."""
        return {
            "event_types": [
                {"value": "wedding", "label": "Wedding"},
                {"value": "corporate", "label": "Corporate Event"},
                {"value": "birthday", "label": "Birthday Party"},
                {"value": "anniversary", "label": "Anniversary"},
                {"value": "conference", "label": "Conference"},
                {"value": "party", "label": "Party"},
            ]
        }
    
    @app.get("/api/v1/vendor-categories")
    async def get_vendor_categories():
        """Get vendor categories."""
        return {
            "categories": [
                {"value": "venue", "label": "Venue"},
                {"value": "catering", "label": "Catering"},
                {"value": "decoration", "label": "Decoration"},
                {"value": "photography", "label": "Photography"},
                {"value": "entertainment", "label": "Entertainment"},
                {"value": "transportation", "label": "Transportation"},
                {"value": "accommodation", "label": "Accommodation"},
            ]
        }
    
    return app


# Create app instance
app = create_app()
