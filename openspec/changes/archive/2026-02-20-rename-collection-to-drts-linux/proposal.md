## Why

The current collection name `drts.ansible_collection` is generic and doesn't clearly communicate its purpose. Renaming to `drts.linux` better reflects the collection's focus on Linux system configuration and hardening, making it more discoverable and intuitive for users seeking Linux-specific Ansible automation.

## What Changes

- Collection name changes from `drts.ansible_collection` to `drts.linux` (namespace `drts` remains unchanged)
- All references to the collection name updated across documentation, configuration files, and code
- Installation commands and examples updated to reflect new collection name
- Python project configuration updated to reflect new package name
- Development environment configuration updated
- All role references, filter references, and imports updated throughout the codebase

## Capabilities

### New Capabilities

- `collection-rename`: Rename the Ansible collection from `drts.ansible_collection` to `drts.linux` across all configuration files, documentation, playbooks, tests, and code references

### Modified Capabilities

(No existing capabilities have requirement changes - this is a pure rename operation)

## Impact

**Affected Files:**
- `galaxy.yml` - collection metadata
- `pyproject.toml` - Python project configuration
- `README.md` - documentation and installation instructions
- `docs/docsite/links.yml` - repository documentation links
- `playbooks/fedora_minimal_setup.yml` - role references
- `playbooks/test_fedora_minimal.yml` - role references
- `playbooks/README.md` - example commands
- `plugins/README.md` - plugin documentation
- `tests/integration/targets/hello_world/tasks/main.yml` - filter references
- `tests/unit/test_basic.py` - docstring references
- `devfile.yaml` - development environment configuration

**Breaking Changes:**
- **BREAKING**: Users will need to update their `requirements.yml` files to use `drts.linux` instead of `drts.ansible_collection`
- **BREAKING**: Any existing playbooks referencing `drts.ansible_collection` roles/plugins will need to be updated to use `drts.linux`

**Dependencies:**
- No external dependencies affected
- Internal references only (no published API changes beyond the collection name itself)
