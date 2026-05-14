"""Research Agent - Fetches knowledge using RAG."""

from typing import Any, Dict
from .base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """Agent responsible for researching event planning knowledge."""
    
    def __init__(self, rag_system=None):
        """Initialize research agent.
        
        Args:
            rag_system: RAG system instance
        """
        super().__init__("ResearchAgent")
        self.rag_system = rag_system
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Research event planning information.
        
        Args:
            input_data: Contains query and event context
            
        Returns:
            Research results from RAG system
        """
        self.log_execution("Researching event planning knowledge")
        
        query = input_data.get("query", "")
        event_type = input_data.get("event_type", "")
        
        # If RAG system is available, use it
        if self.rag_system:
            results = await self.rag_system.query(query, event_type)
            return {
                "knowledge": results.get("answer", ""),
                "sources": results.get("sources", []),
                "confidence": results.get("confidence", 0.0)
            }
        
        # Fallback: Return basic knowledge
        return {
            "knowledge": self._get_basic_knowledge(event_type),
            "sources": [],
            "confidence": 0.5
        }
    
    def _get_basic_knowledge(self, event_type: str) -> str:
        """Get basic event planning knowledge.
        
        Args:
            event_type: Type of event
            
        Returns:
            Basic knowledge string
        """
        knowledge_base = {
            "wedding": (
                "Wedding planning typically requires 6-12 months of preparation. "
                "Key priorities include venue, catering, photography, and decoration. "
                "Budget allocation: Venue (30%), Catering (25%), Photography (15%), "
                "Decoration (15%), Entertainment (10%), Others (5%)."
            ),
            "corporate": (
                "Corporate events require professional planning with focus on logistics. "
                "Key priorities include venue with AV facilities, catering, and accommodation. "
                "Budget allocation: Venue (35%), Catering (30%), AV Equipment (15%), "
                "Accommodation (15%), Others (5%)."
            ),
            "birthday": (
                "Birthday parties can be planned 2-4 weeks in advance. "
                "Key priorities include venue, cake, catering, and entertainment. "
                "Budget allocation: Venue (25%), Catering (30%), Entertainment (20%), "
                "Decoration (15%), Others (10%)."
            ),
        }
        return knowledge_base.get(event_type, "General event planning requires careful coordination of vendors and timeline management.")
