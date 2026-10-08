---
name: python-code-review
description: Review Python code for language-specific correctness, typing, packaging and async risks. Use for Python-focused reviews outside a PR review workflow.
---

# Python Code Review

## Purpose

Find concrete Python risks before style advice. Prefer actionable findings tied
to behaviour, data handling, typing, packaging, operational safety, or missing
verification.

Remain read-only unless fixes are requested. If `review-pull-request` is already
active, use its Python reference instead of loading this second workflow.
Use `debug-failing-tests` only when a failure needs a separate diagnosis;
reproducing a defect during review does not authorise fixing it.

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
3. Inspect existing validation evidence. Run a targeted check when it resolves
   a concrete concern, selecting the relevant test path, typing boundary or
   packaging check rather than running every tool.
4. Use the repository's environment and documented commands; do not install or
   introduce a linter, type checker or runner just for the review.
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
