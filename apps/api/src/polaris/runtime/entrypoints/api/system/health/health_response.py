from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Response body returned when the API is healthy"""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )
    status: Literal["ok"]
