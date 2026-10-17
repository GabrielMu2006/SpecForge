# Specification and task guide

Read when drafting or reviewing a handoff. The output serves both a nontechnical owner and a coding agent. Match the user's language; retain stable IDs and filenames.

## Content that earns its place

Use the [template](../assets/SPEC.template.md) as a starting point. Include positioning, primary user and situation, core needs, chosen V1, exclusions, possible V2, relevant surfaces, essential flows, rules, data needs, acceptance, roadmap, tasks, and uncertainty. Combine short sections when clearer. Do not manufacture pages for a script or a V2 promise for a tiny tool.

Keep technical constraints the user actually supplied. Explain why any additional technical decision affects the product before including it. Product entities and access rules are useful; an invented SQL schema is unnecessary.

## Core promise and experience

Describe a representative input/situation, the useful outcome, and a counterexample or failure boundary for the core promise. For a quality-dependent capability such as semantic grouping, explain how representative material and judgments will establish usefulness; a single easy match is not enough to settle the core promise. Identify validation tasks and blocked dependents when missing evidence could invalidate V1. Ordinary implementation and performance tuning need not be completed during discovery.

For an interface product, describe key scenes, the primary action and information hierarchy, important states, chosen/provisional visual direction, needed assets, and relevant window/device constraints. Describe behavior rather than only adjectives such as “modern” or “game-like.” A management game should include a concrete cycle of decision, cost, result, explanation, and next decision. Open design choices can become prerequisite design/prototype tasks; do not manufacture images, approval gates, or a UI for a command-line tool.

## Requirements

A useful requirement contains:

- a stable ID and user-visible outcome;
- the rule that determines success, including important invalid or empty cases;
- observable acceptance criteria;
- its release/scope status and any provisional dependency.

Example:

**R-003 — Find a shared free slot (V1).** A group member selects a date, participants, and a minimum duration. Results contain only intervals inside the chosen search window when every selected participant is available.

Acceptance: if one selected participant has not supplied availability, identify that person and do not present the incomplete result as everyone's free time. If no interval is long enough, show an empty result and allow changing the inputs. The duration, time-zone, and interval-boundary rules must be settled elsewhere in the spec.

Avoid “works correctly” and “has a good UX.” If a target is a recommendation rather than a user's decision or measured fact, say so.

For consequential combinations, record **current state + action → resulting state, cost, retained/lost work, feedback**. For example, decide whether publishing ends or continues an ongoing investigation and how any lost budget is shown. Check that a preview and its final operation use the same product rules, and that navigating or undoing does not silently discard work. Link a few end-to-end scenarios to requirements/tasks rather than enumerating every possible combination. Distinguish an undefined rule from an implementation that violates an already-defined rule.

## Tasks

Use a table for a short backlog; use task blocks when acceptance needs more explanation:

```markdown
### T-003 — Find common availability
- Goal: Let a group member find a time when all selected participants are available.
- Requirements: R-003
- Depends on: T-001, T-002
- Done when: The accepted scenarios in R-003 pass, including missing availability and no common slot.
- Status: Planned
```

Prefer end-to-end outcomes to premature file/function instructions. Dependencies must identify existing tasks, form an acyclic order, and not point to deferred V2 features. Every V1 requirement must be covered; every task must support a requirement or a stated enabling/validation need. Avoid both untestably large tasks and line-by-line implementation choreography.

Task status defaults to Planned. An implementation request, generated code, or completed spec does not itself prove a task is done. Preserve existing completion evidence when revising a backlog; flag changed acceptance for revalidation instead of silently declaring it still complete.

Use explicit dependency IDs rather than abbreviated ranges in new task tables. IDs remain stable when prerequisites are added later; graph order is determined by dependencies, not numeric ID order. For the optional repository maintainer linter, canonical statuses are Planned, In progress, Blocked, Complete, Needs revalidation, Removed, or Superseded (and the documented Chinese equivalents). Other host formats remain usable; structural lint cannot establish prose quality or lifecycle correctness.

## Uncertainty and provenance

Keep three concepts separate:

| Kind | Record |
| --- | --- |
| Product decision | Chosen behavior, who/what selected it, rationale when relevant |
| Assumption | Provisional choice, rationale, impact if false, validation or revisit condition, blocking or nonblocking |
| External evidence | Exact factual claim, source URL or supplied artifact, access date, what remains unverified |

Do not label a suggested choice “confirmed” because it appeared in an assistant recap. Do not treat the user's anecdote as market validation. An existing spec is the recorded baseline, not evidence that its assumptions or implementation have been verified.

Write blockers as concrete decisions, not “TBD.” For an essential unknown integration, explain the requirement it blocks and create a validation task if useful. The whole handoff stays Draft while a V1 blocker remains, even if independent work can proceed.

For a critical numeric target, record its definition/unit and counting method, dataset/source, proposed or adopted status, adoption basis (including an explicit delegation), and affected requirements/tasks. Keep measurements and their evidence separate from targets. Carry this status into task completion conditions and handoff prompts; mentioning a proposal there does not adopt it. Quality experiments distinguish development material from independent acceptance material. A metric or dataset change retains the old baseline and a reason; no mandatory reconfirmation is needed for a choice already authorized.

## Roadmap and document structure

Use milestones defined by outcomes and exit conditions. Do not assign delivery dates or effort estimates without a basis. Keep V2 ideas explicitly provisional and outside V1 acceptance and tasks.

Default to one `SPEC.md`. If splitting is justified, give one authoritative home to each item: for example, `TASKS.md` owns tasks while `SPEC.md` owns product requirements and links to the task file. Retain requirement IDs in tasks, update both sides together, and do not leave an obsolete embedded backlog behind. Preserve existing filenames where practical.

When several plans exist, keep a compact current-document index in the entrypoint: role, active revision/file, and what it replaces. Update current status at its authoritative location instead of leaving a contradictory old status above a new appendix. Historical measurements and completion evidence remain history, visibly dated.

## Executable handoff, when requested

Provide the entry documents and their authority, current assignment and already-authorized operations, core promise and scope/exclusions, task order with prerequisites, expected artifacts, validation steps/evidence, proposed versus adopted targets, and unresolved blockers with independent work that can continue. A short copyable startup prompt can summarize these and link to the authoritative plan; it must not create extra permissions or an approval gate. Preserve planning-only scope across feedback, and honor a later explicit implementation instruction without asking again. Do not invent a file list or command before checking an existing repository when those details matter.

## Final consistency pass

Check the actual content, not only the headings:

1. Does each chosen feature serve the core outcome, and do exclusions agree with flows and acceptance?
2. Can a coding agent execute the main journey without guessing a major business rule?
3. Are ownership, visibility, deletion/revocation, and failure behaviors covered wherever they affect that journey?
4. Are assumptions distinguishable from decisions, and do blocking facts have evidence or an explicit unresolved status?
5. Does every V1 requirement have acceptance and task coverage, with valid dependencies and no V2 leakage?
6. Do the status, linked files, and summary agree with unresolved issues?
7. Do the core examples and evaluation method support the actual promise, and are important feature intersections settled?
8. Are experience/design prerequisites and metric adoption states preserved in the task order and handoff?

If a document has a blocker, deliver it as Draft rather than claiming completeness. Stop questioning once the core decisions are sufficient; preserve nonblocking uncertainties without turning them into extra rounds.
