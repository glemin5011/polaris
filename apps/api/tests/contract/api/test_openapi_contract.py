import json
from pathlib import Path
from typing import cast

from polaris.runtime.bootstrap.api import create_app

CONTRACT_PATH = Path(__file__).resolve().parents[5] / "contracts" / "openapi.json"


def test_versioned_openapi_contract_matches_application() -> None:
    assert CONTRACT_PATH.exists(), (
        "The OpenAPI contract does not exist. Run `pnpm run openapi` to generate it."
    )

    versioned_contract = cast(
        dict[str, object], json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    )

    generated_contract = cast(dict[str, object], create_app().openapi())

    assert versioned_contract == generated_contract, (
        "The OpenAPI contract is stale. Run `pnpm run openapi` to regenerate it."
    )
