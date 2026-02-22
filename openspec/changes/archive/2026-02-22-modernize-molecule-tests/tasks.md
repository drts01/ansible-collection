## 1. Create TOML Configuration

- [x] 1.1 Create tox-ansible.toml file with [ansible] section
- [x] 1.2 Add skip list for Python versions < 3.14
- [x] 1.3 Add skip list for Ansible versions < 2.14
- [x] 1.4 Add [tox] section with requires: tox>=4.0, tox-ansible>=26.1, tox-uv>=1.29
- [x] 1.5 Test locally with `tox list` to verify environment generation
- [x] 1.6 Verify tox-uv activation by checking for UV logs in output

## 2. Create pytest-ansible Integration Structure

- [x] 2.1 Create tests/molecule/ directory
- [x] 2.2 Create tests/conftest.py with Molecule scenario fixtures
- [x] 2.3 Create tests/molecule/test_fedora_minimal.py wrapper
- [x] 2.4 Create tests/molecule/test_integration_hello_world.py wrapper
- [x] 2.5 Create tests/molecule/test_utils.py wrapper
- [x] 2.6 Test locally with `pytest tests/molecule/test_fedora_minimal.py -v`

## 3. Update pyproject.toml Configuration

- [x] 3.1 Update [tool.pytest] testpaths to include "tests/molecule"
- [x] 3.2 Add pytest verbosity configuration for Molecule tests
- [x] 3.3 Verify pytest discovers both unit and molecule tests with `pytest --collect-only`

## 4. Create Tox Environments for Testing

- [x] 4.1 Add molecule test environment configuration to tox-ansible.toml
- [x] 4.2 Test molecule environment with `tox -e molecule` (or similar env name)
- [x] 4.3 Verify all three scenarios execute successfully
- [x] 4.4 Check tox-uv is used (faster dependency installation)

## 5. Add GitHub Actions Molecule Job

- [x] 5.1 Add molecule job definition to .github/workflows/tests.yml
- [x] 5.2 Configure Python 3.14 setup with actions/setup-python@v5
- [x] 5.3 Add step to install tox-ansible and tox-uv
- [x] 5.4 Add step to run tox -e molecule
- [x] 5.5 Configure job timeout (30 minutes)
- [x] 5.6 Add conditional artifact upload on failure

## 6. Update CI Integration

- [x] 6.1 Add molecule job to all_green job dependencies
- [x] 6.2 Update all_green assertion to include molecule result
- [x] 6.3 Verify concurrency controls apply to molecule job
- [x] 6.4 Test workflow on a PR branch

## 7. Validate and Test

- [x] 7.1 Run full test suite locally: `tox`
- [x] 7.2 Verify Molecule scenarios pass with pytest integration
- [x] 7.3 Check CI workflow executes successfully in GitHub Actions
- [x] 7.4 Verify tox-uv reduces dependency installation time
- [x] 7.5 Confirm all_green gate blocks PR merge on Molecule failure

## 8. Documentation and Cleanup

- [x] 8.1 Delete tox-ansible.ini file
- [x] 8.2 Update README.md with new testing instructions
- [x] 8.3 Document how to run Molecule tests locally via pytest/tox
- [x] 8.4 Add comments to tox-ansible.toml explaining configuration
- [x] 8.5 Update contributing guide if present
