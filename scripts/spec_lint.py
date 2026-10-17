"""Optional structural lint for the documented SPEC/task subset; no prose scoring."""

import re

from markdown_it import MarkdownIt

STATUSES = {
    "planned", "in progress", "blocked", "complete", "needs revalidation",
    "removed", "superseded", "计划中", "进行中", "阻塞", "已完成", "待复验",
    "已移除", "已替代",
}
NONE = {"none", "无", "无依赖", "-", "—"}
LABELS = {
    "goal": "goal", "目标": "goal",
    "requirements": "refs", "需求": "refs", "覆盖需求": "refs",
    "depends on": "depends", "依赖": "depends",
    "done when": "done", "完成条件": "done",
    "status": "status", "状态": "status",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def plain(parser, text):
    return "".join(token.content for root in parser.parseInline(text)
                   for token in (root.children or [])
                   if token.type in {"text", "code_inline", "softbreak"}).strip()


def document(path):
    parser = MarkdownIt("commonmark").enable("table")
    lines = path.read_text(encoding="utf-8").splitlines()
    tokens = parser.parse("\n".join(lines))
    for token in tokens:
        if token.type in {"fence", "code_block", "html_block"} and token.map:
            for index in range(*token.map):
                lines[index] = ""
    return parser, lines, tokens


def split_row(line):
    cells, cell, escaped = [], [], False
    for char in line.strip():
        if char == "|" and not escaped:
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(char)
        escaped = char == "\\" and not escaped
    cells.append("".join(cell).strip())
    if cells and not cells[0]:
        cells.pop(0)
    if cells and not cells[-1]:
        cells.pop()
    return cells


def references(value, prefix, known, allow_none, context):
    if allow_none and value.strip().casefold() in NONE:
        return set()
    require(value.strip(), f"Missing {prefix} references: {context}")
    pattern = re.compile(rf"({prefix}-[0-9]+)(?:\s*(?:—|–|\.\.|至|到|-)\s*({prefix}-[0-9]+))?")
    result, end = set(), 0
    for match in pattern.finditer(value):
        gap = value[end:match.start()]
        require((not gap and end == 0) or
                bool(re.fullmatch(r"[\s,，、;；]+", gap)),
                f"Malformed {prefix} references: {context}: {value}")
        first, last = match.groups()
        ids = [first]
        if last:
            start, finish = first.split("-")[1], last.split("-")[1]
            require(len(start) == len(finish) and int(start) <= int(finish),
                    f"Invalid reference range: {context}: {match.group()}")
            ids = (f"{prefix}-{number:0{len(start)}d}"
                   for number in range(int(start), int(finish) + 1))
        for identifier in ids:
            require(identifier in known, f"Unknown reference {identifier}: {context}")
            result.add(identifier)
        end = match.end()
    require(result and not value[end:].strip(" \t,，、;；"),
            f"Malformed {prefix} references: {context}: {value}")
    return result


def check_spec(path, task_path=None):
    parser, _, tokens = document(path)
    requirements = set()
    for index, token in enumerate(tokens[:-1]):
        inline = tokens[index + 1]
        if inline.type != "inline":
            continue
        is_definition = token.type == "heading_open" or (
            token.type == "paragraph_open" and
            re.match(r"^(?:\*\*|__)R[-_ ]?[0-9]", inline.content))
        if not is_definition:
            continue
        title = plain(parser, inline.content)
        match = re.match(r"^(R-[0-9]+)\b", title)
        if not match:
            require(not re.match(r"^R[-_ ]?[0-9]", title), f"Malformed requirement ID: {title}")
            continue
        identifier = match.group(1)
        require(identifier not in requirements, f"Duplicate requirement ID: {identifier}")
        requirements.add(identifier)
    require(requirements, f"No requirements found: {path}")

    tasks_file = task_path or path
    parser, lines, tokens = document(tasks_file)
    tasks = {}

    def add(identifier, fields):
        require(re.fullmatch(r"T-[0-9]+", identifier), f"Malformed task ID: {identifier}")
        require(identifier not in tasks, f"Duplicate task: {identifier}")
        for field in ("goal", "refs", "depends", "done"):
            require(fields.get(field, "").strip(), f"Missing task {field}: {identifier}")
        status = fields.get("status", "Planned")
        require(status.casefold() in STATUSES, f"Unknown task status: {identifier}: {status}")
        tasks[identifier] = fields

    for line in lines:
        if not line.lstrip().startswith("|"):
            continue
        cells = [plain(parser, cell) for cell in split_row(line)]
        if not cells or not re.match(r"^T(?:[-_ ]|[0-9])", cells[0]):
            continue
        require(len(cells) in {5, 6}, f"Malformed task row: {line}")
        identifier, goal, refs, depends, done = cells[:5]
        fields = dict(goal=goal, refs=refs, depends=depends, done=done)
        if len(cells) == 6:
            fields["status"] = cells[5]
        add(identifier, fields)

    headings = [(token.map[0], index) for index, token in enumerate(tokens)
                if token.type == "heading_open"]
    for position, (start, index) in enumerate(headings):
        title = plain(parser, tokens[index + 1].content)
        match = re.match(r"^(T-[0-9]+)\b", title)
        if not match:
            require(not re.match(r"^T[-_ ]?[0-9]", title), f"Malformed task ID: {title}")
            continue
        stop = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        fields = {"goal": title[match.end():].lstrip(" —–:-")}
        for line in lines[start + 1:stop]:
            field = re.match(r"^\s*[-*]\s+([^:：]+)[:：]\s*(.*)$", line)
            if field:
                label = LABELS.get(plain(parser, field[1]).casefold())
                if label:
                    require(label not in fields or label == "goal",
                            f"Duplicate task field: {match[1]}: {label}")
                    fields[label] = plain(parser, field[2])
        add(match[1], fields)

    require(tasks, f"No supported tasks found: {tasks_file}")
    covered, graph = set(), {}
    for identifier, fields in tasks.items():
        covered.update(references(fields["refs"], "R", requirements, False, identifier))
        graph[identifier] = references(fields["depends"], "T", tasks, True, identifier)
    require(covered == requirements, f"Uncovered requirements: {sorted(requirements - covered)}")
    visited, visiting = set(), set()

    def visit(identifier):
        require(identifier not in visiting, f"Dependency cycle at {identifier}")
        if identifier in visited:
            return
        visiting.add(identifier)
        for dependency in graph[identifier]:
            visit(dependency)
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in tasks:
        visit(identifier)
    return len(requirements), len(tasks)
