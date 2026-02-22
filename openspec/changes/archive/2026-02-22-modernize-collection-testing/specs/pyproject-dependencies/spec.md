# PyProject Dependencies Specification

## ADDED Requirements

### Requirement: Centralized dependency management
The system SHALL manage all runtime and development dependencies in `pyproject.toml` using PEP 621 and PEP 735 standards.

#### Scenario: All dependencies in pyproject.toml
- **WHEN** developer needs to install dependencies
- **THEN** system provides all dependency information in `pyproject.toml`
- **THEN** system does not require separate requirements.txt files for dependency resolution

### Requirement: Runtime dependencies
The system SHALL declare Ansible core runtime dependencies in `[project.dependencies]` section.

#### Scenario: Ansible version specified
- **WHEN** collection is installed
- **THEN** system requires `ansible-core>=2.20` as runtime dependency
- **THEN** system ensures Fedora 43+ compatibility through version constraint

### Requirement: Development dependency groups
The system SHALL organize development dependencies into logical groups using `[dependency-groups]` section.

#### Scenario: Dev dependency group
- **WHEN** developer installs development dependencies with `uv sync --group dev`
- **THEN** system installs pytest, pytest-cov, pytest-xdist, pytest-ansible
- **THEN** system installs molecule and molecule-plugins with podman support
- **THEN** system installs coverage tools with TOML support

#### Scenario: Build dependency group
- **WHEN** developer installs build dependencies with `uv sync --group build`
- **THEN** system installs tox>=4.40
- **THEN** system installs tox-ansible>=26.1
- **THEN** system installs tox-uv>=1.29

#### Scenario: Lint dependency group
- **WHEN** developer installs lint dependencies with `uv sync --group lint`
- **THEN** system installs ansible-lint>=26.1
- **THEN** system installs yamllint>=1.35

### Requirement: Version constraints
The system SHALL use appropriate version constraints for dependency stability and compatibility.

#### Scenario: Compatible release constraints
- **WHEN** specifying development tools
- **THEN** system uses `>=` for minimum version requirements
- **THEN** system uses `~=` for compatible release constraints when API stability is important

### Requirement: Legacy requirements.txt compatibility
The system SHALL provide reference requirements.txt files that point to pyproject.toml for legacy tool compatibility.

#### Scenario: Requirements.txt references pyproject.toml
- **WHEN** legacy tools read requirements.txt
- **THEN** file contains comment explaining dependencies are in pyproject.toml
- **THEN** file contains `-e .` to install from pyproject.toml

#### Scenario: Test-requirements.txt references dependency groups
- **WHEN** legacy tools read test-requirements.txt
- **THEN** file contains comment explaining dependencies are in pyproject.toml
- **THEN** file contains `-e .[dev]` to install dev dependency group

### Requirement: Lock file management
The system SHALL maintain uv.lock file for reproducible dependency resolution.

#### Scenario: Dependencies locked
- **WHEN** dependencies are updated in pyproject.toml
- **THEN** developer runs `uv lock` to update lock file
- **THEN** system records exact versions in uv.lock
- **THEN** CI/CD uses locked versions for reproducible builds

### Requirement: Collection metadata
The system SHALL maintain project metadata in `[project]` section consistent with galaxy.yml.

#### Scenario: Project metadata defined
- **WHEN** pyproject.toml is read
- **THEN** system provides project name, version, description
- **THEN** system specifies requires-python>=3.14
- **THEN** system lists authors and classifiers
