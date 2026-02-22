## Why

The current testing infrastructure uses outdated configuration formats and doesn't leverage modern tooling for fast, efficient testing. Migrating to tox-ansible's TOML format (per tox v4.41.0), integrating tox-uv for faster dependency resolution, and adding proper pytest-ansible integration will improve maintainability, reduce CI run times, and provide better test organization. Additionally, Molecule tests are not currently running in GitHub Actions, leaving a gap in CI coverage.

## What Changes

- Migrate `tox-ansible.ini` to `tox-ansible.toml` using modern TOML configuration format
- Configure tox-uv for faster dependency resolution and package installation
- Integrate pytest-ansible to run Molecule scenarios as pytest tests with better reporting
- Add GitHub Actions workflow to execute Molecule tests via tox-ansible
- Configure tox environments for testing across multiple Ansible versions (2.20+)
- Update test structure to leverage pytest-ansible features (fixtures, markers, reporting)

## Capabilities

### New Capabilities

- `tox-ansible-toml-config`: Modern TOML-based tox-ansible configuration replacing the legacy INI format, with proper environment definitions for Ansible version matrix testing
- `tox-uv-integration`: Integration of tox-uv plugin for accelerated dependency resolution and installation during test runs
- `pytest-molecule-integration`: Running Molecule test scenarios through pytest-ansible framework with enhanced reporting and test discovery
- `github-actions-molecule-tests`: CI/CD workflow for executing Molecule tests in GitHub Actions using tox-ansible orchestration

### Modified Capabilities

<!-- No existing capabilities are being modified at the requirement level -->

## Impact

**Files Modified:**
- `tox-ansible.ini` → deleted and replaced by `tox-ansible.toml`
- `pyproject.toml` → updated pytest configuration for Molecule integration
- `.github/workflows/tests.yml` → add Molecule test job

**Files Created:**
- `tox-ansible.toml` → new configuration file
- `.github/workflows/molecule.yml` → new workflow (or integrate into existing tests.yml)
- `tests/conftest.py` → pytest fixtures for Molecule scenarios

**Dependencies:**
- Already present: `tox-ansible>=26.1`, `tox-uv>=1.29`, `pytest-ansible~=26.1`, `molecule-plugins[podman]~=25.8`
- No new dependencies required

**Systems Affected:**
- Local development testing workflow
- GitHub Actions CI pipeline
- Molecule test scenarios in `extensions/molecule/`
