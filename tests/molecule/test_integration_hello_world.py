"""
Pytest wrapper for integration_hello_world Molecule scenario.

This test executes the integration_hello_world scenario which tests
the hello_world integration target.
"""

import pytest


@pytest.mark.molecule
def test_integration_hello_world_converge(molecule_scenario_integration_hello_world):
    """Test that integration_hello_world scenario converges successfully."""
    molecule_scenario_integration_hello_world.converge()


@pytest.mark.molecule
def test_integration_hello_world_verify(molecule_scenario_integration_hello_world):
    """Test that integration_hello_world scenario verification passes."""
    molecule_scenario_integration_hello_world.verify()
