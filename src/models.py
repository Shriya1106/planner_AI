"""Data models for Festiva Planner AI."""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum


class EventType(str, Enum):
    """Supported event types."""
    WEDDING = "wedding"
    CORPORATE = "corporate"
    BIRTHDAY = "birthday"
    ANNIVERSARY = "anniversary"
    CONFERENCE = "conference"
    PARTY = "party"


class EventRequest(BaseModel):
    """Event planning request model."""
    event_type: EventType
    city: str
    budget: float = Field(..., gt=0, description="Budget in INR")
    guest_count: Optional[int] = Field(None, gt=0)
    date: Optional[str] = None
    preferences: List[str] = Field(default_factory=list)
    special_requirements: Optional[str] = None


class VendorCategory(str, Enum):
    """Vendor categories."""
    VENUE = "venue"
    CATERING = "catering"
    DECORATION = "decoration"
    PHOTOGRAPHY = "photography"
    ENTERTAINMENT = "entertainment"
    TRANSPORTATION = "transportation"
    ACCOMMODATION = "accommodation"


class BudgetBreakdown(BaseModel):
    """Budget allocation per category."""
    category: VendorCategory
    allocated_amount: float
    percentage: float
    priority: int = Field(..., ge=1, le=5)


class TimelineTask(BaseModel):
    """Event timeline task."""
    task_name: str
    description: str
    days_before_event: int
    category: VendorCategory
    is_critical: bool = False


class VendorSuggestion(BaseModel):
    """Vendor recommendation."""
    name: str
    category: VendorCategory
    estimated_cost: float
    rating: Optional[float] = None
    description: Optional[str] = None


class EventPlan(BaseModel):
    """Complete event plan."""
    event_type: EventType
    city: str
    total_budget: float
    budget_breakdown: List[BudgetBreakdown]
    timeline: List[TimelineTask]
    vendor_suggestions: List[VendorSuggestion]
    recommendations: List[str]
    estimated_guest_count: Optional[int] = None


class KnowledgeQuery(BaseModel):
    """RAG knowledge query."""
    query: str
    event_type: Optional[EventType] = None
    top_k: int = Field(default=5, ge=1, le=10)


class KnowledgeResponse(BaseModel):
    """RAG knowledge response."""
    answer: str
    sources: List[Dict[str, str]]
    confidence: float = Field(..., ge=0.0, le=1.0)
