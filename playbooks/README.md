# Playbooks

This directory contains example playbooks demonstrating how to use the roles and plugins from the `drts.linux` collection.

## Available Playbooks

### test_fedora_minimal.yml

Basic test playbook for the `fedora_minimal` role running against localhost.

**Usage**:
```bash
ansible-playbook drts.linux.test_fedora_minimal
```

### fedora_minimal_setup.yml

Production-ready example playbook for configuring Fedora systems with CIS benchmark-aligned security hardening.

**Usage**:
```bash
# Run against specific hosts
ansible-playbook drts.linux.fedora_minimal_setup -i inventory/

# Check mode (dry-run)
ansible-playbook drts.linux.fedora_minimal_setup -i inventory/ --check

# Limit to specific hosts
ansible-playbook drts.linux.fedora_minimal_setup -i inventory/ --limit webservers
```

## Best Practices

- Always test playbooks in a non-production environment first
- Use `--check` mode to preview changes before applying
- Use inventory groups to organize hosts by function or environment
- Leverage role variables to customize behavior per environment
- Consider using vault for sensitive data like passwords or API keys

## Additional Resources

- [Using Ansible Collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)
- [Ansible Playbooks Guide](https://docs.ansible.com/ansible/latest/playbook_guide/index.html)
- [Collection Documentation](../README.md)
