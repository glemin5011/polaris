from fastapi import FastAPI

from polaris.runtime.entrypoints.api.system_router import system_router


def create_app() -> FastAPI:
    app = FastAPI(title="POLARIS API")

    app.include_router(system_router)

    return app
