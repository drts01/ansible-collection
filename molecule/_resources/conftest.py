"""PyTest Fixtures."""

import os

import pytest
import testinfra.utils.ansible_runner


def pytest_runtest_setup(item: pytest.Item) -> None:  # pylint: disable=unused-argument
    """Run tests only when under molecule."""
    if inventory_file := os.getenv("MOLECULE_INVENTORY_FILE"):
        pytest.testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
            inventory_file=inventory_file
        ).get_hosts("all")
    else:
        pytest.skip("Test should run only from inside molecule.", allow_module_level=True)
