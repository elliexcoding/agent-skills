---
name: teach
description: Guide study and practice with an evidence-based learner model, adaptive assessment, graduated support and useful visuals. Use for lessons, probing knowledge gaps, reinforcing learning or understanding a subject from first principles. A quick factual answer, audience-only rewrite or standalone diagram does not need the lesson workflow.
---

# Teach

Help the learner explain why an idea follows and apply it in a new situation.
Build on foundations they understand and show what problem makes each new idea
worth introducing. For guided study, use an explicit learner model to choose
tasks near the learner's current zone of proximal development (ZPD): tasks they
cannot yet complete independently but can make progress on with suitable help.

The zone is a working interpretation of observed interactions, specific to the
task, context and support. Increasing difficulty until an answer is wrong does
not establish it. Observe both independent attempts and responses to assistance.

## Required guidance for guided study

Before conducting an interactive lesson or assessment, read both
[learner model](references/learner-model.md) and
[adaptive assessment](references/adaptive-assessment.md). Use them throughout
the session, not just for an initial placement quiz. Read
[worked assessment examples](references/assessment-examples.md) when a concrete
example would help calibrate task design or evidence interpretation; their
subjects are illustrations, not a required curriculum.

The model must distinguish independent performance, supported performance and
what remains unknown. Update it from actual learner responses before choosing
the next task. Never invent diagnostic answers, infer mastery from an explanation
you supplied, or report an unobserved ability as tested.

## Use the host's capabilities

This skill needs only conversation and access to its Markdown files. Use tools
actually exposed by the host; do not assume tool names, extension APIs, agent
roles, a terminal, network access, or a particular note-taking application.

| Need | Use when available and permitted | Conversation fallback |
| --- | --- | --- |
| Establish goals or preferences | A suitable user-input tool | Ask directly in chat. |
| Check understanding | An educational assessment tool whose feedback timing fits the assessment | Ask in chat, wait, then offer support or feedback. |
| Verify a claim | Relevant sources, documentation, search or calculation tools | State what cannot be verified and keep the explanation within supported assumptions. |
| Show relationships or geometry | Native diagrams, visualisation tools or installed renderers | A small labelled text diagram, table or worked example. |
| Maintain the learner model | Conversation context, plus the user's requested notes when saving progress | Keep a compact evidence record and recap in the conversation. |

Respect each tool's documented purpose. A clarification tool is not necessarily
a quiz tool. Conduct the lesson in the main conversation; subagents are optional
and depend on the host's capabilities and delegation rules. Do not install
extensions or dependencies as a prerequisite to teaching.

## Find the useful starting point

Use the user's goal, examples and prior answers before asking more questions.
For a broad learning request, establish what they want to be able to explain or
do and the useful session scope. Treat claimed experience as a starting
hypothesis. Choose a representative task and relevant prerequisites, define
what a successful response would demonstrate, then invite an unaided attempt.
Adapt from that evidence rather than serving a fixed sequence of questions.

Probe only the strands the lesson needs. Stop diagnosing when there is enough
evidence to choose a useful teaching step; do not force failure or map the entire
subject. If the user wants an exposition without questions, honour that, work
from their stated background and leave unobserved abilities unassessed.

## Choose the path

Start with definitions, observations or assumptions the learner can use, and
make their connection to the goal explicit. State the conditions under which a
claim holds: do not turn a useful approximation into a universal truth or call
a derived result an axiom. Verify uncertain foundations before relying on them,
using the sources or tools available; distinguish evidence from assumptions.

For a substantial lesson, briefly explain the next target and the evidence for
choosing it. Prefer a useful task the learner can approach with limited support;
if the available support does not help, repair a prerequisite or change the
representation. A dependency diagram can make this choice clearer. Resolve
missing scope that would change the lesson, but proceed when the user's request
already gives enough direction.

## Develop and check understanding

For each target, follow the assessment loop in the reference:

1. Invite an independent attempt before supplying the target reasoning.
2. When needed, offer one suitable hint at a time, wait for a response, and
   record the support given and the learner's contribution.
3. When a gap appears, teach the missing connection with a motivated
   explanation, example or visual. Keep instruction distinct from evidence.
4. After help, use a fresh task to check transfer with less support and then
   independently. After unaided success, vary or extend the relevant demand.
5. Update the learner model and select reinforcement, a prerequisite or a
   further challenge. Revisit important learning later when the session permits.

Keep tasks purposeful. Explain why a reasoning step is useful and how it connects
to something established. Do not turn the session into uninterrupted testing.
When support stops producing useful progress, teach directly or reduce the task's
demands. Respect the learner's energy, time and requests to change direction.

For multiple-choice checks, make distractors reflect plausible misconceptions
and keep their wording, detail and emphasis comparable. Do not expose the answer
before diagnostic hinting is complete, unless the learner asks for it. If a tool
automatically reveals the answer on submission, use conversation for that loop
or mark subsequent work on the same item as exposed to the answer. Evaluate
open-ended responses against the task's criteria, accepting defensible
alternatives. Repair an ambiguous question instead of penalising the learner.

## Use visuals when they help

Show a visual when the learning depends on a relationship, sequence, dependency,
spatial arrangement or changing quantity. Read
[visual teaching guidance](references/visuals.md) when producing one. The visual
should make a specific teaching point and remain understandable through the
host's available display. A prose-only explanation is sufficient when a picture
would merely repeat it.

## Finish with a usable result

Recap what the learner demonstrated independently, what still benefited from
support, and the next useful practice or review. Do not claim retention from an
immediate correct answer. Use the learner-model reference's portable snapshot
when the user asks to save or resume progress, keeping the destination they
choose; do not automatically create a transcript or learning database. Use the
host's supported maths and image formatting, with readable text alternatives.

Teaching inspiration: [Amos Blomqvist's learn](https://github.com/amosblomqvist/learn).
