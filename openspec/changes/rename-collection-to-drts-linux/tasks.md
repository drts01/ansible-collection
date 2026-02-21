## 1. Core Configuration Files

- [ ] 1.1 Update galaxy.yml - change name from `ansible_collection` to `linux`
- [ ] 1.2 Update pyproject.toml - change project name and known_first_party references
- [ ] 1.3 Update devfile.yaml - change project name in identifier

## 2. Documentation Files

- [ ] 2.1 Update README.md - all `ansible-galaxy collection install` commands
- [ ] 2.2 Update README.md - all references to `drts.ansible_collection` in text
- [ ] 2.3 Update README.md - all URLs and links referencing the collection
- [ ] 2.4 Update docs/docsite/links.yml - repository references
- [ ] 2.5 Update plugins/README.md - collection name references
- [ ] 2.6 Update playbooks/README.md - example commands and role references

## 3. Playbook Files

- [ ] 3.1 Update playbooks/fedora_minimal_setup.yml - role references
- [ ] 3.2 Update playbooks/test_fedora_minimal.yml - role references

## 4. Test Files

- [ ] 4.1 Update tests/integration/targets/hello_world/tasks/main.yml - filter references
- [ ] 4.2 Update tests/unit/test_basic.py - docstring references

## 5. Verification and Documentation

- [ ] 5.1 Verify all files have been updated by searching for remaining `ansible_collection` references
- [ ] 5.2 Test that collection can be installed with new name
- [ ] 5.3 Update CHANGELOG.md with breaking change notice
- [ ] 5.4 Create git commit with all changes
