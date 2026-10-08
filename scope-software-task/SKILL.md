---
name: scope-software-task
description: Define repository-grounded scope, acceptance criteria and work units when a software change needs planning or consequential requirements are unresolved.
---

# Scope Software Task

Turn a software objective into bounded, verifiable work grounded in repository
evidence. Distinguish requirements from proposed implementation choices.

## Match the request

For planning-only work, inspect without modifying source, tests, configuration
or documentation unless a saved plan is requested. If implementation is also
requested, scope it and continue through implementation and verification; stop
only for a consequential unresolved decision or an execution boundary.

A local change with a clear boundary may need one short contract. Use ordered
work units for multiple components, and decision gates and rollout obligations
for cross-service changes, migrations or difficult recovery. Choose depth by
consequences and uncertainty, not diff size.

## Ground the contract

Inspect repository instructions and the entry points, consumers, tests and
validation commands relevant to the objective. Establish what happens now,
where the authoritative contract lives and how success can be observed. Expand
the search when evidence exposes another dependency, not to preload the repo.

Record these at the depth the change needs:

- **Outcome:** Observable result and beneficiary.
- **Current behaviour:** Baseline with supporting paths or symbols.
- **Scope and non-goals:** Allowed changes and plausible adjacent work excluded.
- **Constraints:** Compatibility, security, data, performance and operational
  invariants that must hold.
- **Acceptance:** Falsifiable nominal and adverse behaviours.
- **Verification:** Checks or measurements that distinguish success from failure.
- **Uncertainty:** Assumptions, missing evidence and decision owners.

Correct assumptions that conflict with repository evidence. Do not make a
preferred class, library or file an acceptance criterion without a real
requirement for it.

## Resolve consequential decisions

Investigate discoverable questions yourself. Ask only when an unresolved choice
materially affects product semantics, contracts, data safety, security, cost or
irreversibility. Give the options, evidence, recommendation and dependent work.
State reasonable assumptions for minor ambiguities and continue independent
work while waiting.

## Decompose when needed

Each unit should have one meaningful outcome, bounded ownership, prerequisites,
preserved invariants, a completion signal and focused verification. Prefer a
reviewable and independently reversible result where practical.

Sequence enabling work before dependent behaviour. Do not split merely by file
or layer, or schedule concurrent work against an unsettled shared contract.
Keep behavioural changes and preparatory refactors distinguishable. Planning
parallel work does not itself authorise spawning agents.

Check that every acceptance criterion has an owner and verification, that
relevant permission, lifecycle and partial-failure paths are covered, and that
consequential steps have a safe stopping point. For migrations, include rollout,
compatibility and recovery evidence. For difficult decomposition, read
[task contract examples](references/task-contract-examples.md).

## Deliverable

Use a concise contract for a small task. For larger work, add ordered units with
outcome, dependencies, ownership, verification and risks; include decision gates
only when needed. Follow existing document conventions when saving a requested
plan. Do not add a separate planning artefact to every implementation task.

Recommend an independent review when consequences or uncertainty warrant one;
do not make it a universal gate for routine changes. Completion means the
requested outcome and its evidence are delivered, not merely a plan or a PR.
