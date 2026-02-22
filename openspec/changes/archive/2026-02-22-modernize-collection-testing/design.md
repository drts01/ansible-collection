## Context

The drts.casc Ansible collection currently has a functional testing infrastructure using pytest, tox-ansible, tox-uv, and molecule. However, several gaps exist:

**Current State:**
- Dependencies scattered across `requirements.txt`, `test-requirements.txt`, and `pyproject.toml`
- Minimal pytest configuration
- No coverage reporting configured
- Basic tox configuration with only molecule environment
- CI/CD workflows lack coverage visibility
- No formal testing documentation
- Testing targets Fedora 43+ with Ansible 2.20+

**Constraints:**
- Must maintain pytest + tox + molecule architecture (user requirement)
- Must keep `extensions/molecule/` structure (follows Molecule documentation for collections)
- Must use uv for dependency management (already in place with uv.lock)
- Must support Fedora 43+ containers via Podman
- Cannot use ansible-test (user prefers modern pytest approach)

**Stakeholders:**
- Collection maintainers who need clear test feedback
- Contributors who need easy local testing
- CI/CD systems that need reliable coverage reporting

## Goals / Non-Goals

**Goals:**
1. Centralize all dependencies in `pyproject.toml` using PEP 621/735 standards
2. Enable comprehensive coverage reporting with multiple formats (HTML, XML, JUnit, terminal)
3. Display coverage in GitHub Actions via PR comments and test summaries
4. Create Ansible version matrix testing (2.20+) with enhanced tox environments
5. Provide clear testing documentation for contributors
6. Maintain fast test execution with uv and parallel testing

**Non-Goals:**
- Migrating to ansible-test (staying with pytest)
- Restructuring Molecule scenario locations (keeping extensions/molecule/)
- Adding integration with external services (e.g., Codecov paid features)
- Testing Ansible versions below 2.20
- Testing operating systems other than Fedora 43+

## Decisions

### Decision 1: Dependency Management Strategy

**Choice:** Consolidate all dependencies into `pyproject.toml` with dependency groups

**Rationale:**
- PEP 621 (project metadata) + PEP 735 (dependency groups) are modern standards
- `uv` has excellent support for dependency groups
- Single source of truth reduces maintenance burden
- Allows optional dependency groups (dev, test, build, lint)

**Alternatives Considered:**
- Keep requirements.txt: Rejected - duplicates metadata, harder to maintain
- Use extras in pyproject.toml: Rejected - dependency groups are more flexible and modern

**Implementation:**
```toml
[project]
dependencies = [
  "ansible-core>=2.20",
]

[dependency-groups]
dev = [
  "pytest>=8.0",
  "pytest-cov>=6.0",
  "pytest-xdist>=3.0",
  "pytest-ansible>=26.1",
  "coverage[toml]>=7.0",
  "molecule>=7.0",
  "molecule-plugins[podman]>=25.8",
]

build = [
  "tox>=4.40",
  "tox-ansible>=26.1",
  "tox-uv>=1.29",
]

lint = [
  "ansible-lint>=26.1",
  "yamllint>=1.35",
]
```

### Decision 2: Coverage Reporting Format

**Choice:** Multi-format coverage output (HTML + XML + JUnit + Terminal)

**Rationale:**
- HTML: Best for local development and debugging
- XML: Standard format for tools and CI/CD integration
- JUnit: Test result reporting in GitHub Actions
- Terminal: Immediate feedback during test runs

**Alternatives Considered:**
- Single format (XML only): Rejected - poor local developer experience
- External service (Codecov): Deferred - can add later without architecture changes

**Implementation:**
```toml
[tool.pytest.ini_options]
addopts = [
  "--cov=ansible_collections.drts.casc",
  "--cov-report=html:tests/output/coverage/html",
  "--cov-report=xml:tests/output/coverage/coverage.xml",
  "--cov-report=term-missing",
  "--junit-xml=tests/output/junit/results.xml",
]

[tool.coverage.run]
source = ["ansible_collections.drts.casc"]
omit = ["*/tests/*", "*/test_*"]

[tool.coverage.report]
exclude_lines = [
  "pragma: no cover",
  "def __repr__",
  "raise AssertionError",
  "raise NotImplementedError",
]
```

### Decision 3: GitHub Actions Coverage Display

**Choice:** Three-pronged display strategy (PR comments + test summary + actions summary)

**Rationale:**
- PR comments (py-cov-action): Reviewers see coverage changes directly on PRs
- Test summary (dorny/test-reporter): Formatted JUnit results for debugging failures
- Actions summary (native): Quick glance at coverage without extra actions

**Alternatives Considered:**
- Codecov only: Rejected - requires external service, overkill for current needs
- Actions summary only: Rejected - insufficient visibility for reviewers
- Custom script: Rejected - third-party actions are well-maintained

**Implementation:**
```yaml
- name: Coverage comment
  uses: py-cov-action/python-coverage-comment-action@v3
  with:
    GITHUB_TOKEN: ${{ github.token }}

- name: Test Report
  uses: dorny/test-reporter@v1
  if: always()
  with:
    name: Test Results
    path: tests/output/junit/results.xml
    reporter: java-junit

- name: Coverage Summary
  run: |
    echo "## Coverage Report" >> $GITHUB_STEP_SUMMARY
    pytest --cov --cov-report=term | tee -a $GITHUB_STEP_SUMMARY
```

### Decision 4: Tox Environment Strategy

**Choice:** Multiple specialized environments (coverage, lint, py314-ansible{matrix})

**Rationale:**
- Separation of concerns: coverage, linting, and testing are distinct
- Parallel execution: Can run environments concurrently
- Matrix testing: tox-ansible generates Ansible version combinations automatically
- Developer choice: Run specific environments based on needs

**Alternatives Considered:**
- Single environment: Rejected - slower, less flexible
- Manual Ansible versions: Rejected - tox-ansible automates this better

**Implementation:**
```toml
[env.coverage]
description = "Run tests with coverage reporting"
commands = [
  ["pytest", "tests/", "--cov", "--cov-report=html", "--cov-report=xml", "--cov-report=term-missing"],
]

[env.lint]
description = "Run linting and validation"
commands = [
  ["ansible-lint", "."],
  ["yamllint", "."],
]

# tox-ansible generates these automatically:
# py314-ansible-core-2.20
# py314-ansible-core-2.21
# etc.
```

### Decision 5: Test Structure - Keep extensions/molecule/

**Choice:** Maintain current structure with Molecule scenarios in `extensions/molecule/`

**Rationale:**
- Official Molecule documentation recommends `extensions/` for collections
- Current structure is correct per upstream docs
- No benefit to restructuring, would be breaking change
- Pytest wrappers in `tests/molecule/` provide good integration

**Alternatives Considered:**
- Move to tests/integration/targets/: Rejected - contradicts Molecule docs for collections

**Implementation:**
Keep existing:
```
extensions/molecule/          # Molecule scenarios (official location)
  ├── fedora_minimal/
  ├── integration_hello_world/
  └── utils/
tests/molecule/               # Pytest wrappers
  ├── test_fedora_minimal.py
  └── test_integration_hello_world.py
```

### Decision 6: Requirements.txt Handling

**Choice:** Convert to reference files pointing to pyproject.toml

**Rationale:**
- Some legacy tools may expect requirements.txt
- pip can install from pyproject.toml via `-e .`
- Maintains compatibility while migrating to modern approach

**Implementation:**
```
# requirements.txt
# Dependencies managed in pyproject.toml
# Install with: uv sync
-e .

# test-requirements.txt
# Test dependencies in pyproject.toml [dependency-groups]
# Install with: uv sync --group dev
-e .[dev]
```

## Risks / Trade-offs

### Risk 1: Breaking Changes for Local Development
**Risk:** Developers with cached virtualenvs may have conflicts  
**Mitigation:** Document migration steps in TESTING.md, include cleanup commands

### Risk 2: GitHub Actions Permission Issues
**Risk:** Coverage PR comments require write permissions  
**Mitigation:** Document required permissions in workflow, provide fallback to summary only

### Risk 3: Coverage Overhead on Test Execution Time
**Risk:** Coverage instrumentation can slow tests by 10-20%  
**Mitigation:** Use pytest-xdist for parallel execution to offset overhead

### Risk 4: Dependency Group Compatibility
**Risk:** Some older tools may not recognize PEP 735 dependency groups  
**Mitigation:** Keep reference requirements.txt files, document uv usage

### Risk 5: Test Output Directory Conflicts
**Risk:** Multiple test runs may conflict on output paths  
**Mitigation:** Use .gitignore for tests/output/, document cleanup in TESTING.md

### Risk 6: Ansible Version Matrix Size
**Risk:** Testing multiple Ansible versions increases CI time  
**Mitigation:** Use tox parallel execution, limit to supported versions (2.20+)

## Migration Plan

### Phase 1: Update Dependencies (Low Risk)
1. Update `pyproject.toml` with all dependency groups
2. Update `requirements.txt` and `test-requirements.txt` to reference files
3. Run `uv lock` to update lock file
4. Test locally with `uv sync --group dev`

### Phase 2: Configure Coverage (Low Risk)
1. Add pytest configuration to `pyproject.toml`
2. Add coverage configuration to `pyproject.toml`
3. Create `.gitignore` entry for `tests/output/`
4. Test locally: `pytest --cov`

### Phase 3: Enhance Tox (Medium Risk)
1. Add coverage environment to `tox.toml`
2. Add lint environment to `tox.toml`
3. Update skip configuration for Ansible 2.20+
4. Test locally: `tox run -e coverage`

### Phase 4: Update CI/CD (Medium Risk)
1. Update `.github/workflows/tests.yml` with coverage steps
2. Update `.github/workflows/molecule.yml` with reporting
3. Configure GitHub Actions permissions
4. Test on feature branch PR first

### Phase 5: Add Documentation (Low Risk)
1. Create `TESTING.md` with comprehensive guide
2. Update `README.md` with testing section
3. Add coverage badge to README (optional)
4. Document migration for existing contributors

### Rollback Strategy
If issues arise after deployment:
1. Revert to previous `pyproject.toml` (git revert)
2. Restore old `requirements.txt` files
3. Remove coverage steps from GitHub Actions
4. Run `uv lock` to restore previous state

All changes are additive except dependency consolidation, which is easily reversible.

## Open Questions

1. **Coverage Thresholds:** Should we enforce minimum coverage percentages? If so, what thresholds?
   - Recommendation: Start without thresholds, add later based on baseline

2. **Badge Display:** Do we want coverage/test badges in README?
   - Recommendation: Add shields.io badges for visual status

3. **Test Parallelization:** Should we increase pytest-xdist worker count beyond default?
   - Recommendation: Start with `-n 2`, monitor CI performance

4. **Lint Enforcement:** Should lint failures block CI?
   - Recommendation: Yes for new PRs, but document how to fix locally first
