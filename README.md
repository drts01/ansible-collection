# Drts CASC Collection

[![Tests](https://github.com/drts01/ansible-collection/actions/workflows/tests.yml/badge.svg)](https://github.com/drts01/ansible-collection/actions/workflows/tests.yml)
[![Molecule Tests](https://github.com/drts01/ansible-collection/actions/workflows/molecule.yml/badge.svg)](https://github.com/drts01/ansible-collection/actions/workflows/molecule.yml)

This repository contains the `drts.casc` Ansible Collection.

<!--start requires_ansible-->
<!--end requires_ansible-->

## External requirements

Some modules and plugins require external libraries. Please check the
requirements for each plugin or module you use in the documentation to find out
which requirements are needed.

## Included content

<!--start collection content-->
<!--end collection content-->

## Using this collection

```bash
    ansible-galaxy collection install drts.casc
```

You can also include it in a `requirements.yml` file and install it via
`ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
  - name: drts.casc
```

To upgrade the collection to the latest available version, run the following
command:

```bash
ansible-galaxy collection install drts.casc --upgrade
```

You can also install a specific version of the collection, for example, if you
need to downgrade when something is broken in the latest version (please report
an issue in this repository). Use the following syntax where `X.Y.Z` can be any
[available version](https://galaxy.ansible.com/drts/casc):

```bash
ansible-galaxy collection install drts.casc:==X.Y.Z
```

See
[Ansible Using Collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)
for more details.

## Testing

This collection includes comprehensive test coverage using pytest, tox, and Molecule.

### Quick Start

```bash
# Install dependencies
uv sync --group dev

# Run all tests with coverage
uv run pytest tests/ --cov

# Run tests via tox
tox run -e coverage

# Run linting
tox run -e lint
```

### Detailed Testing Guide

For comprehensive testing documentation, including:
- Setting up your development environment
- Running different types of tests (unit, integration, molecule)
- Understanding coverage reports
- CI/CD testing workflows
- Troubleshooting common issues

See [TESTING.md](TESTING.md) for complete details.

## Development

### Setting Up Development Environment

This collection uses [uv](https://docs.astral.sh/uv/) for fast, reliable Python dependency management.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/drts01/ansible-collection.git
cd ansible-collection

# Install all development dependencies
uv sync --group dev --group build --group lint

# Verify installation
uv run pytest --version
uv run ansible --version
```

### Development Workflow

```bash
# Run tests during development
uv run pytest tests/ --cov

# Run linting before committing
tox run -e lint

# Run full test matrix
tox run

# Run specific tox environment
tox run -e coverage
tox run -e ansible-2.20-py3.14
```

### Contributing

When contributing to this collection:
1. Install development dependencies with `uv sync --group dev`
2. Run tests locally before submitting PRs
3. Ensure linting passes with `tox run -e lint`
4. Update tests for any new features or bug fixes
5. Follow the [Ansible Collection Development Guidelines](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html)

## Release notes

See the
[changelog](https://github.com/ansible-collections/drts.casc/tree/main/CHANGELOG.rst).

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/matrix channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible collection development forum](https://forum.ansible.com/c/project/collection-development/27)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_requirements.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn)
- [News for Maintainers](https://forum.ansible.com/tag/news-for-maintainers)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
