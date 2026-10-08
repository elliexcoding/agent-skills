---
name: writing-feature-comments
description: Write or revise code comments and docstrings that explain purpose, constraints or verified pitfalls. Use when comments are part of the requested change.
---

# Writing Feature Comments

Write for people reading the finished code. Explain the feature's purpose, why
the behavior matters, and concerns a reader needs to understand or change it
safely. Apply this guidance within the project's development workflow.

## Choose what earns a comment

| Reader's need | Useful content |
| --- | --- |
| Understand the feature | The problem it solves or the user outcome it supports. |
| Understand an unusual choice | The reason for the behavior or constraint that must survive future edits. |
| Avoid a known pitfall | The condition, its consequence, and any established handling or limitation. |

Comment when that information is missing from clear names and code. A simple
expression or obvious helper may need no comment. Each comment should add a
distinct fact; explain a concern once, where it is most useful.

## Write the lasting explanation

- Use short, direct sentences and familiar words. Keep precise technical terms
  when they help; explain unfamiliar ones. Usually one or two sentences suffice,
  but retain context needed for accuracy.
- Put feature-wide purpose and limitations on the feature's entry point or in
  existing documentation. Attach local constraints to the code they affect;
  proximity alone does not make an unrelated constant the right home.
- Ground claims in the code, tests, requirements, or verified behavior. Describe
  known limitations accurately. Keep unverified concerns in the task discussion
  or issue until investigated; do not turn guesses into guarantees.
- State the enduring reason for a change. Keep drafting thoughts, abandoned
  approaches, progress reports, and review chatter out of source comments.
  Relevant design tradeoffs belong as settled rationale, without the deliberation.
- Update comments affected by the feature. Keep unrelated cleanup out of the diff.

For example, a search feature can explain its behavior without narrating the work:

```typescript
// Keep previous results visible while searching so the list does not flash empty.
async function refreshResults(query: string): Promise<void> {
  const thisRequest = ++requestNumber;
  const results = await search(query);
  // Searches can finish out of order; an older response must not replace newer results.
  if (thisRequest !== requestNumber) return;
  setResults(results);
}
```

## Check before finishing

Read changed comments as someone who has never seen the conversation. Remove
restatements of nearby code, repeated explanations, and phrases such as “I think,”
“for now,” or “added this” that merely narrate the task. Preserve useful purpose
and verified concerns, and check that every claim still matches the implementation.
