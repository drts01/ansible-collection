# Tox Test Environments Specification

## ADDED Requirements

### Requirement: Coverage test environment
The system SHALL provide a dedicated tox environment for running tests with coverage reporting.

#### Scenario: Coverage environment execution
- **WHEN** developer runs `tox run -e coverage`
- **THEN** system executes pytest with coverage enabled
- **THEN** system generates all configured coverage report formats
- **THEN** system displays coverage summary in terminal

### Requirement: Lint test environment
The system SHALL provide a dedicated tox environment for code quality checks and linting.

#### Scenario: Lint environment execution
- **WHEN** developer runs `tox run -e lint`
- **THEN** system executes ansible-lint on collection files
- **THEN** system executes yamllint on YAML files
- **THEN** system reports linting errors and warnings

### Requirement: Ansible version matrix testing
The system SHALL generate test environments for multiple Ansible versions using tox-ansible plugin.

#### Scenario: Matrix environments generated
- **WHEN** tox-ansible plugin is configured
- **THEN** system generates environments for Python 3.14 with Ansible 2.20+
- **THEN** system skips Ansible versions below 2.20
- **THEN** environment names follow pattern `py314-ansible-core-{version}`

### Requirement: UV runner integration
The system SHALL use uv-venv-lock-runner for fast, reproducible environment creation.

#### Scenario: UV runner used for environments
- **WHEN** tox creates test environments
- **THEN** system uses uv for dependency resolution
- **THEN** system respects uv.lock file for reproducibility
- **THEN** system creates environments faster than pip-based approach

### Requirement: Molecule test environment
The system SHALL maintain existing molecule environment for running Molecule scenarios via pytest.

#### Scenario: Molecule environment execution
- **WHEN** developer runs `tox run -e molecule`
- **THEN** system executes pytest tests in tests/molecule/ directory
- **THEN** system runs Molecule scenarios through pytest wrappers
- **THEN** system uses Podman for container-based testing

### Requirement: Parallel environment execution
The system SHALL support running multiple tox environments in parallel.

#### Scenario: Parallel execution
- **WHEN** developer runs `tox run-parallel`
- **THEN** system executes multiple environments concurrently
- **THEN** system maximizes CPU utilization for faster feedback
- **THEN** system provides aggregated results from all environments

### Requirement: Environment description
The system SHALL provide clear descriptions for each test environment.

#### Scenario: Environment listing with descriptions
- **WHEN** developer runs `tox list`
- **THEN** system displays all available environments
- **THEN** system shows description for each environment
- **THEN** developer understands purpose of each environment

### Requirement: Skip configuration for Ansible versions
The system SHALL configure version skipping in ansible section of tox.toml.

#### Scenario: Ansible version filtering
- **WHEN** tox-ansible generates environments
- **THEN** system skips Python 3.10, 3.11, 3.12
- **THEN** system skips Ansible 2.18 and 2.19
- **THEN** system only tests supported version combinations
