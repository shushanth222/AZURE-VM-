import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "prototype_data.json"


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def remediate_vm(vm, required_extension):
    print(f"\n[M4] Remediation started for: {vm['name']}")

    # Prototype simulation only
    print(f"Installing: {required_extension}")

    existing = [
        extension["name"]
        for extension in vm["extensions"]
    ]

    if required_extension not in existing:
        vm["extensions"].append({
            "name": required_extension,
            "status": "Succeeded"
        })
    else:
        for extension in vm["extensions"]:
            if extension["name"] == required_extension:
                extension["status"] = "Succeeded"

    print("Remediation completed successfully.")

    return vm


def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    data = load_data()

    required_extension = "AzureMonitorLinuxAgent"

    print("=" * 70)
    print("       PROTOTYPE REMEDIATION")
    print("=" * 70)

    # Remediate the simulated non-compliant VM
    for vm in data["vms"]:
        if vm["name"] == "vm-extension-02":
            remediate_vm(vm, required_extension)

    save_data(data)

    print("\nPrototype data updated.")
    print("Azure resources were NOT modified.")
    print("=" * 70)