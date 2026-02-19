---
description: 'POSIX-first shell scripting guidance for Linux, BSD, and macOS'
applyTo: '**/*.zsh, **/*.sh, **/*.bash, **/.bashrc, **/.bash_profile, **/.bash_aliases, **/.profile, **/.zprofile, **/.zshrc, **/.zshenv'
---

# Shell Scripts

Clear, safe, and portable shell guidance for Linux, BSD, and macOS.

## Overview

Generate POSIX-first shell code and call out bash/zsh-only features with minimum versions.

## Project Context

- Target environments: Linux, BSD, macOS
- Shells: POSIX sh, bash (≥ 4), zsh (≥ 5)

## General Instructions

- Prefer POSIX; call out bash/zsh-only features and minimum versions.
- Keep scripts small, readable, and commented when intent is unclear.
- Be quiet by default; use opt-in verbosity (`--verbose`/`DEBUG=1`).
- Use imperative phrasing in comments and docstrings.
- Measure before micro-optimizing; document non-obvious speedups.
- Prefer clear usage text and predictable exit codes for CLI UX.

## Architecture & Structure

- Separate configuration, helpers, and main flow.
- Prefer functions over repetition.
- Keep side effects in `main`; keep helpers pure when practical.

## Style & Conventions

- Use `snake_case` for variables and functions.
- Use ALL_CAPS for constants and exported environment variables.
- Keep lines <= 100 characters when practical.
- Prefer `case` over long `if/elif` chains for option parsing.
- Prologue: correct shebang + strict mode (`/bin/sh` + `set -eu`; bash/zsh + `set -euo pipefail`).
- Quote expansions: `"${var}"` and `$(cmd)`; avoid backticks.
- Use `printf` over `echo`; send errors to stderr: `printf '%s\n' "error: msg" >&2`.
- Avoid `ls` parsing; use globs or `find ... -print0` + `IFS= read -r`.
- Use `--` to terminate options before user-provided args.

## State & Dependencies

- Use locals (`local`/`typeset`) and pass data via args; avoid global mutation.
- Mark constants as `readonly`/`typeset -r`.
- Check tools via `command -v tool >/dev/null 2>&1`.

## Reliability & Logging

### Best Practices
- Validate inputs early; fail fast with clear errors.
- Keep helpers small; avoid cleverness.
- Document dependencies and side effects inline.
- Prefer `getopts` for POSIX; document non-POSIX parsers.

### Error Handling & Logging
- Use consistent error format: `error: <message>` to stderr.
- Use levels: `info`, `warn`, `error` when logging.
- Exit `0` on success, `1` on failure, `2` for misuse (bad args).
- Prefer explicit checks over relying on `set -e` for critical paths.
- Log only when useful; avoid noisy loops and per-item logs in hot paths.

## Security & Portability

### Security & Safety
- Never hard-code or log secrets.
- Avoid `eval`, process substitution, and indirect expansion unless documented.
- Use `mktemp` + `umask 077` + `trap` cleanup.
- Pin `PATH`; reject unsafe paths; validate files before use.

### Portability
- Document GNU-only flags (`sed -i`, `date -d`, etc.).
- Note Linux vs BSD/macOS tool differences when relevant.
- Avoid bashisms in `/bin/sh`; if required, switch shebang and document minimum version.

## Performance

- Avoid unnecessary subshells and pipelines in hot paths.
- Prefer built-in shell operations over external commands when practical.
- Batch filesystem ops; avoid per-file `stat`/`grep` in loops.
- Cache computed values used repeatedly within a script run.

## Testing

- Use smoke tests for critical paths.
- Validate scripts with representative input fixtures.

## Quick Do/Don’t

| Do                           | Don't                          |
| ---------------------------- | ------------------------------ |
| Quote variables              | Rely on word splitting         |
| Validate inputs early        | Assume defaults are safe       |
| Prefer `printf`              | Use `echo -e`                  |
| Use `case` for options       | Deep `if/elif` chains          |
| Clean up temp files          | Leave temp dirs behind         |

## Common Issues

| Issue            | Solution          | Example           |
| ---------------- | ----------------- | ----------------- |
| Magic numbers    | Use constants     | `MAX_RETRIES=3`   |
| Deep nesting     | Extract functions | `do_work()`       |
| Hardcoded values | Use config vars   | `API_URL="${API_URL:-}"` |

## Common Patterns

### Tool check
```sh
if ! command -v jq >/dev/null 2>&1; then
  printf '%s\n' "error: jq is required" >&2
  exit 1
fi
```

### Good Example
```sh
printf '%s\n' "info: starting"
```

### Bad Example
```sh
echo -e "starting"
```

### Good Example - Safe temp dir
```sh
umask 077
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT
```

### Bad Example - Unsafe temp dir
```sh
TEMP_DIR="/tmp/mydir"
rm -rf "$TEMP_DIR"
```

## Compatibility Matrix

| Shell | Minimum | Notes |
| ----- | ------- | ----- |
| sh    | POSIX   | No arrays, no `[[ ]]`, no process substitution |
| bash  | 4.0     | Document bash-only features and reason |
| zsh   | 5.0     | Guard zsh-only behavior with `$ZSH_VERSION` |

## Tooling Minimums

- `shellcheck` ≥ 0.8
- `shfmt` ≥ 3.6 (if used)
- `jq` ≥ 1.6 (if required)

## Maintenance

- Review guidance when shell/version targets change.
- Update examples to reflect current best practices.
- Remove or annotate deprecated patterns promptly.

## Validation and Verification

- Lint: `shellcheck <file>` (≥ 0.8).
- Format: `shfmt -w <file>` (≥ 3.6, if allowed).
- Run: `/bin/sh <file>` and `bash <file>` when applicable.
- Performance sanity: time hot paths with representative inputs.

## Example Template

```sh
#!/bin/sh

# ============================================================================
# Script Description Here
# ============================================================================
# Script Name: shell.instructions.md
# Author: Carlos Meza
# Date: 2023-04-13
# Version: 1.0
# ============================================================================
set -eu

cleanup() {
  if [ -n "${TEMP_DIR:-}" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
  fi
}
trap cleanup EXIT

# Default values
RESOURCE_GROUP=""
REQUIRED_PARAM=""
OPTIONAL_PARAM="default-value"
SCRIPT_NAME="$(basename "$0")"

TEMP_DIR=""

usage() {
  printf '%s\n' "Usage: $SCRIPT_NAME [OPTIONS]"
  printf '%s\n' "Options:"
  printf '%s\n' "  -g, --resource-group   Resource group (required)"
  printf '%s\n' "  -h, --help            Show this help"
  exit 0
}

validate_requirements() {
  if [ -z "$RESOURCE_GROUP" ]; then
    printf '%s\n' "error: resource group is required" >&2
    exit 1
  fi
}

main() {
  validate_requirements

  TEMP_DIR="$(mktemp -d)"
  if [ ! -d "$TEMP_DIR" ]; then
    printf '%s\n' "error: failed to create temporary directory" >&2
    exit 1
  fi

  printf '%s\n' "============================================================================"
  printf '%s\n' "Script Execution Started"
  printf '%s\n' "============================================================================"

  # Main logic here

  printf '%s\n' "============================================================================"
  printf '%s\n' "Script Execution Completed"
  printf '%s\n' "============================================================================"
}

while [ "$#" -gt 0 ]; do
  case $1 in
    -g|--resource-group)
      RESOURCE_GROUP="$2"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    *)
      printf '%s\n' "error: unknown option: $1" >&2
      exit 1
      ;;
  esac
done

main "$@"
```
