import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "prototype_data.json"
STANDARD_PATH = (
    Path(__file__).parent.parent
    / "config"
    / "standard.json"
)


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def load_standard():
    with open(STANDARD_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def check_vm(vm, required_extensions):
    installed_extensions = vm["extensions"]

    installed_names = {
        extension["name"]
        for extension in installed_extensions
    }

    missing_extensions = [
        extension
        for extension in required_extensions
        if extension not in installed_names
    ]

    failed_extensions = [
        extension["name"]
        for extension in installed_extensions
        if extension["status"] == "Failed"
    ]

    if failed_extensions:
        status = "FAILED"
    elif missing_extensions:
        status = "NON-COMPLIANT"
    else:
        status = "COMPLIANT"

    return {
        "vm_name": vm["name"],
        "resource_group": vm["resource_group"],
        "location": vm["location"],
        "status": status,
        "missing_extensions": missing_extensions,
        "failed_extensions": failed_extensions
    }


def run_scan():
    data = load_data()
    standard = load_standard()

    required_extensions = standard["required_extensions"]

    print("\n")
    print("=" * 70)
    print("       AZURE VM EXTENSION STANDARDISATION - PROTOTYPE")
    print("=" * 70)

    print("\nRequired Extension:")
    for extension in required_extensions:
        print(f"  - {extension}")

    results = []

    for vm in data["vms"]:
        result = check_vm(vm, required_extensions)
        results.append(result)

        print("\n" + "-" * 70)
        print(f"VM Name       : {result['vm_name']}")
        print(f"Resource Group: {result['resource_group']}")
        print(f"Location      : {result['location']}")
        print(f"Status        : {result['status']}")

        if result["missing_extensions"]:
            print("Missing       :")
            for extension in result["missing_extensions"]:
                print(f"  - {extension}")

        if result["failed_extensions"]:
            print("Failed        :")
            for extension in result["failed_extensions"]:
                print(f"  - {extension}")

        if (
            not result["missing_extensions"]
            and not result["failed_extensions"]
        ):
            print("Missing       : None")
            print("Failed        : None")

    compliant = sum(
        1 for result in results
        if result["status"] == "COMPLIANT"
    )

    non_compliant = sum(
        1 for result in results
        if result["status"] == "NON-COMPLIANT"
    )

    failed = sum(
        1 for result in results
        if result["status"] == "FAILED"
    )

    print("\n")
    print("=" * 70)
    print("                         SCAN SUMMARY")
    print("=" * 70)
    print(f"Total VMs       : {len(results)}")
    print(f"Compliant VMs   : {compliant}")
    print(f"Non-Compliant   : {non_compliant}")
    print(f"Failed VMs      : {failed}")
    print("=" * 70)


if __name__ == "__main__":
    run_scan()