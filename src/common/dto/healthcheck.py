from src.common.dto.base import DTO


class HealthCheckResponseSchema(DTO):
    ok: bool


class Status(DTO):
    ok: bool
