---
name: scope-software-task
description: |
  Turn ambiguous or non-trivial software changes into repository-grounded,
  agent-executable task contracts and implementation plans. Use when scoping or
  tightening a feature, bug fix, migration, refactor, or technical-debt item
  before implementation, especially when acceptance criteria, constraints,
  non-goals, risks, affected interfaces, verification, or boundaries between
  agent-executable work units are incomplete.
---

# Scope Software Task

## Mission

Convert a software objective into the smallest set of independently
understandable, executable, verifiable, and reversible work units that can
safely be handed to an engineer or coding agent.

Own the quality of the problem definition. Do not hide unresolved product,
architecture, security, data, or operational decisions inside implementation
tasks.

## Operating Contract

- Ground the scope in repository evidence before prescribing implementation.
- During a planning-only request, inspect without modifying source,
  configuration, tests, or documentation.
- When the user also requests implementation, complete the scoping pass first
  and then continue unless a consequential decision genuinely requires input.
- Correct task assumptions that conflict with the repository and cite the
  relevant files, symbols, tests, or documentation.
- Ask only about decisions that cannot be discovered safely and would
  materially change the result. State a reasonable assumption for minor
  ambiguities.
- Match the amount of process to the task. Keep trivial tasks compact.
- Prefer behavioural outcomes and evidence over prescribed file edits.

## Select Scoping Depth

Classify the work after a targeted reconnaissance pass:

- **Compact:** One local behaviour, an obvious implementation boundary, and an
  existing validation path. Produce a short contract and one work unit.
- **Standard:** Several affected components, incomplete acceptance criteria, or
  meaningful failure cases. Produce the full task contract and ordered units.
- **Extended:** Cross-service work, public contract or schema changes,
  migrations, security boundaries, difficult rollback, or several unresolved
  design decisions. Add decision gates, rollout and rollback obligations, and
  explicit integration checkpoints.

Do not classify solely from the requested diff size. A one-line permission or
schema change may deserve extended treatment.

## Default Workflow

### 1. Establish the Objective

Determine:

- the user or system outcome;
- whether the request is planning-only or includes execution;
- the current pain or failure being addressed;
- the strongest available completion signal;
- explicit deadlines, compatibility requirements, and risk constraints.

Rewrite activity language such as "add caching" or "refactor auth" into
observable behaviour. Preserve the user's intent rather than inventing a larger
objective.

### 2. Perform Targeted Reconnaissance

Read repository instructions first. Search for the relevant entry points,
interfaces, callers, tests, conventions, documentation, recent related changes,
and validation commands.

Investigate far enough to answer:

1. What happens now?
2. Where is the authoritative behaviour or contract?
3. What depends on it?
4. What failures or invariants matter?
5. How can the change be proved correct?

Do not preload an entire repository. Widen the search only when evidence exposes
another dependency or trust boundary.

### 3. Build the Task Contract

Produce these fields at a depth proportionate to the task:

1. **Outcome:** Observable result and intended beneficiary.
2. **Current behaviour:** Repository-grounded baseline and entry points.
3. **In scope:** Behaviour and surfaces that may change.
4. **Non-goals:** Plausible adjacent work explicitly excluded.
5. **Constraints and invariants:** Compatibility, security, data, performance,
   reliability, architectural, and operational properties that must hold.
6. **Acceptance criteria:** Falsifiable nominal and adverse behaviours.
7. **Required verification:** Commands, tests, inspections, or measurements
   that provide completion evidence.
8. **Known uncertainties:** Remaining assumptions, evidence gaps, and decision
   owners.

Distinguish requirements from suggested implementation choices. Do not turn an
unverified design preference into a constraint.

### 4. Expose Decision Gates

Resolve discoverable questions through code, documentation, or safe read-only
checks. Escalate only when choosing would materially affect product semantics,
public contracts, data safety, security posture, operational risk, cost, or
irreversibility.

For each unresolved decision, state:

- why it matters;
- the viable options and tradeoffs;
- what evidence is available;
- which downstream work is blocked;
- the recommended default when one is defensible.

### 5. Decompose by Outcome and Verification Boundary

Split work so each unit has:

- one coherent behavioural or enabling outcome;
- a bounded ownership surface;
- explicit prerequisites and preserved invariants;
- an observable completion condition;
- a focused validation method;
- a reviewable, independently reversible change when practical.

Prefer units such as reconnaissance, characterization, interface introduction,
one end-to-end behaviour, failure handling, migration, observability, and
rollout. Sequence enabling work before dependent behaviour.

Do not decompose merely by file, architectural layer, or job title. Avoid
parallel units that must edit the same contract or rely on unstated shared
assumptions.

### 6. Challenge the Plan

Before presenting it, test whether:

- every acceptance criterion is owned by a work unit and verification step;
- nominal, permission, lifecycle, partial-failure, and rollback behaviour are
  covered where relevant;
- behavioural changes and preparatory refactors are separated;
- units are small enough to review but still deliver meaningful evidence;
- parallel work is actually independent;
- the plan preserves a safe stopping point after each consequential step;
- completion measures user or system value rather than code or PR volume.

If the task remains too vague, read
`references/task-contract-examples.md` for calibration and use the closest
pattern without copying irrelevant requirements.

## Decomposition Smells

Reject or revise plans that exhibit:

- **File slicing:** "Agent A edits the handler; Agent B edits the service."
- **Fake parallelism:** Concurrent tasks share an interface that is not yet
  stable.
- **Big-bang validation:** Correctness can only be checked after every change.
- **Hidden redesign:** A bounded request silently becomes an architectural
  rewrite.
- **Mixed intent:** Behaviour change, migration, and unrelated cleanup land
  together.
- **Implementation-shaped criteria:** Acceptance requires a chosen class,
  library, or file rather than externally meaningful behaviour.
- **Evidence-free completion:** "Tests pass" without identifying which tests
  discriminate correct from broken behaviour.

## Output Format

Use the smallest format that preserves the necessary decisions:

```markdown
## Task Contract
Outcome:
Current behaviour:
In scope:
Non-goals:
Constraints and invariants:
Acceptance criteria:
Required verification:
Known uncertainties:

## Decision Gates
- Decision, options, recommendation, owner, and blocked work.

## Work Units
1. Unit name
   - Outcome:
   - Depends on:
   - Scope:
   - Verification:
   - Risks and stopping condition:

## Execution Notes
- Safe sequencing, parallelism, rollback, and handoff guidance.
```

Omit an empty `Decision Gates` section. For a compact task, collapse the
contract and work units into a concise list.

## Coordination

- Use a refactoring workflow when a unit must preserve behaviour while changing
  structure.
- Use a focused debugging workflow when the current failure is not yet
  reproduced or understood.
- Use a dedicated security workflow for security-sensitive discovery,
  validation, or remediation.
- After implementation, use an independent adversarial review against the task
  contract rather than asking the implementing context to certify itself.
