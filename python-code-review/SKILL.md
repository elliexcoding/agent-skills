---
name: python-code-review
description:
  Review Python changes for correctness, typing, packaging, tests, async
  behaviour, and maintainability. Use when asked to review Python code, Python
  diffs, packages, PRs, scripts, or service changes.
---

# Python Code Review

## Purpose

Find concrete Python risks before style advice. Prefer actionable findings tied
to behaviour, data handling, typing, packaging, operational safety, or missing
verification.

## Companion Skills

- Use `debug-failing-tests` when tests fail, a traceback needs reproduction, or
  the review depends on proving a suspected runtime failure.
- Use this skill before broad cleanup advice; review should establish whether
  the current change is correct and maintainable.

## Review Priorities

1. Correctness, edge cases, and data-shape assumptions.
2. Exceptions, retries, partial failure, cleanup, and resource management.
3. Type hints, `mypy`/pyright compatibility, generics, and `Any` leakage.
4. Async/event-loop behaviour, cancellation, timeouts, blocking calls, and
   concurrency hazards.
5. Security-sensitive handling of paths, shell commands, serialisation, secrets,
   SQL, HTTP, and user-controlled input.
6. Packaging, dependency boundaries, optional extras, import side effects, and
   CLI entry points.
7. Performance risks from repeated I/O, unbounded memory use, N+1 calls, and
   accidental quadratic work.
8. Tests that prove behaviour, including failures and boundary cases.

## Workflow

1. Inspect the diff first, then read the surrounding code needed to understand
   intent.
2. Identify public contracts, data models, and likely production failure modes.
3. Run targeted checks when practical:

   ```bash
   python -m pytest
   python -m ruff check .
   python -m mypy .
   ```

4. If the project uses `uv`, `tox`, `nox`, `poetry`, `hatch`, or `make`, follow
   the repo's documented commands instead.
5. Avoid formatting-only findings unless they hide a real maintenance problem.
6. Treat missing tests as findings only when a realistic bug could escape.

## Output

Lead with findings, ordered by severity. Use file and line references when
available.

```text
Findings
- [severity] path:line - Concrete issue, impact, and suggested fix.

Open Questions
- Product or API intent that could change the recommendation.

Verification
- Commands run, or "not run" with a reason.
```

If there are no findings, say that clearly and mention any remaining test gaps
or residual risk.
