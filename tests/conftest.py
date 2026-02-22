"""
Pytest configuration and fixtures for Molecule scenario testing.

This module provides pytest fixtures that wrap Molecule scenarios,
allowing them to be executed through pytest with enhanced reporting
and test discovery capabilities.
"""

import subprocess

from pathlib import Path

import pytest


def pytest_configure(config):
    """Configure pytest markers for Molecule tests."""
    config.addinivalue_line(
        "markers",
        "molecule: mark test as a Molecule scenario execution",
    )


class MoleculeScenario:
    """Wrapper class for executing Molecule scenarios as pytest tests."""

    def __init__(self, scenario_name):
        """
        Initialize a Molecule scenario wrapper.

        Args:
            scenario_name (str): Name of the Molecule scenario to run
                                (e.g., 'fedora_minimal', 'integration_hello_world')
        """
        self.scenario_name = scenario_name
        self.scenario_path = Path(__file__).parent.parent / "extensions" / "molecule" / scenario_name

    def converge(self):
        """Execute molecule converge phase for the scenario."""
        self._run_molecule("converge")

    def verify(self):
        """Execute molecule verify phase for the scenario."""
        self._run_molecule("verify")

    def test(self):
        """Execute full molecule test (destroy + create + converge + verify + destroy)."""
        self._run_molecule("test")

    def cleanup(self):
        """Clean up molecule resources."""
        self._run_molecule("destroy")

    def _run_molecule(self, action):
        """
        Execute a molecule action.

        Args:
            action (str): Molecule action to execute (converge, verify, test, destroy)

        Raises:
            subprocess.CalledProcessError: If molecule command fails
        """
        cmd = [
            "molecule",
            action,
            "--scenario-name",
            self.scenario_name,
        ]

        # Change to the extensions/molecule directory for execution
        result = subprocess.run(
            cmd,
            cwd=self.scenario_path.parent,
            capture_output=False,
            text=True,
            check=True,
        )
        return result


@pytest.fixture
def molecule_scenario_fedora_minimal():
    """Fixture for fedora_minimal Molecule scenario."""
    scenario = MoleculeScenario("fedora_minimal")
    yield scenario
    # Cleanup after test
    try:
        scenario.cleanup()
    except subprocess.CalledProcessError:
        pass  # Ignore cleanup errors


@pytest.fixture
def molecule_scenario_integration_hello_world():
    """Fixture for integration_hello_world Molecule scenario."""
    scenario = MoleculeScenario("integration_hello_world")
    yield scenario
    # Cleanup after test
    try:
        scenario.cleanup()
    except subprocess.CalledProcessError:
        pass  # Ignore cleanup errors


@pytest.fixture
def molecule_scenario_utils():
    """Fixture for utils Molecule scenario."""
    scenario = MoleculeScenario("utils")
    yield scenario
    # Cleanup after test
    try:
        scenario.cleanup()
    except subprocess.CalledProcessError:
        pass  # Ignore cleanup errors
