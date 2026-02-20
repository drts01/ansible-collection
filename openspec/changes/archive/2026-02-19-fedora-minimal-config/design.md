## Context

The current collection has sample roles but lacks production-ready, security-focused roles for specific distributions. Organizations running Fedora 43+ need a baseline configuration role that implements security hardening aligned with CIS benchmarks. This design addresses that gap by creating a dedicated role following Ansible best practices and the collection's established patterns.

**Current State:**
- Collection has basic role structure under `roles/run/`
- Molecule testing framework exists but minimal scenarios
- ansible-lint and yamllint configured
- No distribution-specific hardening roles

**Constraints:**
- Must follow FQCN (Fully Qualified Collection Name) for all modules
- Must be idempotent and check-mode compatible
- Must target Fedora 43+ specifically
- Must align with CIS Fedora/RHEL benchmarks
- Must maintain cross-collection compatibility

## Goals / Non-Goals

**Goals:**
- Create `fedora_minimal` role for secure baseline configuration
- Implement four core capabilities as separate task files
- Provide comprehensive defaults with clear documentation
- Include Molecule test scenario for Fedora 43+
- Map security controls to CIS benchmark IDs
- Ensure all tasks are idempotent and use FQCN
- Support check mode for dry-run validation

**Non-Goals:**
- Multi-distribution support (Fedora-specific only)
- GUI/desktop configuration (server baseline only)
- Application-specific hardening beyond baseline
- Automated CIS compliance scanning (manual verification only)
- Network firewall configuration (delegated to separate role)
- SELinux policy customization beyond defaults

## Decisions

### 1. Role Structure: Task File Organization

**Decision:** Split capabilities into separate task files, included from `main.yml`

**Rationale:**
- Improves maintainability and readability
- Allows selective capability execution via tags
- Matches established Ansible patterns
- Easier to test individual capabilities

**Structure:**
```
roles/fedora_minimal/
├── tasks/
│   ├── main.yml              # Orchestrator with includes
│   ├── packages.yml          # fedora-base-packages
│   ├── ssh.yml               # fedora-ssh-hardening
│   ├── services.yml          # fedora-system-services
│   └── security.yml          # fedora-baseline-security
├── defaults/main.yml
├── handlers/main.yml
├── meta/
│   ├── main.yml
│   └── argument_specs.yml
├── templates/
│   └── sshd_config.j2
└── README.md
```

**Alternatives Considered:**
- Single `main.yml` with all tasks: Rejected due to poor maintainability
- Separate roles per capability: Rejected as overkill for related tasks

### 2. Module Selection: Prefer Built-ins

**Decision:** Use `ansible.builtin.*` modules wherever possible

**Rationale:**
- No external collection dependencies to manage
- Guaranteed availability and stability
- Better performance (no collection resolution)
- Aligns with project instructions

**Key Modules:**
- `ansible.builtin.package` - Cross-package-manager support
- `ansible.builtin.service` - Service management
- `ansible.builtin.template` - SSH config from template
- `ansible.builtin.lineinfile` - Targeted config edits
- `ansible.builtin.file` - Permissions management
- `ansible.builtin.user` / `ansible.builtin.group` - User management
- `ansible.builtin.command` - Only with `creates:`/`removes:` for idempotency

**Exception:** If AIDE initialization requires it, use `community.general.aide` with pinned version in requirements.yml

### 3. Variable Management: Layered Defaults

**Decision:** Use defaults in `defaults/main.yml` with clear override paths

**Rationale:**
- Defaults provide sensible secure baselines
- Easy to override per inventory/group/host
- Self-documenting through variable names
- Follows Ansible precedence patterns

**Variable Naming Convention:**
```yaml
fedora_minimal_<capability>_<setting>: value
```

**Example:**
```yaml
# defaults/main.yml
fedora_minimal_packages_install:
  - vim-enhanced
  - git
  - curl
  - aide

fedora_minimal_ssh_port: 22
fedora_minimal_ssh_permit_root_login: false
fedora_minimal_ssh_password_authentication: false
fedora_minimal_ssh_protocol: 2

fedora_minimal_services_enabled:
  - chronyd
  - rsyslog

fedora_minimal_security_aide_init: true
```

### 4. SSH Hardening: Template-Based Configuration

**Decision:** Use Jinja2 template for sshd_config, not line-by-line edits

**Rationale:**
- Full control over configuration
- Easier to audit and validate
- Prevents configuration drift
- Supports `validate` parameter for syntax checking
- More deterministic than lineinfile

**Implementation:**
```yaml
- name: Configure SSH daemon
  ansible.builtin.template:
    src: sshd_config.j2
    dest: /etc/ssh/sshd_config
    owner: root
    group: root
    mode: '0600'
    validate: '/usr/sbin/sshd -t -f %s'
    backup: true
  notify: Restart sshd
```

**Alternatives Considered:**
- `lineinfile` per setting: Rejected due to drift potential and complexity
- Drop-in configs: Not widely supported for sshd

### 5. CIS Benchmark Alignment: Documentation-Driven

**Decision:** Document CIS control IDs in task names and README, not automated scanning

**Rationale:**
- Manual mapping provides clear audit trail
- Automated scanning tools vary and change
- Documentation approach is maintainable
- Aligns with manual verification practices

**Format:**
```yaml
- name: "CIS 5.2.2 - Configure SSH daemon to disable root login"
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^PermitRootLogin'
    line: 'PermitRootLogin no'
```

**Target Benchmark:** CIS Fedora Linux Benchmark v1.0.0 (or latest available)

### 6. Testing Strategy: Molecule with Fedora Container

**Decision:** Use Molecule with Podman driver and Fedora 43 container image

**Rationale:**
- Fast feedback loop for development
- Consistent test environment
- Matches target distribution exactly
- Podman available on Fedora development hosts

**Test Scenario:**
```yaml
# extensions/molecule/fedora_minimal/molecule.yml
scenario:
  name: fedora_minimal
platforms:
  - name: fedora43
    image: registry.fedoraproject.org/fedora:43
    pre_build_image: true
provisioner:
  name: ansible
verifier:
  name: ansible
```

**Verification Tasks:**
- Package installation
- Service states (active/enabled)
- SSH configuration validation
- File permissions checks
- AIDE database initialization

### 7. Handler Design: Shared Listeners

**Decision:** Use handlers with `listen` for service restarts

**Rationale:**
- Multiple tasks can trigger same handler
- More flexible than handler name references
- Cleaner task readability

**Implementation:**
```yaml
# handlers/main.yml
- name: Restart sshd
  ansible.builtin.service:
    name: sshd
    state: restarted
  listen: restart sshd

- name: Restart chronyd
  ansible.builtin.service:
    name: chronyd
    state: restarted
  listen: restart chronyd
```

## Risks / Trade-offs

### Risk: AIDE Initialization Performance

**Risk:** Initial AIDE database creation can take 10+ minutes on systems with many files

**Mitigation:**
- Make AIDE initialization optional via `fedora_minimal_security_aide_init: false`
- Document expected initialization time in README
- Consider async task with poll for large systems
- Provide skip tag: `skip_aide_init`

### Risk: SSH Lockout During Configuration

**Risk:** Incorrect SSH configuration could lock out remote access

**Mitigation:**
- Use `validate` parameter on template task
- Maintain backup of original config (`backup: true`)
- Test in Molecule before production
- Document recovery procedure in README
- Consider requiring `--diff` review before apply

### Risk: CIS Benchmark Version Drift

**Risk:** CIS benchmarks update; role may not reflect latest controls

**Mitigation:**
- Pin specific benchmark version in README
- Schedule quarterly reviews of benchmark updates
- Accept that role targets specific benchmark version
- Provide clear upgrade path documentation

### Risk: Fedora Version Compatibility

**Risk:** Fedora releases every 6 months; package names or configs may change

**Mitigation:**
- Target Fedora 43+ explicitly in documentation
- Test against latest Fedora in CI when possible
- Use generic module names (`package` vs `dnf`)
- Monitor Fedora changelogs for breaking changes
- Plan for Fedora 44, 45 validation updates

### Trade-off: Opinionated Defaults vs Flexibility

**Trade-off:** Strong defaults may not fit all environments

**Mitigation:**
- All defaults overridable via variables
- Document customization patterns in README
- Provide example inventory structures
- Consider role arguments for common variations
- Use tags for selective execution

### Trade-off: Template-Based SSH Config vs Line Edits

**Trade-off:** Template overwrites existing customizations

**Mitigation:**
- Backup original config (`backup: true`)
- Document that role manages full sshd_config
- Provide variable for every common SSH setting
- Consider `fedora_minimal_ssh_manage: false` escape hatch

## Migration Plan

**Deployment Steps:**

1. **Development Phase:**
   - Create role structure and task files
   - Implement each capability with tests
   - Validate with Molecule on Fedora 43
   - Run ansible-lint and yamllint

2. **Testing Phase:**
   - Test in isolated Fedora 43 VM
   - Verify idempotence (run twice, no changes)
   - Validate check mode functionality
   - Test with custom variables

3. **Documentation Phase:**
   - Complete README with CIS mappings
   - Document all variables in argument_specs.yml
   - Create example playbook
   - Document known limitations

4. **Release:**
   - Tag in collection version
   - Update CHANGELOG.md
   - Announce in collection documentation

**Rollback Strategy:**

- Role is additive (new capability); rollback is simply not including role in playbooks
- If applied and issues arise, restore SSH backup: `cp /etc/ssh/sshd_config.backup /etc/ssh/sshd_config && systemctl restart sshd`
- AIDE database can be removed: `rm -f /var/lib/aide/aide.db*`

## Open Questions

1. Should we support multiple SSH configurations (internal vs DMZ)?
   - Resolution: Start with single config; add multi-config support if requested

2. How to handle existing customizations in sshd_config?
   - Resolution: Document that role manages full config; provide override variables

3. Should AIDE checks run automatically via cron?
   - Resolution: No - leave scheduling to user/organization policy; document options

4. Do we need separate Molecule scenarios for check mode and regular mode?
   - Resolution: Single scenario with check mode test in verify phase

5. Should we include firewalld configuration?
   - Resolution: No - out of scope per non-goals; delegate to separate role
