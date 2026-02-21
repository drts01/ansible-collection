## Context

The Ansible collection is currently named `drts.ansible_collection`, which is generic and doesn't communicate its purpose. The collection focuses on Linux system configuration and hardening, particularly for Fedora systems. Renaming to `drts.linux` will improve discoverability and clarity for users seeking Linux-specific Ansible automation.

This is a straightforward rename operation affecting configuration files, documentation, and code references. The namespace (`drts`) remains unchanged, only the collection name (`ansible_collection` → `linux`) changes.

## Goals / Non-Goals

**Goals:**
- Rename the collection from `drts.ansible_collection` to `drts.linux` across all files
- Update all references in configuration, documentation, playbooks, and tests
- Maintain backward compatibility considerations (document breaking changes)
- Ensure all installation instructions and examples reflect the new name
- Update Python package references and imports

**Non-Goals:**
- Changing the namespace from `drts` to something else
- Modifying collection functionality or features
- Creating migration tooling or compatibility shims
- Updating external documentation outside this repository

## Decisions

### Decision 1: Scope of Rename
**Choice**: Rename across all files (configuration, documentation, code, tests)
**Rationale**: A partial rename would create confusion and inconsistency. Users need to see the new name everywhere.
**Alternatives Considered**:
- Gradual rename (phase 1: config, phase 2: docs, etc.) - Rejected: Creates confusion during transition
- Keep old name in some places - Rejected: Inconsistent and confusing

### Decision 2: File-by-File Approach
**Choice**: Use targeted find-and-replace operations on each file type
**Rationale**: Allows verification of each change and ensures accuracy. Different file types have different contexts where the name appears.
**Alternatives Considered**:
- Automated bulk rename script - Rejected: Risk of unintended replacements in comments or URLs
- Manual editing - Rejected: Error-prone and time-consuming

### Decision 3: Breaking Change Communication
**Choice**: Document breaking changes in proposal and changelog
**Rationale**: Users need to know they must update their requirements.yml and playbooks
**Alternatives Considered**:
- Create compatibility layer - Rejected: Out of scope, adds complexity
- Silent breaking change - Rejected: Poor user experience

## Risks / Trade-offs

**Risk**: Users with existing playbooks referencing `drts.ansible_collection` will experience failures
- **Mitigation**: Document breaking changes clearly in CHANGELOG and README. Provide migration instructions.

**Risk**: External documentation or tutorials referencing the old name will become outdated
- **Mitigation**: This is expected for a major rename. Update repository documentation; external sources will eventually update.

**Risk**: Galaxy.com may cache the old collection name temporarily
- **Mitigation**: This is normal behavior for Galaxy. New releases will be published under the new name.

**Trade-off**: Breaking change vs. clarity
- **Rationale**: The improved clarity and discoverability of `drts.linux` outweighs the inconvenience of a one-time update for users.

## Migration Plan

### Implementation Steps
1. Update `galaxy.yml` - change collection name from `ansible_collection` to `linux`
2. Update `pyproject.toml` - change project name and known_first_party references
3. Update `README.md` - all installation commands and examples
4. Update `docs/docsite/links.yml` - repository references
5. Update playbook files - role references
6. Update test files - filter and import references
7. Update `devfile.yaml` - project name
8. Update `plugins/README.md` - documentation
9. Update `playbooks/README.md` - example commands

### Deployment
- Create a new release (e.g., 1.1.0) with the renamed collection
- Publish to Ansible Galaxy under the new name `drts.linux`
- Update repository documentation

### Rollback Strategy
- If critical issues arise, the old collection remains available on Galaxy as `drts.ansible_collection`
- Users can pin to older versions if needed
- No data loss or state concerns (stateless collection)

## Open Questions

- Should we maintain the old collection on Galaxy for a deprecation period? (Recommendation: Yes, for 2-3 releases)
- Do we need to update any CI/CD workflows that reference the collection name? (Recommendation: Yes, check GitHub Actions workflows)
