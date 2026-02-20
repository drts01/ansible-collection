# Fedora Minimal Role

Secure baseline configuration for Fedora 43+ systems following CIS benchmark best practices.

## Requirements

- Ansible 2.12 or higher
- Target systems: Fedora 43+
- Python 3.9+ on target systems
- Network connectivity to Fedora repositories

## Role Variables

All variables use the `fedora_minimal_` prefix for clarity and namespace isolation.

### Package Management

`fedora_minimal_packages_install` (list, default: `['vim-enhanced', 'git', 'curl', 'aide']`)
- Essential system packages to install on target systems
- Uses generic `ansible.builtin.package` module for compatibility

### SSH Hardening

- `fedora_minimal_ssh_port` (int, default: `22`) - SSH listening port
- `fedora_minimal_ssh_permit_root_login` (bool, default: `false`) - Allow root login (CIS 5.2.2)
- `fedora_minimal_ssh_password_authentication` (bool, default: `false`) - Allow password auth (CIS 5.2.4)
- `fedora_minimal_ssh_protocol` (int, default: `2`) - SSH protocol version

### System Services

`fedora_minimal_services_enabled` (list, default: `['chronyd', 'rsyslog']`)
- System services to enable and start
- chronyd: NTP time synchronization
- rsyslog: Centralized system logging

### Baseline Security

- `fedora_minimal_security_aide_init` (bool, default: `true`) - Initialize AIDE database on first run
- Additional security hardening via sysctl, limits, and file permissions

## CIS Benchmark Alignment

This role implements controls from CIS Fedora Linux Benchmark v1.0.0:

| Control ID | Task | Description |
|-----------|------|-------------|
| 5.2.2 | SSH disable root login | Disable direct root SSH access |
| 5.2.4 | SSH disable password auth | Require key-based authentication |
| 5.2.6 | SSH protocol version | Enforce SSH protocol 2 |
| 2.1.x | Time synchronization | Install and enable chronyd |
| 4.1.x | System logging | Install and enable rsyslog |

See task names for complete CIS control mapping.

## Example Playbook

```yaml
---
- name: Configure Fedora baseline
  hosts: fedora_servers
  become: true

  roles:
    - role: fedora_minimal
      vars:
        fedora_minimal_packages_install:
          - vim-enhanced
          - git
          - curl
          - aide
        fedora_minimal_ssh_port: 22
        fedora_minimal_security_aide_init: true
```

## Testing

This role is tested using Molecule with Podman driver on Fedora 43+ container images.

```bash
# Run all tests
molecule test -s fedora_minimal

# Converge (apply) the role
molecule converge -s fedora_minimal

# Verify tests only
molecule verify -s fedora_minimal

# Test idempotence
molecule idempotence -s fedora_minimal

# Run in check mode
ansible-playbook site.yml --check
```

## Known Limitations

### SSH Lockout Risk

The role manages the complete `/etc/ssh/sshd_config` file. Incorrect configuration can prevent SSH access. Always:
- Test in isolated environment first
- Maintain SSH backup for recovery
- Use `--check` mode before applying to production
- Keep recovery access available (console, out-of-band)

### AIDE Database Initialization

Initial AIDE database creation can take 10+ minutes on systems with many files. Large systems should:
- Run with `--async` for background execution
- Consider disabling with `fedora_minimal_security_aide_init: false` initially
- Schedule initialization during maintenance windows

### Performance Considerations

- Check mode may report false positives for service state changes
- AIDE initialization is idempotent (only runs once)
- All tasks use FQCN modules for clarity and compatibility

## Troubleshooting

### SSH Configuration Fails

If SSH configuration deployment fails:

1. Check template syntax: `sudo sshd -t -f /etc/ssh/sshd_config`
2. Restore backup: `sudo cp /etc/ssh/sshd_config.backup /etc/ssh/sshd_config`
3. Restart SSH: `sudo systemctl restart sshd`

### AIDE Initialization Hangs

For large systems with many files:

1. Skip initial AIDE: `fedora_minimal_security_aide_init: false`
2. Run separately: `sudo aideinit`
3. Run with timeout: `ansible-playbook site.yml --timeout=3600`

### Variables Not Applied

Ensure variable precedence:
1. Play-level variables override role defaults
2. Group variables override play variables
3. Host variables override group variables
4. Use `ansible-playbook -e` to verify override

## Rollback Procedures

### Undo Role Changes

Role is additive; rollback is simply not including the role:

```bash
# Simply remove from playbook and re-run with role removed
ansible-playbook site.yml
```

### Recover SSH Access

If SSH is locked out:

1. **Console access** (if available):
   ```bash
   sudo cp /etc/ssh/sshd_config.backup /etc/ssh/sshd_config
   sudo systemctl restart sshd
   ```

2. **Out-of-band recovery**:
   - Use cloud provider console
   - Use physical console
   - Use rescue mode

### Remove AIDE Database

If AIDE initialization caused issues:

```bash
sudo rm -f /var/lib/aide/aide.db*
sudo systemctl restart aide.service
```

## License

See collection LICENSE file

## Author

Ansible Collection Contributors
