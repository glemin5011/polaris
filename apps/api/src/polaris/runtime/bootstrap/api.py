from fastapi import FastAPI

from polaris.runtime.entrypoints.api.system.health.health_router import health_router


def create_app() -> FastAPI:
    app = FastAPI(title="POLARIS API")

    app.include_router(health_router)

    return app
