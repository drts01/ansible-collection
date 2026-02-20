## ADDED Requirements

### Requirement: SSH root login disabled

The role SHALL configure SSH daemon to prevent direct root login access.

#### Scenario: Root login prevented
- **WHEN** the role has configured SSH
- **THEN** the SSH configuration SHALL have `PermitRootLogin no` set

#### Scenario: Root login attempt fails
- **WHEN** a user attempts to SSH as root
- **THEN** the connection SHALL be rejected with authentication failure

### Requirement: SSH password authentication disabled

The role SHALL configure SSH daemon to disable password-based authentication, requiring key-based authentication only.

#### Scenario: Password authentication disabled
- **WHEN** the role has configured SSH
- **THEN** the SSH configuration SHALL have `PasswordAuthentication no` set

#### Scenario: Key-based authentication required
- **WHEN** a user attempts to SSH without a valid key
- **THEN** the connection SHALL be rejected

### Requirement: SSH protocol version enforcement

The role SHALL configure SSH daemon to use SSH protocol version 2 only.

#### Scenario: Protocol 2 enforced
- **WHEN** the role has configured SSH
- **THEN** the SSH configuration SHALL have `Protocol 2` set

### Requirement: SSH configuration template management

The role SHALL manage the complete SSH daemon configuration using a Jinja2 template with syntax validation.

#### Scenario: Template deployment
- **WHEN** the role deploys SSH configuration
- **THEN** the configuration SHALL be generated from template and validated before activation

#### Scenario: Configuration backup
- **WHEN** the role modifies SSH configuration
- **THEN** a backup of the original configuration SHALL be created

#### Scenario: Invalid configuration prevention
- **WHEN** the role attempts to deploy an invalid SSH configuration
- **THEN** the task SHALL fail before overwriting the existing configuration

### Requirement: SSH service restart on configuration change

The role SHALL restart the SSH daemon only when configuration changes are detected.

#### Scenario: Configuration changed
- **WHEN** the SSH configuration file is modified
- **THEN** the SSH daemon SHALL be restarted via handler

#### Scenario: No configuration change
- **WHEN** the SSH configuration is already in desired state
- **THEN** the SSH daemon SHALL not be restarted

### Requirement: SSH port configuration

The role SHALL allow configurable SSH port with a secure default of port 22.

#### Scenario: Default SSH port
- **WHEN** the role is executed with default variables
- **THEN** SSH SHALL listen on port 22

#### Scenario: Custom SSH port
- **WHEN** the role is executed with `fedora_minimal_ssh_port` set to a custom value
- **THEN** SSH SHALL listen on the specified port

### Requirement: SSH configuration permissions

The role SHALL enforce strict file permissions on SSH configuration files.

#### Scenario: sshd_config permissions
- **WHEN** the role deploys SSH configuration
- **THEN** /etc/ssh/sshd_config SHALL have mode 0600 with root:root ownership

### Requirement: Check mode support for SSH

The role SHALL support Ansible check mode to preview SSH configuration changes without applying them.

#### Scenario: Check mode execution
- **WHEN** the role is executed with --check flag
- **THEN** the system SHALL report SSH configuration changes without applying them
