import sys
import json
from pathlib import Path

from .discovery import get_all_vms
from .extensions import get_installed_extensions
from .compliance import check_compliance
from .remediation import remediate_vm
from .verification import verify_extension
from .reporting import generate_report, generate_summary


CONFIG_PATH = (
    Path(__file__).parent.parent
    / "config"
    / "standard.json"
)


def load_standard():
    """Load the extension standard."""

    with open(
        CONFIG_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def run():

    remediate_requested = "--remediate" in sys.argv
    demo_missing = "--demo-missing" in sys.argv

    standard = load_standard()

    required_extensions = standard[
        "required_extensions"
    ]

    print("\nAzure VM Extension Standardisation")
    print("=" * 70)

    # ============================================================
    # M1 — VM DISCOVERY
    # ============================================================

    print("\n[M1] VM Discovery")

    vms = get_all_vms()

    if not vms:

        print("No Azure VMs found.")
        return

    print(
        f"Discovered VMs: {len(vms)}"
    )

    # Store results for final summary
    scan_results = []

    # ============================================================
    # PROCESS EVERY VM
    # ============================================================

    for vm in vms:

        vm_name = vm["name"]

        resource_group = vm[
            "resource_group"
        ]

        print("\n" + "=" * 70)

        print(
            f"VM Name       : {vm_name}"
        )

        print(
            f"Resource Group: {resource_group}"
        )

        print(
            f"Location      : {vm['location']}"
        )

        print("=" * 70)

        # ========================================================
        # M2 — EXTENSION INSPECTION
        # ========================================================

        print(
            "\n[M2] Extension Inspection"
        )

        actual_extensions = (
            get_installed_extensions(
                resource_group,
                vm_name
            )
        )

        # --------------------------------------------------------
        # SAFE DEMO MODE
        # --------------------------------------------------------

        if demo_missing:

            print(
                "\n*** DEMO MODE ***"
            )

            print(
                "Simulating missing "
                "required extension."
            )

            installed_extensions = []

        else:

            installed_extensions = (
                actual_extensions
            )

        print(
            "\nInstalled Extensions:"
        )

        if installed_extensions:

            for extension in installed_extensions:

                print(
                    f"  - {extension}"
                )

        else:

            print("  None")

        # ========================================================
        # M3 — COMPLIANCE
        # ========================================================

        print(
            "\n[M3] Compliance Engine"
        )

        result = check_compliance(
            installed_extensions
        )

        status = result["status"]

        print(
            "\nCompliance Status:"
        )

        print(
            f"  {status}"
        )

        if result[
            "missing_extensions"
        ]:

            print(
                "\nMissing Extensions:"
            )

            for extension in result[
                "missing_extensions"
            ]:

                print(
                    f"  - {extension}"
                )

            print(
                "\nAction: "
                "REMEDIATION REQUIRED"
            )

        else:

            print(
                "Missing Extensions: None"
            )

            print(
                "\nAction: "
                "NO REMEDIATION REQUIRED"
            )

        # Save result for summary
        scan_results.append(
            {
                "vm_name": vm_name,
                "status": status
            }
        )

        # ========================================================
        # M4 — REMEDIATION
        # ========================================================

        if (
            status == "NON-COMPLIANT"
            and remediate_requested
        ):

            print(
                "\n[M4] Remediation"
            )

            # ----------------------------------------------------
            # SAFE DEMO MODE
            # ----------------------------------------------------

            if demo_missing:

                print(
                    "Demo mode active."
                )

                print(
                    "Real Azure remediation "
                    "was NOT performed."
                )

            # ----------------------------------------------------
            # REAL REMEDIATION
            # ----------------------------------------------------

            else:

                for extension in result[
                    "missing_extensions"
                ]:

                    if (
                        extension
                        == "AzureMonitorLinuxAgent"
                    ):

                        print(
                            "\nInstalling "
                            "AzureMonitorLinuxAgent..."
                        )

                        remediate_vm(
                            resource_group,
                            vm_name
                        )

                # =================================================
                # M5 — VERIFICATION
                # =================================================

                print(
                    "\n[M5] Verification"
                )

                verification = (
                    verify_extension(
                        resource_group,
                        vm_name,
                        "AzureMonitorLinuxAgent"
                    )
                )

                print(
                    f"Extension    : "
                    f"{verification['extension']}"
                )

                print(
                    f"Provisioning : "
                    f"{verification['provisioning_state']}"
                )

                print(
                    f"Verified     : "
                    f"{verification['verified']}"
                )

        # ========================================================
        # M8 — REPORTING
        # ========================================================

        print(
            "\n[M8] Reporting"
        )

        report_path = generate_report(
            vm_name=vm_name,
            resource_group=resource_group,
            required_extensions=(
                required_extensions
            ),
            installed_extensions=(
                installed_extensions
            ),
            status=status
        )

        print(
            f"Report Generated: "
            f"{report_path}"
        )

    # ============================================================
    # FINAL SUMMARY
    # ============================================================

    generate_summary(
        scan_results
    )

    print("\n" + "=" * 70)

    print(
        "VM Extension Standardisation "
        "Scan Completed"
    )

    print("=" * 70)


if __name__ == "__main__":

    run()