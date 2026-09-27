#!/usr/bin/env python3
"""Check distributable skill metadata, local links, and example task graphs."""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "specforge"


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
    version = metadata.get("metadata", {}).get("version", "")
    require(isinstance(version, str) and re.fullmatch(r"\d+\.\d+\.\d+", version),
            "Version must be a quoted X.Y.Z string")
    require("[TODO:" not in text, "Unfinished skill scaffold")
    return metadata


def check_links(paths, boundary):
    boundary = boundary.resolve()
    count = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]\n]+\]\(([^\s)]+)\)", text):
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
    """Validate IDs, requirement coverage, and task dependencies, not prose quality."""
    text = path.read_text(encoding="utf-8")
    requirement_ids = re.findall(r"^### (R-\d+)\b", text, re.M)
    require(len(requirement_ids) == len(set(requirement_ids)),
            f"Duplicate requirement IDs: {path}")
    requirements = set(requirement_ids)
    require(requirements, f"No requirements found in example: {path}")
    tasks = {}
    covered = set()
    for line in text.splitlines():
        if not re.match(r"^\| T-\d+\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        require(len(cells) == 6, f"Malformed example task row: {line}")
        task_id, _, refs, depends, done, status = cells
        require(task_id not in tasks, f"Duplicate task: {task_id}")
        refs = set(re.findall(r"R-\d+", refs))
        require(refs and refs <= requirements, f"Unknown/missing requirements: {task_id}")
        require(done and status, f"Missing task completion/status: {task_id}")
        covered.update(refs)
        tasks[task_id] = set(re.findall(r"T-\d+", depends))
    require(covered == requirements, f"Uncovered requirements: {requirements - covered}")
    visited = set()

    def visit(task_id, stack):
        require(task_id in tasks, f"Unknown dependency: {task_id}")
        require(task_id not in stack, f"Dependency cycle at {task_id}")
        if task_id in visited:
            return
        for dependency in tasks[task_id]:
            visit(dependency, stack | {task_id})
        visited.add(task_id)

    for task_id in tasks:
        visit(task_id, set())
    return len(requirements), len(tasks)


def validate():
    metadata = read_metadata()
    required = ["SKILL.md", "LICENSE", "agents/openai.yaml",
                "references/interview.md", "references/specification.md",
                "references/revisions.md", "assets/SPEC.template.md"]
    for name in required:
        require((SKILL / name).is_file(), f"Missing runtime file: {name}")
    for path in SKILL.rglob("*"):
        require(not path.is_symlink(), f"Do not distribute symlinks: {path}")
        require(not path.name.startswith("."), f"Unexpected hidden runtime file: {path}")
    require((SKILL / "LICENSE").read_bytes() == (ROOT / "LICENSE").read_bytes(),
            "Runtime and repository licenses differ")
    ui = yaml.safe_load((SKILL / "agents/openai.yaml").read_text(encoding="utf-8"))
    interface = ui["interface"]
    require(25 <= len(interface["short_description"]) <= 64,
            "UI short description must be 25–64 characters")
    require("$specforge" in interface["default_prompt"], "UI prompt must name the skill")
    require(ui.get("policy", {}).get("allow_implicit_invocation", True) is True,
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


if __name__ == "__main__":
    try:
        validate()
    except (ValueError, KeyError, TypeError, OSError, yaml.YAMLError) as error:
        raise SystemExit(f"Check failed: {error}")
