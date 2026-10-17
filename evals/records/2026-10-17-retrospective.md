# Retrospective evidence, version 0.1.0

Date: 2026-10-17. Method: read all user/assistant messages across three selected Codex histories (35 host turns, including an empty interrupted turn and a mistaken-project exchange), and inspect key historical specification/tool records. The runtime version visible in the historical skill record was 0.1.0. Models were not established for this record.

This is a retrospective review, not a replay, independent forward test, or cross-host benchmark. Later turns also used other skills and implementation agents, so implementation defects are not automatically attributed to SpecForge. Private raw histories are not copied into this repository.

| Case | Observed behavior | Revision it motivates |
| --- | --- | --- |
| Document grouping | First handoff treated core grouping quality as nonblocking; a user follow-up caused a validation blocker and Draft status. Proposed numeric targets later required explicit adoption clarification. | Core examples, readiness/dependencies, target provenance in handoffs |
| Management game | A question batch needed repeating after a user reported an interrupted interaction. First handoff was followed by requests for more detail and experience/UI guidance. | Resumable pending questions, experience handoff |
| Newspaper game | Scope and narrative choices were preserved. UI production detail came after the first handoff; investigating while publishing lacked a settled interaction. An unrelated project report was correctly rejected as mismatched. | Experience/state intersections; preserve project isolation |

The new [E-11 through E-18 scenarios](../README.md) use synthetic inputs that isolate these behaviors. This record does not mark E-01 through E-18 passed and is not evidence that version 0.2.0 resolves them.
