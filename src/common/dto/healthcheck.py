from pydantic import BaseModel


class HealthCheckResponseSchema(BaseModel):
    ok: bool
