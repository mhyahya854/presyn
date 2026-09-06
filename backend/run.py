"""Entrypoint script for launching the Presyn backend server."""

import sys
from pathlib import Path

if __name__ == "__main__":
    # Ensure repository root is on sys.path
    ROOT = Path(__file__).resolve().parent.parent
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    import uvicorn
    from backend.app.core.config import settings

    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower(),
        reload=settings.ENVIRONMENT == "development",
    )
