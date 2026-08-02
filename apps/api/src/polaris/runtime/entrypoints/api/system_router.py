from fastapi import APIRouter, status

from polaris.runtime.entrypoints.api.system.responses.health_response import HealthResponse

system_router = APIRouter()


@system_router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    operation_id="get_health",
    summary="Check API health",
)
def health() -> HealthResponse:
    return HealthResponse(status="ok")
