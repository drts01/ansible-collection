## Why

The current testing infrastructure needs enhancement to align with Ansible collection best practices and modern Python tooling. While the foundation (pytest + tox + molecule) is solid, gaps exist in dependency management, test coverage reporting, and CI/CD visibility. Modernizing now will improve maintainability, enable better test coverage tracking, and provide clear feedback to contributors.

## What Changes

- Consolidate all dependencies into `pyproject.toml` using modern PEP 621/735 standards
- Add comprehensive coverage reporting (HTML, XML, JUnit, terminal formats)
- Configure GitHub Actions to display coverage in PR comments and test result summaries
- Enhance tox configuration with coverage, lint, and Ansible 2.20+ matrix environments
- Add pytest-cov integration for automated coverage collection
- Expand unit test framework for role testing
- Update CI/CD workflows to use `uv sync` for faster, reproducible builds
- Add comprehensive testing documentation (TESTING.md) and README updates
- Configure coverage thresholds and quality gates

## Capabilities

### New Capabilities
- `pytest-coverage-config`: Pytest and pytest-cov configuration for comprehensive coverage reporting with multiple output formats
- `pyproject-dependencies`: Centralized dependency management in pyproject.toml with proper dependency groups for dev, test, and build tools
- `tox-test-environments`: Enhanced tox environments for coverage, linting, and Ansible version matrix testing
- `github-actions-coverage`: GitHub Actions integration for coverage PR comments, test result summaries, and actions summaries
- `testing-documentation`: Comprehensive testing documentation including TESTING.md, README updates, and contributor guidelines

### Modified Capabilities
<!-- No existing capabilities are being modified - this is enhancement only -->

## Impact

**Affected Files:**
- `pyproject.toml` - Add dependency groups and pytest/coverage configuration
- `tox.toml` - Add new test environments and coverage integration
- `requirements.txt` - Convert to reference pyproject.toml
- `test-requirements.txt` - Convert to reference pyproject.toml
- `.github/workflows/tests.yml` - Add coverage reporting steps
- `.github/workflows/molecule.yml` - Add coverage and test reporting
- `tests/conftest.py` - Enhance pytest fixtures for better test support
- `tests/unit/` - Add comprehensive role unit tests

**New Files:**
- `TESTING.md` - Testing guide for contributors
- `.coveragerc` or coverage config in pyproject.toml
- `tests/output/` - Coverage and test report output directory (gitignored)

**Dependencies:**
- Add pytest-cov, coverage[toml], pytest-xdist to dev dependencies
- Pin Ansible versions to 2.20+ (Fedora 43+ compatibility)
- Add test reporting tools for GitHub Actions

**Systems:**
- GitHub Actions workflows enhanced with coverage display
- Local development workflow improved with clear testing commands
- CI/CD feedback loop enhanced with immediate coverage visibility
