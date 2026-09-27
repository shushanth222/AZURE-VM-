import subprocess


RESOURCE_PROVIDER = "Microsoft.Azure.Monitor"
EXTENSION_TYPE = "AzureMonitorLinuxAgent"


def remediate_vm(resource_group, vm_name):

    try:

        print(
            f"\nRemediation started for: {vm_name}"
        )

        print(
            "Installing AzureMonitorLinuxAgent..."
        )

        command = [
            "az",
            "vm",
            "extension",
            "set",
            "--resource-group",
            resource_group,
            "--vm-name",
            vm_name,
            "--name",
            EXTENSION_TYPE,
            "--publisher",
            RESOURCE_PROVIDER,
            "--enable-auto-upgrade",
            "true"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:

            print(
                "\nERROR: Remediation failed."
            )

            print(
                result.stderr.strip()
            )

            return {
                "success": False,
                "extension": EXTENSION_TYPE,
                "provisioning_state": "Failed",
                "error": result.stderr.strip()
            }

        print(
            "\nRemediation completed successfully."
        )

        print(
            result.stdout.strip()
        )

        return {
            "success": True,
            "extension": EXTENSION_TYPE,
            "provisioning_state": "Succeeded"
        }

    except Exception as error:

        print(
            "\nERROR: Remediation failed."
        )

        print(
            f"Details: {error}"
        )

        return {
            "success": False,
            "extension": EXTENSION_TYPE,
            "provisioning_state": "Failed",
            "error": str(error)
        }


if __name__ == "__main__":

    RESOURCE_GROUP = "RG-VM-EXTENSION-STANDARD"
    VM_NAME = "vm-extension-01"

    result = remediate_vm(
        RESOURCE_GROUP,
        VM_NAME
    )

    print("\nRemediation Result")
    print("=" * 50)

    print(
        f"Success: {result['success']}"
    )