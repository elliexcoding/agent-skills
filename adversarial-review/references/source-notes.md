# Source Notes

These sources inform the skill's controls. They are not copied procedures; the
skill synthesizes them into a portable workflow for coding agents.

## Independent Review

- [Microsoft Security Development Lifecycle](https://learn.microsoft.com/en-us/compliance/assurance/assurance-microsoft-security-development-lifecycle)
  requires manual review by someone other than the code's developer and treats
  separation of duties as a verification control. This supports assigning the
  adversarial pass to a fresh reviewer and keeping it read-only by default.
- [NASA Software Independent Verification and Validation](https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604595/SWE-141%2B-%2BSoftware%2BIndependent%2BVerification%2Band%2BValidation)
  distinguishes building the right system from building the system correctly
  and explicitly considers unintended behavior and adverse conditions. This
  supports challenging requirements, negative behavior, and implementation.
- [Anthropic multi-agent orchestration](https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration)
  gives agents separate context-isolated session threads and recommends
  specialization for domain-focused work. This supports using a reviewer that
  did not inherit the implementer's conversational assumptions.

## Review Scope And Evidence

- [Google Engineering Practices: What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
  emphasizes inspecting broader system context, design, functionality,
  complexity, concurrency, and whether tests are meaningful. This supports
  reviewing call sites and testing the tests rather than reading only the diff.
- [Google Engineering Practices: How to write code review comments](https://google.github.io/eng-practices/review/reviewer/comments.html)
  recommends clear reasoning, respectful comments about the code, and explicit
  severity. This supports evidence-backed, non-personal findings.
- [NIST SP 800-218, Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
  includes review and analysis of human-readable code plus documentation and
  triage of findings. This supports combining manual reasoning with automated
  checks and preserving actionable evidence.

## Threat And Misuse Analysis

- [OWASP Secure Code Review Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html)
  recommends data-flow tracing, trust-boundary analysis, state analysis, threat
  modeling, misuse cases, and attack-scenario simulation. This supports the
  focused security and abuse lenses in the playbook.

## Derived Rules

The workflow derives these practical rules from the sources:

1. Preserve reviewer independence before exposing author conclusions.
2. Verify intent and implementation separately.
3. Challenge nominal, unintended, and adverse behavior.
4. Combine human reasoning, automated checks, and narrow reproductions.
5. Require a trigger, path, consequence, and evidence for every finding.
6. Distinguish confirmed defects from hypotheses and residual uncertainty.
7. Keep review comments respectful, severity-calibrated, and actionable.
