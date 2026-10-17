# Maintainer tools

These repository tools require `requirements-dev.txt` and Python 3.9+. They are not installed in the skill bundle and are not required to use SpecForge.

```sh
python -m unittest discover -s tests -v
python scripts/check.py
python scripts/package.py
python scripts/check.py --spec examples/timetable/SPEC.md
python scripts/check.py --spec evals/fixtures/split-spec/SPEC.md --tasks evals/fixtures/split-spec/TASKS.md
```

Repository validation checks runtime files against the explicit `RUNTIME_FILES` manifest in `check.py`, rejects extra files/directories and symlinks, checks metadata and used Markdown file links/images, and structurally checks teaching examples. Packaging uses the same manifest and refuses an output directory inside the skill. ZIP timestamps/order/modes are fixed; two builds are compared in tests within the same environment. Identical bytes across different zlib/Python implementations have not been established.

Markdown links use CommonMark parsing with table support, including inline, angle-bracket destinations with spaces, full/collapsed/shortcut references and images. Escaped/code examples are not links. Remote URL validity, heading anchors, raw HTML and unused reference definitions are outside the file-existence check.

## Optional specification lint

`--spec` reads only the selected spec and, if supplied, the explicit `--tasks` file. It does not follow arbitrary links, research facts or modify documents. Without `--tasks`, the spec itself owns tasks.

Supported structures:

- Requirement definitions beginning with `R-` and digits in Markdown headings or bold paragraphs, such as `### R-001 — Import` or `**R-001 — Import.**`.
- Pipe task tables with five columns (ID, goal, requirements, dependencies, done condition; status defaults to Planned), or six columns with an explicit status. A literal pipe inside a cell must be escaped.
- Heading task blocks with `Goal`, `Requirements`, `Depends on`, `Done when`, `Status` list fields. Chinese labels 目标、需求/覆盖需求、依赖、完成条件、状态 also work. The heading title may supply the goal. Required fields fit on one line; this is not a general Markdown schema parser.
- Explicit reference lists separated by spaces, commas, `、` or semicolons. Legacy ranges `R-001—R-003`, `T-001 至 T-003`, `T-001..T-003` (also en dash or hyphen) expand all intermediate IDs; missing IDs, reversed ranges and inconsistent padding fail. Prefer explicit IDs in new output. Dependencies may point to a higher-numbered ID; cycles/self-dependencies fail.
- No dependencies is `None`, `无`, `无依赖`, `-` or `—`. Blank is rejected.
- Statuses (case-insensitive English): Planned, In progress, Blocked, Complete, Needs revalidation, Removed, Superseded. Chinese equivalents: 计划中、进行中、阻塞、已完成、待复验、已移除、已替代. An explicit blank or unknown status fails; the tool never silently assigns a new meaning.

Fenced/indented code samples do not define requirements/tasks. Duplicate IDs, empty task fields, malformed/unknown references, uncovered declared requirements and cycles fail. Every declared R-ID in the selected input needs structural coverage, including any historical/deferred definitions supplied there. Lifecycle/release scope, retirement semantics, acceptance quality, target adoption and Ready/Draft correctness are not inferred. For a mixed archival document, supply an active-scope extract or review manually; a lint pass is not permission to implement or evidence of working software.
