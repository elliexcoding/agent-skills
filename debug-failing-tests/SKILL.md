---
name: debug-failing-tests
description: Diagnose and fix failing Rust or Python tests, tracebacks and CI failures using a focused reproduction.
---

# Debug Failing Tests

## Purpose

Turn a failing test, traceback, CI log, or suspected regression into a small
reproduction, a likely cause, and a verified fix path. Optimise for evidence
over speculation.

For diagnosis-only or review requests, report the cause and fix path without
editing. When a fix is requested, continue through implementation and relevant
verification. A separate code-review workflow is not required for every failure.

## Workflow

1. Capture the exact failure:
   - failing command
   - failing test name
   - first useful error or traceback
   - relevant environment details when visible
2. Re-run the narrowest failing command before editing.
3. Reduce noise:
   - Rust: prefer one package, one test, and `-- --nocapture` only when useful.
   - Python: prefer one test path or `-k` expression, and increase verbosity
     only when useful.
4. Read the test and the smallest amount of production code needed to explain
   the failure.
5. Form one hypothesis at a time and test it with code inspection, a narrower
   test, or a temporary diagnostic.
6. Make the smallest durable fix that addresses the cause, not just the symptom.
7. Re-run the narrow failing command, then required repository checks. Broaden
   further when the failure or changed dependencies leave a concrete concern.

## Useful Commands

Rust:

```bash
cargo test <test_name>
cargo test -p <package> <test_name> -- --nocapture
```

Python:

```bash
python -m pytest path/to/test.py::test_name -q
python -m pytest -k "<expression>" -vv
```

## Guardrails

- Do not hide failures by weakening assertions without explaining why the old
  expectation was wrong.
- Do not delete or skip tests unless the test is obsolete and the replacement
  coverage is clear.
- Do not make broad refactors while debugging unless the current structure
  prevents a safe fix.
- Keep temporary logging, print statements, and probes out of the final patch.

## Output

```text
Failure
- Command and concise error summary.

Root Cause
- The specific cause, with file and line references where possible.

Fix
- What changed and why it addresses the cause.

Verification
- Narrow command run.
- Broader command run, or "not run" with a reason.
```
