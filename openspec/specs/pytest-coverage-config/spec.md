# Pytest Coverage Configuration Specification

## ADDED Requirements

### Requirement: Multiple coverage output formats
The system SHALL generate coverage reports in HTML, XML, JUnit, and terminal formats simultaneously.

#### Scenario: Coverage reports generated in all formats
- **WHEN** tests run with coverage enabled via `pytest --cov`
- **THEN** system generates HTML report at `tests/output/coverage/html/index.html`
- **THEN** system generates XML report at `tests/output/coverage/coverage.xml`
- **THEN** system generates JUnit XML at `tests/output/junit/results.xml`
- **THEN** system displays coverage summary in terminal output

### Requirement: Coverage source configuration
The system SHALL track coverage for the collection code under `ansible_collections.drts.casc` package.

#### Scenario: Collection code tracked for coverage
- **WHEN** tests execute collection roles or plugins
- **THEN** system records coverage metrics for files under `ansible_collections/drts/casc/`
- **THEN** system excludes test files matching `*/tests/*` and `*/test_*` patterns

### Requirement: Coverage exclusion rules
The system SHALL exclude common non-testable code patterns from coverage requirements.

#### Scenario: Standard exclusions applied
- **WHEN** coverage report is generated
- **THEN** system excludes lines with `pragma: no cover` comment
- **THEN** system excludes `__repr__` method definitions
- **THEN** system excludes `raise AssertionError` statements
- **THEN** system excludes `raise NotImplementedError` statements

### Requirement: Pytest configuration in pyproject.toml
The system SHALL configure pytest and coverage settings in `pyproject.toml` using standard tool configuration sections.

#### Scenario: Pytest configuration loaded
- **WHEN** pytest runs without command-line arguments
- **THEN** system applies configuration from `[tool.pytest.ini_options]`
- **THEN** system applies coverage settings from `[tool.coverage.run]` and `[tool.coverage.report]`

### Requirement: Terminal coverage display
The system SHALL show missing coverage lines in terminal output for immediate developer feedback.

#### Scenario: Missing coverage highlighted
- **WHEN** tests run with coverage enabled
- **THEN** terminal output shows coverage percentage for each file
- **THEN** terminal output lists line numbers with missing coverage

### Requirement: Coverage report output directory
The system SHALL write all coverage artifacts to `tests/output/` directory structure.

#### Scenario: Organized output directory
- **WHEN** coverage reports are generated
- **THEN** HTML reports are in `tests/output/coverage/html/`
- **THEN** XML reports are in `tests/output/coverage/`
- **THEN** JUnit XML is in `tests/output/junit/`
- **THEN** output directories are created automatically if missing
