"""Base agent class for multi-agent system."""

from abc import ABC, abstractmethod
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, name: str):
        """Initialize agent.
        
        Args:
            name: Agent name
        """
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent task.
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Agent execution result
        """
        pass
    
    def log_execution(self, action: str, details: str = ""):
        """Log agent execution.
        
        Args:
            action: Action being performed
            details: Additional details
        """
        self.logger.info(f"[{self.name}] {action} {details}")
