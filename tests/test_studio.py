"""Verify that broken continuation records cannot silently pass the studio check."""

import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("studio", Path(__file__).resolve().parents[1] / "tools/studio.py")
studio = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(studio)


class StudioStructureTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
