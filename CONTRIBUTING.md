# Contributing

Improve decisions and observable behavior rather than adding a rule for every imaginable edge case. Keep the runtime skill portable, concise, and useful to nontechnical users.

## Making a change

1. Describe the concrete planning failure or use case. Use an issue for discussion when the intended behavior is unclear.
2. Change the relevant instruction or reference. Keep Chinese and English README behavior descriptions aligned.
3. Run `python -m unittest discover -s tests -v`, `python scripts/check.py` and `python scripts/package.py` in the development environment described in the README. Add negative regressions when changing validation or packaging. See [tool formats and limits](scripts/README.md).
4. When behavior changes, exercise the affected [evaluation scenarios](evals/README.md) in a fresh conversation. Record the host/model if known, inputs, actual outputs, and observed failures. Do not put private projects, account data, or credentials in public transcripts.
5. Explain the change and validation limits in your pull request. Do not claim live evaluations when only static checks or an author walkthrough were performed.

## Release bundle

The version in `skills/specforge/SKILL.md` is authoritative. Update it for a release, run the checks, and build the ZIP plus its SHA-256 checksum with `scripts/package.py`. Every runtime resource must be deliberately listed in `RUNTIME_FILES` in `scripts/check.py`; extra files, caches, directories and symlinks fail validation. The archive contains one top-level `specforge/` directory with the skill, its resources, and the MIT license; repository examples and development tools are not installed.

Publish a matching `vX.Y.Z` Git tag and attach both generated files to its GitHub release. Publish only after reviewing the actual diff and archive. CI runs static checks and packaging on pushes and pull requests; behavioral evaluation remains a separate activity.
