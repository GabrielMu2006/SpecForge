"""Regression tests for observable lint, link, manifest, and archive behavior."""

import contextlib
import hashlib
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import check
import package
from spec_lint import check_spec

SPEC = """# Example

### R-001 — Import
Preserve the original.

### R-002 — Review
Confirm before changing membership.

| ID | Goal | Requirements | Depends on | Done when | Status |
| --- | --- | --- | --- | --- | --- |
| T-001 | Import | R-001 | None | Original is unchanged | Planned |
| T-002 | Review | R-002 | T-001 | Membership needs confirmation | Planned |
"""


class SpecTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "SPEC.md"

    def lint(self, text=SPEC):
        self.path.write_text(text, encoding="utf-8")
        return check_spec(self.path)

    def reject(self, text, message):
        with self.assertRaisesRegex(ValueError, message):
            self.lint(text)

    def test_existing_teaching_examples(self):
        self.assertEqual(check_spec(REPO / "examples/timetable/SPEC.md"), (5, 7))
        self.assertEqual(check_spec(REPO / "examples/file-organizer/SPEC.md"), (2, 2))

    def test_bold_requirements_and_five_column_tasks(self):
        text = SPEC.replace("### R-001 — Import", "**R-001 — Import**")
        text = text.replace("### R-002 — Review", "**R-002 — Review**")
        text = text.replace(" | Status", "").replace(" | --- |\n| T-001", " |\n| T-001", 1)
        text = text.replace(" | Planned |", " |")
        self.assertEqual(self.lint(text), (2, 2))

    def test_task_blocks_with_explicit_goal(self):
        text = """### R-001 — Import

### T-011 — Import work
- Goal: Keep an editable copy.
- Requirements: R-001
- Depends on: None
- Done when: The original stays unchanged.
- Status: Needs revalidation
"""
        self.assertEqual(self.lint(text), (1, 1))

    def test_split_files_are_explicit(self):
        source, table = SPEC.split("| ID", 1)
        self.path.write_text(source)
        tasks = self.path.with_name("TASKS.md")
        tasks.write_text("| ID" + table)
        self.assertEqual(check_spec(self.path, tasks), (2, 2))
        with self.assertRaisesRegex(ValueError, "No supported tasks"):
            check_spec(self.path)

    def test_forward_numbered_prerequisite_is_allowed(self):
        text = SPEC.replace("| None | Original", "| T-002 | Original")
        text = text.replace("| T-001 | Membership", "| None | Membership")
        self.assertEqual(self.lint(text), (2, 2))

    def test_dependency_typos_and_residual_text_are_rejected(self):
        for dependency in ("T_001", "T001", "T-001 typo", "T-001/T-002", "T-001T-002"):
            with self.subTest(dependency=dependency):
                self.reject(SPEC.replace("| T-001 | Membership", f"| {dependency} | Membership"),
                            "Malformed T references")

    def test_unknown_requirement_and_dependency(self):
        self.reject(SPEC.replace("| R-002 | T-001", "| R-999 | T-001"), "Unknown reference R-999")
        self.reject(SPEC.replace("| T-001 | Membership", "| T-999 | Membership"), "Unknown reference T-999")

    def test_missing_task_fields(self):
        for old, new, field in (
            ("| Import |", "|  |", "goal"),
            ("| R-001 | None", "|  | None", "refs"),
            ("| None | Original", "|  | Original", "depends"),
            ("| Original is unchanged |", "|  |", "done"),
        ):
            with self.subTest(field=field):
                self.reject(SPEC.replace(old, new), "Missing task " + field)

    def test_explicit_blank_or_unknown_status_is_rejected(self):
        for status in ("", "Banana"):
            with self.subTest(status=status):
                self.reject(SPEC.replace("| Planned |", "| " + status + " |", 1), "Unknown task status")

    def test_chinese_status_and_dependency(self):
        self.assertEqual(self.lint(SPEC.replace("None", "无").replace("Planned", "计划中")), (2, 2))

    def test_duplicate_ids(self):
        self.reject(SPEC.replace("R-002 — Review", "R-001 — Review"), "Duplicate requirement")
        row = "| T-002 | Review | R-002 | T-001 | Membership needs confirmation | Planned |\n"
        self.reject(SPEC + row, "Duplicate task")

    def test_malformed_bold_requirement_is_not_skipped(self):
        self.reject(SPEC.replace("### R-002 — Review", "**R_002 — Review**"),
                    "Malformed requirement ID")

    def test_task_id_and_row_shape(self):
        self.reject(SPEC.replace("| T-002 |", "| T_002 |"), "Malformed task ID")
        self.reject(SPEC.replace("| Review | R-002 | T-001", "| R-002"), "Malformed task row")

    def test_cycles_and_self_dependency(self):
        self.reject(SPEC.replace("| None | Original", "| T-002 | Original"), "Dependency cycle")
        self.reject(SPEC.replace("| None | Original", "| T-001 | Original"), "Dependency cycle")

    def test_ranges_expand_middle_ids(self):
        text = SPEC.replace("| R-002 | T-001", "| R-001—R-002 | T-001")
        self.assertEqual(self.lint(text), (2, 2))
        text += "| T-003 | Check | R-001 | T-001 至 T-002 | Both tasks checked | Planned |\n"
        self.assertEqual(self.lint(text), (2, 3))
        text = text.replace("| None | Original", "| T-003 | Original")
        self.reject(text, "Dependency cycle")

    def test_range_missing_middle_is_not_silently_skipped(self):
        text = SPEC.replace("R-002", "R-003")
        self.reject(text.replace("| R-003 | T-001", "| R-001—R-003 | T-001"), "Unknown reference R-002")

    def test_reversed_and_inconsistently_padded_ranges(self):
        for refs in ("R-002—R-001", "R-1—R-002"):
            with self.subTest(refs=refs):
                self.reject(SPEC.replace("| R-002 |", "| " + refs + " |"), "Invalid reference range")

    def test_escaped_pipe_in_goal(self):
        self.assertEqual(self.lint(SPEC.replace("| Import |", r"| Import \| review |")), (2, 2))

    def test_code_examples_do_not_define_ids_or_tasks(self):
        self.assertEqual(self.lint(SPEC + "\n```markdown\n" + SPEC + "\n```\n"), (2, 2))

    def test_uncovered_and_empty_documents(self):
        self.reject(SPEC.replace("| R-002 |", "| R-001 |"), "Uncovered requirements")
        self.reject("# No structure\n", "No requirements")

    def test_cli_success_and_clean_failure(self):
        self.path.write_text(SPEC)
        command = [sys.executable, "-B", str(REPO / "scripts/check.py"), "--spec", str(self.path)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("readiness and implementation remain unverified", result.stdout)
        self.path.write_text(SPEC.replace("| T-001 | Membership", "| T_001 | Membership"))
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Check failed:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.doc = self.root / "README.md"
        (self.root / "a file.md").write_text("content")
        (self.root / "图(one).png").write_bytes(b"image fixture")

    def links(self, text):
        self.doc.write_text(text, encoding="utf-8")
        return check.check_links([self.doc], self.root)

    def test_inline_spaces_percent_encoding_parentheses_and_images(self):
        self.assertEqual(self.links('[a](<a file.md>) [b](a%20file.md#section) ![c](图(one).png)'), 3)

    def test_full_collapsed_and_shortcut_reference_links(self):
        self.assertEqual(self.links('[a][target] [target][] [target]\n\n[target]: <a file.md> "title"'), 3)

    def test_broken_links_in_all_supported_forms(self):
        for text in ("[x](absent.md)", "[x](<absent file.md>)",
                     "[x][ref]\n\n[ref]: absent.md", "![x](absent.png)"):
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, "Broken local link"):
                    self.links(text)

    def test_remote_fragments_and_code_are_not_files(self):
        text = "[a](https://example.invalid/a) [b](#section) [c](mailto:a@example.invalid)\n"
        text += "`[not a link](absent.md)`\n\n```md\n[not a link](absent.md)\n```\n"
        self.assertEqual(self.links(text), 0)

    def test_encoded_boundary_escape(self):
        with self.assertRaisesRegex(ValueError, "escapes distribution root"):
            self.links("[x](%2e%2e/outside.md)")

    def test_symlink_boundary_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "outside.md"
            target.write_text("outside")
            (self.root / "alias.md").symlink_to(target)
            with self.assertRaisesRegex(ValueError, "escapes distribution root"):
                self.links("[x](alias.md)")


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(REPO / "skills/specforge", self.root / "skills/specforge")
        shutil.copytree(REPO / "examples", self.root / "examples")
        shutil.copyfile(REPO / "LICENSE", self.root / "LICENSE")
        self.skill = self.root / "skills/specforge"
        self.addCleanup(patch.stopall)
        patch.object(check, "ROOT", self.root).start()
        patch.object(check, "SKILL", self.skill).start()

    def build(self, name="output"):
        with contextlib.redirect_stdout(io.StringIO()):
            return package.build(self.root / name)

    def test_reproducible_archive_manifest_bytes_and_checksum(self):
        first, second = self.build("a"), self.build("b")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with ZipFile(first) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(set(archive.namelist()), {"specforge/" + p for p in check.RUNTIME_FILES})
            for filename in check.RUNTIME_FILES:
                self.assertEqual(archive.read("specforge/" + filename), (self.skill / filename).read_bytes())
        expected = hashlib.sha256(first.read_bytes()).hexdigest() + "  " + first.name + "\n"
        self.assertEqual(first.with_suffix(".zip.sha256").read_text(), expected)

    def test_unexpected_runtime_files_are_rejected(self):
        for name in ("__pycache__/temp.pyc", "temp.pyc", "notes.txt", ".DS_Store"):
            with self.subTest(name=name):
                path = self.skill / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"not a release input")
                with self.assertRaisesRegex(ValueError, "Unexpected runtime entry"):
                    self.build()
                path.unlink()
                if path.parent.name == "__pycache__":
                    path.parent.rmdir()

    def test_unexpected_empty_directory(self):
        (self.skill / "scratch").mkdir()
        with self.assertRaisesRegex(ValueError, "Unexpected runtime entry"):
            check.check_runtime_files()

    def test_runtime_symlinks_are_rejected(self):
        path = self.skill / "LICENSE"
        path.unlink()
        path.symlink_to(self.root / "LICENSE")
        with self.assertRaisesRegex(ValueError, "symlinks"):
            check.check_runtime_files()

    def test_missing_resource(self):
        (self.skill / "references/interview.md").unlink()
        with self.assertRaisesRegex(ValueError, "Missing runtime file"):
            self.build()

    def test_license_mismatch(self):
        (self.skill / "LICENSE").write_text("different")
        with self.assertRaisesRegex(ValueError, "licenses differ"):
            self.build()

    def test_build_output_cannot_pollute_runtime(self):
        with self.assertRaisesRegex(ValueError, "outside the runtime"):
            self.build("skills/specforge/new-output")
        self.assertFalse((self.skill / "new-output").exists())

    def test_failed_validation_preserves_existing_archive(self):
        destination = self.build()
        original = destination.read_bytes()
        (self.skill / "notes.txt").write_text("junk")
        with self.assertRaises(ValueError):
            self.build()
        self.assertEqual(destination.read_bytes(), original)

    def test_invalid_nested_metadata_is_a_validation_error(self):
        path = self.skill / "SKILL.md"
        text = path.read_text().replace("metadata:\n", "metadata: []\n# ", 1)
        path.write_text(text)
        with self.assertRaisesRegex(ValueError, "metadata must be a mapping"):
            check.read_metadata()

    def test_invalid_ui_shape_is_a_validation_error(self):
        path = self.skill / "agents/openai.yaml"
        for content in ("[]", "interface: []", "interface: null"):
            with self.subTest(content=content):
                path.write_text(content)
                with self.assertRaisesRegex(ValueError, "interface mapping"):
                    self.build()


if __name__ == "__main__":
    unittest.main()
