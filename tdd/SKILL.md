---
name: tdd
description: Implement features and bug fixes through test-driven development. Use for TDD, test-first implementation, or red-green-refactor requests. Ordinary test-failure diagnosis, code review and mechanical refactoring do not require this workflow.
---

# Test-driven development

Build one observable behaviour at a time: demonstrate a missing capability with
a failing test, implement enough to pass, then improve the structure while
keeping tests green. Use the project's language, test runner and conventions.

## Choose the behaviour and boundary

Read the relevant code, callers, existing tests and repository instructions.
Use the project's glossary and relevant architecture decisions when present
to keep test names and contracts consistent with the domain.

Identify the behaviour being changed and the public interface that exposes it:
a function, module API, HTTP endpoint, CLI or user interaction. Choose the
narrowest stable boundary that can catch the actual defect or missing
capability. A public module function can be a valid boundary; every test need
not exercise the whole application.

Briefly state the first behaviour, boundary and important coverage limitation.
Infer these from the request and existing contracts when clear. Ask only when
unresolved requirements or interface choices would materially change the work;
do not require routine approval of each test or cycle. A short list of intended
behaviours is useful, but implement and verify them one at a time.

## Red, green, refactor

1. **Red:** Add one focused test for the next behaviour. For a bug, capture the
   failing input as a regression test. An existing test can serve this purpose
   if it already expresses the correct contract. Run the narrowest relevant
   test command before changing production behaviour and inspect the failure.
   It must fail for the missing behaviour, not a broken fixture, syntax error,
   missing dependency or unrelated environment problem. If a new API needs a
   declaration or stub to compile, add only that scaffold and rerun until the
   test reaches the intended behavioural failure.
2. **Green:** Make the smallest coherent production change that satisfies the
   behaviour. Run the test again and fix the cause until it passes. Do not add
   speculative features, weaken the assertion or skip the test to obtain a
   pass. If it passed before implementation, investigate whether the behaviour
   already exists or the test fails to distinguish the required outcome.
3. **Refactor:** Once the relevant tests pass, improve names, duplication or
   structure where that makes this change clearer. Keep observable behaviour
   unchanged and rerun affected tests after the refactor. Refactoring is
   optional; a broader redesign is a separate scope decision.
4. **Repeat:** Select the next missing behaviour based on the requirement and
   what the previous cycle revealed. Do not write the entire test suite first
   and then the entire implementation.

If tests cannot run, record the precise blockage and label the work unverified.
Do not claim an observed red or green result from inspection alone. Distinguish
pre-existing failures from regressions introduced by this change.

## Tests worth keeping

- Exercise the contract through its public interface. Prefer real internal
  collaborators so tests remain useful when the implementation is reorganised.
- Obtain expected results independently from a specification, worked example
  or known value. Do not reproduce the implementation to calculate the answer.
- Keep each test about one behaviour; several assertions are appropriate when
  they describe the same outcome or invariant.
- Cover meaningful boundaries and failure paths as their own cycles. Avoid
  tests of private helpers, incidental call order or generated wording unless
  those details are themselves part of the required contract.
- Control external services, time and randomness at explicit boundaries. Use
  existing test facilities and isolated resources; normal tests must not depend
  on live production services.

Read [test design examples](references/tests.md) when choosing assertions or
deciding between unit and integration coverage. Read
[test doubles and external boundaries](references/mocking.md) when dependencies
make a test slow, nondeterministic or difficult to isolate.

## Finish with evidence

Run the affected tests and required repository checks. Broaden testing when
changed dependencies, failures or unresolved risks justify it. Check the final
diff for weakened tests, unrelated edits and speculative code.

Report the behaviour delivered, the observed reason for the initial failure,
the final test commands and results, and any remaining coverage or execution
limits. Keep this proportionate to the change; a separate report file is not
required.

Adapted from [Matt Pocock's TDD skill](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/tdd).
The upstream MIT licence is included in [LICENSE](LICENSE). This adaptation
includes refactoring after green and infers established test boundaries without
requiring a separate confirmation gate.
