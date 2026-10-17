#!/usr/bin/env python3
"""Validate the repository/bundle, or structurally lint explicitly selected specs."""

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt

from spec_lint import check_spec

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "specforge"
# One reviewed manifest drives validation and packaging.
RUNTIME_FILES = (
    "LICENSE", "SKILL.md", "agents/openai.yaml", "assets/SPEC.template.md",
    "references/interview.md", "references/revisions.md",
    "references/specification.md",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_metadata():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    require(match is not None, "SKILL.md must start with YAML frontmatter")
    metadata = yaml.safe_load(match.group(1))
    require(isinstance(metadata, dict), "Frontmatter must be a mapping")
    require(metadata.get("name") == SKILL.name, "Skill name must match its folder")
    description = metadata.get("description")
    require(isinstance(description, str) and 0 < len(description) <= 1024,
            "Description must be a nonempty string of at most 1024 characters")
    require(metadata.get("license") == "MIT", "Expected MIT license metadata")
    details = metadata.get("metadata")
    require(isinstance(details, dict), "metadata must be a mapping")
    version = details.get("version")
    require(isinstance(version, str) and re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version),
            "Version must be a quoted X.Y.Z string")
    require("[TODO:" not in text, "Unfinished skill scaffold")
    return metadata


def check_runtime_files():
    require(not SKILL.is_symlink(), "Do not distribute a symlinked skill root")
    allowed_dirs = {parent.as_posix() for name in RUNTIME_FILES
                    for parent in Path(name).parents if parent != Path(".")}
    for name in RUNTIME_FILES:
        require((SKILL / name).is_file(), f"Missing runtime file: {name}")
    for path in SKILL.rglob("*"):
        name = path.relative_to(SKILL).as_posix()
        require(not path.is_symlink(), f"Do not distribute symlinks: {name}")
        require((path.is_dir() and name in allowed_dirs) or
                (path.is_file() and name in RUNTIME_FILES),
                f"Unexpected runtime entry (not in release manifest): {name}")


def inline_tokens(tokens):
    for token in tokens:
        yield token
        yield from inline_tokens(token.children or [])


def check_links(paths, boundary):
    """Check rendered Markdown file links/images, including reference syntax.

    Code samples, raw HTML, unused definitions, remote URLs and heading fragments
    are outside this file-existence check. No network requests are made.
    """
    boundary = boundary.resolve()
    parser = MarkdownIt("commonmark").enable("table")
    count = 0
    for path in paths:
        for token in inline_tokens(parser.parse(path.read_text(encoding="utf-8"))):
            target = (token.attrGet("href") if token.type == "link_open" else
                      token.attrGet("src") if token.type == "image" else None)
            if not target:
                continue
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            local = (path.parent / unquote(parsed.path)).resolve()
            require(local == boundary or boundary in local.parents,
                    f"Link escapes distribution root: {path}: {target}")
            require(local.exists(), f"Broken local link: {path}: {target}")
            count += 1
    return count


def check_example(path):
    return check_spec(path)


def validate():
    check_runtime_files()
    metadata = read_metadata()
    require((SKILL / "LICENSE").read_bytes() == (ROOT / "LICENSE").read_bytes(),
            "Runtime and repository licenses differ")
    ui = yaml.safe_load((SKILL / "agents/openai.yaml").read_text(encoding="utf-8"))
    require(isinstance(ui, dict) and isinstance(ui.get("interface"), dict),
            "UI metadata must contain an interface mapping")
    interface = ui["interface"]
    description = interface.get("short_description")
    require(isinstance(description, str) and 25 <= len(description) <= 64,
            "UI short description must be 25–64 characters")
    prompt = interface.get("default_prompt")
    require(isinstance(prompt, str) and "$specforge" in prompt,
            "UI prompt must name the skill")
    policy = ui.get("policy", {})
    require(isinstance(policy, dict) and policy.get("allow_implicit_invocation", True) is True,
            "Automatic discovery should remain enabled")
    runtime_links = check_links(SKILL.rglob("*.md"), SKILL)
    docs = list(ROOT.glob("*.md"))
    for directory in ("examples", "evals"):
        docs.extend((ROOT / directory).rglob("*.md"))
    repo_links = check_links(docs, ROOT)
    counts = [check_example(path) for path in sorted((ROOT / "examples").glob("*/SPEC.md"))]
    require(len(counts) >= 2, "Expected app and small-tool examples")
    print(f"SpecForge {metadata['metadata']['version']}: metadata and resources valid")
    print(f"Local file links: {runtime_links} runtime, {repo_links} repository")
    print(f"Examples: {sum(c[0] for c in counts)} requirements, "
          f"{sum(c[1] for c in counts)} tasks; coverage and dependency graphs valid")
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, help="Lint one spec instead of the repository")
    parser.add_argument("--tasks", type=Path, help="Explicit authoritative task file for --spec")
    args = parser.parse_args()
    if args.tasks and not args.spec:
        parser.error("--tasks requires --spec")
    if args.spec:
        requirements, tasks = check_spec(args.spec, args.tasks)
        print(f"Structure valid: {requirements} requirements, {tasks} tasks; "
              "prose, readiness and implementation remain unverified")
    else:
        validate()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, yaml.YAMLError) as error:
        raise SystemExit(f"Check failed: {error}")
