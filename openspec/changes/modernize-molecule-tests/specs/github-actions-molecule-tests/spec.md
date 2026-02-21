## ADDED Requirements

### Requirement: Molecule test job in GitHub Actions

The CI/CD workflow SHALL include a dedicated job for executing Molecule tests via tox-ansible.

#### Scenario: Job definition
- **WHEN** a pull request is opened or code is pushed to main
- **THEN** the workflow SHALL trigger a molecule test job
- **AND** SHALL run in parallel with other test jobs (sanity, lint, unit)

#### Scenario: Job dependencies
- **WHEN** the molecule job executes
- **THEN** the job SHALL have no dependencies on other jobs
- **AND** SHALL be independently runnable

### Requirement: Python and dependency setup

The GitHub Actions job SHALL configure Python 3.14+ and install required testing dependencies.

#### Scenario: Python installation
- **WHEN** the molecule job initializes
- **THEN** the system SHALL install Python 3.14
- **AND** SHALL use actions/setup-python@v5 or later

#### Scenario: Test dependency installation
- **WHEN** Python is configured
- **THEN** the system SHALL install tox-ansible and tox-uv
- **AND** SHALL use pip or uv for installation
- **AND** installation SHALL complete within 2 minutes

### Requirement: Tox-ansible execution

The workflow SHALL execute Molecule tests using tox-ansible orchestration.

#### Scenario: Tox environment execution
- **WHEN** dependencies are installed
- **THEN** the system SHALL run tox -e molecule (or similar)
- **AND** SHALL execute all configured Molecule scenarios

#### Scenario: Test failure handling
- **WHEN** a Molecule test fails
- **THEN** the GitHub Actions job SHALL fail with non-zero exit code
- **AND** SHALL display pytest output in job logs
- **AND** SHALL prevent PR merge

### Requirement: Container runtime availability

The GitHub Actions runner SHALL have Podman available for Molecule container operations.

#### Scenario: Podman availability
- **WHEN** Molecule scenarios execute in CI
- **THEN** Podman SHALL be available and functional
- **AND** SHALL support privileged containers for systemd testing

#### Scenario: Container cleanup
- **WHEN** tests complete or fail
- **THEN** the system SHALL cleanup all created containers
- **AND** SHALL not leave orphaned containers on the runner

### Requirement: Integration with PR checks

The Molecule test job SHALL be integrated into the workflow's all_green status check.

#### Scenario: All green gate
- **WHEN** all test jobs complete
- **THEN** the all_green job SHALL consider molecule test results
- **AND** SHALL fail if molecule tests fail
- **AND** SHALL block PR merge until all tests pass

#### Scenario: Status check requirement
- **WHEN** a PR is ready for merge
- **THEN** the repository SHALL require all_green status check to pass
- **AND** SHALL include molecule test results in the check

### Requirement: Execution time optimization

The Molecule test job SHALL complete within reasonable time limits using tox-uv acceleration.

#### Scenario: Target execution time
- **WHEN** Molecule tests run in CI
- **THEN** the job SHALL complete within 15 minutes
- **AND** tox-uv SHALL reduce dependency installation time
- **AND** SHALL provide feedback on excessive test duration

#### Scenario: Timeout protection
- **WHEN** tests exceed reasonable time limits
- **THEN** the job SHALL timeout after 30 minutes
- **AND** SHALL fail with a timeout error message

### Requirement: Test result artifacts

The workflow SHALL preserve test results and logs as GitHub Actions artifacts on failure.

#### Scenario: Failure artifact upload
- **WHEN** Molecule tests fail
- **THEN** the workflow SHALL upload pytest output as artifact
- **AND** SHALL upload container logs if available
- **AND** artifacts SHALL be retained for 7 days

#### Scenario: Success artifact skipping
- **WHEN** all Molecule tests pass
- **THEN** the workflow SHALL not upload artifacts
- **AND** SHALL conserve storage space

### Requirement: Manual trigger support

The workflow SHALL support manual triggering via workflow_dispatch for testing purposes.

#### Scenario: Manual execution
- **WHEN** a developer manually triggers the workflow
- **THEN** the system SHALL execute all test jobs including molecule
- **AND** SHALL allow testing without creating a PR

#### Scenario: Branch selection
- **WHEN** manually triggering the workflow
- **THEN** the developer SHALL be able to select the target branch
- **AND** SHALL execute tests against that branch's code

### Requirement: Concurrency control

The workflow SHALL use concurrency groups to cancel outdated test runs.

#### Scenario: PR update cancellation
- **WHEN** new commits are pushed to a PR
- **THEN** the system SHALL cancel in-progress test runs for that PR
- **AND** SHALL start new test runs with updated code
- **AND** SHALL use the PR head_ref as concurrency group key

#### Scenario: Main branch protection
- **WHEN** tests run on the main branch
- **THEN** concurrent runs SHALL not cancel each other
- **AND** SHALL allow multiple main branch test runs
