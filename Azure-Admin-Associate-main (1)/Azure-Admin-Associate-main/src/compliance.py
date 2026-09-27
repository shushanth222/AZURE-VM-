import json
from pathlib import Path

from .extensions import get_installed_extensions


CONFIG_PATH = Path(__file__).parent.parent / "config" / "standard.json"


def load_standard():
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)


def check_compliance(installed_extensions):

    standard = load_standard()

    required_extensions = set(
        standard["required_extensions"]
    )

    installed_extensions = set(
        installed_extensions
    )

    missing_extensions = (
        required_extensions - installed_extensions
    )

    if not missing_extensions:
        return {
            "status": "COMPLIANT",
            "missing_extensions": []
        }

    return {
        "status": "NON-COMPLIANT",
        "missing_extensions": sorted(missing_extensions)
    }


if __name__ == "__main__":

    print("\nAzure VM Extension Compliance")
    print("=" * 60)

    # Get REAL extensions from Azure
    installed_extensions = get_installed_extensions()

    result = check_compliance(
        installed_extensions
    )

    print(
        "Required Extensions :",
        ", ".join(load_standard()["required_extensions"])
    )

    print(
        "Installed Extensions:",
        ", ".join(installed_extensions)
        if installed_extensions
        else "None"
    )

    print(
        "Compliance Status    :",
        result["status"]
    )

    if result["missing_extensions"]:
        print(
            "Missing Extensions  :",
            ", ".join(result["missing_extensions"])
        )
    else:
        print(
            "Missing Extensions  : None"
        )