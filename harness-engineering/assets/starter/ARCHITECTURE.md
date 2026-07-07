# {{PROJECT_NAME}} Architecture

Last reviewed: {{DATE}}

## Purpose

Describe what this system does, who it serves, and the main runtime surfaces.

## System Map

- Entry points:
- Core domains:
- Data stores:
- External services:
- Background jobs:
- User interfaces:
- Operational tooling:

## Boundaries

Document dependency direction, ownership boundaries, and modules that should not
import each other directly. Promote stable boundaries into mechanical checks
when possible.

## Invariants

- Data crossing external boundaries is validated or parsed before use.
- Runtime failures emit actionable diagnostics.
- Tests cover public behavior and critical failure paths.
- Generated or derived artifacts can be regenerated from documented commands.

## Change Guidance

- Read this file before changing architecture.
- Update this file when adding a new domain, dependency direction, runtime
  surface, storage layer, or external integration.
- Prefer local, inspectable abstractions over opaque behavior when agent
  maintainability is a project goal.
