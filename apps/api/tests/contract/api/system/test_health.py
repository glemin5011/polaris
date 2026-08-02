from fastapi.testclient import TestClient

from polaris.runtime.bootstrap.api import create_app
from polaris.runtime.entrypoints.api.system.health.health_response import HealthResponse


def test_health_endpoint_reports_ok() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200

    health_response = HealthResponse.model_validate(response.json())

    assert health_response == HealthResponse(status="ok")
