"""Planner Agent - Creates event plans."""

from typing import Any, Dict, List
from .base_agent import BaseAgent
from ..models import EventRequest, EventPlan, TimelineTask, VendorCategory


class PlannerAgent(BaseAgent):
    """Agent responsible for creating event plans."""
    
    def __init__(self):
        """Initialize planner agent."""
        super().__init__("PlannerAgent")
        self._load_templates()
    
    def _load_templates(self):
        """Load event planning templates."""
        # Wedding timeline template
        self.wedding_timeline = [
            TimelineTask(
                task_name="Book Venue",
                description="Research and book the wedding venue",
                days_before_event=180,
                category=VendorCategory.VENUE,
                is_critical=True
            ),
            TimelineTask(
                task_name="Hire Photographer",
                description="Book professional photographer and videographer",
                days_before_event=150,
                category=VendorCategory.PHOTOGRAPHY,
                is_critical=True
            ),
            TimelineTask(
                task_name="Select Caterer",
                description="Finalize menu and catering service",
                days_before_event=120,
                category=VendorCategory.CATERING,
                is_critical=True
            ),
            TimelineTask(
                task_name="Plan Decoration",
                description="Decide theme and book decoration service",
                days_before_event=90,
                category=VendorCategory.DECORATION,
                is_critical=False
            ),
            TimelineTask(
                task_name="Book Entertainment",
                description="Arrange DJ, band, or entertainment",
                days_before_event=60,
                category=VendorCategory.ENTERTAINMENT,
                is_critical=False
            ),
            TimelineTask(
                task_name="Arrange Transportation",
                description="Book transportation for guests",
                days_before_event=30,
                category=VendorCategory.TRANSPORTATION,
                is_critical=False
            ),
        ]
        
        # Corporate event timeline
        self.corporate_timeline = [
            TimelineTask(
                task_name="Book Conference Venue",
                description="Reserve conference hall or hotel",
                days_before_event=90,
                category=VendorCategory.VENUE,
                is_critical=True
            ),
            TimelineTask(
                task_name="Arrange Catering",
                description="Book catering for meals and refreshments",
                days_before_event=60,
                category=VendorCategory.CATERING,
                is_critical=True
            ),
            TimelineTask(
                task_name="Setup AV Equipment",
                description="Arrange audio-visual equipment",
                days_before_event=30,
                category=VendorCategory.ENTERTAINMENT,
                is_critical=True
            ),
            TimelineTask(
                task_name="Book Accommodation",
                description="Reserve hotel rooms for attendees",
                days_before_event=45,
                category=VendorCategory.ACCOMMODATION,
                is_critical=False
            ),
        ]
        
        # Birthday party timeline
        self.birthday_timeline = [
            TimelineTask(
                task_name="Book Venue",
                description="Reserve party venue or restaurant",
                days_before_event=30,
                category=VendorCategory.VENUE,
                is_critical=True
            ),
            TimelineTask(
                task_name="Order Cake and Catering",
                description="Finalize cake design and food menu",
                days_before_event=14,
                category=VendorCategory.CATERING,
                is_critical=True
            ),
            TimelineTask(
                task_name="Plan Decoration",
                description="Arrange balloons, banners, and theme decoration",
                days_before_event=7,
                category=VendorCategory.DECORATION,
                is_critical=False
            ),
            TimelineTask(
                task_name="Book Entertainment",
                description="Arrange DJ, games, or entertainment",
                days_before_event=14,
                category=VendorCategory.ENTERTAINMENT,
                is_critical=False
            ),
        ]
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create event plan.
        
        Args:
            input_data: Contains EventRequest
            
        Returns:
            Initial event plan structure
        """
        self.log_execution("Creating event plan")
        
        event_request: EventRequest = input_data["event_request"]
        
        # Select timeline based on event type
        timeline = self._get_timeline_template(event_request.event_type)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(event_request)
        
        return {
            "timeline": timeline,
            "recommendations": recommendations,
            "vendor_categories": self._get_required_vendors(event_request.event_type)
        }
    
    def _get_timeline_template(self, event_type: str) -> List[TimelineTask]:
        """Get timeline template for event type.
        
        Args:
            event_type: Type of event
            
        Returns:
            List of timeline tasks
        """
        templates = {
            "wedding": self.wedding_timeline,
            "corporate": self.corporate_timeline,
            "birthday": self.birthday_timeline,
            "anniversary": self.wedding_timeline,  # Similar to wedding
            "conference": self.corporate_timeline,  # Similar to corporate
            "party": self.birthday_timeline,  # Similar to birthday
        }
        return templates.get(event_type, self.birthday_timeline)
    
    def _get_required_vendors(self, event_type: str) -> List[VendorCategory]:
        """Get required vendor categories for event type.
        
        Args:
            event_type: Type of event
            
        Returns:
            List of vendor categories
        """
        vendor_map = {
            "wedding": [
                VendorCategory.VENUE,
                VendorCategory.CATERING,
                VendorCategory.DECORATION,
                VendorCategory.PHOTOGRAPHY,
                VendorCategory.ENTERTAINMENT,
                VendorCategory.TRANSPORTATION,
            ],
            "corporate": [
                VendorCategory.VENUE,
                VendorCategory.CATERING,
                VendorCategory.ACCOMMODATION,
                VendorCategory.ENTERTAINMENT,
            ],
            "birthday": [
                VendorCategory.VENUE,
                VendorCategory.CATERING,
                VendorCategory.DECORATION,
                VendorCategory.ENTERTAINMENT,
            ],
        }
        return vendor_map.get(event_type, vendor_map["birthday"])
    
    def _generate_recommendations(self, event_request: EventRequest) -> List[str]:
        """Generate event recommendations.
        
        Args:
            event_request: Event request details
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Budget-based recommendations
        if event_request.budget < 100000:
            recommendations.append("Consider outdoor venues to reduce costs")
            recommendations.append("Opt for buffet-style catering instead of plated meals")
        elif event_request.budget > 500000:
            recommendations.append("Consider premium venues with in-house services")
            recommendations.append("Invest in professional photography and videography")
        
        # Event type recommendations
        if event_request.event_type == "wedding":
            recommendations.append("Book vendors at least 6 months in advance")
            recommendations.append("Create a backup plan for outdoor venues")
        elif event_request.event_type == "corporate":
            recommendations.append("Ensure venue has proper AV equipment")
            recommendations.append("Arrange for parking and transportation")
        
        # Preference-based recommendations
        if "outdoor" in event_request.preferences:
            recommendations.append("Check weather forecasts and have contingency plans")
        if "traditional" in event_request.preferences:
            recommendations.append("Look for vendors experienced in traditional events")
        
        return recommendations
