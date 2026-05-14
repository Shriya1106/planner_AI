"""Main entry point for Festiva Planner AI."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import uvicorn
from src.config import settings


def main():
    """Run the FastAPI application."""
    uvicorn.run(
        "src.api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level="info"
    )


if __name__ == "__main__":
    main()
