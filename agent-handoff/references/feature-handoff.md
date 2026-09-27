# Feature Handoffs

The handoff is a feature brief an engineer, designer, or product lead can read
without the original conversation. Give enough depth to build and review the
feature; scale detail to the work rather than targeting a page count.

## Document Structure

Adapt these sections to the feature. Keep the main narrative understandable
before readers open an appendix or follow a source link.

### 1. What We Are Building and Why

Explain the problem, intended users, current experience, and desired outcome.
Define scope and explicit exclusions. State the document's readiness and any
decision that prevents implementation. Separate document readiness from
implementation progress: a complete handoff can describe unbuilt work.

### 2. How It Should Work

Walk through the primary journey from entry point to outcome. Explain what the
user sees, does, and receives in response. Place relevant screenshots,
wireframes, or diagrams next to the behaviour they explain.

Cover the states that affect this feature: loading, empty results, errors and
recovery, permissions, keyboard use, and narrow screens where applicable.
Identify unresolved behaviour as an open decision. For a backend or nonvisual
feature, describe the caller's flow and observable outcomes; use a data-flow
diagram or concrete example when that improves understanding.

### 3. Expected Behaviour and Acceptance Criteria

Translate agreed requirements into observable checks. A compact table can
connect the situation, expected result, and relevant journey or figure. Include
important failure cases. Keep new recommendations visibly separate from
agreed acceptance criteria; do not silently decide missing product behaviour.

### 4. Decisions and Open Questions

Explain consequential choices and rejected alternatives with their reasons.
Distinguish approved direction from proposed design and assumptions. For each
open question, describe the effect on implementation and the next action to
resolve it. Include owners or dates only when known.

### 5. Delivery and Next Steps

Describe what exists, what remains, dependencies, and the next implementable
step. Summarise validation in terms of what a user can rely on and what remains
unverified. Include rollout or migration considerations when relevant and
supported by the source material.

### Technical Appendix

Put repository state, changed files, detailed API/data contracts, commands,
test results, source links, and continuation notes here. Keep architectural
decisions that explain the feature in the main narrative. Record the check,
outcome, source, and limits of each validation claim; a supplied test result
is not a newly executed check. Select useful evidence rather than pasting
entire logs.

## Visual Evidence and Proposed Designs

Choose visuals to resolve a reader's likely uncertainty:

| Need | Useful visual |
| --- | --- |
| Understand an existing screen or verified implementation | Capture or reuse an actual screenshot from the relevant application state. |
| Understand proposed layout or interaction | Create a labelled wireframe or sequence of states. |
| Follow navigation, permissions, or data movement | Use a small flow or architecture diagram. |
| Understand straightforward nonvisual behaviour | Use a concrete example or concise prose; no decorative screenshot is needed. |

If the interface is accessible and its current behaviour matters, inspect it
and capture the relevant state. If access or source images are missing, state
the limitation and continue with a clearly labelled proposal or textual flow.
Never reconstruct an image and call it an observed screenshot. Do not claim
visual fidelity or validation without viewing the relevant material.

Use available browser or application tools for captures. For low-fidelity
wireframes and diagrams, prefer editable SVG, HTML/CSS, or supported diagram
syntax. Use image generation only when a raster illustration or mockup adds
value. Follow the relevant available creation tool or skill; the handoff
workflow does not require a particular external design service.

For each included figure:

- Embed it beside the associated explanation, with meaningful alt text.
- Supply a caption stating what to notice and whether it is **observed**,
  **proposed**, or **approved**. Record its source and capture date or known
  version for screenshots; identify supplied images whose provenance is unknown.
- Use numbered callouts when annotation clarifies behaviour. Explain the
  callouts in adjacent text and keep labels readable at document scale.
- Preserve the evidence: annotations must not imply controls or behaviour that
  were absent. Exclude secrets and irrelevant personal information from captures.

Save required assets with the document. In saved Markdown, use relative paths
so the folder travels intact. If the destination cannot render a diagram or
asset format, provide a supported rendered version. An editable source may
accompany it. A link to an ephemeral preview is not a durable figure.

## Delivery and Readability Check

Default to Markdown and companion assets unless the user requests another
format. For Word or PDF, use the available document/PDF workflow and inspect
the rendered result. If export is unavailable, preserve the source and state
which requested output remains undelivered.

Before delivery:

1. Read only the main narrative: can a new reader explain the feature, its
   workflow, scope, and unresolved decisions without reading the chat?
2. Check that expected behaviour is testable and proposals have not become
   requirements merely by appearing in a wireframe.
3. Verify every local asset/link resolves. Open the document in an available
   renderer and inspect figures for readable text, cropping, and correspondence
   with the prose. Inspect exported pages for clipped content and broken layout.
   If rendering is unavailable, report that visual QA remains unverified.
4. Check that the next person knows where to begin, what evidence exists, and
   what still needs deciding or validating. Remove empty template sections and
   unfinished placeholders; express unknowns as specific open questions.

## Illustrative Excerpt

This invented example shows the level of explanation, not requirements to copy
into another feature:

> **Recovering a failed comment**
>
> Reviewers sometimes lose a long comment when saving fails. The agreed change
> keeps their text available so they can retry without rewriting it. Automatic
> background retry is outside this change.
>
> A reviewer writes a comment and selects Save. If the save fails, the form
> keeps the comment and explains how to retry. Only a confirmed save displays
> success. The proposed placement below keeps recovery beside the affected text.

```text
Comment
+--------------------------------------+
| Please clarify the delivery date.    |
+--------------------------------------+
Couldn't save. Your text is still here.
[Retry saving]
```

*Figure 1 — Proposed error-state wireframe, derived from the illustrative brief.
The retained comment and retry action stay together. This is not a screenshot.*

> **Acceptance:** after a failed save, the original text remains editable;
> retry submits that text and success appears only after confirmation.
>
> **Open decision:** should drafts survive a page reload? The agreed requirement
> covers failed saves in the current form; reload persistence needs a decision
> before storage behaviour is specified.
