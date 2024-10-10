from typing import Mapping

from fastapi import APIRouter, status

from src.common.dto.healthcheck import HealthCheckResponseSchema
from src.api.v1.docs.healthcheck import (
    HEALTH_DESCRIPTION,
    HEALTH_RESPONCE,
    HEALTH_SUMMARY,
)

healthcheck_router = APIRouter(tags=["healthcheck"])


@healthcheck_router.get(
    "",
    response_model=HealthCheckResponseSchema,
    status_code=status.HTTP_200_OK,
    response_description=HEALTH_RESPONCE,
    description=HEALTH_DESCRIPTION,
    summary=HEALTH_SUMMARY,
)
async def healthcheck_endpoint() -> Mapping[str, bool]:
    return {"ok": True}
