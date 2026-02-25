# Event-Driven Ansible (EDA)

This directory contains Event-Driven Ansible rulebooks for the `drts.casc` collection.

## Overview

Event-Driven Ansible (EDA) is a highly scalable, flexible automation capability that works with event sources such as monitoring tools, webhooks, and other streaming data to automatically trigger remediation, provisioning, or other defined actions.

The rulebooks in this directory demonstrate how to:
- Define event sources
- Create conditional rules that respond to events
- Trigger automated actions based on event conditions

## Directory Structure

```
extensions/eda/
├── README.md           # This file
└── rulebooks/          # EDA rulebook definitions
    └── rulebook.yml    # Example rulebook
```

## Example Rulebook

The `rulebooks/rulebook.yml` file serves as a basic example of EDA functionality:

### What It Does

The example rulebook:
1. **Event Source**: Uses `ansible.eda.range` to generate 5 sequential events (i=0 through i=4)
2. **Rule Condition**: Matches when `event.i == 1` (triggers on the second event)
3. **Action**: Executes the `ansible.eda.hello` playbook when the condition is met

### Rulebook Structure

```yaml
---
- name: Hello Events
  hosts: localhost
  sources:
    - ansible.eda.range:
        limit: 5
  rules:
    - name: Say Hello
      condition: event.i == 1
      action:
        run_playbook:
          name: ansible.eda.hello
```

### Key Components

- **name**: Descriptive name for the rulebook
- **hosts**: Target hosts (typically localhost for EDA controller)
- **sources**: Event sources that generate events
- **rules**: Conditional logic and actions
  - **condition**: Expression evaluated against incoming events
  - **action**: What to execute when condition is true

## Running Rulebooks

### Prerequisites

1. Install Event-Driven Ansible:
   ```bash
   pip install ansible-rulebook
   ```

2. Install required collections:
   ```bash
   ansible-galaxy collection install ansible.eda
   ```

### Running the Example

Execute the example rulebook:

```bash
ansible-rulebook --rulebook extensions/eda/rulebooks/rulebook.yml -i localhost,
```

Expected output:
- 5 events will be generated
- When event.i equals 1, the hello playbook will run
- Other events (0, 2, 3, 4) will not trigger the action

## Creating Custom Rulebooks

### Common Event Sources

Event-Driven Ansible supports various event sources:

- **Webhooks**: `ansible.eda.webhook` - Listen for HTTP webhook events
- **File Monitoring**: `ansible.eda.file` - Watch for file changes
- **Kafka**: `ansible.eda.kafka` - Consume Kafka messages
- **AlertManager**: `sabre1041.eda.alertmanager` - Process Prometheus AlertManager events
- **Generic URL**: `ansible.eda.url_check` - Poll URLs for changes

### Example Custom Rulebook Template

```yaml
---
- name: Custom Event Handler
  hosts: localhost
  sources:
    - ansible.eda.webhook:
        host: 0.0.0.0
        port: 5000
  rules:
    - name: Handle Critical Alert
      condition: event.payload.severity == "critical"
      action:
        run_playbook:
          name: playbooks/remediation.yml
          extra_vars:
            alert_id: "{{ event.payload.id }}"
```

### Condition Expressions

Conditions use Python-like expressions:

```yaml
# Simple equality
condition: event.status == "down"

# Multiple conditions (AND)
condition: event.severity == "critical" and event.source == "monitoring"

# Multiple conditions (OR)
condition: event.type == "error" or event.type == "critical"

# Pattern matching
condition: event.hostname is match("prod-.*")

# Numeric comparisons
condition: event.cpu_usage > 90
```

### Available Actions

- **run_playbook**: Execute an Ansible playbook
- **run_job_template**: Trigger an Automation Controller job template
- **run_module**: Run a single Ansible module
- **set_fact**: Store data for later use
- **post_event**: Send a new event to the system
- **print_event**: Log event data (useful for debugging)

## Use Cases

### 1. Auto-Remediation

Respond automatically to system alerts:
- Restart services when they fail
- Clear disk space when thresholds are exceeded
- Scale infrastructure based on load

### 2. Security Response

Trigger security playbooks based on alerts:
- Isolate compromised hosts
- Block suspicious IP addresses
- Rotate credentials after potential exposure

### 3. Configuration Enforcement

Maintain desired state:
- Revert unauthorized configuration changes
- Enforce compliance policies
- Synchronize configuration across environments

### 4. Workflow Automation

Chain automation based on events:
- Deploy applications after successful builds
- Update inventories when infrastructure changes
- Coordinate multi-step provisioning workflows

## Best Practices

1. **Start Simple**: Begin with basic event sources and rules, then increase complexity
2. **Test Conditions**: Use `print_event` action to debug condition logic
3. **Error Handling**: Include error handling in triggered playbooks
4. **Idempotency**: Ensure actions are safe to run multiple times
5. **Monitoring**: Log rule executions for audit and troubleshooting
6. **Documentation**: Document rule purposes and expected event schemas

## Development Workflow

1. **Create Rulebook**: Define event sources and rules
2. **Test Locally**: Run with `ansible-rulebook` in development
3. **Validate**: Ensure conditions trigger correctly
4. **Deploy**: Add to automation controller or standalone EDA controller
5. **Monitor**: Track rule executions and refine as needed

## Additional Resources

- [Event-Driven Ansible Documentation](https://ansible.readthedocs.io/projects/rulebook/)
- [ansible.eda Collection](https://github.com/ansible/event-driven-ansible)
- [Event-Driven Ansible Examples](https://github.com/ansible/eda-examples)
- [Rulebook Best Practices](https://ansible.readthedocs.io/projects/rulebook/en/stable/best-practices.html)

## Contributing

To add new rulebooks to this directory:

1. Create rulebook files in `rulebooks/` directory
2. Use descriptive names (e.g., `webhook_remediation.yml`, `security_alerts.yml`)
3. Document the purpose and expected event schema
4. Test thoroughly before committing
5. Update this README with usage examples

## Support

For issues or questions:
- Collection Repository: https://github.com/drts01/ansible-collection
- Event-Driven Ansible Issues: https://github.com/ansible/event-driven-ansible/issues
