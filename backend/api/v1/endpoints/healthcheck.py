from typing import Any, Dict

from fastapi import APIRouter, status

from backend.common.dto.healthcheck import HealthCheckResponseSchema

healthcheck_router = APIRouter(tags=["healthcheck"])


@healthcheck_router.get(
    "/healthcheck",
    response_model=HealthCheckResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def healthcheck_endpoint() -> Dict[str, Any]:
    return {"ok": True}