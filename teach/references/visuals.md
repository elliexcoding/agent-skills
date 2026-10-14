# Visual teaching across hosts

Choose the representation from the idea and the available display. The teaching
point should survive a move between agent harnesses, even when the presentation
changes. No particular extension, rendering service or agent role is required.

## Pick a representation

| Teaching point | Suitable representation |
| --- | --- |
| Dependencies, branching or containment | A small Mermaid graph, tree or labelled text diagram. |
| Exchanges or changes of state | A sequence diagram, state diagram or short sequence of panels. |
| Exact positions, shapes or vectors | SVG or a plot with explicit coordinates and labels. |
| How a parameter changes an outcome | An interactive visual if supported; otherwise a few labelled cases. |
| Numerical behaviour or measured data | A plot generated from the actual formula or data. |
| Differences between a few alternatives | A table when it makes comparison easier than a diagram. |

Start with the smallest view that carries the point. Label what the arrows mean
and keep causal, chronological and logical dependency relationships distinct.
Show units, assumptions, scale and uncertainty when they affect interpretation.
Mark a schematic as such if distances or sizes are not meaningful.

During assessment, decide whether the visual belongs to the original task or is
additional help. Record added annotations, highlighted relationships or worked
diagrams as support when they supply the target insight. A later independent
probe should not inadvertently repeat that hint. Keep normal task materials and
accessibility aids available under the agreed assessment conditions.

## Produce and inspect

Use the host's existing visualisation skill or tool if it fits the task. Otherwise
use supported inline Mermaid, or create a local SVG, HTML or plotted image with
the available tools. Prefer deterministic geometry and plotting for claims that
depend on precise relationships or values. Richer rendering is optional; do not
require package installation or external hosting to complete the lesson.

When rendering and image inspection are available:

1. Write the source from the established explanation or data.
2. Render it in the intended format and inspect the actual result.
3. Check both meaning and legibility: arrow direction, labels, numeric values,
   axis scales, clipping, overlap and contrast.
4. Correct any issue and inspect the revised result before presenting it.

A successful render verifies neither the underlying claim nor the lesson's
accuracy. Check the visual against the reasoning and sources as well as checking
its appearance. If a delegated tool returns an image, inspect that result when
possible rather than relying only on its success message.

If the host can display a diagram but cannot return its rendered appearance for
inspection, review the source and semantics, keep the layout simple, and do not
claim visual verification. If it cannot render the chosen format, use a readable
text diagram, table or worked example. Provide source as well when requested;
do not make the learner decipher raw Mermaid or SVG merely to follow the lesson.

## Present and preserve

Place the visual beside the explanation it supports. Supply a short caption or
text equivalent stating the relationship it demonstrates. Use ordinary supported
Markdown or the host's native attachment format. Use application-specific embeds
only when the user has chosen that application.

For files, follow the workspace's output conventions and use a descriptive,
non-conflicting name. Preserve editable source alongside an exported image when
the user needs a reusable artefact. Link or attach only files actually created,
and distinguish an inspected export from source whose rendering was unavailable.
For interaction, check that the controls alter the relevant relationship and
that the labels still match the displayed state.
