## ADDED Requirements

### Requirement: File integrity monitoring with AIDE

The role SHALL install and initialize AIDE (Advanced Intrusion Detection Environment) for file integrity monitoring.

#### Scenario: AIDE package installed
- **WHEN** the role is executed
- **THEN** the aide package SHALL be installed on the system

#### Scenario: AIDE database initialization
- **WHEN** the role is executed with `fedora_minimal_security_aide_init` set to true
- **THEN** the AIDE database SHALL be initialized at /var/lib/aide/aide.db

#### Scenario: AIDE initialization skipped when disabled
- **WHEN** the role is executed with `fedora_minimal_security_aide_init` set to false
- **THEN** AIDE database initialization SHALL be skipped

#### Scenario: AIDE initialization idempotency
- **WHEN** the role is executed multiple times with AIDE initialization enabled
- **THEN** the AIDE database SHALL only be created if it does not already exist

### Requirement: Secure file permissions on sensitive files

The role SHALL enforce strict file permissions on security-sensitive system files and directories.

#### Scenario: SSH key permissions
- **WHEN** the role configures the system
- **THEN** /etc/ssh directory SHALL have mode 0755 and /etc/ssh/*_key files SHALL have mode 0600

#### Scenario: Shadow file permissions
- **WHEN** the role configures the system
- **THEN** /etc/shadow SHALL have mode 0000 with root:root ownership

#### Scenario: Sudoers file permissions
- **WHEN** the role configures the system
- **THEN** /etc/sudoers SHALL have mode 0440 with root:root ownership

### Requirement: Sudo configuration hardening

The role SHALL configure sudo with security best practices including requiring password and disabling root environment preservation.

#### Scenario: Sudo password required
- **WHEN** the role configures sudo
- **THEN** sudo SHALL be configured to require password authentication

#### Scenario: Sudo environment reset
- **WHEN** the role configures sudo
- **THEN** sudo SHALL be configured to reset user environment variables

#### Scenario: Sudo timestamp timeout
- **WHEN** the role configures sudo
- **THEN** sudo SHALL be configured with a reasonable timestamp timeout (default: 15 minutes)

### Requirement: Core dump restriction

The role SHALL disable core dumps to prevent potential information disclosure.

#### Scenario: Core dumps disabled via limits
- **WHEN** the role configures the system
- **THEN** /etc/security/limits.conf SHALL include hard core limit of 0

#### Scenario: Core dumps disabled via sysctl
- **WHEN** the role configures the system
- **THEN** kernel.core_pattern sysctl SHALL be configured to prevent core dumps

### Requirement: Secure umask enforcement

The role SHALL enforce a secure default umask of 0027 for all users to restrict default file permissions.

#### Scenario: System-wide umask
- **WHEN** the role configures the system
- **THEN** /etc/profile SHALL include umask 0027 setting

#### Scenario: Bash profile umask
- **WHEN** the role configures the system
- **THEN** /etc/bashrc SHALL include umask 0027 setting

### Requirement: CIS benchmark alignment documentation

The role SHALL document CIS benchmark control mappings for all security hardening tasks.

#### Scenario: Task documentation
- **WHEN** the role tasks are reviewed
- **THEN** each security-related task SHALL include CIS control ID in the task name

#### Scenario: README documentation
- **WHEN** the role README is reviewed
- **THEN** it SHALL include a table mapping role tasks to specific CIS benchmark controls

### Requirement: Security configuration validation

The role SHALL validate security configurations before applying them to prevent system lockout or misconfiguration.

#### Scenario: Sudoers syntax validation
- **WHEN** the role modifies sudoers configuration
- **THEN** the configuration SHALL be validated with visudo before activation

#### Scenario: Configuration backup
- **WHEN** the role modifies security-critical files
- **THEN** backups SHALL be created before modifications

### Requirement: Check mode support for security hardening

The role SHALL support Ansible check mode to preview security hardening changes without applying them.

#### Scenario: Check mode execution
- **WHEN** the role is executed with --check flag
- **THEN** the system SHALL report security hardening changes without applying them

#### Scenario: AIDE initialization in check mode
- **WHEN** the role is executed with --check flag
- **THEN** AIDE database initialization SHALL be skipped and reported as a pending change

### Requirement: Configurable security hardening

The role SHALL allow users to selectively enable or disable specific security hardening features via variables.

#### Scenario: AIDE optional
- **WHEN** AIDE is disabled via `fedora_minimal_security_aide_init: false`
- **THEN** AIDE initialization SHALL be skipped but package SHALL still be installed

#### Scenario: Individual hardening controls
- **WHEN** specific security controls are disabled via variables
- **THEN** only the enabled security controls SHALL be applied

### Requirement: No secrets in logs

The role SHALL use `no_log: true` on any tasks that might expose sensitive information in task output.

#### Scenario: Sensitive task output suppression
- **WHEN** the role executes tasks involving passwords or keys
- **THEN** task output SHALL be suppressed from logs

#### Scenario: Diff suppression on sensitive files
- **WHEN** the role modifies files containing secrets
- **THEN** diff output SHALL be disabled with `diff: false`
