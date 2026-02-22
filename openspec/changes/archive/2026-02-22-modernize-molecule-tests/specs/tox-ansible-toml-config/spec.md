## ADDED Requirements

### Requirement: TOML configuration file format

The tox-ansible configuration SHALL use TOML format (tox-ansible.toml) following tox v4.41.0 standards, replacing the legacy INI format.

#### Scenario: Valid TOML structure
- **WHEN** tox-ansible is executed
- **THEN** the system SHALL read configuration from tox-ansible.toml
- **AND** the file SHALL be valid TOML syntax

#### Scenario: INI file deprecated
- **WHEN** both tox-ansible.ini and tox-ansible.toml exist
- **THEN** the system SHALL prioritize tox-ansible.toml
- **AND** emit a warning about the deprecated INI file

### Requirement: Ansible version matrix configuration

The configuration SHALL define which Ansible and Python versions to skip in the test matrix.

#### Scenario: Skip old versions
- **WHEN** tox-ansible generates test environments
- **THEN** the system SHALL exclude Python versions < 3.14
- **AND** SHALL exclude Ansible versions < 2.14
- **AND** SHALL use the skip list from [ansible] section

### Requirement: Tox plugin requirements declaration

The configuration SHALL declare required tox plugins in the [tox] section.

#### Scenario: Required plugins specified
- **WHEN** tox reads the configuration
- **THEN** the system SHALL load tox>=4.0
- **AND** SHALL load tox-ansible>=26.1
- **AND** SHALL load tox-uv>=1.29

### Requirement: Environment generation

The system SHALL generate test environments for all non-skipped Ansible/Python version combinations.

#### Scenario: Matrix expansion
- **WHEN** tox-ansible processes the configuration
- **THEN** the system SHALL create environments for supported versions
- **AND** each environment SHALL be named as ansible-py{version}-ansible{version}
- **AND** SHALL allow manual execution via tox -e <env-name>

### Requirement: Backward compatibility during migration

The system SHALL support both INI and TOML formats during the migration period.

#### Scenario: Gradual migration
- **WHEN** tox-ansible.toml is created alongside tox-ansible.ini
- **THEN** both formats SHALL be valid
- **AND** developers SHALL be able to test TOML locally before removing INI
