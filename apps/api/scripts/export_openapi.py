import json
from pathlib import Path

from polaris.runtime.bootstrap.api import create_app

CONTRACT_PATH = Path(__file__).resolve().parents[3] / "contracts" / "openapi.json"


def export_openapi() -> None:
    contract = create_app().openapi()

    serialised_contract = (
        json.dumps(
            contract,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n"
    )

    CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_PATH.write_text(serialised_contract, encoding="utf-8")

    print(f"Generated {CONTRACT_PATH}")


if __name__ == "__main__":
    export_openapi()
