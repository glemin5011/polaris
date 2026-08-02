from fastapi import APIRouter, status

from polaris.runtime.entrypoints.api.system.health.health_response import HealthResponse

health_router = APIRouter(tags=["system"])


@health_router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    operation_id="get_health",
    summary="Check API health",
    description=(
        "Report whether the API process can receive requests. "
        "This liveness endpoint does not check downstream dependencies."
    ),
)
def health() -> HealthResponse:
    return HealthResponse(status="ok")
