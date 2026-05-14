"""Knowledge base management for RAG system."""

from typing import List, Dict
import os
import json
import logging

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Manages event planning knowledge base."""
    
    def __init__(self, data_dir: str = "./data/knowledge"):
        """Initialize knowledge base.
        
        Args:
            data_dir: Directory containing knowledge documents
        """
        self.data_dir = data_dir
        self.documents = []
        self._load_default_knowledge()
    
    def _load_default_knowledge(self):
        """Load default event planning knowledge."""
        self.documents = [
            {
                "id": "wedding_timeline",
                "title": "Wedding Planning Timeline",
                "content": """
                Wedding planning typically requires 6-12 months of preparation. Here's a comprehensive timeline:
                
                12 Months Before:
                - Set budget and guest list
                - Book venue
                - Hire wedding planner (optional)
                
                9-10 Months Before:
                - Book photographer and videographer
                - Select and order wedding dress
                - Book caterer
                
                6-8 Months Before:
                - Send save-the-date cards
                - Book florist and decorator
                - Arrange transportation
                
                3-4 Months Before:
                - Finalize menu
                - Order wedding cake
                - Book entertainment (DJ/band)
                
                1-2 Months Before:
                - Final dress fitting
                - Confirm all vendor bookings
                - Create seating chart
                
                1 Week Before:
                - Final venue walkthrough
                - Confirm guest count with caterer
                - Pack for honeymoon
                """,
                "category": "wedding",
                "tags": ["timeline", "checklist", "planning"]
            },
            {
                "id": "wedding_budget",
                "title": "Wedding Budget Allocation Guide",
                "content": """
                Typical wedding budget allocation:
                
                Venue (30%): The largest expense, includes rental, setup, and basic amenities
                Catering (25%): Food and beverages for guests
                Photography & Videography (15%): Professional documentation
                Decoration & Flowers (15%): Theme decoration, floral arrangements
                Entertainment (10%): DJ, band, or live performers
                Transportation (5%): Guest transportation, couple's car
                
                Budget-saving tips:
                - Consider off-season dates for better rates
                - Opt for buffet instead of plated meals
                - Use seasonal flowers
                - Limit guest list to reduce costs
                - Book vendors early for better deals
                """,
                "category": "wedding",
                "tags": ["budget", "allocation", "costs"]
            },
            {
                "id": "corporate_event_planning",
                "title": "Corporate Event Planning Best Practices",
                "content": """
                Corporate event planning requires attention to professional details:
                
                Key Considerations:
                - Define clear objectives (networking, training, celebration)
                - Choose accessible venue with parking
                - Ensure proper AV equipment and technical support
                - Plan for dietary restrictions
                - Arrange accommodation for out-of-town attendees
                
                Budget Allocation:
                - Venue (35%): Conference facilities with AV
                - Catering (30%): Professional meals and refreshments
                - Accommodation (15%): Hotel rooms for attendees
                - AV & Technology (15%): Equipment and technical support
                - Transportation (5%): Shuttle services
                
                Timeline:
                - 3 months before: Book venue and send invitations
                - 2 months before: Finalize agenda and speakers
                - 1 month before: Confirm catering and AV requirements
                - 1 week before: Final headcount and logistics check
                """,
                "category": "corporate",
                "tags": ["corporate", "conference", "business"]
            },
            {
                "id": "birthday_party_guide",
                "title": "Birthday Party Planning Guide",
                "content": """
                Birthday party planning can be fun and stress-free with proper planning:
                
                4 Weeks Before:
                - Decide on theme and guest list
                - Book venue (restaurant, party hall, or home)
                - Send invitations
                
                2-3 Weeks Before:
                - Order custom cake
                - Plan menu and book caterer
                - Arrange entertainment (DJ, games, activities)
                
                1 Week Before:
                - Confirm RSVPs
                - Buy decorations
                - Finalize activity schedule
                
                Budget Tips:
                - Home parties save venue costs
                - DIY decorations reduce expenses
                - Potluck style can lower catering costs
                - Digital invitations are free
                
                Budget Allocation:
                - Catering & Cake (30%)
                - Venue (25%)
                - Entertainment (20%)
                - Decoration (15%)
                - Photography (10%)
                """,
                "category": "birthday",
                "tags": ["birthday", "party", "celebration"]
            },
            {
                "id": "vendor_selection",
                "title": "How to Select Event Vendors",
                "content": """
                Selecting the right vendors is crucial for event success:
                
                Research Phase:
                - Get recommendations from friends and family
                - Read online reviews and ratings
                - Check vendor portfolios and past work
                - Compare at least 3 vendors per category
                
                Evaluation Criteria:
                - Experience in your event type
                - Availability on your date
                - Pricing and payment terms
                - Cancellation and refund policy
                - Insurance and licenses
                
                Questions to Ask:
                - What's included in the package?
                - Do you have backup plans?
                - Can you provide references?
                - What's your payment schedule?
                - How do you handle changes or emergencies?
                
                Red Flags:
                - No contract or vague terms
                - Pressure to book immediately
                - No portfolio or references
                - Prices significantly lower than market rate
                - Poor communication or unprofessional behavior
                """,
                "category": "general",
                "tags": ["vendors", "selection", "tips"]
            },
            {
                "id": "event_contingency_planning",
                "title": "Event Contingency Planning",
                "content": """
                Always have backup plans for your event:
                
                Weather Contingencies:
                - Indoor backup for outdoor events
                - Tent or canopy rentals
                - Weather monitoring and decision timeline
                
                Vendor Contingencies:
                - Backup vendor contacts
                - Vendor cancellation clauses in contracts
                - Emergency contact numbers
                
                Technical Contingencies:
                - Backup AV equipment
                - Generator for power outages
                - IT support on standby
                
                Guest Contingencies:
                - Extra food for unexpected guests
                - Flexible seating arrangements
                - First aid kit and emergency contacts
                
                Communication Plan:
                - Emergency contact list
                - Vendor coordination system
                - Guest notification method
                """,
                "category": "general",
                "tags": ["contingency", "backup", "emergency"]
            }
        ]
        
        logger.info(f"Loaded {len(self.documents)} knowledge documents")
    
    def add_document(self, document: Dict):
        """Add document to knowledge base.
        
        Args:
            document: Document with id, title, content, category, tags
        """
        self.documents.append(document)
        logger.info(f"Added document: {document['title']}")
    
    def get_documents(self, category: str = None) -> List[Dict]:
        """Get documents from knowledge base.
        
        Args:
            category: Filter by category (optional)
            
        Returns:
            List of documents
        """
        if category:
            return [doc for doc in self.documents if doc.get("category") == category]
        return self.documents
    
    def search_by_tags(self, tags: List[str]) -> List[Dict]:
        """Search documents by tags.
        
        Args:
            tags: List of tags to search for
            
        Returns:
            Matching documents
        """
        results = []
        for doc in self.documents:
            doc_tags = doc.get("tags", [])
            if any(tag in doc_tags for tag in tags):
                results.append(doc)
        return results
    
    def save_to_file(self, filepath: str):
        """Save knowledge base to JSON file.
        
        Args:
            filepath: Path to save file
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.documents, f, indent=2)
        logger.info(f"Knowledge base saved to {filepath}")
    
    def load_from_file(self, filepath: str):
        """Load knowledge base from JSON file.
        
        Args:
            filepath: Path to load file from
        """
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.documents = json.load(f)
            logger.info(f"Knowledge base loaded from {filepath}")
        else:
            logger.warning(f"File not found: {filepath}")
