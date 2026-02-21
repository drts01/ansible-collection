## ADDED Requirements

### Requirement: Collection name updated in galaxy.yml
The collection metadata file SHALL be updated to reflect the new collection name `linux` while maintaining the `drts` namespace.

#### Scenario: galaxy.yml contains new collection name
- **WHEN** the galaxy.yml file is read
- **THEN** the `name` field contains `linux` instead of `ansible_collection`

### Requirement: Collection name updated in README.md
The README documentation SHALL be updated to reference the new collection name `drts.linux` in all installation instructions and examples.

#### Scenario: README shows correct installation command
- **WHEN** a user reads the README.md file
- **THEN** all `ansible-galaxy collection install` commands reference `drts.linux`

### Requirement: Collection name updated in pyproject.toml
The Python project configuration SHALL be updated to reflect the new collection name in the project metadata and known_first_party imports.

#### Scenario: pyproject.toml contains new collection name
- **WHEN** the pyproject.toml file is read
- **THEN** the `name` field contains `linux` and `known_first_party` references `ansible_collections.drts.linux`

### Requirement: Collection name updated in documentation links
The documentation configuration file SHALL be updated to reference the new collection name in repository paths and URLs.

#### Scenario: docs/docsite/links.yml contains new collection name
- **WHEN** the links.yml file is read
- **THEN** the `repository` field references `drts.linux` instead of `drts.ansible_collection`

### Requirement: Role references updated in playbooks
All playbook files SHALL be updated to reference roles using the new collection name `drts.linux`.

#### Scenario: Playbooks reference new collection name
- **WHEN** a playbook file is read
- **THEN** all role references use `drts.linux.role_name` format instead of `drts.ansible_collection.role_name`

### Requirement: Filter references updated in tests
Test files SHALL be updated to reference filters using the new collection name `drts.linux`.

#### Scenario: Test files reference new collection name
- **WHEN** a test file is read
- **THEN** all filter references use `drts.linux.filter_name` format instead of `drts.ansible_collection.filter_name`

### Requirement: Development environment configuration updated
The devfile.yaml configuration SHALL be updated to reflect the new collection name in the project identifier.

#### Scenario: devfile.yaml contains new collection name
- **WHEN** the devfile.yaml file is read
- **THEN** the project name field contains `drts.linux` instead of `drts.ansible_collection`

### Requirement: Python imports updated
Python source files SHALL be updated to import from the new collection package path `ansible_collections.drts.linux`.

#### Scenario: Python imports reference new collection name
- **WHEN** Python test files are read
- **THEN** docstrings and imports reference `drts.linux` instead of `drts.ansible_collection`
