"""Agent Orchestrator - Coordinates multi-agent workflow."""

from typing import Dict, Any
from .planner_agent import PlannerAgent
from .research_agent import ResearchAgent
from .optimizer_agent import OptimizerAgent
from ..models import EventRequest, EventPlan, VendorSuggestion
import logging

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Orchestrates multiple agents to create complete event plans."""
    
    def __init__(self, rag_system=None, ml_model=None):
        """Initialize orchestrator with agents.
        
        Args:
            rag_system: RAG system for knowledge retrieval
            ml_model: ML model for budget optimization
        """
        self.planner_agent = PlannerAgent()
        self.research_agent = ResearchAgent(rag_system)
        self.optimizer_agent = OptimizerAgent(ml_model)
        self.logger = logging.getLogger(__name__)
    
    async def create_event_plan(self, event_request: EventRequest) -> EventPlan:
        """Create complete event plan using multi-agent workflow.
        
        Args:
            event_request: Event planning request
            
        Returns:
            Complete event plan
        """
        self.logger.info(f"Creating event plan for {event_request.event_type} in {event_request.city}")
        
        # Step 1: Planner Agent creates initial plan
        planner_result = await self.planner_agent.execute({
            "event_request": event_request
        })
        
        # Step 2: Research Agent gathers knowledge
        research_result = await self.research_agent.execute({
            "query": f"Best practices for {event_request.event_type} planning",
            "event_type": event_request.event_type
        })
        
        # Step 3: Optimizer Agent optimizes budget
        optimizer_result = await self.optimizer_agent.execute({
            "budget": event_request.budget,
            "event_type": event_request.event_type,
            "vendor_categories": planner_result["vendor_categories"]
        })
        
        # Step 4: Generate vendor suggestions
        vendor_suggestions = self._generate_vendor_suggestions(
            event_request,
            optimizer_result["budget_breakdown"]
        )
        
        # Step 5: Combine results into complete plan
        event_plan = EventPlan(
            event_type=event_request.event_type,
            city=event_request.city,
            total_budget=event_request.budget,
            budget_breakdown=optimizer_result["budget_breakdown"],
            timeline=planner_result["timeline"],
            vendor_suggestions=vendor_suggestions,
            recommendations=planner_result["recommendations"] + optimizer_result["optimization_notes"],
            estimated_guest_count=event_request.guest_count
        )
        
        self.logger.info("Event plan created successfully")
        return event_plan
    
    def _generate_vendor_suggestions(
        self,
        event_request: EventRequest,
        budget_breakdown
    ) -> list:
        """Generate vendor suggestions based on budget.
        
        Args:
            event_request: Event request details
            budget_breakdown: Budget allocation per category
            
        Returns:
            List of vendor suggestions
        """
        vendors = []
        
        # Sample vendor data (in production, this would come from a database)
        vendor_templates = {
            "venue": [
                {"name": "Grand Palace Hotel", "rating": 4.5, "multiplier": 1.2},
                {"name": "Garden View Resort", "rating": 4.3, "multiplier": 1.0},
                {"name": "City Convention Center", "rating": 4.0, "multiplier": 0.8},
            ],
            "catering": [
                {"name": "Royal Caterers", "rating": 4.6, "multiplier": 1.1},
                {"name": "Spice Kitchen", "rating": 4.4, "multiplier": 1.0},
                {"name": "Budget Bites", "rating": 4.0, "multiplier": 0.7},
            ],
            "photography": [
                {"name": "Moments Studio", "rating": 4.8, "multiplier": 1.3},
                {"name": "Capture Memories", "rating": 4.5, "multiplier": 1.0},
                {"name": "Quick Shots", "rating": 4.2, "multiplier": 0.8},
            ],
            "decoration": [
                {"name": "Dream Decorators", "rating": 4.5, "multiplier": 1.1},
                {"name": "Elegant Events", "rating": 4.3, "multiplier": 1.0},
                {"name": "Simple Decor", "rating": 4.0, "multiplier": 0.7},
            ],
            "entertainment": [
                {"name": "Party Rockers DJ", "rating": 4.6, "multiplier": 1.2},
                {"name": "Live Band Express", "rating": 4.4, "multiplier": 1.0},
                {"name": "Music Mix", "rating": 4.1, "multiplier": 0.8},
            ],
        }
        
        for breakdown in budget_breakdown:
            category_key = breakdown.category.value
            if category_key in vendor_templates:
                # Select vendor based on budget (higher budget = premium vendor)
                vendor_list = vendor_templates[category_key]
                
                # Choose vendor based on allocated amount
                if breakdown.allocated_amount > 200000:
                    vendor_data = vendor_list[0]  # Premium
                elif breakdown.allocated_amount > 100000:
                    vendor_data = vendor_list[1]  # Mid-range
                else:
                    vendor_data = vendor_list[2]  # Budget
                
                vendors.append(
                    VendorSuggestion(
                        name=vendor_data["name"],
                        category=breakdown.category,
                        estimated_cost=breakdown.allocated_amount * vendor_data["multiplier"],
                        rating=vendor_data["rating"],
                        description=f"Recommended {category_key} service in {event_request.city}"
                    )
                )
        
        return vendors
