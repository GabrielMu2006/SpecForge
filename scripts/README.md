# Maintainer tools

These repository tools require `requirements-dev.txt` and Python 3.9+. They are not installed in the skill bundle and are not required to use SpecForge.

```sh
python -m unittest discover -s tests -v
python scripts/check.py
python scripts/package.py
python scripts/check.py --spec examples/timetable/SPEC.md
python scripts/check.py --spec evals/fixtures/split-spec/SPEC.md --tasks evals/fixtures/split-spec/TASKS.md
```

Repository validation checks runtime files against the explicit `RUNTIME_FILES` manifest in `check.py`, rejects extra files/directories and symlinks, checks metadata and used Markdown file links/images, and structurally checks teaching examples. The Codex metadata must explicitly set `policy.allow_implicit_invocation` to the boolean `true`. Packaging uses the same manifest and refuses an output directory inside the skill. ZIP timestamps/order/modes are fixed; two builds are compared in tests within the same environment. Identical bytes across different zlib/Python implementations have not been established.

Markdown links use CommonMark parsing with table support, including inline, angle-bracket destinations with spaces, full/collapsed/shortcut references and images. Escaped/code examples are not links. Remote URL validity, heading anchors, raw HTML and unused reference definitions are outside the file-existence check.

## Optional specification lint

`--spec` reads only the selected spec and, if supplied, the explicit `--tasks` file. It does not follow arbitrary links, research facts or modify documents. Without `--tasks`, the spec itself owns tasks.

Supported structures:

- Requirement definitions beginning with `R-` and digits in Markdown headings or bold paragraphs, such as `### R-001 — Import` or `**R-001 — Import.**`. Leave a blank line before a bold definition after prose so CommonMark starts a new paragraph.
- A requirement title ending in `(Removed)`, `(Superseded)`, `（已移除）` or `（已替代）` keeps its ID available for references and is exempt from task coverage. Either pair of parentheses works with all four labels. In a bold paragraph, put the marker inside the bold title. A final period is allowed after the marker.
- Pipe task tables with five columns (ID, goal, requirements, dependencies, done condition; status defaults to Planned), or six columns with an explicit status. A literal pipe inside a cell must be escaped.
- Heading task blocks with `Goal`, `Requirements`, `Depends on`, `Done when`, `Status` list fields. Chinese labels 目标、需求/覆盖需求、依赖、完成条件、状态 also work. The heading title may supply the goal. Required fields fit on one line; this is not a general Markdown schema parser.
- Explicit reference lists separated by spaces, commas, `、` or semicolons. Legacy ranges `R-001—R-003`, `T-001 至 T-003`, `T-001..T-003` (also en dash or hyphen) expand all intermediate IDs; missing IDs, reversed ranges and inconsistent padding fail. Prefer explicit IDs in new output. Dependencies may point to a higher-numbered ID; cycles/self-dependencies fail.
- No dependencies is `None`, `无`, `无依赖`, `-` or `—`. Blank is rejected.
- English statuses are Planned, In progress, Blocked, Complete, Needs revalidation, Removed and Superseded, matched case-insensitively. Chinese equivalents are 计划中、进行中、阻塞、已完成、待复验、已移除、已替代. The status must match in full before `;`, `；`, `—`, `–` or a hyphen surrounded by spaces. For example, `Complete; see VERIFY.md` is valid. A blank or unknown status fails even when followed by a note.

Fenced/indented code samples do not define requirements/tasks. Duplicate IDs, empty task fields, malformed/unknown references and cycles fail. Every declared R-ID without an explicit retirement marker needs coverage, including deferred definitions. A spec containing only explicitly retired requirements can pass with zero tasks. Lifecycle/release scope, acceptance quality, target adoption and Ready/Draft correctness are not inferred. For a mixed archival document, supply an active-scope extract or review manually; a lint pass is not permission to implement or evidence of working software.
