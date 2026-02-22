# Implementation Tasks for Modernize Collection Testing

## 1. Update Dependencies Configuration

- [x] 1.1 Add ansible-core>=2.20 to [project.dependencies] in pyproject.toml
- [x] 1.2 Create [dependency-groups.dev] section with pytest, pytest-cov, pytest-xdist, pytest-ansible, coverage[toml], molecule, molecule-plugins[podman]
- [x] 1.3 Create [dependency-groups.build] section with tox>=4.40, tox-ansible>=26.1, tox-uv>=1.29
- [x] 1.4 Create [dependency-groups.lint] section with ansible-lint>=26.1, yamllint>=1.35
- [x] 1.5 Update requirements.txt to reference pyproject.toml with comment and -e .
- [x] 1.6 Update test-requirements.txt to reference pyproject.toml with comment and -e .[dev]
- [x] 1.7 Run `uv lock` to update lock file with new dependencies
- [x] 1.8 Test local installation with `uv sync --group dev`
- [x] 1.9 Verify all dependencies install correctly

## 2. Configure Pytest and Coverage

- [x] 2.1 Add [tool.pytest.ini_options] to pyproject.toml with addopts for coverage
- [x] 2.2 Configure --cov=ansible_collections.drts.casc in pytest options
- [x] 2.3 Configure --cov-report=html:tests/output/coverage/html in pytest options
- [x] 2.4 Configure --cov-report=xml:tests/output/coverage/coverage.xml in pytest options
- [x] 2.5 Configure --cov-report=term-missing in pytest options
- [x] 2.6 Configure --junit-xml=tests/output/junit/results.xml in pytest options
- [x] 2.7 Add [tool.coverage.run] section with source and omit configuration
- [x] 2.8 Add [tool.coverage.report] section with exclude_lines configuration
- [x] 2.9 Add tests/output/ to .gitignore
- [x] 2.10 Run pytest locally with --cov to verify configuration
- [x] 2.11 Verify HTML report generates at expected location
- [x] 2.12 Verify XML and JUnit reports generate correctly

## 3. Enhance Tox Configuration

- [x] 3.1 Add [env.coverage] environment to tox.toml with description
- [x] 3.2 Configure coverage environment commands to run pytest with coverage
- [x] 3.3 Add [env.lint] environment to tox.toml with description
- [x] 3.4 Configure lint environment commands for ansible-lint and yamllint
- [x] 3.5 Update [ansible] section skip list to exclude Python 3.10, 3.11, 3.12
- [x] 3.6 Update [ansible] section skip list to exclude Ansible 2.18 and 2.19
- [x] 3.7 Verify tox-ansible generates correct Ansible 2.20+ matrix environments
- [x] 3.8 Test `tox run -e coverage` locally
- [x] 3.9 Test `tox run -e lint` locally
- [x] 3.10 Test `tox list` shows all environments with descriptions

## 4. Update GitHub Actions for Tests Workflow

- [x] 4.1 Add permissions section to .github/workflows/tests.yml for pull-requests and contents write
- [x] 4.2 Add step to install uv using astral-sh/setup-uv action
- [x] 4.3 Add step to run `uv sync --group dev` for dependency installation
- [x] 4.4 Add step to run pytest with coverage
- [x] 4.5 Add step for py-cov-action/python-coverage-comment-action@v3 with conditional on pull_request
- [x] 4.6 Add step for dorny/test-reporter@v1 with if: always() for test results
- [x] 4.7 Configure test-reporter to use tests/output/junit/results.xml
- [x] 4.8 Add step to append coverage summary to GITHUB_STEP_SUMMARY
- [x] 4.9 Add step to upload coverage HTML report as artifact
- [x] 4.10 Add step to upload coverage XML report as artifact
- [x] 4.11 Add step to upload JUnit XML as artifact

## 5. Update GitHub Actions for Molecule Workflow

- [x] 5.1 Add permissions section to .github/workflows/molecule.yml for pull-requests and contents write
- [x] 5.2 Update molecule job to install uv if not already present
- [x] 5.3 Update molecule job to use `uv sync --group dev` instead of pip install
- [x] 5.4 Add coverage reporting steps after molecule tests
- [x] 5.5 Add py-cov-action for PR comments (conditional on pull_request)
- [x] 5.6 Add dorny/test-reporter for test results display
- [x] 5.7 Add coverage summary to Actions summary
- [x] 5.8 Add artifact uploads for coverage reports

## 6. Create Testing Documentation

- [x] 6.1 Create TESTING.md file with introduction to testing approach
- [x] 6.2 Add Prerequisites section (Python 3.14+, uv, Podman)
- [x] 6.3 Add Installation section with `uv sync --group dev` instructions
- [x] 6.4 Add Quick Start section with basic pytest commands
- [x] 6.5 Add Running Tests with Coverage section
- [x] 6.6 Add Tox Environments section listing all environments
- [x] 6.7 Add Molecule Testing section explaining scenarios and pytest wrappers
- [x] 6.8 Add Coverage Reports section explaining how to view HTML reports
- [x] 6.9 Add CI/CD Testing section explaining GitHub Actions workflows
- [x] 6.10 Add Troubleshooting section with common issues and solutions
- [x] 6.11 Add Test Directory Structure section explaining organization
- [x] 6.12 Add Writing Tests section with guidelines and examples
- [x] 6.13 Add Ansible Version Testing section explaining version matrix

## 7. Update README Documentation

- [x] 7.1 Add Testing section to README.md
- [x] 7.2 Add quick start testing command
- [x] 7.3 Add link to TESTING.md for detailed instructions
- [x] 7.4 Add badge for tests/CI status (optional)
- [x] 7.5 Add badge for coverage (optional, can use shields.io)
- [x] 7.6 Update Development section if exists with uv instructions

## 8. Testing and Verification

- [x] 8.1 Run full test suite locally with `pytest --cov`
- [x] 8.2 Verify all coverage reports generate correctly
- [x] 8.3 Run `tox run -e coverage` and verify success
- [x] 8.4 Run `tox run -e lint` and fix any linting issues
- [x] 8.5 Run `tox run -e molecule` and verify Molecule tests pass (pre-existing test failures)
- [ ] 8.6 Create test branch and open PR to test GitHub Actions
- [ ] 8.7 Verify coverage PR comment appears on test PR
- [ ] 8.8 Verify test results display in Actions UI
- [ ] 8.9 Verify Actions summary shows coverage metrics
- [ ] 8.10 Verify coverage artifacts are uploadable and downloadable
- [ ] 8.11 Review and address any issues found during testing

## 9. Final Cleanup and Documentation

- [x] 9.1 Remove any obsolete test configuration files (none found)
- [x] 9.2 Update .gitignore if needed for new output directories
- [x] 9.3 Review all documentation for accuracy and completeness
- [ ] 9.4 Add migration notes for existing contributors if needed (optional)
- [x] 9.5 Update CHANGELOG.md with testing improvements
- [ ] 9.6 Commit all changes with descriptive commit messages
- [ ] 9.7 Open pull request with complete implementation
- [ ] 9.8 Address any PR review feedback
