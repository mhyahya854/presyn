"""Presyn FastAPI Application Entrypoint."""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.api.router import api_v1_router
from backend.app.camera.events import live_event_hub
from backend.app.camera.manager import camera_manager
from backend.app.core.config import settings
from backend.app.core.exceptions import PresynException
from backend.app.core.logging import logger
import backend.app.db.models  # noqa: F401
from backend.app.db.session import ensure_data_directory, get_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager handling startup and shutdown events."""
    logger.info("Initializing Presyn Platform (Environment: %s)", settings.ENVIRONMENT)
    ensure_data_directory(settings.DATABASE_URL)

    # Register asyncio loop with LiveEventHub for async event broadcasting from worker threads
    live_event_hub.set_loop(asyncio.get_running_loop())

    # Launch background capture workers for any pre-configured active cameras
    try:
        db_gen = get_db()
        db = next(db_gen)
        try:
            camera_manager.startup_active_cameras(db)
        finally:
            try:
                next(db_gen)
            except StopIteration:
                pass
    except Exception as exc:
        logger.warning("Could not auto-start cameras on startup: %s", exc)

    yield

    logger.info("Shutting down Presyn Platform - stopping all camera workers")
    camera_manager.stop_all(timeout=3.0)
    logger.info("Presyn Platform shutdown complete")


app = FastAPI(
    title="Presyn Platform API",
    description="CPU-first local workplace presence, CCTV intelligence, and attendance API foundation.",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure Cross-Origin Resource Sharing (CORS) using explicit local development origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Register versioned API routers
app.include_router(api_v1_router)


@app.exception_handler(PresynException)
async def presyn_exception_handler(request: Request, exc: PresynException) -> JSONResponse:
    """Structured handler for domain-specific Presyn exceptions."""
    logger.warning("Domain exception on %s: %s [%s]", request.url.path, exc.message, exc.error_code)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details,
        },
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Sanitized validation error handler masking sensitive input payload echoes."""
    errors = []
    for err in exc.errors():
        errors.append({
            "loc": list(err.get("loc", [])),
            "msg": err.get("msg", "Validation error"),
            "type": err.get("type", "value_error"),
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Standardized handler for HTTPExceptions without internal tracebacks."""
    detail = exc.detail
    if isinstance(detail, dict):
        error_code = detail.get("error_code", "HTTP_ERROR")
        message = detail.get("message", str(detail))
    else:
        error_code = "HTTP_ERROR"
        message = str(detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": error_code, "message": message},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Fallback handler masking internal tracebacks and filesystem paths from external consumers."""
    logger.error("Unhandled server exception on %s: %s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An internal server error occurred. Please contact the system administrator.",
        },
    )


@app.get(
    "/",
    tags=["Root"],
    summary="Application Metadata",
    description="Minimal service discovery metadata.",
)
def get_root():
    """Return truthful platform service identity without fake metrics."""
    return {
        "application": "Presyn",
        "version": "0.1.0",
        "status": "running",
        "docs_url": "/docs",
    }
