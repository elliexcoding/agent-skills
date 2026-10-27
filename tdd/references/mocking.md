# Test doubles and external boundaries

Prefer real code inside the behaviour under test. Replace dependencies where
their actual operation would make feedback unreliable, slow or externally
destructive: network clients, clocks, randomness and some storage operations.

Choose the replacement for the contract you need to verify:

| Dependency or risk | Useful approach |
| --- | --- |
| Expiry, timeouts or random identifiers | Inject a clock or deterministic source. |
| External API success, rejection or timeout | Use a stub or fake with realistic responses and errors. |
| SQL semantics, constraints or transactions | Use the project's isolated test database; an in-memory substitute may differ. |
| File contents, permissions or rename behaviour | Prefer a temporary directory when real filesystem behaviour matters. |
| Pure calculations or internal orchestration | Exercise the real collaborators through the chosen interface. |

Pass dependencies through an existing constructor, argument or adapter seam.
If none exists, introduce the smallest useful boundary rather than a new
framework. Avoid changing public interfaces solely to expose private state to
tests.

An interaction assertion is appropriate when the interaction is itself the
contract: for example, a payment adapter sends the amount, currency and
idempotency key required by its provider. It is weaker evidence for an internal
method call whose name and ordering are free to change. State what a double
cannot prove about the real provider and use contract or integration coverage
when that distinction matters.

Keep doubles simple and faithful to the dependency's interface. Do not
reimplement business rules inside the fake or let it silently accept operations
the real dependency rejects. Simulate the particular failure required by the
test rather than constructing a general-purpose service emulator.

Follow repository conventions for asynchronous tests and cleanup. Prefer
explicit completion signals or controlled time to arbitrary sleeps, and keep
tests independent of live credentials and production data.
