# Test design examples

Choose a boundary that exposes the promised behaviour. Prefer a small unit
test for a pure calculation, and an integration test when the risk lies in
components working together. Use the existing framework; the Python examples
below illustrate decisions rather than prescribe a language.

## Assert an independent result

For a basket containing items priced at 10 and 5, the specified total is 15:

```python
def test_basket_total_includes_each_item():
    assert basket_total([10, 5]) == 15
```

Computing `expected = sum(prices)` repeats the likely implementation. A known
result keeps the assertion independent. For complex calculations, use a worked
example, a trusted reference or a separately justified invariant.

## Observe the promised effect

For a user service whose contract includes retrieving a created user:

```python
def test_created_user_can_be_retrieved(user_service):
    created = user_service.create(name="Alice")
    retrieved = user_service.get(created.id)
    assert retrieved.id == created.id
    assert retrieved.name == "Alice"
```

These assertions describe one outcome. Checking that an internal repository
method was called would not establish that the user is retrievable. Reading a
private cache or database row can also bypass the behaviour callers rely on.
When testing a database adapter or migration itself, however, persisted state
may be the actual contract and direct database assertions are appropriate.

## Make a regression test discriminate

Use the smallest input that triggers the reported defect. Confirm that the
assertion fails on the unfixed implementation and passes after the fix. For
example, a duplicate registration test should verify the specified rejection
and preservation of the original user, rather than merely accepting any error.

If the new test passes immediately, check the fixture, exercised path and
assertion. The requirement may already be met. Do not deliberately break
unrelated code just to manufacture a red result.

## Keep the feedback useful

- Use deterministic fixtures and isolated state; a test should not depend on
  another test's execution order.
- Assert errors precisely enough to distinguish the intended failure from an
  unrelated exception. Avoid broad exception assertions and swallowed errors.
- Use snapshots only when the captured output is a meaningful, reviewed
  contract; do not accept a changed snapshot simply because the runner offers it.
- Include a real integration test when a fake cannot detect the relevant risk,
  such as query semantics, serialisation or transaction rollback.
