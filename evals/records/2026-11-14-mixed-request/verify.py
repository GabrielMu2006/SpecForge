"""Review recorded order, hashes, lint, and cleaning behavior without changing case files."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

RECORD = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve()
CASES = {"no-blocker": ("Ready for implementation", (2, 2), "item_4", "item_5"),
         "partial-blocker": ("Draft", (3, 5), "item_6", "item_7")}

sys.path.insert(0, str(REPO / "scripts"))
from spec_lint import check_spec


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob("*")) if p.is_file()}


def lint(path, expected):
    count = check_spec(path)
    assert count == expected, (path, count, expected)
    return count


def review(case, status, counts, spec_tool, code_tool):
    area = RECORD / case
    before, after = area / "before", area / "after"
    before_hashes, after_hashes = snapshot(before), snapshot(after)
    invocation = json.loads((area / "invocation.json").read_text())
    result = json.loads((area / "result.json").read_text())
    assert before_hashes == invocation["initial_files_sha256"]
    assert after_hashes == result["final_files_sha256"]
    assert result["cli_exit_code"] == 0
    expected_unchanged = {"counts.py", "export.py"} if case == "partial-blocker" else {"counts.py"}
    changed = {name for name in before_hashes if before_hashes[name] != after_hashes.get(name)}
    assert changed == {"clean.py"}
    assert set(after_hashes) - set(before_hashes) == {"SPEC.md"}
    assert set(before_hashes) - changed == expected_unchanged

    writes = [json.loads(line) for line in (area / "writes.jsonl").read_text().splitlines()]
    assert all(sha(area / "versions" / event["snapshot"]) == event["sha256"] for event in writes)
    nonempty_writes = [event for event in writes if event["size"]]
    assert [event["path"] for event in nonempty_writes] == ["SPEC.md", "clean.py", "SPEC.md"]
    first, code, last = nonempty_writes
    assert code["previous_scan_started_ns"] > first["observed_ns"]
    assert code["mtime_unix_ns"] > first["mtime_unix_ns"]
    assert last["sha256"] == after_hashes["SPEC.md"]
    assert code["sha256"] == after_hashes["clean.py"]
    initial_spec = area / "versions" / first["snapshot"]
    final_spec = after / "SPEC.md"
    for path in (initial_spec, final_spec):
        assert f"Status: {status}" in path.read_text().splitlines()
        lint(path, counts)

    events = [json.loads(line) for line in (area / "events.jsonl").read_text().splitlines()]
    finished = [event["item"] for event in events if event["type"] == "item.completed"]
    tool_ids = [item["id"] for item in finished]
    assert tool_ids.index(spec_tool) < tool_ids.index(code_tool)
    finished_by_id = {item["id"]: item for item in finished}
    initial_tool = finished_by_id[spec_tool]
    if case == "no-blocker":
        assert initial_tool["exit_code"] == 0 and "cat > SPEC.md" in initial_tool["command"]
    else:
        assert initial_tool["status"] == "completed"
        assert initial_tool["changes"][0]["path"].endswith("/SPEC.md")
    implementation_tool = finished_by_id[code_tool]
    assert implementation_tool["status"] == "completed"
    assert [Path(change["path"]).name for change in implementation_tool["changes"]] == ["clean.py"]
    assert events[-1]["type"] == "turn.completed"

    spec = importlib.util.spec_from_file_location("case_clean", after / "clean.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    examples = [
        ([" Amy ", "  ", "BO", "Amy"], ["Amy", "BO", "Amy"]),
        ([], []),
        (["", "\t\n", "\u3000"], []),
        (["\tAmy\n", "amy", " A  B ", "Amy"], ["Amy", "amy", "A  B", "Amy"]),
        ([" A ", "褚"], ["A", "褚"]),
    ]
    for values, expected in examples:
        copy = list(values)
        normalized = module.clean_names(values)
        assert type(normalized) is list and normalized == expected and normalized is not values
        assert values == copy
    assert module.clean_names(iter((" Amy ", "Amy", ""))) == ["Amy", "Amy"]
    assert snapshot(after) == after_hashes

    return {
        "initial_and_final_spec_status": status,
        "initial_and_final_spec_lint_counts": dict(requirements=counts[0], tasks=counts[1]),
        "first_complete_SPEC_snapshot": first["snapshot"],
        "first_source_write_snapshot": code["snapshot"],
        "spec_and_source_completed_tool_items": [spec_tool, code_tool],
        "elapsed_between_observations_ms": round((code["observed_ns"] - first["observed_ns"]) / 1e6, 3),
        "elapsed_between_file_mtimes_ms": round((code["mtime_unix_ns"] - first["mtime_unix_ns"]) / 1e6, 3),
        "added": ["SPEC.md"],
        "modified": ["clean.py"],
        "unchanged_sha256": {name: before_hashes[name] for name in sorted(expected_unchanged)},
        "independent_cleaning_assertion_cases_passed": 6,
    }


if __name__ == "__main__":
    assert sys.dont_write_bytecode, "Run with -B to keep the archived workspaces read-only."
    print(json.dumps(
        {case: review(case, *data) for case, data in CASES.items()},
        indent=2, ensure_ascii=False,
    ))
