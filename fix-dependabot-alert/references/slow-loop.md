# Slow-Loop Method for Dependabot Fixes

Use a slow loop when reviewability and trust matter more than update throughput.
The loop intentionally produces one bounded result and then waits for a human
decision.

## Operating principles

1. **One signal:** Start from one current Dependabot alert. Do not sweep the
   backlog.
2. **One isolated change:** Use a dedicated branch or worktree and keep the diff
   small enough for a person to understand in one review session.
3. **Evidence before confidence:** Bind every completion claim to fresh alert
   data, resolved-version evidence, exact validation commands, and the final
   diff.
4. **Maker and checker:** Keep implementation and acceptance distinct. The
   checker must be able to reject shortcut work.
5. **Slow quality gate:** Let the repository's complete CI and security policy
   act as the non-bypassable outer gate even when local checks are fast.
6. **Bounded retries:** Stop after three materially different failed attempts or
   any repeated no-progress failure. Preserve what was learned instead of
   spending indefinitely.
7. **Durable memory:** Put the alert, hypothesis, diff scope, command results,
   checker result, and next decision in the pull request or repository-approved
   run note.
8. **Human merge decision:** Opening a reviewable pull request may complete the
   agent loop. Merging it does not; keep that judgment with a person.

## Why the unit is one alert

A single-alert unit keeps cause and effect legible. Dependency resolvers may
change transitive packages, and one update may incidentally close related
alerts, but the agent should not deliberately add unrelated upgrades. If the
fix fails, the reviewer can attribute the failure to one package and one
hypothesis.

## Evidence ladder

Prefer stronger evidence as the run progresses:

1. current GitHub alert metadata;
2. manifest and dependency-graph inspection;
3. resolved version outside the vulnerable range;
4. targeted tests or audit checks;
5. the repository's complete required checks;
6. independent diff and evidence review;
7. post-merge GitHub confirmation that the alert is fixed.

Only levels 1–6 are available before merge. Do not substitute a prediction for
level 7.

## Sources

- GitHub, “Viewing and updating Dependabot alerts”:
  <https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-dependabot-alerts/view-dependabot-alerts>
- GitHub, “REST API endpoints for Dependabot alerts”:
  <https://docs.github.com/en/rest/dependabot/alerts>
- GitHub, “Dependabot security updates”:
  <https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-security-updates>
- Loop Engineering, “Dependency Update Loop”:
  <https://loopengineering.app/templates/dependency-update-loop/>
- Loop Engineering, “Build Your First Loop”:
  <https://loopengineering.app/guides/build-your-first-loop/>
