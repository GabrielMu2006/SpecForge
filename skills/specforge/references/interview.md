# Interview guide

Read this when deciding what to ask next. Select questions that change a decision; do not present this guide as a questionnaire.

## 1. Problem and people

Discover the person, situation, and outcome before the feature list. Distinguish a user from a buyer only when that difference matters. Ask about the current workaround rather than demanding market-size estimates from a beginner.

For “a site where friends share timetables and find free time,” a useful opening is:

1. “Who is the first version mainly for: classmates at one school, or friends across different schools?”
2. “Is the main goal to browse friends' timetables, or quickly find a time when everyone is free? I recommend choosing one as the main action.”
3. “How do you coordinate this today: messages, screenshots, or a shared calendar?”

Do not start by asking about login providers, databases, deployment, or every future feature.

## 2. First useful release

Describe one end-to-end outcome and identify the smallest release that delivers it. “Smallest” must still respect the user's chosen core promise. A read-only mockup is not a working collaboration product.

For each tempting addition, explain who benefits, what burden it adds, and whether the V1 promise fails without it. Suggest deferral, then preserve the user's choice. Confirm the meaningful boundary, not every minor detail.

Useful decisions include who can participate, how information enters the product, whether collaboration is essential, and which constraints actually matter. A hard deadline or budget changes scope; do not invent either.

Example challenge: “Importing school timetables could save effort, but we have not verified access to the school's system. Manual entry would make a smaller first version possible. Would manual entry still meet your first-release goal?”

Manual entry becomes V1 only after the user's choice or explicit delegation; an unverified integration cannot quietly become a promised feature.

## 3. Behavior, adapted to the product

| Project | Clarify the relevant surfaces and behavior |
| --- | --- |
| Web or mobile app | Entry point, screens, navigation, empty/loading/error states, ownership, collaboration, offline behavior if needed |
| Script or command-line tool | Inputs, invocation, outputs, invalid input, overwrite behavior, repeat runs, partial failure; no invented pages |
| Automation | Trigger, schedule/time zone if relevant, connected accounts, duplicate runs, retry/stop behavior, failure visibility |
| Plugin or extension | Host application, invocation, context access, permissions, output, unsupported host states |
| Agent skill | Trigger, inputs, conversation contract, tool availability, artifacts, handoff, resumption, boundaries |

Trace one realistic journey from start to outcome. Then examine the failures that would change product behavior: missing inputs, denied access, no results, stale data, incompatible data, or a failed dependency. Do not enumerate irrelevant edge cases.

Describe data with familiar nouns (person, timetable, group, invitation), relationships, and visibility. A business rule such as “leaving a group immediately removes access to its shared availability” is a product decision, not a database choice.

## 4. Handoff

Turn “easy,” “fast,” and “smart” into observable outcomes without inventing measurements. For example: “When no common slot exists, say so and let the person change the date or duration; do not invent a suggestion that overlaps a busy period.”

Prioritize tasks by dependencies and useful outcomes. Do not force dates or numerical estimates. Keep a research/validation task separate when its result decides whether implementation should proceed.

## Pace and recovery

- Three unanswered questions are enough for one turn; avoid extra questions in the introduction or conclusion.
- If a user only answers one, incorporate that answer and ask only what still matters.
- “I don't know” calls for a recommendation, not the same question in more technical language.
- At a stage boundary, use a short recap: “We have chosen X. Y is a provisional assumption. Z remains open. Next we will describe the main journey.”
- A well-specified brief can skip stages. A changed primary user may reopen stage 1. Do not restart unaffected stages.
- A pause checkpoint should state the next unresolved decision so another session can continue without the full chat history.
