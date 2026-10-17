# Revising or resuming an existing specification

Read when the user supplies an existing spec or requests a change to one.

1. **Recover the baseline.** Read `SPEC.md`, its authoritative linked files, active plan/revision, current assignment and authorization, status, pending decisions, and the user's change request. Reuse the existing IDs, accepted terminology, and unaffected content. Do not assume that a polished document was implemented. If supplied material describes another project, resolve the mismatch before editing; a withdrawn mistaken message does not enter the baseline.
2. **Explain the effect.** Identify which users, V1 boundaries, journeys, requirements, data/visibility rules, acceptance criteria, roadmap milestones, and tasks the request touches. State material tradeoffs plainly. A cosmetic change need not reopen discovery.
3. **Ask only consequential questions.** Use at most three per turn. A direct instruction that clearly changes scope is already a decision; do not seek the same permission again. Ask when its consequences leave a core choice ambiguous. Do not reinterpret an ambiguous idea as an approved scope change.
4. **Apply a coherent revision.** Update the affected content and cross-references together. Preserve stable IDs; allocate new IDs for new items. Mark a referenced removed requirement/task as removed or superseded with a reason instead of reusing its ID. Remove stale acceptance and dependencies. Keep V2 ideas outside V1 unless moved explicitly.
5. **Recheck status.** Reevaluate the readiness conditions in `SKILL.md`. A new unresolved V1 dependency makes the proposed revision Draft. Preserve completed-task evidence; if the definition of done changes, flag that task for revalidation and explain why.
6. **Summarize the delta.** Record a concise change note: what changed, why, affected IDs, unresolved choices, and the next step. Mention the files actually saved. A change note describes decisions, not fictional approval or implementation history.

When a new plan replaces an old one, update the entrypoint's active-document index and label/link the superseded plan. Reconcile the current status and affected acceptance/task text, not just a final appended note. Preserve old evidence as history and distinguish a new definition of done from a previously completed one.

Propagate a critical target's proposed/adopted status, counting method, dataset, and adoption basis into the revised tasks and any startup prompt. Copying a proposed percentage out of an assumption does not turn it into a formal release gate. Preserve the baseline and rationale when the metric or evaluation material changes.

## Pending proposals and checkpoints

If a proposed change is unresolved, keep the current baseline requirements intact and record a clearly labeled **Pending change** with its affected IDs and unanswered decision. Distinguish the baseline's status from the proposed revision's status. Do not blend two incompatible versions into one current spec.

For a first-time interview with no baseline, save a Draft checkpoint at the known output path when useful. It should contain the current assignment/authorized work, stage, decisions made, provisional assumptions, blockers and affected task IDs, pending question batch with partial answers, active files, and next step. On resumption, merge late answers and start at the earliest unresolved stage without repeating settled questions or choosing unanswered items.

A complaint about a prototype during a planning-only assignment remains feedback for that assignment; it does not itself authorize source changes. A later clear implementation request updates the assignment and should proceed within the existing authorization. Do not turn this distinction into a routine confirmation step.

If the user requests an early handoff, output a Draft with the blockers rather than requiring more conversation. If file tools are unavailable, return revised Markdown or a precise patch and disclose that no file was changed.
