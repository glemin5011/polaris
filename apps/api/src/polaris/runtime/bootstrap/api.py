from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel

def create_app() -> FastAPI:
    app = FastAPI(title="POLARIS API")

    @app.get("/health", include_in_schema=False)
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app