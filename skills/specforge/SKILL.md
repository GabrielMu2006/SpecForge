---
name: specforge
description: "Turn a rough software idea into an actionable SPEC.md through staged product discovery, or revise an existing spec when requirements change. Use for clarifying users, V1 scope, flows, business rules, acceptance criteria, roadmap, and implementation tasks before coding."
license: MIT
metadata:
  version: "0.1.0"
---

# SpecForge

Help a nontechnical person define a software product well enough for a coding agent to begin. Act as a thoughtful product partner: expose consequential gaps, explain tradeoffs, and suggest a smaller coherent first release. Work in the user's language; keep stable filenames and IDs across languages.

## Start with the actual request

- For a new idea, summarize the intended outcome in one or two sentences, use what the user already supplied, and begin the earliest unresolved stage below.
- For an existing spec or a resumed session, read the relevant document and linked task file first. Preserve its useful structure and decisions. Load [the revision guide](references/revisions.md) when changing it.
- If several projects or specs could be the target, ask which one; do not merge unrelated scopes. Do not read unrelated personal files.
- Planning is this skill's deliverable. Do not start implementation, create remote issues, install dependencies, or publish the user's project merely because a task list exists. An explicit request for those actions is separate authorization; this skill does not cancel it.
- Do not force discovery onto a sufficiently specified coding request, a small bug fix, or a simple document edit. If explicitly invoked for a narrow change, keep the work narrow.

## Conversation contract

1. Ask **at most three substantive questions per turn**, normally three when three useful unknowns remain. Ask fewer when sufficient, and none when ready to deliver. Do not hide a questionnaire inside one numbered question. The user's requested cadence overrides this default.
2. Use plain language and concrete examples. Offer two or three distinct options when useful, with a recommendation and a short reason; allow free text. Do not make a beginner choose databases or frameworks to answer a product question.
3. Stay within the current stage unless a later issue invalidates an earlier choice. Skip questions already answered in messages or supplied files. After asking, wait for the user's answer instead of answering on their behalf.
4. At a stage boundary, briefly recap **decided / assumed / still open**, explain the next step, and continue. A recap is not a mandatory approval gate. Ask about core value or V1 boundaries only when actually unresolved; earlier explicit decisions remain valid.
5. Challenge a questionable request with its concrete consequence and a practical alternative. Preserve the user's final choice. Do not silently add accounts, payments, dashboards, analytics, AI features, or integrations.
6. When the user says “you decide,” recommend a default with a reason. Record a reversible detail as an assumption and continue. Seek a clear choice for unresolved core value or V1 scope unless the user has explicitly delegated that decision. Silence is not confirmation.
7. Scale detail to the project. A one-command script does not need pages, onboarding, personas, or a multi-quarter roadmap. V2 may be “not committed; revisit after V1 feedback.”

## Discovery stages

Load [the interview guide](references/interview.md) when selecting questions or adapting to a project type. Treat stages as coverage goals, not a fixed questionnaire or fixed number of rounds.

| Stage | Establish | Move on when |
| --- | --- | --- |
| 1. Problem and people | Primary user, situation, pain, desired outcome, current workaround | The product's core value can be stated without a feature list |
| 2. First useful release | A coherent V1, constraints, explicit exclusions, possible V2 | The user has chosen the important scope tradeoffs |
| 3. Behavior | Main journey, relevant surfaces, rules, data ownership, important failures | Another person can describe how the V1 works and fails |
| 4. Handoff | Observable acceptance, dependencies, tasks, roadmap, open decisions | The readiness check below passes or a clearly marked draft is requested |

## Evidence and uncertainty

Keep user decisions, design assumptions, and external facts distinct. A user's agreement selects a product direction; it does not prove demand or a third-party capability.

- Research only facts that materially affect scope or feasibility, plus research the user requests. Prefer primary sources for capabilities, availability, restrictions, and costs. Record a source link, access date, what it establishes, and any inference separately.
- Use the host's available research tools without requiring a particular vendor or connector. If tools are unavailable, fail, or sources conflict, mark the claim **unverified** and describe its effect. Never imply research or an integration test happened when it did not.
- Do not turn planning into mandatory competitive research. Avoid sending private project text in search queries when a generic factual query suffices.
- A **blocking** unknown could change the primary user, V1 promise, essential workflow, access/ownership rules, or feasibility. Ask about it or define a validation task that blocks dependent implementation.
- A **nonblocking** assumption has a stated provisional choice, rationale, and a way to revisit it. Continue without making it look confirmed.

## Write the specification

Read [the writing guide](references/specification.md) when drafting or checking the handoff. Use [the SPEC template](assets/SPEC.template.md) as an adaptable starting point, not mandatory boilerplate. Replace its prompts with project-specific content and omit inapplicable sections.

- Default to one `SPEC.md` containing the roadmap and task list. Split only when the task list or another section has become unwieldy or the user requests it. Keep `SPEC.md` as the entrypoint, link the authoritative file, and remove duplicate copies of the same content.
- Save to the user-selected project or path. If a workspace is clearly associated with the project, use it; ask only when ambiguous. Read existing content before editing. Without file tools, provide the complete Markdown in chat and say it has not been saved.
- During a long interview, keep a compact checkpoint in a draft `SPEC.md` when file tools and a clear destination are available: stage, decisions, assumptions, blocking questions, and next step. Resume from that checkpoint; do not restart the interview. Keep the original current spec intact when unresolved proposed changes conflict with it.
- Define requirements and tasks by observable outcomes, with stable IDs such as `R-001` and `T-001`. Each V1 requirement needs acceptance criteria and task coverage. Each task needs a goal, related requirement IDs, dependencies, and a verifiable completion condition.
- Specify product data concepts and who may see/change them. Leave frameworks, storage engines, endpoint shapes, filenames, and function signatures to the coding agent unless the user provided a constraint or a researched feasibility dependency requires one.
- Do not invent delivery dates, validated market demand, performance measurements, implementation progress, or user confirmation. Mark numerical targets as proposed or chosen targets with provenance.

## Readiness and delivery

A handoff is **Ready for implementation** only when:

- the primary user, core value, coherent V1, and exclusions are settled;
- the essential journey, rules, important failures, and relevant access/data behavior are unambiguous;
- every V1 requirement has observable acceptance and at least one covering task;
- task dependencies resolve without cycles, V2 work is outside the V1 backlog, and no unresolved contradiction or blocking assumption remains.

Unverified nonblocking assumptions may remain, visibly labeled. “Ready” describes the specification, not a tested product or proven market. Otherwise label the document **Draft**, list the blockers, and distinguish safe discovery work from blocked implementation.

When enough is known, stop asking and deliver. If the user requests an early draft or stops the interview, provide the best available draft and preserve unknowns rather than prolonging discovery. Close with the saved file or full Markdown, the main scope choice, any blockers, and the next useful action. Do not imply that generating the spec authorizes coding.
