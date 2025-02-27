"""Role testing files using testinfra."""

import testinfra.host


def test_additonal_packages(host: testinfra.host):
    """Validate additional packages install."""
    cmd = host.run("nmap --version")

    assert cmd.succeeded
    assert not cmd.stderr
    assert cmd.stdout.startswith("Nmap")
