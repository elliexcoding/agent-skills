---
name: eli5
description: "Explain topics, code, concepts, or errors at a requested level or for a specific audience. Use for ELI5, 'explain like I am', 'simplify this for', or explanations aimed at children, non-technical readers, or a named person or role."
---

# Explain Like I Am... (ELI5)

Make the topic accessible to the intended audience, matching their background,
vocabulary, and interests while preserving the facts.

## Step 1: Identify the Audience

Use the user's stated audience and existing context. The categories below are
starting points; age, job title, or relationship alone does not establish what
someone knows or enjoys. Prefer known interests over assumed ones.

### Ages

| Audience | Style |
| --- | --- |
| Age 5 | Very simple words, short sentences, and concrete analogies with toys, animals, sweets, or playgrounds. "Imagine you have a box of crayons..." |
| Age 10 | Primary school level. Basic cause and effect, with school, sport, or video game analogies. |
| Age 15 | Some abstraction is appropriate. Phone or gaming references can help when familiar to the reader. Keep the tone slightly casual. |
| Age 20–30 | Clear and direct. Real-world analogies from daily life, work, or money. |
| Age 40+ | Clear and respectful. Use familiar experiences from daily life, work, or family when relevant. |

### Education Levels

| Audience | Style |
| --- | --- |
| Year 6 / fifth grade | Simple vocabulary, concrete examples, and minimal jargon. "Think of it like..." |
| Early secondary school / middle school | Introduce basic terminology with definitions and explain the logic step by step. |
| Upper secondary school | Moderate complexity is appropriate. Introduce proper terms but explain them. |
| University student | Connect theory to practical applications. Use technical terms with brief context. |
| Postgraduate student | Use the stated subject background to calibrate detail. Focus on nuance, trade-offs, edge cases, and implications. |

### Job Roles

| Audience | They may care about... | Frame explanations around... |
| --- | --- | --- |
| Manager | Impact, timeline, risk, cost | Business outcomes, team implications, and decisions |
| Engineer | How it works, architecture, trade-offs | Technical details, implementation, performance, and maintainability |
| Designer | User experience, visual impact, flow | Effects on users, interaction patterns, and accessibility |
| Director | Strategy, return on investment, competitive advantage | The big picture, market position, and resource allocation |
| Colleague | Practical context, shared work | Effects on their work and what they need to collaborate |
| Product manager | User value, priorities, scope | Feature impact, user stories, and scope decisions |

### Relationships

| Audience | Tone | Analogy style |
| --- | --- | --- |
| Wife / husband / partner | Warm and conversational | Shared experiences and daily routines |
| Father / mother / parents | Respectful and clear | Familiar activities or technology they use |
| Kids / children | Playful, encouraging, and short | Games, school, or animals they know |
| Friend | Casual, with humour when suitable | Shared interests or familiar experiences |

For an ELI5 request without a stated audience, default to the age-five level.
For another named audience without a stated knowledge level, use accessible,
respectful language and adjust to any context the user supplies.

## Step 2: Read the Source Material

Understand what needs explaining before translating it:

- **Code:** Read the relevant code files and establish their purpose and behaviour.
- **A concept:** Identify its core components and how they relate.
- **An error message:** Use the message and available evidence to establish what
  failed. Distinguish a confirmed cause from a possible explanation.
- **A technical document:** Extract the key points that matter to the audience.
- **Anything else:** Identify the essential "what" and "why".

## Step 3: Craft the Explanation

### Structure

Start with one sentence that captures the essence. Use an analogy when it helps,
add details appropriate to the audience, and explain why the topic matters to
them. Adapt this structure to the user's requested format and length.

### Language Calibration

For readers unfamiliar with the topic:

- Avoid jargon; define essential technical terms immediately.
- Keep one main idea per sentence and prefer concrete examples.
- Connect the explanation to the reader's experience. For example, a server can
  be compared to a waiter taking requests and bringing back results.

For technical readers:

- Use proper terminology, calibrated to their actual background.
- Focus on useful trade-offs, edge cases, and design decisions.
- Compare with concepts they already know and respect their existing knowledge.

For business readers:

- Lead with impact and outcomes.
- Quantify when the source supports it; do not invent costs, timelines, or limits.
- Include implementation details when they affect a decision or the user asks.
- Explain what the evidence implies for the decisions at hand.

### Tone Matching

- Young children: encouraging and playful, with clear, short sentences.
- Teenagers: slightly casual without forced slang.
- Professionals: confident and clear, respecting their intelligence.
- Family and friends: warm and conversational, without condescension.

## Examples

**User says:** "ELI5 what a database index is"

**Audience:** Age 5 by default.

**Response style:** "Imagine a big book about animals. To find dinosaurs, you
could look through every page, or use a list that tells you which pages mention
dinosaurs. A database index is like that list. It helps the computer find the
information it needs quickly."

**User says:** "Explain this API rate limiting to my manager"

**Audience:** Manager.

**Response style:** Explain the limit as a speed limit, using the actual figures
from the source. Describe the observed impact and any supported options, costs,
and trade-offs that matter to the manager's decision.

**User says:** "Break down this React useEffect hook for a university student"

**Audience:** University student, calibrated to their stated experience.

**Response style:** Read the hook first. Explain its purpose, what causes its
effect to run, and how its setup and clean-up relate to the surrounding component.
Define relevant terms and connect the mechanism to a practical example.

## Important Reminders

- Explain the purpose before the mechanism, especially for code.
- Never talk down to the reader or equate unfamiliarity with low intelligence.
- Simplify detail without making the explanation false. Flag the limits of an
  analogy or a meaningful omission when they would otherwise mislead the reader.
- Match length to the request and audience: concise for young children, with
  more depth when the reader needs it.
