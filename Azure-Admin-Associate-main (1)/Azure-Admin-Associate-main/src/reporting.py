import csv
from pathlib import Path
from datetime import datetime


REPORT_PATH = (
    Path(__file__).parent.parent
    / "reports"
    / "compliance_report.csv"
)


def generate_report(
    vm_name,
    resource_group,
    required_extensions,
    installed_extensions,
    status
):
    """
    Generate a compliance report for one VM.
    """

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    scan_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    rows = []

    for required_extension in required_extensions:

        if required_extension in installed_extensions:
            installed = required_extension
        else:
            installed = "Missing"

        rows.append({
            "Scan Time": scan_time,
            "VM Name": vm_name,
            "Resource Group": resource_group,
            "Required Extension": required_extension,
            "Installed Extension": installed,
            "Status": status
        })

    fieldnames = [
        "Scan Time",
        "VM Name",
        "Resource Group",
        "Required Extension",
        "Installed Extension",
        "Status"
    ]

    with open(
        REPORT_PATH,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    return REPORT_PATH


def generate_summary(results):
    """
    Generate a summary of the complete VM scan.
    """

    total_vms = len(results)

    compliant_vms = sum(
        1
        for result in results
        if result["status"] == "COMPLIANT"
    )

    non_compliant_vms = sum(
        1
        for result in results
        if result["status"] == "NON-COMPLIANT"
    )

    print("\nScan Summary")
    print("=" * 50)

    print(f"Total VMs       : {total_vms}")
    print(f"Compliant VMs   : {compliant_vms}")
    print(f"Non-Compliant VMs: {non_compliant_vms}")

    print("=" * 50)


if __name__ == "__main__":

    report = generate_report(
        vm_name="vm-extension-01",
        resource_group="RG-VM-EXTENSION-STANDARD",
        required_extensions=[
            "AzureMonitorLinuxAgent"
        ],
        installed_extensions=[
            "AzureMonitorLinuxAgent"
        ],
        status="COMPLIANT"
    )

    print("\nCompliance Report Generated")
    print("=" * 50)
    print(f"Report: {report}")

    generate_summary([
        {
            "vm_name": "vm-extension-01",
            "status": "COMPLIANT"
        }
    ])