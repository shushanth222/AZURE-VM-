from src.compliance import check_compliance


def test_compliant_vm():
    installed_extensions = [
        "AzureMonitorLinuxAgent"
    ]

    result = check_compliance(installed_extensions)

    assert result["status"] == "COMPLIANT"
    assert result["missing_extensions"] == []


def test_missing_extension():
    installed_extensions = []

    result = check_compliance(installed_extensions)

    assert result["status"] == "NON-COMPLIANT"
    assert "AzureMonitorLinuxAgent" in result["missing_extensions"]


if __name__ == "__main__":
    test_compliant_vm()
    test_missing_extension()

    print("All compliance tests passed!")