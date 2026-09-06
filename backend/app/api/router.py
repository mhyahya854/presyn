"""Central API v1 Router Aggregator."""

from fastapi import APIRouter
from backend.app.api.routes import health, system

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health.router)
api_v1_router.include_router(system.router)
