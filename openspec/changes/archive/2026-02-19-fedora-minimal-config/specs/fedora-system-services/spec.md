## ADDED Requirements

### Requirement: Time synchronization service

The role SHALL ensure chronyd (NTP client) is installed, configured, enabled, and running for system time synchronization.

#### Scenario: Chronyd installed
- **WHEN** the role is executed
- **THEN** the chronyd package SHALL be installed on the system

#### Scenario: Chronyd enabled at boot
- **WHEN** the role completes execution
- **THEN** chronyd service SHALL be enabled to start automatically at boot

#### Scenario: Chronyd running
- **WHEN** the role completes execution
- **THEN** chronyd service SHALL be in active/running state

#### Scenario: Chronyd service restart on configuration change
- **WHEN** chronyd configuration is modified
- **THEN** the chronyd service SHALL be restarted via handler

### Requirement: System logging service

The role SHALL ensure rsyslog is installed, configured, enabled, and running for centralized system logging.

#### Scenario: Rsyslog installed
- **WHEN** the role is executed
- **THEN** the rsyslog package SHALL be installed on the system

#### Scenario: Rsyslog enabled at boot
- **WHEN** the role completes execution
- **THEN** rsyslog service SHALL be enabled to start automatically at boot

#### Scenario: Rsyslog running
- **WHEN** the role completes execution
- **THEN** rsyslog service SHALL be in active/running state

### Requirement: Configurable service list

The role SHALL support a configurable list of system services to manage via the `fedora_minimal_services_enabled` variable.

#### Scenario: Default service list
- **WHEN** the role is executed with default variables
- **THEN** chronyd and rsyslog SHALL be enabled and running

#### Scenario: Custom service list
- **WHEN** the role is executed with a custom `fedora_minimal_services_enabled` variable
- **THEN** only the services specified in the custom list SHALL be managed by the role

#### Scenario: Additional services
- **WHEN** the role is executed with additional services in `fedora_minimal_services_enabled`
- **THEN** all specified services SHALL be enabled and running

### Requirement: Service state enforcement

The role SHALL use the generic `ansible.builtin.service` module to manage service states for compatibility.

#### Scenario: Service state idempotency
- **WHEN** the role is executed multiple times
- **THEN** service states SHALL remain stable and unchanged on subsequent runs

#### Scenario: Service enablement verification
- **WHEN** the role completes execution
- **THEN** all managed services SHALL be verified as enabled

### Requirement: Service management error handling

The role SHALL fail with a clear error message if any specified service cannot be started or enabled.

#### Scenario: Service not found
- **WHEN** the role attempts to manage a non-existent service
- **THEN** the task SHALL fail with an error message identifying the missing service

#### Scenario: Service start failure
- **WHEN** a service fails to start due to misconfiguration
- **THEN** the task SHALL fail with the service-specific error message

### Requirement: Check mode support for services

The role SHALL support Ansible check mode to preview service state changes without applying them.

#### Scenario: Check mode execution
- **WHEN** the role is executed with --check flag
- **THEN** the system SHALL report which services would be enabled or started without actually changing them
