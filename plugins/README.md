# Plugins

This directory contains Ansible plugins for the `drts.linux` collection.

## Directory Structure

- `action/` - Action plugins that execute on the controller
- `become/` - Become (privilege escalation) plugins
- `cache/` - Cache plugins for fact caching
- `callback/` - Callback plugins for event handling
- `cliconf/` - CLI configuration plugins for network devices
- `connection/` - Connection plugins for communicating with managed nodes
- `doc_fragments/` - Shared documentation fragments
- `filter/` - Custom Jinja2 filter plugins
- `httpapi/` - HTTP API plugins for API-based systems
- `inventory/` - Dynamic inventory plugins
- `lookup/` - Lookup plugins for data retrieval
- `module_utils/` - Shared code utilities for modules
- `modules/` - Custom Ansible modules
- `netconf/` - NETCONF plugins for network devices
- `shell/` - Shell plugins for command execution
- `strategy/` - Strategy plugins for execution control
- `terminal/` - Terminal plugins for network devices
- `test/` - Custom Jinja2 test plugins
- `vars/` - Variable plugins for dynamic variables

## Development

For information on developing plugins, see:
- [Ansible Plugin Development](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html)
- [Ansible Module Development](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)

## Current Plugins

Currently, this collection does not include custom plugins. The directory structure is in place for future extensibility.
