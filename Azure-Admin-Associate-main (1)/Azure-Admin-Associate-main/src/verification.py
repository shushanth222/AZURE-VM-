from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient


SUBSCRIPTION_ID = "28c5e2e6-3755-4bb7-be4c-86f67e7e3142"


def verify_extension(
    resource_group,
    vm_name,
    extension_name
):

    try:

        credential = AzureCliCredential()

        compute_client = ComputeManagementClient(
            credential,
            SUBSCRIPTION_ID
        )

        extension = (
            compute_client
            .virtual_machine_extensions
            .get(
                resource_group,
                vm_name,
                extension_name
            )
        )

        provisioning_state = (
            extension.provisioning_state
        )

        verified = (
            provisioning_state
            == "Succeeded"
        )

        return {
            "verified": verified,
            "extension": extension.name,
            "provisioning_state": provisioning_state
        }

    except Exception as error:

        print(
            "\nERROR: Extension verification failed."
        )

        print(
            f"Details: {error}"
        )

        return {
            "verified": False,
            "extension": extension_name,
            "provisioning_state": "Failed",
            "error": str(error)
        }


if __name__ == "__main__":

    RESOURCE_GROUP = (
        "RG-VM-EXTENSION-STANDARD"
    )

    VM_NAME = "vm-extension-01"

    EXTENSION_NAME = (
        "AzureMonitorLinuxAgent"
    )

    result = verify_extension(
        RESOURCE_GROUP,
        VM_NAME,
        EXTENSION_NAME
    )

    print(
        "\nAzure VM Extension Verification"
    )

    print("=" * 60)

    print(
        f"Extension       : "
        f"{result['extension']}"
    )

    print(
        f"Provisioning    : "
        f"{result['provisioning_state']}"
    )

    print(
        f"Verified        : "
        f"{result['verified']}"
    )