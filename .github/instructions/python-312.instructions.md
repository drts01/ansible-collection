---
name: Python 3.12+
description: Python 3.12+ coding conventions and tooling
applyTo: "**/*.py"
---

# Python 3.12+ Copilot Instructions

## Overview

Write typed, testable, performance-aware Python 3.12+ using the standard library first.
Use preferred third-party libraries when needed.

## Tooling and validation

- Python 3.12+.
- Validate with pre-commit and tox.
- Use Ruff for linting/formatting (120-char line length).
- Use uv for scripting and dependency management.

## Core Python guidelines

- Implement functionality with full typing and clear errors.
- Prefer stdlib solutions; justify non-stdlib dependencies.
- Target Python 3.12+; use `match/case`, `|` unions, type parameter syntax, and `type` aliases.
- Add type annotations everywhere and docstrings for public APIs.
- Prefer pathlib.Path for filesystem work.
- Use f-strings; avoid `%` and `str.format`.
- Use tabulate for user-facing tables.
- Prefer pydantic-settings for configuration and CLI-like inputs.
- Prefer comprehensions/functools when concise.
- Avoid global mutable state; module constants are OK.
- Prefer asyncio.TaskGroup for concurrency.
- Ensure functions have descriptive names and include type hints.
- Use the `typing` module for type annotations (e.g., `List[str]`, `Dict[str, int]`).
- Break down complex functions into smaller, more manageable functions.

## Code style and documentation

- Always prioritize readability and clarity.
- Handle edge cases and write clear exception handling.
- For libraries or external dependencies, mention their usage and purpose in comments.
- Use consistent naming conventions and follow language-specific best practices.
- Maintain proper indentation (use 4 spaces for each level of indentation).
- Place function and class docstrings immediately after the `def` or `class` keyword.
- Use blank lines to separate functions, classes, and code blocks where appropriate.
- Use imperative phrasing in comments and docstrings.
- Write concise, efficient, and idiomatic code that is also easily understandable.
- For algorithm-related code, include explanations of the approach used.
- Write clear and concise comments for each function.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Provide docstrings following PEP 257 conventions.

## Error handling and logging

- Define custom exceptions with clear, actionable messages.
- Catch specific exceptions, use chaining, include key context.
- Use logging (no print except user-facing output).
- Use lazy logging formatting; keep log messages clear and consistent tense.
- Use structured logs with context fields.
- Avoid blocking I/O in async functions.

## Security and safety

- Validate inputs with Pydantic; reject unknown fields by default.
- Avoid `eval`/unsafe `pickle`; prefer `json` or Pydantic serialization.
- Use `subprocess.run` with argument lists; never `shell=True` for user input.
- Do not log secrets; redact tokens/credentials.
- Use `secrets` for tokens and `hashlib` for hashing.
- Use `tempfile` for secure temporary files.
- Enforce limits on file/payload sizes.
- Prefer `Path.resolve()` and allowlists to prevent traversal.
- Pin dependency versions and review advisories.

## Performance and data structures

- Optimize real bottlenecks with efficient data structures.
- Stream with iterators when full materialization is unnecessary.
- Prefer dict/set for membership, list for ordering, deque for queues.
- Use heapq for priority queues, array for compact numeric buffers.
- Use bisect for binary search on sorted sequences.
- Avoid unnecessary copies and repeated calls in loops.
- Use itertools for combinatorial operations.
- Use math functions over operators.
- Pre-allocate memory when sizes are known.
- Use `__slots__` or Pydantic v2 slots for tiny, frequently instantiated classes.

## Preferred libraries

- httpx
- pydantic v2+
- pydantic-settings
- fastapi
- tabulate

## Examples

### Slotted classes

```python
from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict


@dataclass(slots=True)
class MetricPoint:
    name: str
    value: float


class SlottedModel(BaseModel):
    model_config = ConfigDict(slots=True)
    name: str
    value: float
```

### Async HTTP with httpx

Use httpx for HTTP clients; prefer async, timeouts, and connection limits.

```python
import httpx


async def fetch_json(url: str) -> dict[str, object]:
    transport = httpx.AsyncHTTPTransport(retries=3)
    async with httpx.AsyncClient(
        transport=transport,
        timeout=httpx.Timeout(10.0),
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
        follow_redirects=True,
        http2=True,
    ) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()
```

### Pydantic v2 and settings

Use Pydantic v2+ for validation and pydantic-settings for configuration.

```python
from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "MyApp"
    debug: bool = False


class User(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(..., min_length=3, max_length=50)
```

### FastAPI services

Keep handlers typed and small; push logic into separate functions/classes.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
```

### Proper documentation example

```python
def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle given the radius.

    Parameters:
    radius (float): The radius of the circle.

    Returns:
    float: The area of the circle, calculated as π * radius^2.
    """
    import math
    return math.pi * radius**2
```

## Testing and edge cases

- Add tests with pytest fixtures and Hypothesis where appropriate.
- Always include test cases for critical paths of the application.
- Account for common edge cases like empty inputs, invalid data types, and large datasets.
- Include comments for edge cases and the expected behavior in those cases.
- Write unit tests for functions and document them with docstrings explaining the test cases.

```python
import pytest
from hypothesis import given
from hypothesis import strategies as st


@pytest.fixture
def items() -> list[str]:
    return ["alpha", "beta", "gamma"]


def test_items_fixture(items: list[str]) -> None:
    assert "beta" in items


@given(st.text(min_size=1))
def test_round_trip_text(value: str) -> None:
    assert value == value
```

## References

- https://docs.astral.sh/ruff/
- https://docs.astral.sh/uv/
- https://docs.pytest.org/
- https://hypothesis.readthedocs.io/
- https://www.python-httpx.org/
- https://docs.pydantic.dev/latest/
- https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- https://fastapi.tiangolo.com/
