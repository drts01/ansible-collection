---
description: 'Copilot instructions for Ansible roles and playbooks'
applyTo: '**/roles/**/*.y*ml, **/playbooks/**/*.y*ml, **/ansible/**/*.y*ml, **/requirements.y*ml, **/molecule/**/*.y*ml, **/galaxy.y*ml'
---

# Ansible Development Instructions

## Overview

Write idempotent, secure roles, tasks, and playbooks for RPM/DEB systems. Align implementations to relevant CIS benchmarks (Linux/Ubuntu/RHEL) and document the benchmark/version each role targets.

## General Instructions

- Use Ansible to configure and manage infrastructure.
- Use version control for your Ansible configurations.
- Keep things simple; only use advanced features when necessary
- Give every play, block, and task a concise but descriptive `name`
  - Start names with an action verb that indicates the operation being performed, such as "Install," "Configure," or "Copy"
  - Capitalize the first letter of the task name
  - Omit periods from the end of task names for brevity
  - Omit the role name from role tasks; Ansible will automatically display the role name when running a role
  - When including tasks from a separate file, you may include the filename in each task name to make tasks easier to locate (e.g., `<TASK_FILENAME> : <TASK_NAME>`)
- Use comments to provide additional context about **what**, **how**, and/or **why** something is being done
  - Don't include redundant comments
- Use dynamic inventory for cloud resources
  - Use tags to dynamically create groups based on environment, function, location, etc.
  - Use `group_vars` to set variables based on these attributes
- Use idempotent Ansible modules whenever possible; avoid `shell`, `command`, and `raw`, as they break idempotency
  - If you have to use `shell` or `command`, use the `creates:` or `removes:` parameter, where feasible, to prevent unnecessary execution
  - Keep tasks idempotent and check-mode friendly; avoid `changed_when` unless absolutely necessary and document rationale
- Use [fully qualified collection names (FQCN)](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html#term-Fully-Qualified-Collection-Name-FQCN) to ensure the correct module or plugin is selected
  - Use the `ansible.builtin` collection for [builtin modules and plugins](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html#plugin-index)
  - Prefer `ansible.builtin.*` modules; pin external collections in `requirements.yml` when necessary


- Group related tasks together to improve readability and modularity
- For modules where `state` is optional, explicitly set `state: present` or `state: absent` to improve clarity and consistency
- Use the lowest privileges necessary to perform a task
  - Only set `become: true` at the play level or on an `include:` statement, if all included tasks require super user privileges; otherwise, specify `become: true` at the task level
  - Only set `become: true` on a task if it requires super user privileges
- Prefer declarative, idempotent modules (for example: `package`, `service`, `user`, `group`, `file`, `template`, `copy`) over imperative `shell`/`command`/`raw` invocations
- Prefer generic modules (`service`, `package`) for cross-distro compatibility; use distro-specific modules only when required
 - Branch on `ansible_facts.os_family` or `ansible_facts.distribution` and maintain per-distro maps (for example: `packages_by_os`, `service_name_map`)
 - Enforce strict ownership and permissions for files (`mode: '0640'` or stricter); avoid world-writable or world-readable modes for secrets
 - Use `validate` on templates and prefer atomic writes; document any use of `unsafe_writes`
 - Use `block` with `rescue`/`always` for safe cleanup (for example, temporary-secret cleanup) and use `assert` for critical preconditions (supported OS, minimum package versions, required vars)
 - Avoid `ignore_errors`; prefer explicit `failed_when` with justification or `block`/`rescue` flows
 - Place sensible, low-priority defaults in `defaults/main.yml`; use `vars/` for higher-priority variables and document intended use
 - Use handlers for service reloads/restarts and prefer shared handlers with `listen`


## Secret Management
 
- Avoid using `set_fact` to store secrets
- When using Ansible alone, store secrets using Ansible Vault
  - Use the following process to make it easy to find where vaulted variables are defined
    1. Create a `group_vars/` subdirectory named after the group
    2. Inside this subdirectory, create two files named `vars` and `vault`
    3. In the `vars` file, define all of the variables needed, including any sensitive ones
    4. Copy all of the sensitive variables over to the `vault` file and prefix these variables with `vault_`
    5. Adjust the variables in the `vars` file to point to the matching `vault_` variables using Jinja2 syntax: `db_password: "{{ vault_db_password }}"`
    6. Encrypt the `vault` file to protect its contents
    7. Use the variable name from the `vars` file in your playbooks
- When using other tools with Ansible (e.g., Terraform), store secrets in a third-party secrets management tool (e.g., Hashicorp Vault, AWS Secrets Manager, etc.)
  - This allows all tools to reference a single source of truth for secrets and prevents configurations from getting out of sync
 - Never store secrets in plaintext; prefer Ansible Vault or an external secret manager and document where secrets live
 - Mark sensitive tasks and variables with `no_log: true` and consider `diff: false` for sensitive file changes

## Style

- Use 2-space indentation and always indent lists
- Separate each of the following with a single blank line:
  - Two host blocks
  - Two task blocks
  - Host and include blocks
- Use `snake_case` for variable names
- Sort variables alphabetically when defining them in `vars:` maps or variable files
- Always use multi-line map syntax, regardless of how many pairs exist in the map
  - It improves readability and reduces changeset collisions for version control
- Prefer single quotes over double quotes
  - The only time you should use double quotes is when they are nested within single quotes (e.g. Jinja map reference), or when your string requires escaping characters (e.g., using "\n" to represent a newline)
  - If you must write a long string, use folded block scalar syntax (i.e., `>`) to replace newlines with spaces or literal block scalar syntax (i.e., `|`) to preserve newlines; omit all special quoting
- The `host` section of a play should follow this general order:
  - `hosts` declaration
  - Host options in alphabetical order (e.g., `become`, `remote_user`, `vars`)
  - `pre_tasks`
  - `roles`
  - `tasks`
- Each task should follow this general order:
  - `name`
  - Task declaration (e.g., `service:`, `package:`)
  - Task parameters (using multi-line map syntax)
  - Loop operators (e.g., `loop`)
  - Task options in alphabetical order (e.g. `become`, `ignore_errors`, `register`)
  - `tags`
- For `import_tasks`/`include_tasks` statements, quote filenames and only use blank lines between `include` statements if they are multi-line (e.g., they have tags)

## Hardening

- Apply a CIS or organizational hardening profile when relevant and document the pinned benchmark/version.
- SSH: disable root login and password authentication unless explicitly justified.
- Sudo: prefer requiring MFA where available and document privilege boundaries in the role README.
- Ensure time sync (chronyd/ntp), centralized logging, and file-integrity monitoring (e.g., `aide`) are part of the hardened baseline.

## CIS Benchmark Alignment

- Pin the benchmark version at the role level and document which controls the role covers.
- Reference control IDs in the role `README.md` and provide verification/test tasks mapping to those controls.

## Testing & Validation

- Provide Molecule scenarios for each supported platform/variant and include idempotence and verification tests.
- Include security validation checks (file modes, ownership, service state) and read-only audit tasks for sensitive settings where applicable.

## Linting

- Use `ansible-lint` and `yamllint` to check syntax and enforce project standards
- Use `ansible-playbook --syntax-check` to check for syntax errors
- Use `ansible-playbook --check --diff` to perform a dry-run of playbook execution

<!-- 
These guidelines were based on, or copied from, the following sources:

- [Ansible Documentation - Tips and Tricks](https://docs.ansible.com/ansible/latest/tips_tricks/index.html)
- [Whitecloud Ansible Styleguide](https://github.com/whitecloud/ansible-styleguide)
-->
