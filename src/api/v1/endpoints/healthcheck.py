from typing import Mapping

from fastapi import APIRouter, status

from src.common.dto.healthcheck import HealthCheckResponseSchema

healthcheck_router = APIRouter(tags=["healthcheck"])


@healthcheck_router.get(
    "",
    response_model=HealthCheckResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def healthcheck_endpoint() -> Mapping[str, bool]:
    """
    Health check for the service.

        This route checks if the service is operational and accessible.
        It returns a status code of 200 if the service is healthy, along
        with a JSON message indicating the service status.
    """
    return {"ok": True}
