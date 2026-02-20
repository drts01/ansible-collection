## Why

Organizations need a repeatable, secure baseline configuration for Fedora systems that follows security best practices and CIS benchmarks. Manual configuration is error-prone and doesn't scale across multiple systems.

## What Changes

- Create a new Ansible role for minimal Fedora system configuration
- Implement security hardening tasks aligned with CIS Fedora/RHEL benchmarks
- Configure essential system services (SSH, time sync, logging)
- Establish baseline package management
- Add Molecule test scenarios for Fedora variants
- Include ansible-lint and yamllint validation

## Capabilities

### New Capabilities

- `fedora-base-packages`: Manage installation and configuration of essential system packages for Fedora
- `fedora-ssh-hardening`: Configure SSH daemon with secure settings (disable root login, password auth, etc.)
- `fedora-system-services`: Configure and enable essential system services (chronyd for time sync, rsyslog for logging)
- `fedora-baseline-security`: Apply baseline security hardening (file permissions, sudo configuration, file integrity monitoring with AIDE)

### Modified Capabilities

<!-- No existing capabilities are being modified -->

## Impact

- **New Code**: New role under `roles/fedora_minimal/` with tasks, defaults, handlers, and meta
- **Testing**: New Molecule scenario for Fedora 43+ testing
- **Documentation**: Role README with CIS benchmark control mapping
- **Dependencies**: May require additional collections pinned in `requirements.yml` (e.g., `community.general` for specific modules)
- **Target Systems**: Fedora 43+ (RPM-based systems)
