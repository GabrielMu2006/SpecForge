# Behavioral regression scenarios

These scenarios are a reusable evaluation plan, not a claim of completed model runs. Static CI checks package structure and sample task graphs; it cannot prove interviewing quality or correct skill selection.

## How to evaluate

Use a fresh conversation for each case in a temporary project. Provide the complete `skills/specforge/` directory. For automatic-selection checks, make it discoverable and send the prompt without explicitly invoking it. For workflow checks, explicitly invoke the skill. Give only the prompt and specified raw fixture to the agent, keeping the assessment criteria separate from its context.

Advance multi-turn scenarios with the stated user messages. Save actual responses and generated documents. Record the host and model when known, date, skill version/commit, tools available, and pass/fail evidence. Use only synthetic data. A transcript must not be reconstructed and presented as a real run.

Assess the decision and observable outcome, not exact wording or heading names. Count substantive questions rather than question marks. Mark a scenario failed when any required behavior is absent; use “not run” rather than inferring a pass from static analysis. External research claims need source evidence in the actual output.

## Cases

### E-01 — A beginner's vague idea

Prompt: “我不懂开发，想做一个朋友共享课表、找共同空闲时间的网站。帮我先把需求想清楚。”

Expect: selects product discovery; asks no more than three understandable questions about problem/users/value; does not generate a supposedly final spec, demand a technology stack, or begin implementation. No extra questions hidden in the introduction or conclusion.

### E-02 — Uncertainty without silent scope decisions

After E-01, say: “同一所学校的朋友，主要是找共同空闲，平时发截图。其他我不知道，你给我建议。”

Expect: incorporates those answers, suggests a coherent next scope choice, does not ask again who the users are. Minor defaults can be marked provisional. It does not quietly claim that school-system imports, public profiles, or paid subscriptions are part of confirmed V1.

### E-03 — Complete brief, small tool

Fixture: [file organizer spec](../examples/file-organizer/SPEC.md).

Prompt: “使用这个已定范围生成可交给开发 Agent 的规格。只预览文件归类，绝不移动文件；需求和规则都在附件里。如果没有阻塞项就直接交付。”

Expect: no forced four-round interview, pages, accounts, or invented V2. Preserves read-only behavior and supplied choices, keeps tasks covered and acyclic, and delivers without asking for another approval merely to write the requested document.

### E-04 — Existing spec, material change

Fixture: [timetable spec](../examples/timetable/SPEC.md), copied to the temporary project's `SPEC.md`.

Prompt: “让 V1 支持跨学校、跨时区的朋友。检查需要变更的规则，先问清楚关键问题。”

Expect: recognizes the explicit new scope while explaining consequential unknowns such as display time zones and date/week semantics. Asks at most three focused questions. Does not erase the baseline, silently retain same-zone acceptance, or claim the unresolved revision is Ready. Keeps existing IDs and records pending change clearly.

Follow-up: “先保存待定变更，我下次再决定。” Expect: a resumable checkpoint that distinguishes current baseline from the unresolved proposal.

### E-05 — Changed definition of done

Fixture: timetable spec, with T-004 marked Complete and a synthetic note “old R-004 scenarios passed.”

Prompt: “我决定增加一个需求：结果也显示只差一个人就全员空闲的候选时间，但必须和全员空闲分开。请更新规格。”

Expect: preserves completion evidence for the previous acceptance, explains whether the new behavior is a new requirement/task or changes existing acceptance, and flags affected completed work for revalidation if necessary. It must not silently mark new behavior complete or mislabel partial availability as everyone's free time.

### E-06 — Essential external fact, no browsing

Environment: file access available, browsing unavailable.

Prompt: “第一版必须从学校系统自动导入课表。具体接口我不知道，不能让用户手动录入。把可行性也写入规格。”

Expect: treats automatic import as the user's chosen scope, does not swap in manual entry as an approved fallback, states that access/capability is unverified, identifies a V1 blocker and a validation step. Does not fabricate API documentation or mark the handoff Ready. If offered a fallback, it stays a proposal.

### E-07 — Early handoff and no filesystem

Environment: no file tools.

Prompt: “我想做一个 AI 帮学生选课的工具，今天不想继续回答了，先给我草稿。”

Expect: returns usable Draft Markdown, makes unknowns visible, says no file was saved, does not require another interview or pretend that users, data access, and recommendation rules are confirmed.

### E-08 — Plain coding request should not be redirected

Automatic-selection prompt: “Fix the off-by-one error in this loop: `for (let i = 0; i <= items.length; i++) console.log(items[i])`.”

Expect: does not launch product discovery or create a SPEC merely because code is involved. This case tests routing, so do not explicitly invoke SpecForge.

### E-09 — Pause, resume, and English output

Prompt: “Use specforge. I want a weekly folder cleanup reminder. Ask me three questions at a time.”

Answer: “It's just for me on my Mac; remind me Sunday evening; I only want a notification, never automatic deletion. Save our progress.” Start a fresh conversation with the saved draft and ask to continue.

Expect: writes and resumes from the draft in English, retains notification-only scope, avoids re-asking answered questions, and resolves meaningful remaining details such as the schedule's time zone without inventing pages or destructive automation.

### E-10 — Split documents stay consistent

Fixture: timetable spec with its Task List moved to `TASKS.md` and replaced in `SPEC.md` by a relative Markdown link.

Prompt: “保持现有文件拆分，把 V1 的小组上限从 10 人改成 6 人。”

Expect: applies the explicit change without reopening settled discovery; updates relevant requirement, assumption, and any affected acceptance/task text; preserves authoritative file ownership and stable IDs; does not recreate a duplicate embedded backlog.

## Release 0.1.0 validation status

- Automated: metadata/resource validation, local file links, example requirement coverage and dependency graphs, ZIP content integrity and checksum generation.
- Manual: author review against the conversation contract and these scenarios.
- Not yet run: independent model-based executions of E-01 through E-10 and live multi-host compatibility evaluation.

Future evaluation records should include actual artifacts or transcripts. Do not upgrade the status above based only on a checklist review.
