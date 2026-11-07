"""Protect motion review boundaries and natural-speed editorial selection."""

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


SPEC = importlib.util.spec_from_file_location(
    "full_film_editor", Path(__file__).resolve().parents[1] /
    "productions/join-me-in-life/full-film/edit.py")
editor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(editor)


class RendererFixture(unittest.TestCase):
    real_media = False

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        patch = mock.patch.object(editor, "ROOT", self.root)
        patch.start()
        self.addCleanup(patch.stop)
        (self.root / "review").mkdir()
        self.clip = self.root / "motion.mp4"
        self.clip.write_bytes(b"reviewed test source")
        (self.root / "plate.ppm").write_bytes(b"P6\n64 36\n255\n" + b"\x40\x50\x60" * (64 * 36))
        (self.root / "song.mp3").write_bytes(b"unused fixture audio")
        if not self.real_media:
            patch = mock.patch.object(editor, "probe", return_value={
                "format": {"duration": "12"},
                "streams": [{"codec_type": "video", "duration": "8"}]})
            patch.start()
            self.addCleanup(patch.stop)
        camera = dict(zoom_start=1, zoom_end=1, center_start=[.5, .5], center_end=[.5, .5])
        self.edit = {
            "fps": 24, "total_frames": 6667, "audio": "song.mp3",
            "approved_motion": "review/approved-motion.json", "production_tools": [],
            "sources": {"window": {"path": "plate.ppm"}},
            "shots": [
                dict(id="S001", source_key="window", start_frame=0,
                     end_frame_exclusive=154, camera=camera, title=False),
                dict(id="S002", source_key="window", start_frame=154,
                     end_frame_exclusive=6667, camera=camera, title=False),
            ],
        }

    def approve(self, **changes):
        clip = dict(id="window-reviewed", source_key="window", path="motion.mp4",
                    in_seconds=0, duration_seconds=8, status="approved", provider="Test provider",
                    reviewed_source_sha256=editor.sha256(self.clip),
                    review_note="Synthetic fixture; not a production motion approval.", shot_ids=["S001"])
        clip.update(changes)
        (self.root / self.edit["approved_motion"]).write_text(json.dumps({
            "schema": "jml-approved-motion/v1", "clips": [clip]}), encoding="utf-8")


class MotionSelectionTests(RendererFixture):
    def test_source_presence_does_not_create_motion_approval(self):
        shots, note = editor.assemble_plan(self.edit)
        self.assertTrue(all(s["motion"] is None for s in shots))
        self.assertEqual(editor.report(self.edit, shots, note)["motion_accounting"]["generated_video_seconds"], 0)

    def test_approved_status_without_review_is_rejected(self):
        for note in (None, "", "   "):
            with self.subTest(note=note):
                self.approve(review_note=note)
                with self.assertRaisesRegex(ValueError, "review note"):
                    editor.assemble_plan(self.edit)

    def test_replacing_reviewed_source_invalidates_approval(self):
        self.approve()
        self.clip.write_bytes(b"a different take at the same path")
        with self.assertRaisesRegex(ValueError, "reviewed source checksum"):
            editor.assemble_plan(self.edit)

    def test_nonfinite_or_out_of_picture_intervals_are_rejected(self):
        for start, duration in [(-1, 4), (0, 0), (float("nan"), 4), (float("inf"), 4),
                                (0, float("nan")), (0, float("inf")), (7, 2)]:
            with self.subTest(start=start, duration=duration):
                self.approve(in_seconds=start, duration_seconds=duration)
                # Container/audio lasts 12 seconds; picture ends at 8 seconds.
                with self.assertRaisesRegex(ValueError, "Invalid natural-speed"):
                    editor.assemble_plan(self.edit)

    def test_eight_second_source_fills_window_slot_without_reuse(self):
        self.approve(shot_ids=[])
        shots, note = editor.assemble_plan(self.edit)
        self.assertEqual(shots[0]["motion"]["used_frames"], 154)
        self.assertIsNone(shots[1]["motion"])
        accounting = editor.report(self.edit, shots, note)["motion_accounting"]
        self.assertAlmostEqual(accounting["generated_video_seconds"], 154 / 24)
        self.assertEqual(accounting["endpoint_hold_seconds"], 0)

    def test_approval_cannot_silently_target_an_unknown_shot(self):
        self.approve(shot_ids=["S999"])
        with self.assertRaisesRegex(ValueError, "Motion targets"):
            editor.assemble_plan(self.edit)

    def test_title_cannot_restart_inside_the_song(self):
        self.edit["shots"][1]["title"] = True
        with self.assertRaisesRegex(ValueError, "full-song frame zero"):
            editor.validate_edit(self.edit)

    def test_original_motion_filename_guard_remains(self):
        for filename in ("M01_Embrace.mp4", "M02_Summer.mp4"):
            (self.root / filename).write_bytes(b"legacy source")
            with self.assertRaisesRegex(ValueError, "Rejected baseline motion"):
                editor.resolve_path(filename)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg integration tools unavailable")
class NaturalSpeedRenderTests(RendererFixture):
    real_media = True

    def test_logo_and_title_form_one_compact_lockup_with_the_same_fade(self):
        # A white test logo on a black plate makes the two separate title bands
        # observable in decoded pixels without depending on particular letterforms.
        (self.root / "plate.ppm").write_bytes(b"P6\n64 36\n255\n" + b"\0" * (64 * 36 * 3))
        logo = self.root / "logo.ppm"
        logo.write_bytes(b"P6\n300 100\n255\n" + b"\xff" * (300 * 100 * 3))
        shots, _ = editor.assemble_plan(self.edit)
        shot = dict(shots[0], title=True, branding={"absolute_path": str(logo), "sha256": editor.sha256(logo)})
        output = editor.render_shot(shot, SimpleNamespace(width=480, height=270, crf=0,
                                                        threads=1, force=True), self.root)
        frames = editor.run(["ffmpeg", "-v", "error", "-i", output, "-vf",
                             r"select=eq(n\,8)+eq(n\,12)+eq(n\,18)+eq(n\,116)",
                             "-fps_mode", "vfr", "-pix_fmt", "gray", "-f", "rawvideo", "-"], True)
        size = 480 * 270
        self.assertEqual(len(frames), 4 * size)
        before, partial, full, after = [frames[i * size:(i + 1) * size] for i in range(4)]
        self.assertLessEqual(max(before), 1)
        self.assertLessEqual(max(after), 1)
        rows = [y for y in range(270) if max(full[y * 480:(y + 1) * 480]) > 20]
        bands = []
        for y in rows:
            if not bands or y != bands[-1][-1] + 1:
                bands.append([])
            bands[-1].append(y)
        self.assertEqual(len(bands), 2, "Logo and song title must be distinct visible bands")
        self.assertLess(bands[1][0] - bands[0][-1], 15, "Title must sit directly beneath logo")
        ratios = []
        for band in bands:
            peak = max(full[band[0] * 480:(band[-1] + 1) * 480])
            faded = max(partial[band[0] * 480:(band[-1] + 1) * 480])
            self.assertGreater(peak, 200)
            self.assertGreater(faded, 30)
            self.assertLess(faded, 150)
            ratios.append(faded / peak)
        self.assertAlmostEqual(ratios[0], ratios[1], delta=.025)

    def test_longer_take_renders_exact_selected_frames_and_only_holds_when_short(self):
        # Every frame has a different luminance: loops, reversal, speed changes,
        # an incorrect seek or a premature endpoint hold alter the decoded sequence.
        editor.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                    "color=c=black:s=64x36:r=24:d=8,geq=lum=16+N:cb=128:cr=128",
                    "-c:v", "libx264", "-crf", "0", "-threads", "1",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                    "-color_range", "tv", self.clip])
        self.approve(in_seconds=1, duration_seconds=7)
        shots, _ = editor.assemble_plan(self.edit)
        args = SimpleNamespace(width=64, height=36, crf=0, threads=1, force=True)
        output = editor.render_shot(shots[0], args, self.root)

        def decoded(path):
            return editor.run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:v:0",
                               "-pix_fmt", "gray", "-f", "rawvideo", "-"], True)

        frame_bytes = 64 * 36
        source = decoded(self.clip)
        expected = source[24 * frame_bytes:(24 + 154) * frame_bytes]
        self.assertEqual(len(decoded(output)), 154 * frame_bytes)
        self.assertEqual(decoded(output), expected)
        # A short approved interval gets a true endpoint hold, not a stretched action.
        self.approve(in_seconds=1, duration_seconds=2)
        shots, _ = editor.assemble_plan(self.edit)
        output = editor.render_shot(shots[0], args, self.root)
        action = source[24 * frame_bytes:72 * frame_bytes]
        self.assertEqual(decoded(output), action + action[-frame_bytes:] * (154 - 48))


if __name__ == "__main__":
    unittest.main()
