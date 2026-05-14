"""Optimizer Agent - Optimizes budget allocation."""

from typing import Any, Dict, List
from .base_agent import BaseAgent
from ..models import BudgetBreakdown, VendorCategory


class OptimizerAgent(BaseAgent):
    """Agent responsible for optimizing budget allocation."""
    
    def __init__(self, ml_model=None):
        """Initialize optimizer agent.
        
        Args:
            ml_model: ML model for budget prediction
        """
        super().__init__("OptimizerAgent")
        self.ml_model = ml_model
        self._load_allocation_rules()
    
    def _load_allocation_rules(self):
        """Load budget allocation rules."""
        # Default allocation percentages by event type
        self.allocation_rules = {
            "wedding": {
                VendorCategory.VENUE: 0.30,
                VendorCategory.CATERING: 0.25,
                VendorCategory.PHOTOGRAPHY: 0.15,
                VendorCategory.DECORATION: 0.15,
                VendorCategory.ENTERTAINMENT: 0.10,
                VendorCategory.TRANSPORTATION: 0.05,
            },
            "corporate": {
                VendorCategory.VENUE: 0.35,
                VendorCategory.CATERING: 0.30,
                VendorCategory.ACCOMMODATION: 0.15,
                VendorCategory.ENTERTAINMENT: 0.15,
                VendorCategory.TRANSPORTATION: 0.05,
            },
            "birthday": {
                VendorCategory.VENUE: 0.25,
                VendorCategory.CATERING: 0.30,
                VendorCategory.ENTERTAINMENT: 0.20,
                VendorCategory.DECORATION: 0.15,
                VendorCategory.PHOTOGRAPHY: 0.10,
            },
        }
        
        # Priority levels by category
        self.priority_map = {
            VendorCategory.VENUE: 5,
            VendorCategory.CATERING: 5,
            VendorCategory.PHOTOGRAPHY: 4,
            VendorCategory.DECORATION: 3,
            VendorCategory.ENTERTAINMENT: 3,
            VendorCategory.TRANSPORTATION: 2,
            VendorCategory.ACCOMMODATION: 4,
        }
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize budget allocation.
        
        Args:
            input_data: Contains budget, event_type, and vendor_categories
            
        Returns:
            Optimized budget breakdown
        """
        self.log_execution("Optimizing budget allocation")
        
        total_budget = input_data["budget"]
        event_type = input_data["event_type"]
        vendor_categories = input_data["vendor_categories"]
        
        # Get allocation percentages
        allocations = self._get_allocations(event_type, vendor_categories)
        
        # Create budget breakdown
        budget_breakdown = []
        for category in vendor_categories:
            percentage = allocations.get(category, 0.1)
            allocated_amount = total_budget * percentage
            
            budget_breakdown.append(
                BudgetBreakdown(
                    category=category,
                    allocated_amount=allocated_amount,
                    percentage=percentage * 100,
                    priority=self.priority_map.get(category, 3)
                )
            )
        
        return {
            "budget_breakdown": budget_breakdown,
            "optimization_notes": self._generate_optimization_notes(total_budget, event_type)
        }
    
    def _get_allocations(self, event_type: str, vendor_categories: List[VendorCategory]) -> Dict[VendorCategory, float]:
        """Get budget allocation percentages.
        
        Args:
            event_type: Type of event
            event_type: Type of event
            vendor_categories: Required vendor categories
            
        Returns:
            Allocation percentages by category
        """
        # Get base allocations for event type
        base_allocations = self.allocation_rules.get(
            event_type,
            self.allocation_rules["birthday"]
        )
        
        # Filter to only required categories
        allocations = {}
        total = 0.0
        
        for category in vendor_categories:
            if category in base_allocations:
                allocations[category] = base_allocations[category]
                total += base_allocations[category]
        
        # Normalize to ensure sum is 1.0
        if total > 0:
            for category in allocations:
                allocations[category] = allocations[category] / total
        
        return allocations
    
    def _generate_optimization_notes(self, budget: float, event_type: str) -> List[str]:
        """Generate budget optimization notes.
        
        Args:
            budget: Total budget
            event_type: Type of event
            
        Returns:
            List of optimization notes
        """
        notes = []
        
        if budget < 100000:
            notes.append("Consider combining vendor services to reduce costs")
            notes.append("Look for package deals from venues")
            notes.append("Prioritize essential categories: venue and catering")
        elif budget < 500000:
            notes.append("Balance between quality and cost")
            notes.append("Allocate more to high-priority categories")
        else:
            notes.append("Consider premium vendors for better experience")
            notes.append("Invest in professional services across all categories")
        
        if event_type == "wedding":
            notes.append("Photography and videography are long-term investments")
        elif event_type == "corporate":
            notes.append("Ensure adequate budget for AV and technical requirements")
        
        return notes
