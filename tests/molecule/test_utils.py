"""
Pytest wrapper for utils Molecule scenario.

This test executes the utils scenario which tests utility playbooks
and helper roles.
"""

import pytest


@pytest.mark.molecule
def test_utils_converge(molecule_scenario_utils):
    """Test that utils scenario converges successfully."""
    molecule_scenario_utils.converge()


@pytest.mark.molecule
def test_utils_verify(molecule_scenario_utils):
    """Test that utils scenario verification passes."""
    molecule_scenario_utils.verify()
