"""
Pytest wrapper for fedora_minimal Molecule scenario.

This test executes the fedora_minimal scenario which tests the
fedora_minimal Ansible role with basic package and security configuration.
"""

import pytest


@pytest.mark.molecule
def test_fedora_minimal_converge(molecule_scenario_fedora_minimal):
    """Test that fedora_minimal scenario converges successfully."""
    molecule_scenario_fedora_minimal.converge()


@pytest.mark.molecule
def test_fedora_minimal_verify(molecule_scenario_fedora_minimal):
    """Test that fedora_minimal scenario verification passes."""
    molecule_scenario_fedora_minimal.verify()
