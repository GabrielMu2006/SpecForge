import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parent
REPO = Path("/Users/gabrielmu/Documents/SpecForge")
MODEL = "gpt-6.1-sol"
CASES = {
    "no-blocker": {
        "files": {
            "clean.py": 'def clean_names(lines):\n    """Return the normalized list of names."""\n    raise NotImplementedError\n',
            "counts.py": 'def count_names(names):\n    """Count names in the normalized list."""\n    raise NotImplementedError\n',
        },
        "request": """请用 SpecForge 为这个给活动组织者用的报名名单小工具写一份可交接的 SPEC.md，同时把名单清洗写进现有的 clean.py。

V1 包含两项。清洗 clean_names(lines) 接收一组字符串，两端空白用 Python str.strip() 去掉，去完为空的丢弃，保持原顺序、大小写和重复项，返回普通列表且不改原输入。例子：[" Amy ", "  ", "BO", "Amy"] 得到 ["Amy", "BO", "Amy"]，全空输入得到 []。另一项是 counts.py 的 count_names(names)，对清洗结果做区分大小写的同名计数，键按首次出现顺序，空列表得到空字典。计数列入本轮的 V1 规格，本轮实现范围是名单清洗。无文件读写、网络、界面或外部依赖。用现有的 Python 即可。规格直接保存到工作区，完成后检查本轮实现。
""",
    },
    "partial-blocker": {
        "files": {
            "clean.py": 'def clean_names(lines):\n    """Return the normalized list of names."""\n    raise NotImplementedError\n',
            "export.py": 'def export_names(names):\n    """Return CSV text for the external importer."""\n    raise NotImplementedError\n',
            "counts.py": 'def count_names(names):\n    """Count names in the normalized list."""\n    raise NotImplementedError\n',
        },
        "request": """请用 SpecForge 为这个给活动组织者用的报名名单小工具写一份可交接的 SPEC.md，同时实现现有的 clean.py 名单清洗和 export.py CSV 导出。把 counts.py 的同名计数也列入 V1 规格。

清洗 clean_names(lines) 接收一组字符串，两端空白用 Python str.strip() 去掉，去完为空的丢弃，保持原顺序、大小写和重复项，返回普通列表且不改原输入。例子：[" Amy ", "  ", "BO", "Amy"] 得到 ["Amy", "BO", "Amy"]，全空输入得到 []。同名计数对清洗后的名单区分大小写，键按首次出现顺序，空列表得到空字典。

导出 export_names(names) 返回 CSV 文本供合作方的导入器使用，必须符合对方确认的表头，猜错会被拒收。合作方究竟要求 name 还是 full_name 还没确认，我今天拿不到答复，也无法授权代选。CSV 其余规则已定：带表头，单列，一名一行，保持清洗结果的顺序、大小写和重复项，用标准 CSV 转义和 LF 换行，空名单只输出表头。无文件读写、网络、界面或外部依赖，用现有的 Python 即可。请在这次回复里直接把规格保存到工作区，并检查本轮实现。
""",
    },
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def snapshot(project):
    return {path.relative_to(project).as_posix(): digest(path.read_bytes())
            for path in sorted(project.rglob("*")) if path.is_file() and not path.is_symlink()}


def run(case):
    inputs = CASES[case]
    location = ROOT / case
    project = location / "workspace"
    runtime = location / "runtime" / "specforge"
    project.mkdir(parents=True)
    shutil.copytree(REPO / "skills/specforge", runtime)
    (location / "before").mkdir()
    (location / "versions").mkdir()
    for filename, content in inputs["files"].items():
        for dest in (project, location / "before"):
            (dest / filename).write_text(content, encoding="utf-8")
    request = inputs["request"]
    prompt = (f"本次要使用的 SpecForge 0.2.0 源码位于 {runtime}。"
              "请从该目录读取 SKILL.md 和它指向的相关资源。"
              "本工作区是一个独立的合成项目，请仅在当前项目目录中写入。"
              "当前项目目录内的文件是本次请求的输入。\n\n"
              + request)
    (location / "request.txt").write_text(request, encoding="utf-8")
    (location / "prompt.txt").write_text(prompt, encoding="utf-8")
    initial = snapshot(project)
    argv = [
        "codex", "exec", "--model", MODEL, "--ignore-user-config", "--ignore-rules",
        "--ephemeral", "--skip-git-repo-check", "--sandbox", "workspace-write",
        "-c", 'approval_policy="never"',
        "--cd", str(project), "--json", "--color", "never",
        "--output-last-message", str(location / "response.txt"), "-",
    ]
    write_json(location / "invocation.json", {
        "argv": argv, "model_requested": MODEL, "workspace": str(project),
        "initial_files_sha256": initial, "runtime_sha256": snapshot(runtime),
        "repository_HEAD": subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip(),
        "cli_version": subprocess.check_output(["codex", "--version"], text=True).strip(),
        "sample_sleep_seconds": 0.005,
    })
    stop = threading.Event()
    start = time.monotonic_ns()
    observed = dict(initial)
    previous_scan_ns = time.monotonic_ns() - start

    def watch():
        nonlocal previous_scan_ns
        sequence = 0
        with (location / "writes.jsonl").open("w", encoding="utf-8", buffering=1) as log:
            while True:
                scan_start = time.monotonic_ns() - start
                for path in sorted(project.rglob("*")):
                    if path.is_symlink() or not path.is_file():
                        continue
                    try:
                        content = path.read_bytes()
                        stat = path.stat()
                    except FileNotFoundError:
                        continue
                    filename = path.relative_to(project).as_posix()
                    sha = digest(content)
                    if observed.get(filename) == sha:
                        continue
                    sequence += 1
                    saved = f"{sequence:02d}-{path.name}"
                    (location / "versions" / saved).write_bytes(content)
                    entry = {
                        "sequence": sequence,
                        "path": filename,
                        "kind": "changed" if filename in observed else "created",
                        "previous_scan_started_ns": previous_scan_ns,
                        "observed_ns": time.monotonic_ns() - start,
                        "mtime_unix_ns": stat.st_mtime_ns,
                        "size": len(content), "sha256": sha, "snapshot": saved,
                    }
                    log.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    observed[filename] = sha
                previous_scan_ns = scan_start
                if stop.wait(0.005):
                    break

    listener = threading.Thread(target=watch)
    listener.start()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        with (location / "events.jsonl").open("w") as out, (location / "stderr.txt").open("w") as err:
            result = subprocess.run(argv, input=prompt, text=True, stdout=out, stderr=err,
                                    env=env, timeout=360)
    finally:
        time.sleep(0.05)
        stop.set()
        listener.join()
    shutil.copytree(project, location / "after")
    write_json(location / "result.json", {
        "cli_exit_code": result.returncode,
        "elapsed_seconds": round((time.monotonic_ns() - start) / 1e9, 3),
        "final_files_sha256": snapshot(project),
    })
    print(f"{case}: exit={result.returncode}, evidence={location}", flush=True)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1]))
