# Harness

This directory describes how {{PROJECT_NAME}} is made legible, testable, and
maintainable for Codex and future maintainers.

## Contents

- `principles.md`: durable project operating principles.
- `quality-gates.md`: checks and review expectations.

## Maintenance Loop

When Codex struggles, do not only retry the same prompt. Identify which harness
capability is missing:

- documentation map
- architecture boundary
- validation command
- runtime observability
- fixture or reproducible workload
- lint or structural test
- remediation guidance in an error message

Then add the smallest project-local improvement that prevents the same class of
failure from recurring.
