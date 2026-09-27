from azure.identity import AzureCliCredential
from azure.mgmt.compute import ComputeManagementClient


SUBSCRIPTION_ID = "28c5e2e6-3755-4bb7-be4c-86f67e7e3142"


def get_all_vms():

    try:
        credential = AzureCliCredential()

        compute_client = ComputeManagementClient(
            credential,
            SUBSCRIPTION_ID
        )

        vms = []

        for vm in compute_client.virtual_machines.list_all():

            resource_group = vm.id.split("/")[4]

            vms.append({
                "name": vm.name,
                "resource_group": resource_group,
                "location": vm.location
            })

        return vms

    except Exception as error:

        print("\nERROR: Unable to discover Azure VMs.")
        print(f"Details: {error}")

        return []


if __name__ == "__main__":

    print("\nAzure VM Discovery")
    print("=" * 60)

    vms = get_all_vms()

    if not vms:

        print("No VMs found or Azure discovery failed.")

    else:

        for vm in vms:

            print(
                f"VM Name       : "
                f"{vm['name']}"
            )

            print(
                f"Resource Group: "
                f"{vm['resource_group']}"
            )

            print(
                f"Location      : "
                f"{vm['location']}"
            )

            print("-" * 60)