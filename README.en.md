# SpecForge

**Turn a rough idea into a `SPEC.md` a coding agent can act on.**

[中文](README.md) · [Skill](skills/specforge/SKILL.md) · [Example](examples/timetable/SPEC.md) · [Releases](https://github.com/GabrielMu2006/SpecForge/releases/latest)

SpecForge is an Agent skill for people who have a software idea but need help deciding what to build. It works as a product partner: asking focused questions, explaining tradeoffs, challenging scope, and making uncertainty visible before implementation.

> I want a website where friends share class schedules and find free time together.

The conversation develops that idea into positioning, users, core needs, V1, possible V2, relevant surfaces, flows, business rules, boundaries, a roadmap, and tasks with observable completion conditions.

## Workflow

1. Understand the problem and primary user.
2. Choose the first useful release and its exclusions.
3. Describe behavior, data ownership, and important failure cases.
4. Prepare requirements, acceptance criteria, and dependent tasks.

SpecForge asks up to three questions per turn and briefly recaps each stage. It skips answered questions and stops when the spec is ready. Reversible details can remain labeled assumptions; unresolved core value or V1 scope needs a decision unless explicitly delegated. External research is used only when consequential or requested, and missing research tools leave facts visibly unverified.

The default deliverable is one `SPEC.md`. Large backlogs may move to a linked `TASKS.md`. Existing specs can be revised without restarting discovery: changed requirements propagate to affected flows, acceptance, and tasks while IDs remain stable.

The workflow adapts to websites, apps, scripts, automations, plugins, and skills. Small tools do not acquire unnecessary pages, accounts, or release plans.

The first handoff anchors the core promise in concrete success/failure examples and names any validation work that blocks dependents. Interface products include key scenes, actions and information hierarchy. Proposed targets, adopted gates and measurements remain distinct through tasks and startup prompts; partial answers and the current planning assignment survive checkpoints.

## Install

The skill itself requires no Python runtime, API key, MCP server, or particular model. The host needs to read the skill and its supporting files. Research and filesystem capabilities are optional.

Download the [latest release](https://github.com/GabrielMu2006/SpecForge/releases/latest), extract it, and copy the **entire `specforge` folder** into the appropriate skill directory:

| Host | Personal directory | Invocation |
| --- | --- | --- |
| Codex | `~/.agents/skills/specforge/` | `$specforge Help me define my idea` |
| Claude Code | `~/.claude/skills/specforge/` | `/specforge Help me define my idea` |
| Other Agent Skills hosts | Use the host's documented location | Ask to use `specforge` |

Project locations are `.agents/skills/specforge/` for Codex and `.claude/skills/specforge/` for Claude Code. See the official [Codex](https://learn.chatgpt.com/docs/build-skills), [Claude Code](https://code.claude.com/docs/en/skills), and [Agent Skills](https://agentskills.io/specification) documentation. Compatibility is based on the format and documented installation paths; live multi-turn evaluations across hosts have not yet been completed.

Alternatively, run this from a directory where you keep your tools:

```sh
git clone https://github.com/GabrielMu2006/SpecForge.git
cd SpecForge
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/specforge" && cp -R skills/specforge "$HOME/.agents/skills/specforge"
```

For Claude Code, replace `.agents` with `.claude` in the last two lines. The copy is skipped if the destination already exists. Preserve local edits before replacing an installed version. Start a new agent session if the skill does not appear.

For a chat tool without native skills, provide `SKILL.md` and its linked supporting files, then ask the tool to follow the workflow. Without file tools, it can return Markdown for you to save.

## Use

Start from your intended product workspace:

```text
Use specforge. I want a website where friends share class schedules and
find free time together. I do not know how to code. Help me define V1.
```

To revise a spec:

```text
Use specforge to read SPEC.md. I want V1 to support friends at different
schools. Work out which rules and tasks need to change.
```

You can request a recommendation, save a draft, or pause at any point. The workflow uses your language. The skill defines the product; you separately instruct a coding agent to implement it.

## Examples and maintenance

The [timetable example](examples/timetable/SPEC.md) shows a complete collaboration flow. The [file organizer example](examples/file-organizer/SPEC.md) shows a small command-line tool. These Chinese examples are authored teaching fixtures with fictional selected conditions, not recorded user interviews or model evaluation results.

The installable skill lives in `skills/specforge/`. Its references cover interviewing, specification writing, and revisions; its asset is an adaptable template. Examples and evaluation scenarios stay outside the runtime bundle.

Maintainer tools require Python 3.9+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/check.py
.venv/bin/python scripts/package.py
```

Checks validate metadata, an explicit release manifest, Markdown local file links, sample graphs, and archive contents. Optional `scripts/check.py --spec PATH --tasks TASK_FILE` performs structural lint only; see [supported formats and limits](scripts/README.md). Python and parser libraries remain maintainer dependencies outside the runtime bundle.

These checks do not establish interview quality. The [18 behavioral scenarios](evals/README.md) separate historical observations from new forward executions; native multi-host behavior remains separately evaluated. Read [contribution guidance](CONTRIBUTING.md) before proposing changes.

Spec readiness is not evidence of market demand or working software. SpecForge leaves architecture and implementation details to the coding agent unless they are genuine product constraints.

[MIT licensed](LICENSE).
