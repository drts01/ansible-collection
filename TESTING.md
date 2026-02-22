# Testing Guide

This document provides comprehensive information on testing the `drts.casc` Ansible collection.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Running Tests with Coverage](#running-tests-with-coverage)
- [Tox Environments](#tox-environments)
- [Molecule Testing](#molecule-testing)
- [Coverage Reports](#coverage-reports)
- [CI/CD Testing](#cicd-testing)
- [Test Directory Structure](#test-directory-structure)
- [Writing Tests](#writing-tests)
- [Ansible Version Testing](#ansible-version-testing)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- **Python 3.14+**: Required for running tests
- **uv**: Fast Python package installer and resolver
- **Podman**: Container runtime for Molecule tests
- **Git**: Version control

### Installing Prerequisites

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Podman (macOS)
brew install podman

# Install Podman (Fedora/RHEL)
sudo dnf install podman
```

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/drts01/ansible-collection.git
cd ansible-collection

# Install all development dependencies
uv sync --group dev

# Alternatively, install specific dependency groups
uv sync --group dev --group lint --group build
```

## Quick Start

Run all tests with coverage:

```bash
# Using uv directly
uv run pytest tests/ --cov

# Using tox
tox run -e coverage

# Run only unit tests
uv run pytest tests/unit/ -v

# Run only integration tests
uv run pytest tests/integration/ -v
```

## Running Tests with Coverage

The collection is configured to automatically generate coverage reports in multiple formats:

### Local Testing

```bash
# Run tests with coverage (generates HTML, XML, and terminal output)
uv run pytest tests/ --cov

# View HTML coverage report
open tests/output/coverage/html/index.html  # macOS
xdg-open tests/output/coverage/html/index.html  # Linux
```

### Coverage Report Formats

- **HTML**: `tests/output/coverage/html/index.html` - Interactive browseable report
- **XML**: `tests/output/coverage/coverage.xml` - For CI/CD integration
- **Terminal**: Immediate feedback with missing lines highlighted
- **JUnit**: `tests/output/junit/results.xml` - Test execution results

## Tox Environments

This project uses [tox](https://tox.wiki/) with [tox-ansible](https://ansible.readthedocs.io/projects/tox-ansible/) and [tox-uv](https://github.com/tox-dev/tox-uv) for test automation.

### Available Environments

List all available environments:

```bash
tox list
```

### Coverage Environment

Run tests with comprehensive coverage reporting:

```bash
tox run -e coverage
```

This generates:
- HTML coverage report
- XML coverage report
- Terminal output with missing lines
- JUnit XML for test results

### Lint Environment

Run Ansible linting (yamllint runs via pre-commit hooks):

```bash
tox run -e lint
```

### Molecule Environment

Run Molecule scenarios via pytest integration:

```bash
tox run -e molecule

# Run specific molecule test
tox run -e molecule -- tests/molecule/test_fedora_minimal.py
```

### Ansible Version Matrix

tox-ansible automatically generates test environments for different Ansible versions:

```bash
# List all generated environments
tox list

# Run tests against specific Ansible version
tox run -e py314-ansible-core-2.20
tox run -e py314-ansible-core-2.21
```

## Molecule Testing

Molecule scenarios are located in `extensions/molecule/` following the official Molecule documentation for Ansible collections.

### Available Scenarios

- **fedora_minimal**: Tests the `fedora_minimal` role
- **integration_hello_world**: Integration test example
- **utils**: Utility testing scenario

### Running Molecule Tests

```bash
# Via pytest (recommended)
uv run pytest tests/molecule/ -v

# Via tox
tox run -e molecule

# Run specific scenario
uv run pytest tests/molecule/test_fedora_minimal.py -v

# Direct molecule command (from extensions/molecule/)
cd extensions/molecule
molecule test -s fedora_minimal
```

### Molecule Test Structure

```
extensions/molecule/          # Molecule scenarios (official location)
├── fedora_minimal/
│   ├── converge.yml         # Playbook to test
│   ├── molecule.yml         # Scenario configuration
│   └── verify.yml           # Verification tasks
tests/molecule/              # Pytest wrappers
├── test_fedora_minimal.py   # Pytest integration
└── conftest.py              # Shared fixtures
```

## Coverage Reports

### Viewing Local Reports

After running tests with coverage:

```bash
# Open HTML report in browser
open tests/output/coverage/html/index.html

# View XML report
cat tests/output/coverage/coverage.xml

# View JUnit test results
cat tests/output/junit/results.xml
```

### Understanding Coverage Metrics

- **Statements**: Total lines of executable code
- **Missing**: Lines not executed during tests
- **Coverage %**: Percentage of statements executed
- **Branch**: Conditional branches tested

### Coverage Thresholds

Currently, no minimum coverage thresholds are enforced. This allows for incremental improvement while maintaining flexibility during development.

## CI/CD Testing

### GitHub Actions Workflows

The collection uses two main CI/CD workflows:

#### 1. Tests Workflow (`.github/workflows/tests.yml`)

Runs on pull requests:
- Changelog validation
- Build and import checks
- Ansible-lint validation
- Sanity tests
- Unit tests
- **Coverage reporting with PR comments**

#### 2. Molecule Workflow (`.github/workflows/molecule.yml`)

Runs on push and workflow dispatch:
- Full Molecule scenario testing
- Container-based testing with Podman
- **Coverage reporting and test summaries**

### Coverage in Pull Requests

When you open a PR, GitHub Actions automatically:
1. Runs all tests with coverage
2. Posts a coverage comment on the PR
3. Displays test results in the Actions UI
4. Generates a coverage summary in the Actions tab
5. Uploads coverage artifacts for download

### Viewing CI Coverage

1. **PR Comments**: Coverage changes appear directly in PR comments
2. **Actions Summary**: View coverage metrics in the workflow summary
3. **Artifacts**: Download full HTML reports from workflow artifacts
4. **Test Reporter**: Failed tests show detailed error information

## Test Directory Structure

```
tests/
├── conftest.py              # Shared pytest fixtures
├── .gitignore               # Ignore test outputs
├── output/                  # Test outputs (gitignored)
│   ├── coverage/
│   │   ├── html/           # HTML coverage reports
│   │   └── coverage.xml    # XML coverage data
│   └── junit/
│       └── results.xml     # JUnit test results
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_basic.py
│   └── .keep
├── integration/             # Integration tests
│   ├── __init__.py
│   ├── test_integration.py
│   └── targets/            # Integration test targets
│       └── hello_world/
└── molecule/                # Molecule pytest wrappers
    ├── __init__.py
    ├── test_fedora_minimal.py
    ├── test_integration_hello_world.py
    └── test_utils.py
```

## Writing Tests

### Unit Tests

Create unit tests in `tests/unit/`:

```python
# tests/unit/test_my_feature.py
import pytest

def test_example():
    """Test example functionality."""
    assert True

def test_with_fixture(tmp_path):
    """Test using pytest fixture."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")
    assert test_file.read_text() == "content"
```

### Integration Tests

Create integration tests in `tests/integration/targets/`:

```yaml
# tests/integration/targets/my_test/tasks/main.yml
---
- name: Test my feature
  ansible.builtin.debug:
    msg: "Testing feature"

- name: Assert expected behavior
  ansible.builtin.assert:
    that:
      - condition_is_true
    fail_msg: "Test failed"
```

### Molecule Tests

Create pytest wrappers in `tests/molecule/`:

```python
# tests/molecule/test_my_scenario.py
import pytest

@pytest.mark.molecule
def test_my_scenario_converge(molecule_scenario_my_scenario):
    """Test that my_scenario converges successfully."""
    molecule_scenario_my_scenario.converge()

@pytest.mark.molecule
def test_my_scenario_verify(molecule_scenario_my_scenario):
    """Test that my_scenario verification passes."""
    molecule_scenario_my_scenario.verify()
```

### Test Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.molecule  # Molecule scenario test
@pytest.mark.slow      # Slow-running test
```

Run specific markers:

```bash
# Run only molecule tests
uv run pytest -m molecule

# Skip slow tests
uv run pytest -m "not slow"
```

## Ansible Version Testing

The collection supports testing against multiple Ansible versions using tox-ansible.

### Supported Versions

- Ansible Core 2.20+
- Python 3.14+

### Testing Specific Versions

```bash
# List all Ansible version environments
tox list | grep ansible

# Test against specific version
tox run -e py314-ansible-core-2.20

# Test against all versions
tox run -e py314-ansible-core-{2.20,2.21,2.22}
```

### Version Matrix Configuration

The version matrix is configured in `tox.toml`:

```toml
[ansible]
skip = [
    "py3.10", "py3.11", "py3.12",  # Older Python versions
    "2.18", "2.19",                  # Older Ansible versions
]
```

## Troubleshooting

### Common Issues

#### 1. Coverage Reports Not Generated

**Problem**: No coverage data appears after running tests.

**Solution**:
```bash
# Ensure coverage is enabled
uv run pytest tests/ --cov

# Check that tests actually ran
uv run pytest tests/ -v

# Verify output directory exists
ls -la tests/output/coverage/
```

#### 2. Molecule Container Fails to Start

**Problem**: Container exits with code 127 or "command not found".

**Solution**:
```bash
# Check Podman installation
podman --version

# Verify container image
podman pull registry.fedoraproject.org/fedora:43

# Check system init availability
podman run --rm registry.fedoraproject.org/fedora:43 /sbin/init --version
```

#### 3. Python Version Mismatch

**Problem**: Tests fail with "requires python >=3.14" error.

**Solution**:
```bash
# Check Python version
python3 --version

# Install Python 3.14+
# macOS:
brew install python@3.14

# Fedora:
sudo dnf install python3.14

# Update uv Python discovery
uv python list
```

#### 4. Tox Environment Issues

**Problem**: Tox fails to create virtual environments.

**Solution**:
```bash
# Remove existing tox environments
rm -rf .tox/

# Recreate with uv
tox run -e coverage --recreate

# Check tox configuration
tox config
```

#### 5. Import Errors in Tests

**Problem**: Tests fail with "No module named" errors.

**Solution**:
```bash
# Reinstall dependencies
uv sync --group dev --force

# Verify installation
uv run python -c "import pytest; print(pytest.__version__)"

# Check PYTHONPATH
uv run pytest --version
```

### Getting Help

- **Documentation**: Check Ansible collection documentation
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join project discussions
- **Logs**: Check `.tox/*/log` for detailed error logs

## Best Practices

1. **Run tests locally** before pushing commits
2. **Keep tests fast** - use fixtures and mocks where appropriate
3. **Write descriptive test names** - explain what is being tested
4. **Use pytest markers** - categorize tests for selective execution
5. **Maintain coverage** - aim for high coverage on critical code paths
6. **Clean up test outputs** - the `tests/output/` directory is gitignored
7. **Update tests with code** - keep tests in sync with implementation
8. **Use tox for CI consistency** - ensure local and CI environments match

## Additional Resources

- [Ansible Collections Documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html)
- [Molecule Documentation](https://molecule.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [tox Documentation](https://tox.wiki/)
- [tox-ansible Documentation](https://ansible.readthedocs.io/projects/tox-ansible/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
