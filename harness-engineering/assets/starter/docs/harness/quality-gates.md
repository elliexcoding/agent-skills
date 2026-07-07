# Quality Gates

Last reviewed: {{DATE}}

Replace TODO commands with the real commands for {{PROJECT_NAME}}.

## Required Checks

```sh
# TODO: formatting check

# TODO: lint or static analysis

# TODO: unit tests

# TODO: integration or smoke tests
```

## Review Checklist

- Behavior change is intentional and documented where needed.
- Tests cover the main path and relevant failure paths.
- Architecture boundaries in `ARCHITECTURE.md` are preserved.
- New rules are backed by checks when they are likely to recur.
- Logs, errors, and diagnostics are useful to an agent debugging the failure.

## When Checks Cannot Run

Record the reason, the risk, and the narrowest alternative validation performed.
