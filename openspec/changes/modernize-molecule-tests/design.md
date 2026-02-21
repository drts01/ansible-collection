## Context

The ansible collection currently uses:
- **tox-ansible.ini**: Legacy INI format with minimal configuration (only skips old Python/Ansible versions)
- **Molecule scenarios**: Three scenarios exist (`fedora_minimal`, `integration_hello_world`, `utils`) but aren't integrated with tox or CI
- **pytest**: Basic unit/integration tests but no Molecule scenario execution
- **GitHub Actions**: Uses ansible-content-actions workflows but doesn't run Molecule tests
- **Dependencies**: Modern tooling already present (`tox-ansible>=26.1`, `tox-uv>=1.29`, `pytest-ansible~=26.1`)

Constraints:
- Must maintain compatibility with existing Molecule scenarios
- Python 3.14+ requirement (per pyproject.toml)
- Podman as container driver (no Docker dependency)
- Must work in both local development and CI environments

## Goals / Non-Goals

**Goals:**
- Migrate to modern TOML-based tox configuration following tox v4.41.0 standards
- Enable fast dependency installation via tox-uv plugin
- Run Molecule scenarios through pytest-ansible framework for better reporting
- Execute Molecule tests in GitHub Actions CI pipeline
- Support testing across multiple Ansible versions (2.20+)
- Improve local developer testing experience with faster runs

**Non-Goals:**
- Rewriting existing Molecule scenarios or test logic
- Changing from Podman to Docker
- Adding integration tests for all roles (only existing scenarios)
- Modifying ansible-content-actions workflows (sanity, lint, etc.)
- Supporting Python < 3.14 or Ansible < 2.20

## Decisions

### Decision 1: TOML Configuration Structure

**Choice:** Use `tox-ansible.toml` as the primary configuration file with tox v4 TOML syntax.

**Rationale:**
- tox v4+ recommends TOML over INI (per https://tox.wiki/en/4.41.0/reference/config.html)
- Better integration with pyproject.toml ecosystem
- More expressive syntax for complex configurations
- Type safety and validation support

**Alternatives Considered:**
- Keep INI format: Rejected - deprecated in tox v4
- Merge into pyproject.toml `[tool.tox]`: Rejected - tox-ansible expects separate config file for collection-specific settings

**Implementation:**
```toml
[ansible]
skip = [
    "py3.7", "py3.8", "py3.9", "py3.10", "py3.11", "py3.12", "py3.13",
    "2.9", "2.10", "2.11", "2.12", "2.13"
]

[tox]
requires = ["tox>=4.0", "tox-ansible>=26.1", "tox-uv>=1.29"]
```

### Decision 2: tox-uv Integration Approach

**Choice:** Configure tox-uv as a global plugin via `requires` and enable for all environments.

**Rationale:**
- tox-uv dramatically speeds up dependency resolution (10-100x faster than pip)
- Already in project dependencies
- Works seamlessly with tox-ansible
- No per-environment configuration needed

**Alternatives Considered:**
- Per-environment opt-in: Rejected - unnecessary complexity, all envs benefit
- Skip tox-uv: Rejected - significant performance benefit for CI and local dev

**Implementation:**
- Add `tox-uv>=1.29` to `[tox] requires`
- tox-uv auto-activates when present (no explicit config needed)

### Decision 3: pytest-ansible Integration Pattern

**Choice:** Create Molecule test wrappers in `tests/molecule/` that use pytest-ansible fixtures to invoke scenarios.

**Rationale:**
- Leverages pytest's test discovery, reporting, and fixtures
- Maintains existing Molecule scenarios unchanged
- Provides better failure output and debugging
- Enables pytest markers for selective test execution

**Alternatives Considered:**
- Direct molecule command: Rejected - loses pytest benefits, harder to integrate with tox
- Rewrite scenarios as pure pytest: Rejected - too much work, loses Molecule's container orchestration
- Keep Molecule separate: Rejected - doesn't achieve goal of unified test framework

**Implementation:**
```python
# tests/molecule/test_fedora_minimal.py
import pytest
from pytest_ansible.molecule import MoleculeScenario

@pytest.fixture
def molecule_scenario():
    return MoleculeScenario("fedora_minimal")

def test_converge(molecule_scenario):
    molecule_scenario.converge()

def test_verify(molecule_scenario):
    molecule_scenario.verify()
```

### Decision 4: GitHub Actions Workflow Strategy

**Choice:** Add a new job to existing `.github/workflows/tests.yml` rather than creating separate workflow file.

**Rationale:**
- Keeps all testing in one workflow for unified status checks
- Easier to manage required checks
- Single "all_green" gate for PR merges
- Reuses existing concurrency controls

**Alternatives Considered:**
- Separate `molecule.yml` workflow: Rejected - fragments CI status, harder to require all tests
- Matrix strategy for all Ansible versions: Rejected - too slow, test on latest + LTS only

**Implementation:**
```yaml
molecule:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.14'
    - run: pip install tox-ansible tox-uv
    - run: tox -e molecule
```

### Decision 5: Ansible Version Matrix Testing

**Choice:** Test against Ansible 2.20+ (latest) only.

**Rationale:**
- 2.20+ represents bleeding edge
- Balances coverage with CI time/cost

## Risks / Trade-offs

### Risk: Molecule scenarios may not work with pytest-ansible wrapper
**Mitigation:** Keep Molecule scenarios unchanged; wrapper only orchestrates execution. Fallback to direct molecule commands if needed.

### Risk: tox-uv compatibility issues with some dependencies
**Mitigation:** tox-uv is mature and widely adopted. If issues arise, can disable per-environment with `uv = false`.

### Risk: CI runs take longer with additional test job
**Mitigation:** Molecule tests run in parallel with other jobs. tox-uv speeds up installation. Net impact should be minimal (<2min added to total workflow time).

### Trade-off: TOML migration requires learning new syntax
**Upside:** Better documentation, more maintainable config, aligns with Python ecosystem direction.
**Downside:** Team needs to understand TOML format.
**Mitigation:** Provide clear examples and comments in tox-ansible.toml.

### Trade-off: pytest-ansible adds abstraction layer
**Upside:** Better reporting, test discovery, fixtures, markers.
**Downside:** Extra dependency and complexity.
**Mitigation:** Keep wrapper tests simple. Direct molecule commands still work for debugging.

## Migration Plan

### Phase 1: Local Development (Safe, Reversible)
1. Create `tox-ansible.toml` alongside existing `tox-ansible.ini`
2. Test locally: `tox -e ansible-py314-ansible217` (or similar)
3. Verify tox-uv is being used (check for UV logs)
4. Keep `tox-ansible.ini` until TOML is validated

### Phase 2: pytest-ansible Integration
1. Create `tests/conftest.py` with Molecule fixtures
2. Add `tests/molecule/test_*.py` wrappers for each scenario
3. Test locally: `pytest tests/molecule/`
4. Verify all scenarios execute correctly

### Phase 3: GitHub Actions Integration
1. Add `molecule` job to `.github/workflows/tests.yml`
2. Update `all_green` job to include molecule results
3. Test on PR to validate CI execution
4. Monitor CI run times and resource usage

### Phase 4: Cleanup
1. Delete `tox-ansible.ini` once TOML is proven
2. Update documentation (README, contributing guides)
3. Announce changes to team

### Rollback Strategy
- If TOML config fails: Revert to `tox-ansible.ini` (keep both during migration)
- If pytest-ansible issues: Run molecule directly via `molecule test` commands
- If CI problems: Comment out molecule job until resolved

## Open Questions

1. **Should we run Molecule tests on every PR or only on main branch merges?**
   - Recommendation: Every PR for maximum coverage, but allow manual triggers for draft PRs

2. **Which Ansible versions exactly? (2.14.x? 2.16.latest?)**
   - Recommendation: Use tox-ansible's matrix to test 2.14, 2.16, 2.17 specifically

3. **Should we parallelize Molecule scenarios or run sequentially?**
   - Recommendation: Sequential initially for stability; parallelize later if CI times are problematic

4. **Do we need separate tox environments for unit vs molecule tests?**
   - Recommendation: Yes - `tox -e py314` for unit tests, `tox -e molecule` for Molecule tests
