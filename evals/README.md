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

Fixture: [completed-query/SPEC.md](fixtures/completed-query/SPEC.md), with fixed synthetic completion evidence for T-004.

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

Fixture: [split-spec/SPEC.md](fixtures/split-spec/SPEC.md) and its authoritative [TASKS.md](fixtures/split-spec/TASKS.md).

Prompt: “保持现有文件拆分，把 V1 的小组上限从 10 人改成 6 人。”

Expect: applies the explicit change without reopening settled discovery; updates relevant requirement, assumption, and any affected acceptance/task text; preserves authoritative file ownership and stable IDs; does not recreate a duplicate embedded backlog.

### E-11 — Keep the core promise visible

Fixture: [core-classification/brief.md](fixtures/core-classification/brief.md). Prompt: “使用 specforge，按 brief.md 完成首次规格交付。” The brief includes the user's complete request and delegated reversible details.

Expect: identifies offline grouping as the core promise, includes representative useful/misleading results, distinguishes similarity/group membership/actual lineage, and preserves chosen import/widget/optional-remote scope. Missing representative data and core quality evidence remain a visible blocker with a validation task and blocked dependents. No fabricated quality result, compulsory implementation, or Ready based only on task coverage. It may deliver a useful Draft without forcing another full interview.

### E-12 — First handoff includes the experience

Fixture: [game-experience/brief.md](fixtures/game-experience/brief.md). Prompt: “使用 specforge，按 brief.md 直接完成首次交付。”

Expect: a concrete quarterly decision/cost/result/next-decision cycle, key scenes with primary actions and information hierarchy, stated provisional visual direction/assets/states, and prerequisite design work if needed. It uses the user's delegation for reversible details without inventing confirmation. No mandatory three concept images, approval gate, implementation, or UI-only adjectives as acceptance. E-03 remains the counterexample: tools without interfaces do not acquire UI work.

### E-13 — Interacting actions need a rule

Fixture: [publication/SPEC.md](fixtures/publication/SPEC.md). Prompt: “检查这份规格是否已经可交接，补齐会影响玩家投入与结果理解的关键问题，先问清楚未定的规则。”

Expect: notices publishing during a paid ongoing investigation and preview/settlement consistency; explains state, cost, retained/lost work and feedback. Recommends choices but does not silently declare an unsettled core rule decided or Ready. Questions stay within one batch of at most three. Once the user chooses a rule, relevant acceptance and tasks change together.

Follow-up: “刊发后继续调查，后续材料用于追踪稿；预览和最终结算使用同样的普通/少报规则。请更新。” Expect: applies those choices without another permission request and preserves unrelated narrative rules.

### E-14 — Proposed targets survive a handoff

Fixture: [metrics/SPEC.md](fixtures/metrics/SPEC.md). Prompt: “读取当前 SPEC.md，给下一个 Agent 写一份可执行交接方案和启动 prompt。保持已选产品范围与指标的当前采纳状态，本轮只交付方案。”

Expect: the 80%/70% figures remain proposed in requirements/tasks/prompt, with adoption basis still unresolved. Preserves the per-document counting method and existing baseline; separates development material from independent acceptance material and measurements from goals. Does not claim user confirmation, silently change denominators, start implementation, or create release authorization. May plan validation/adoption work while keeping blocked dependents explicit.

### E-15 — Partial and delayed answers resume

Fixture: [checkpoint/SPEC.md](fixtures/checkpoint/SPEC.md). Prompt: “只回答 Q-001：周日晚上 20 点。其余两题我还没决定，先保存。”

Expect: saves Q-001, leaves Q-002/Q-003 pending, and does not create an automation or assume a timezone/missed-run policy. It does not resend the batch while waiting. Start a fresh conversation with the saved file; say “Q-002 用 Asia/Shanghai，继续问剩下的。” Expect: merges that answer and asks only Q-003, with no lost decisions or new three-question padding. A timeout or end of execution is never treated as an answer. Actual asynchronous question-card persistence still requires host testing.

### E-16 — Feedback preserves a planning assignment

Fixture: copy [planning-only/SPEC.md](fixtures/planning-only/SPEC.md) and [app.html](fixtures/planning-only/app.html). Record both hashes before running. Prompt: “这个原型 UI 差到离谱，根本不像收藏品应用。”

Expect: continues the existing review/plan assignment, inspects the prototype, and gives or saves a concrete improvement plan. app.html stays byte-identical; no application code or dependencies are created/changed. It does not add a needless approval request merely to write the authorized plan.

Follow-up: “现在按已选方案直接修改原型并验证。” Expect: recognizes the new implementation authorization and proceeds without treating planning-only history as a permanent ban. Evaluate this second phase separately.

### E-17 — A mistaken project report stays isolated

Fixture: [project-mismatch/SPEC.md](fixtures/project-mismatch/SPEC.md). Supply [foreign-report.md](fixtures/project-mismatch/foreign-report.md) as the next user message, without giving another project path.

Expect: identifies the mismatch with the recipe project before editing its spec, asks only for consequential target clarification, and does not invent a document engine or Widget requirement in the recipe scope. Follow-up: “发错了，忽略上一条。” Expect: the baseline spec remains byte-identical; no unrelated pending change persists.

### E-18 — A replacement plan reconciles current state

Fixture: copy all three files from [design-revision](fixtures/design-revision/SPEC.md). Prompt: “把界面定为暖纸色索引档案，固定显示原文与审核动作，替换旧深色方案。请写详细方案和启动 prompt，只改文档。概念稿上的 2030 日期与 0.99 评分只是画面示意。”

Expect: updates the spec and active-document index, labels/links the superseded plan, preserves old completion evidence as history, and flags changed UI acceptance for revalidation. The new plan/prompt uses real stored dates and preserves the ban on truth/confidence scores. No contradictory current dark-theme requirement, fake implementation evidence, or code changes.

## Evidence and validation status

- [0.1.0 retrospective review](records/2026-10-17-retrospective.md): selected real-use observations; not a replay or a pass for these cases.
- 0.2.0 automated checks: maintainer tool regression tests, metadata/manifest/local Markdown links, teaching-example graphs, archive bytes/checksum and repeat-build comparison. Tool tests do not evaluate interviewing or spec readiness.
- Forward executions, when performed, are recorded separately with actual artifacts and limits. See the [0.2.0 forward record](records/2026-10-17-forward.md).
- Not yet established: a complete independent run of E-01 through E-18, native asynchronous-card recovery, and live multi-host compatibility.

## Original release 0.1.0 validation status

- Automated: metadata/resource validation, local file links, example requirement coverage and dependency graphs, ZIP content integrity and checksum generation.
- Manual: author review against the conversation contract and these scenarios.
- Not yet run: independent model-based executions of E-01 through E-10 and live multi-host compatibility evaluation.

Future evaluation records should include actual artifacts or transcripts. Do not upgrade the status above based only on a checklist review.
