import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "prototype_data.json"
STANDARD_PATH = (
    Path(__file__).parent.parent
    / "config"
    / "standard.json"
)


def load_standard():
    with open(STANDARD_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def create_demo_data():
    return {
        "vms": [
            {
                "name": "vm-extension-01",
                "resource_group": "RG-VM-EXTENSION-STANDARD",
                "location": "centralindia",
                "extensions": [
                    {
                        "name": "AzureMonitorLinuxAgent",
                        "status": "Succeeded"
                    }
                ]
            },
            {
                "name": "vm-extension-02",
                "resource_group": "RG-PROTOTYPE-01",
                "location": "centralindia",
                "extensions": []
            },
            {
                "name": "vm-extension-03",
                "resource_group": "RG-PROTOTYPE-01",
                "location": "centralindia",
                "extensions": [
                    {
                        "name": "AzureMonitorLinuxAgent",
                        "status": "Failed"
                    }
                ]
            }
        ]
    }


def inspect_extensions(vm):
    return vm["extensions"]


def check_compliance(vm, required_extensions):
    installed = {
        extension["name"]
        for extension in vm["extensions"]
    }

    missing = [
        extension
        for extension in required_extensions
        if extension not in installed
    ]

    failed = [
        extension["name"]
        for extension in vm["extensions"]
        if extension["status"] == "Failed"
    ]

    if failed:
        return "FAILED", missing, failed

    if missing:
        return "NON-COMPLIANT", missing, failed

    return "COMPLIANT", missing, failed


def remediate(vm, required_extension):
    print(f"\n[M4] REMEDIATION")
    print(f"     Target VM : {vm['name']}")
    print(f"     Installing: {required_extension}")

    found = False

    for extension in vm["extensions"]:
        if extension["name"] == required_extension:
            extension["status"] = "Succeeded"
            found = True

    if not found:
        vm["extensions"].append({
            "name": required_extension,
            "status": "Succeeded"
        })

    print("     Result    : Remediation successful")
    print("     Mode      : Prototype simulation")


def verify(vm, required_extension):
    print(f"\n[M5] VERIFICATION")
    print(f"     VM        : {vm['name']}")

    for extension in vm["extensions"]:
        if extension["name"] == required_extension:
            if extension["status"] == "Succeeded":
                print("     Extension : Found")
                print("     State     : Succeeded")
                print("     Result    : VERIFIED")
                return True

            print("     Extension : Found")
            print(f"     State     : {extension['status']}")
            print("     Result    : FAILED")
            return False

    print("     Extension : Missing")
    print("     Result    : FAILED")
    return False


def run():
    standard = load_standard()
    required_extensions = standard["required_extensions"]

    # Always start with a fresh prototype scenario.
    data = create_demo_data()

    print("\n")
    print("=" * 70)
    print("        AZURE VM EXTENSION STANDARDISATION")
    print("                 PROTOTYPE DEMO")
    print("=" * 70)

    # ---------------------------------------------------------
    # M1 - VM DISCOVERY
    # ---------------------------------------------------------
    print("\n[M1] VM DISCOVERY")
    print("-" * 70)

    vms = data["vms"]

    print(f"     VMs discovered: {len(vms)}")

    for vm in vms:
        print(
            f"     - {vm['name']} "
            f"({vm['location']})"
        )

    # ---------------------------------------------------------
    # M2 - EXTENSION INSPECTION
    # ---------------------------------------------------------
    print("\n[M2] EXTENSION INSPECTION")
    print("-" * 70)

    for vm in vms:
        extensions = inspect_extensions(vm)

        print(f"\n     {vm['name']}")

        if not extensions:
            print("       No extensions installed")
        else:
            for extension in extensions:
                print(
                    f"       {extension['name']} "
                    f"→ {extension['status']}"
                )

    # ---------------------------------------------------------
    # M3 - COMPLIANCE
    # ---------------------------------------------------------
    print("\n[M3] COMPLIANCE ENGINE")
    print("-" * 70)

    results = []

    for vm in vms:
        status, missing, failed = check_compliance(
            vm,
            required_extensions
        )

        results.append({
            "vm": vm,
            "status": status
        })

        print(
            f"     {vm['name']:<20} → {status}"
        )

        if missing:
            print(
                f"       Missing: {', '.join(missing)}"
            )

        if failed:
            print(
                f"       Failed : {', '.join(failed)}"
            )

    # ---------------------------------------------------------
    # M4 - REMEDIATION
    # ---------------------------------------------------------
    print("\n[M4] REMEDIATION")
    print("-" * 70)

    for result in results:
        if result["status"] == "NON-COMPLIANT":
            vm = result["vm"]

            remediate(
                vm,
                required_extensions[0]
            )

    # ---------------------------------------------------------
    # M5 - VERIFICATION
    # ---------------------------------------------------------
    print("\n[M5] VERIFICATION")
    print("-" * 70)

    for result in results:
        vm = result["vm"]

        if result["status"] == "NON-COMPLIANT":
            verify(
                vm,
                required_extensions[0]
            )

        elif result["status"] == "COMPLIANT":
            print(f"     {vm['name']} → Already verified")

        else:
            print(
                f"     {vm['name']} → "
                "Verification requires investigation"
            )

    # ---------------------------------------------------------
    # FINAL RESCAN
    # ---------------------------------------------------------
    print("\n[M6] POST-REMEDIATION RESCAN")
    print("-" * 70)

    final_results = []

    for vm in vms:
        status, missing, failed = check_compliance(
            vm,
            required_extensions
        )

        final_results.append(status)

        print(
            f"     {vm['name']:<20} → {status}"
        )

    # ---------------------------------------------------------
    # M8 - REPORTING
    # ---------------------------------------------------------
    print("\n[M8] REPORTING")
    print("-" * 70)

    compliant = final_results.count("COMPLIANT")
    non_compliant = final_results.count("NON-COMPLIANT")
    failed = final_results.count("FAILED")

    report_path = (
        Path(__file__).parent.parent
        / "reports"
        / "prototype_report.csv"
    )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(
            "VM Name,Status\n"
        )

        for vm, status in zip(vms, final_results):
            file.write(
                f"{vm['name']},{status}\n"
            )

    print(
        f"     Report generated: {report_path}"
    )

    # ---------------------------------------------------------
    # FINAL SUMMARY
    # ---------------------------------------------------------
    print("\n")
    print("=" * 70)
    print("                       FINAL SUMMARY")
    print("=" * 70)

    print(f"     Total VMs      : {len(vms)}")
    print(f"     Compliant      : {compliant}")
    print(f"     Non-Compliant  : {non_compliant}")
    print(f"     Failed         : {failed}")

    print("=" * 70)

    print("\nPrototype demonstration completed.")
    print("No Azure resources were modified.")
    print("\n")


if __name__ == "__main__":
    run()