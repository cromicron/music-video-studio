"""Verify that broken continuation records cannot silently pass the studio check."""

import importlib.util
import contextlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("studio", Path(__file__).resolve().parents[1] / "tools/studio.py")
studio = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(studio)


class StudioFixture:
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.data = {
            "schema": "mercy-in-minor-studio/v1",
            "active_production": "first-song",
            "productions": [{"id": "first-song", "title": "First Song"}],
        }
        for relative in studio.REQUIRED_FILES:
            self.write(relative, "# Fixture\n")
        for name in studio.PRODUCTION_RECORDS:
            self.write(f"productions/first-song/{name}", "# First Song\n")
        self.save_registry()

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def save_registry(self):
        self.write("studio.json", json.dumps(self.data))


class StudioStructureTests(StudioFixture, unittest.TestCase):
    def test_missing_current_state_blocks_check(self):
        (self.root / "productions/first-song/STATUS.md").unlink()
        with self.assertRaisesRegex(ValueError, "STATUS.md"):
            studio.check_structure(self.root)

    def test_registry_rejects_ambiguous_or_escaping_productions(self):
        cases = [
            {"active_production": "missing"},
            {"active_production": []},
            {"productions": [{"id": "../outside", "title": "Outside"}]},
            {"productions": self.data["productions"] * 2},
            {"productions": [{"id": "first-song", "title": ""}]},
        ]
        for change in cases:
            with self.subTest(change=change):
                self.write("studio.json", json.dumps(self.data | change))
                with self.assertRaises(ValueError):
                    studio.check_structure(self.root)

    def test_unregistered_folder_cannot_hide_a_production(self):
        (self.root / "productions/forgotten-song").mkdir()
        with self.assertRaisesRegex(ValueError, "Unregistered production"):
            studio.check_structure(self.root)

    def test_broken_local_link_blocks_check_but_external_links_are_not_fetched(self):
        self.write("README.md", "[remote](https://example.invalid) [status](productions/first-song/STATUS.md#current)\n")
        studio.check_structure(self.root)
        self.write("README.md", "[handoff](productions/first-song/MISSING.md)\n")
        with self.assertRaisesRegex(ValueError, "Broken/nonportable local link"):
            studio.check_structure(self.root)

    def test_links_outside_checkout_are_not_portable(self):
        self.write("README.md", "[local machine](/etc/hosts)\n")
        with self.assertRaisesRegex(ValueError, "nonportable"):
            studio.check_structure(self.root)

    def test_archived_handoff_does_not_override_maintained_checks(self):
        self.write("productions/first-song/notes/old-handoff.md", "[old workspace](gone.md)\n")
        studio.check_structure(self.root)
        self.write("productions/first-song/notes/README.md", "[current](gone.md)\n")
        with self.assertRaisesRegex(ValueError, "notes/README.md"):
            studio.check_structure(self.root)

    def test_documented_template_method_produces_a_valid_second_production(self):
        template = Path(__file__).resolve().parents[1] / "templates/production"
        shutil.copytree(template, self.root / "templates/production", dirs_exist_ok=True)
        destination = self.root / "productions/second-song"
        shutil.copytree(template, destination)
        self.data["productions"].append({"id": "second-song", "title": "Second Song"})
        self.data["active_production"] = "second-song"
        self.save_registry()
        with self.assertRaisesRegex(ValueError, "Unfilled production template"):
            studio.check_structure(self.root)
        for path in destination.glob("*.md"):
            path.write_text(re.sub(r"\{\{[A-Z_]+\}\}", "Recorded fixture detail",
                                   path.read_text(encoding="utf-8")), encoding="utf-8")
        self.assertEqual(studio.check_structure(self.root)[0], 2)


class StudioContinuityTests(StudioFixture, unittest.TestCase):
    """Use actual Git repos: a valid working tree is not necessarily a recoverable handoff."""

    def setUp(self):
        super().setUp()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Continuity Test")
        self.git("config", "user.email", "continuity@example.invalid")
        self.commit("Initial records")
        self.remote_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.remote_directory.cleanup)
        self.remote = Path(self.remote_directory.name) / "origin.git"
        self.git("init", "--bare", "-q", "-b", "main", str(self.remote))
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "-q", "-u", "origin", "main")

    def git(self, *args, cwd=None):
        return subprocess.run(["git", "-C", str(cwd or self.root), *args], check=True,
                              text=True, capture_output=True).stdout.strip()

    def commit(self, message):
        self.git("add", "--all")
        self.git("commit", "-q", "-m", message)

    def checkpoint_output(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            studio.checkpoint(self.root)
        return output.getvalue()

    def test_checkpoint_succeeds_only_for_clean_live_upstream(self):
        output = self.checkpoint_output()
        self.assertIn(self.git("rev-parse", "HEAD"), output)
        self.assertIn("Cold committed archive", output)
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_structure_can_pass_while_uncommitted_task_fails_checkpoint(self):
        self.write("productions/first-song/new-task.md", "A locally retained task\n")
        studio.check_structure(self.root)
        with self.assertRaisesRegex(ValueError, "untracked files"):
            studio.checkpoint(self.root)
        self.git("add", "productions/first-song/new-task.md")
        with self.assertRaisesRegex(ValueError, "tracked edits"):
            studio.checkpoint(self.root)

    def test_local_branch_without_upstream_cannot_claim_persistence(self):
        self.git("checkout", "-q", "-b", "local-only")
        with self.assertRaisesRegex(ValueError, "remote branch upstream"):
            studio.checkpoint(self.root)

    def test_pushed_task_survives_single_branch_cloud_fetch_configuration(self):
        self.git("config", "remote.origin.fetch", "+refs/heads/main:refs/remotes/origin/main")
        self.git("checkout", "-q", "-b", "film-task")
        self.git("push", "-q", "-u", "origin", "film-task")
        self.assertEqual(self.git("for-each-ref", "--format=%(upstream)",
                                  "refs/heads/film-task"), "")
        self.assertIn("Checkpoint verified: film-task", self.checkpoint_output())

    def test_unpushed_commit_cannot_claim_persistence(self):
        self.write("PROJECT_MEMORY.md", "# A new instruction\n")
        self.commit("Local progress")
        with self.assertRaisesRegex(ValueError, "live origin"):
            studio.checkpoint(self.root)

    def test_unreachable_remote_does_not_turn_into_checkpoint_success(self):
        self.git("remote", "set-url", "origin", str(self.remote.parent / "missing.git"))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with self.assertRaisesRegex(ValueError, "ls-remote.*failed"):
                studio.checkpoint(self.root)
        self.assertNotIn("Checkpoint verified", output.getvalue())

    def test_remote_advance_is_detected_despite_stale_tracking_ref(self):
        original = self.git("rev-parse", "HEAD")
        other = Path(self.remote_directory.name) / "other"
        self.git("clone", "-q", str(self.remote), str(other))
        self.git("config", "user.name", "Other session", cwd=other)
        self.git("config", "user.email", "other@example.invalid", cwd=other)
        (other / "PROJECT_MEMORY.md").write_text("# Remote progress\n", encoding="utf-8")
        self.git("add", "PROJECT_MEMORY.md", cwd=other)
        self.git("commit", "-q", "-m", "Other session progress", cwd=other)
        self.git("push", "-q", cwd=other)
        self.assertEqual(self.git("rev-parse", "origin/main"), original)
        with self.assertRaisesRegex(ValueError, "live origin"):
            studio.checkpoint(self.root)
        self.assertEqual(self.git("rev-parse", "HEAD"), original)

    def test_cold_archive_rejects_link_to_ignored_local_evidence(self):
        self.write(".gitignore", "/local-evidence/\n")
        self.write("local-evidence/review.txt", "Only exists in this task\n")
        self.write("README.md", "[review evidence](local-evidence/review.txt)\n")
        self.commit("An apparently valid evidence link")
        self.git("push", "-q")
        studio.check_structure(self.root)
        self.assertEqual(self.git("status", "--porcelain"), "")
        with self.assertRaisesRegex(ValueError, "Broken/nonportable local link"):
            studio.checkpoint(self.root)

    def test_refresh_finds_unmerged_task_without_changing_local_work(self):
        # A separate session pushes a task the original clone has never fetched.
        other = Path(self.remote_directory.name) / "other"
        self.git("clone", "-q", str(self.remote), str(other))
        self.git("config", "user.name", "Other session", cwd=other)
        self.git("config", "user.email", "other@example.invalid", cwd=other)
        self.git("checkout", "-q", "-b", "film-next", cwd=other)
        (other / "productions/first-song/STATUS.md").write_text("# A new task\n", encoding="utf-8")
        self.git("add", "--all", cwd=other)
        self.git("commit", "-q", "-m", "Next task", cwd=other)
        task_sha = self.git("rev-parse", "HEAD", cwd=other)
        self.git("push", "-q", "origin", "film-next", cwd=other)
        self.git("push", "-q", "origin", "HEAD:refs/heads/codex-sync", cwd=other)
        self.assertNotIn("film-next", self.git("branch", "-r"))
        self.write("local-work.txt", "Preserve unfinished work\n")
        before = self.git("rev-parse", "HEAD")
        studio.refresh(self.root)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            studio.orientation(self.root)
        text = output.getvalue()
        self.assertIn(f"origin/film-next {task_sha} — unmerged", text)
        self.assertIn(f"git show {task_sha}:productions/first-song/STATUS.md", text)
        self.assertNotIn("codex-sync", text)
        self.assertIn("local-work.txt", text)
        self.assertEqual(self.git("rev-parse", "HEAD"), before)
        self.assertEqual(self.git("branch", "--show-current"), "main")
        self.assertEqual((self.root / "local-work.txt").read_text(), "Preserve unfinished work\n")


if __name__ == "__main__":
    unittest.main()
