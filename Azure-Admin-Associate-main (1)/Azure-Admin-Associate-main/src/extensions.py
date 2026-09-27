from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient


SUBSCRIPTION_ID = "28c5e2e6-3755-4bb7-be4c-86f67e7e3142"


def get_installed_extensions(resource_group, vm_name):

    try:
        credential = AzureCliCredential()

        compute_client = ComputeManagementClient(
            credential,
            SUBSCRIPTION_ID
        )

        installed_extensions = []

        extension_result = (
            compute_client.virtual_machine_extensions.list(
                resource_group,
                vm_name
            )
        )

        extension_items = extension_result.value

        for item in extension_items:

            if isinstance(item, dict):

                extension_name = item.get("name")

            else:

                extension_name = getattr(
                    item,
                    "name",
                    None
                )

            if extension_name:

                installed_extensions.append(
                    extension_name
                )

        return installed_extensions

    except Exception as error:

        print(
            f"\nERROR: Unable to inspect extensions "
            f"for VM '{vm_name}'."
        )

        print(
            f"Details: {error}"
        )

        return []


if __name__ == "__main__":

    RESOURCE_GROUP = "RG-VM-EXTENSION-STANDARD"
    VM_NAME = "vm-extension-01"

    print(
        "\nAzure VM Extension Inspection"
    )

    print("=" * 60)

    extensions = get_installed_extensions(
        RESOURCE_GROUP,
        VM_NAME
    )

    if not extensions:

        print(
            "No extensions found "
            "or extension inspection failed."
        )

    else:

        for extension in extensions:

            print(
                f"Extension Name : "
                f"{extension}"
            )

    print("-" * 60)