# GitHub Actions Coverage Integration Specification

## ADDED Requirements

### Requirement: Coverage PR comments
The system SHALL post coverage reports as comments on pull requests.

#### Scenario: Coverage comment on PR
- **WHEN** tests run in a pull request workflow
- **THEN** system posts coverage report as PR comment
- **THEN** comment shows overall coverage percentage
- **THEN** comment highlights files with coverage changes
- **THEN** comment indicates coverage increase or decrease

### Requirement: Test results summary display
The system SHALL display formatted test results in GitHub Actions UI using test reporter.

#### Scenario: Test results in Actions UI
- **WHEN** tests complete in GitHub Actions
- **THEN** system displays test results summary in Actions UI
- **THEN** system shows passed, failed, and skipped test counts
- **THEN** system provides details for failed tests
- **THEN** system uses JUnit XML format for reporting

### Requirement: Native Actions summary display
The system SHALL add coverage information to GitHub Actions run summary using native markdown.

#### Scenario: Coverage in Actions summary
- **WHEN** tests complete in GitHub Actions
- **THEN** system appends coverage report to GITHUB_STEP_SUMMARY
- **THEN** summary shows coverage metrics in markdown table format
- **THEN** summary is visible on Actions run page without opening logs

### Requirement: Coverage report artifacts
The system SHALL upload coverage reports as workflow artifacts for later inspection.

#### Scenario: Coverage artifacts uploaded
- **WHEN** tests complete in GitHub Actions
- **THEN** system uploads HTML coverage report as artifact
- **THEN** system uploads XML coverage report as artifact
- **THEN** system uploads JUnit XML as artifact
- **THEN** artifacts are available for download from Actions UI

### Requirement: UV sync for dependency installation
The system SHALL use uv sync for fast dependency installation in CI/CD.

#### Scenario: Dependencies installed with uv
- **WHEN** GitHub Actions workflow sets up environment
- **THEN** system installs uv tool
- **THEN** system runs `uv sync --group dev` to install dependencies
- **THEN** system uses cached uv environments for speed
- **THEN** installation completes faster than pip-based approach

### Requirement: Workflow permissions
The system SHALL configure appropriate permissions for coverage PR comments.

#### Scenario: Permissions for PR comments
- **WHEN** coverage comment action runs
- **THEN** workflow has write permission for pull-requests
- **THEN** workflow has write permission for contents
- **THEN** GITHUB_TOKEN provides necessary authentication

### Requirement: Coverage on pull request and push
The system SHALL run coverage reporting on both pull request and push events.

#### Scenario: Coverage on PR
- **WHEN** pull request is opened or updated
- **THEN** system runs tests with coverage
- **THEN** system posts coverage comment to PR

#### Scenario: Coverage on push
- **WHEN** code is pushed to main branch
- **THEN** system runs tests with coverage
- **THEN** system uploads coverage reports as artifacts

### Requirement: Conditional coverage comment execution
The system SHALL only post PR comments when running in pull request context.

#### Scenario: PR comment only on pull requests
- **WHEN** workflow runs on push to main branch
- **THEN** system skips PR comment action
- **WHEN** workflow runs on pull request
- **THEN** system executes PR comment action

### Requirement: Test reporter failure handling
The system SHALL always run test reporter even if tests fail.

#### Scenario: Test reporter runs on failure
- **WHEN** tests fail in GitHub Actions
- **THEN** system still executes test reporter action
- **THEN** system displays failed test details
- **THEN** workflow marks test reporter step with if: always() condition
