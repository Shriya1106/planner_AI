"""Simple script to run Festiva Planner AI server."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn

if __name__ == "__main__":
    print("🎉 Starting Festiva Planner AI...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 Documentation: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop\n")
    
    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
