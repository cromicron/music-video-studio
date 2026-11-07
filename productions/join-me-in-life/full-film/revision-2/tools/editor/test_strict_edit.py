"""Failure cases plus real frame-order proof for the v2 assembly boundary."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import strict_edit as editor


class StrictEditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix="v2-editor-test-", dir=editor.REPOSITORY / "build")
        cls.root = Path(cls.tmp.name)
        cls.movie = cls.root / "source.mkv"
        editor.legacy.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=64x36:rate=24:duration=2",
                           "-c:v", "ffv1", "-pix_fmt", "yuv420p", cls.movie])
        cls.digest = editor.legacy.sha256(cls.movie)
        cls.review = cls.root / "source-review.md"
        cls.review.write_text(f"Synthetic test fixture only. Source SHA: {cls.digest}. Frames [0,48) fixture-approved.\n")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def plan(self):
        state = {"location": "test fixture", "blocking": "moving test pattern", "props": {}}
        source = {"kind": "video", "path": "source.mkv", "sha256": self.digest, "take_id": "fixture",
                  "review": {"path": "source-review.md", "sha256": editor.legacy.sha256(self.review),
                             "status": "accepted", "accepted_ranges": [[0, 48]]}}
        shots = []
        for i in range(2):
            shots.append({"id": f"T{i+1}", "start_frame": i*12, "end_frame_exclusive": (i+1)*12,
                          "section": "fixture", "story": {"before": "A", "action": "B", "after": "C"},
                          "continuity": {"entry": copy.deepcopy(state), "exit": copy.deepcopy(state), "cut_to_next": "fixture"},
                          "source": {"id": "a", "in_frame": 1+i*12, "out_frame_exclusive": 13+i*12}})
        return {"schema": editor.SCHEMA, "fps": 24, "total_frames": 24, "sources": {"a": source}, "shots": shots}

    def test_timeline_gap_rejected(self):
        p = self.plan(); p["shots"][1]["start_frame"] += 1
        with self.assertRaisesRegex(ValueError, "Timeline gap"):
            editor.validate_story(p, 24)

    def test_missing_source_never_becomes_a_still(self):
        p = self.plan(); p["sources"] = {}
        with self.assertRaisesRegex(ValueError, "Missing selected motion"):
            editor.bind_sources(p, p["shots"], self.root)

    def test_short_source_selection_never_gets_padding(self):
        p = self.plan(); p["shots"][0]["source"]["out_frame_exclusive"] -= 1
        with self.assertRaisesRegex(ValueError, "exactly fill"):
            editor.bind_sources(p, p["shots"], self.root)

    def test_source_extent_is_decoded_not_assumed(self):
        p = self.plan(); p["shots"][0]["source"].update(in_frame=40, out_frame_exclusive=52)
        with self.assertRaisesRegex(ValueError, "exceeds footage"):
            editor.bind_sources(p, p["shots"], self.root)

    def test_source_alias_cannot_hide_repeated_frames(self):
        p = self.plan(); p["sources"]["alias"] = copy.deepcopy(p["sources"]["a"])
        p["shots"][1]["source"].update(id="alias", in_frame=10, out_frame_exclusive=22)
        with self.assertRaisesRegex(ValueError, "Repeated source frames"):
            editor.bind_sources(p, p["shots"], self.root)

    def test_changed_review_is_rejected(self):
        p = self.plan(); p["sources"]["a"]["review"]["sha256"] = "0"*64
        with self.assertRaisesRegex(ValueError, "Review SHA changed"):
            editor.bind_sources(p, p["shots"], self.root)

    def test_unreviewed_range_is_rejected(self):
        p = self.plan(); p["sources"]["a"]["review"]["accepted_ranges"] = [[3, 48]]
        with self.assertRaisesRegex(ValueError, "interval is unreviewed"):
            editor.bind_sources(p, p["shots"], self.root)

    def test_30fps_is_not_silently_converted(self):
        movie = self.root / "thirty.mkv"
        editor.legacy.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=64x36:rate=30:duration=1",
                           "-c:v", "ffv1", movie])
        with self.assertRaisesRegex(ValueError, "natural 24fps"):
            editor.source_timing(movie)

    def test_real_frame_trim_and_join_preserve_every_selected_picture(self):
        p = self.plan(); editor.validate_story(p, 24)
        shots = editor.bind_sources(p, p["shots"], self.root)
        outputs = [editor.render_shot(s, self.root/f"{s['id']}.mp4", 64, 36, crf=0, threads=1) for s in shots]
        def raw(path, vf=None):
            cmd = ["ffmpeg", "-v", "error", "-i", path]
            if vf:
                cmd += ["-vf", vf]
            return editor.legacy.run(cmd + ["-an", "-pix_fmt", "yuv420p", "-f", "rawvideo", "-"], True)
        expected = raw(self.movie, "trim=start_frame=1:end_frame=25")
        actual = b"".join(raw(p) for p in outputs)
        self.assertEqual(len(expected), 24*64*36*3//2)
        self.assertEqual(actual, expected, "Exact selected source frames changed/repeated/dropped at the join")


if __name__ == "__main__":
    unittest.main()
