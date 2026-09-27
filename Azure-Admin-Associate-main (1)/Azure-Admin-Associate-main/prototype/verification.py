import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "prototype_data.json"


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def verify_extension(vm, required_extension):
    print(f"\n[M5] Verification")
    print(f"VM: {vm['name']}")
    print(f"Checking: {required_extension}")

    for extension in vm["extensions"]:
        if extension["name"] == required_extension:

            if extension["status"] == "Succeeded":
                print("Extension found.")
                print("Provisioning State: Succeeded")
                print("Verification Result: VERIFIED")

                return {
                    "verified": True,
                    "extension": required_extension,
                    "status": "Succeeded"
                }

            else:
                print("Extension found.")
                print(f"Provisioning State: {extension['status']}")
                print("Verification Result: FAILED")

                return {
                    "verified": False,
                    "extension": required_extension,
                    "status": extension["status"]
                }

    print("Extension not found.")
    print("Verification Result: FAILED")

    return {
        "verified": False,
        "extension": required_extension,
        "status": "Missing"
    }


if __name__ == "__main__":
    data = load_data()

    required_extension = "AzureMonitorLinuxAgent"

    print("=" * 70)
    print("       PROTOTYPE EXTENSION VERIFICATION")
    print("=" * 70)

    for vm in data["vms"]:
        result = verify_extension(vm, required_extension)

        print("-" * 70)