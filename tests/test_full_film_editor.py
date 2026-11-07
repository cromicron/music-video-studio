"""Protect motion review boundaries and natural-speed editorial selection."""

import importlib.util
import ast
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
                "streams": [{"codec_type": "video", "duration": "8", "width": 64, "height": 36}]})
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

    def existing_review(self):
        review = self.root / "review/superseding.md"
        review.write_text("Synthetic fixture review of exact source " + editor.sha256(self.clip) + "\n")
        return {"path": "review/superseding.md", "sha256": editor.sha256(review)}


class MotionSelectionTests(RendererFixture):
    def test_deliberate_closeup_does_not_relax_default_camera_limit(self):
        s = self.edit['shots'][0]
        s['camera'] = dict(s['camera'], zoom_start=2, zoom_end=2)
        with self.assertRaisesRegex(ValueError, 'Unsafe crop'):
            editor.validate_edit(self.edit)
        s['framing_intent'] = 'deliberate_stationary_closeup'
        editor.validate_edit(self.edit)
        s['camera']['zoom_end'] = 1.9
        with self.assertRaisesRegex(ValueError, 'must be stationary'):
            editor.validate_edit(self.edit)
        s['camera'].update(zoom_start=2.01, zoom_end=2.01)
        with self.assertRaisesRegex(ValueError, 'Unsafe crop'):
            editor.validate_edit(self.edit)

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

    def test_legacy_exception_requires_real_source_and_superseding_review_hashes(self):
        legacy = self.root / "M01_Embrace.mp4"
        self.clip.rename(legacy)
        self.clip = legacy
        self.approve(path=legacy.name)
        with self.assertRaisesRegex(ValueError, "Rejected baseline motion"):
            editor.assemble_plan(self.edit)
        self.approve(path=legacy.name, usage="reused_existing_video")
        with self.assertRaisesRegex(ValueError, "superseding review"):
            editor.assemble_plan(self.edit)
        review = self.existing_review()
        self.approve(path=legacy.name, usage="reused_existing_video", superseding_review=review)
        self.assertIsNotNone(editor.assemble_plan(self.edit)[0][0]["motion"])
        # A changed source cannot inherit the old approval, including at a guarded name.
        self.clip.write_bytes(b"changed existing take")
        with self.assertRaisesRegex(ValueError, "reviewed source checksum"):
            editor.assemble_plan(self.edit)

    def test_changed_missing_or_unrelated_superseding_review_cannot_authorize_reuse(self):
        review = self.existing_review()
        self.approve(usage="reused_existing_video", superseding_review=review)
        path = self.root / review["path"]
        path.write_text("An unrelated review without the source identity.\n")
        with self.assertRaisesRegex(ValueError, "review file.*checksum"):
            editor.assemble_plan(self.edit)
        self.approve(usage="reused_existing_video", superseding_review=dict(review, sha256=editor.sha256(path)))
        with self.assertRaisesRegex(ValueError, "exact existing source checksum"):
            editor.assemble_plan(self.edit)
        path.unlink()
        with self.assertRaisesRegex(ValueError, "review file is missing"):
            editor.assemble_plan(self.edit)

    def test_lead_in_must_leave_space_for_a_source_frame(self):
        for lead in (-1, True, 1.5, "5", 154):
            with self.subTest(lead=lead):
                self.approve(lead_in_frames=lead)
                with self.assertRaisesRegex(ValueError, "lead_in_frames|Lead-in"):
                    editor.assemble_plan(self.edit)

    def test_reuse_keeps_historical_provider_out_of_new_generation_accounting(self):
        self.approve(usage="reused_existing_video", provider="Runway",
                     superseding_review=self.existing_review(), duration_seconds=2, lead_in_frames=10)
        shots, note = editor.assemble_plan(self.edit)
        report = editor.report(self.edit, shots, note)
        accounting = report["motion_accounting"]
        self.assertEqual(accounting["generated_video_seconds"], 0)
        self.assertEqual(accounting["new_generated_video_seconds"], 0)
        self.assertEqual(accounting["reused_existing_video_seconds"], 2)
        self.assertAlmostEqual(accounting["lead_in_hold_seconds"], 10 / 24)
        self.assertEqual(accounting["endpoint_hold_seconds"], 4)
        self.assertEqual(report["historical_reused_source_providers"], ["Runway"])
        self.assertNotIn("Runway", report["actual_picture_production_tools"])


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg integration tools unavailable")
class NaturalSpeedRenderTests(RendererFixture):
    real_media = True

    def test_contain_keeps_encoded_top_bottom_borders_and_exact_selected_frames(self):
        # The actual7:4 source ratio with a white border reveals cropping immediately;
        # changing center luminance also detects a shifted/repeated source frame.
        editor.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                    "color=c=black:s=112x64:r=24,geq=lum='if(lt(X,4)+gte(X,108)+lt(Y,4)+gte(Y,60),235,16+N*8)':cb=128:cr=128",
                    "-frames:v", "12", "-c:v", "libx264", "-crf", "0", "-threads", "1", self.clip])
        self.edit['shots'][0]['end_frame_exclusive'] = 5
        self.edit['shots'][1]['start_frame'] = 5
        self.approve(in_seconds=3/24, duration_seconds=5/24, framing_policy='contain')
        shots, note = editor.assemble_plan(self.edit)
        self.assertEqual(shots[0]['motion']['framing_policy'], 'contain')
        self.assertEqual(shots[0]['motion']['used_frames'], 5)
        self.assertEqual(shots[0]['motion']['endpoint_hold_frames'], 0)
        self.assertEqual(editor.report(self.edit, shots, note)['shots'][0]['motion']['framing_policy'], 'contain')
        output = editor.render_shot(shots[0], SimpleNamespace(width=960,height=540,crf=0,threads=1,force=True),self.root)
        def gray(path):
            return editor.run(['ffmpeg','-v','error','-i',path,'-pix_fmt','gray','-f','rawvideo','-'],True)
        original, result = gray(self.clip), gray(output)
        self.assertEqual(len(result),5*960*540)
        for n in range(5):
            frame=result[n*960*540:(n+1)*960*540]
            self.assertAlmostEqual(frame[270*960+480],original[(n+3)*112*64+32*112+56],delta=1)
            # Both full original borders survive; 8px side bands are symmetric.
            self.assertGreaterEqual(frame[480],250)
            self.assertGreaterEqual(frame[539*960+480],250)
            self.assertLessEqual(max(frame[270*960:270*960+8]),1)
            self.assertLessEqual(max(frame[270*960+952:271*960]),1)
            self.assertGreaterEqual(frame[270*960+9],250)
            self.assertGreaterEqual(frame[270*960+950],250)
        stamp=json.loads(output.with_suffix('.json').read_text())
        self.assertIn('force_original_aspect_ratio=decrease',stamp['filter'])
        self.assertEqual(stamp['motion_framing_policy'],'contain')
        # Invalid policy must not silently fall through to a crop.
        self.approve(framing_policy='unknown')
        with self.assertRaisesRegex(ValueError,'framing policy'):
            editor.assemble_plan(self.edit)

    def test_local_drawing_exposures_change_only_the_registered_region_on_exact_frames(self):
        # Strongly different whole-frame art must affect only its local mask.
        alt = self.root / "alternate.ppm"
        alt.write_bytes(b"P6\n64 36\n255\n" + b"\xf0\xf0\xf0" * (64*36))
        shots, _ = editor.assemble_plan(self.edit)
        source = shots[0]["source"]
        patch = dict(path=str(alt), sha256=editor.sha256(alt), bounds=[.5,.5,.15,.2], runs=[[2,5]])
        shot = dict(shots[0], frames=8, end_frame_exclusive=8,
                    drawn_art={"source":source,"patches":[patch]})
        output = editor.render_shot(shot, SimpleNamespace(width=64,height=36,crf=0,threads=1,force=True),self.root)
        data = editor.run(["ffmpeg","-v","error","-i",output,"-pix_fmt","rgb24","-f","rawvideo","-"],True)
        size=64*36*3
        self.assertEqual(len(data),8*size)
        frames=[data[i*size:(i+1)*size] for i in range(8)]
        center=(18*64+32)*3
        for i,f in enumerate(frames):
            self.assertEqual(f[:3],frames[0][:3])
            self.assertEqual(f[-3:],frames[0][-3:])
            self.assertEqual(f[center]>200,2<=i<5)
        # The feather's outside boundary must never carry the different portrait.
        self.assertEqual(frames[0][(18*64+12)*3:(18*64+12)*3+3],frames[3][(18*64+12)*3:(18*64+12)*3+3])

    def test_registered_code_and_art_mutations_invalidate_drawing_reuse(self):
        original_root = Path(__file__).resolve().parents[1] / "productions/join-me-in-life/full-film"
        config=json.loads((original_root/"edit-production-candidate.json").read_text())
        with mock.patch.object(editor,"ROOT",original_root):
            poses=editor.historical_pose_track(config["historical_drawn_art"])
            self.assertEqual(poses[305:339],[3]*34)
            self.assertEqual(poses[339],0)
            # Compare all1440 frames to the actual original pure function,
            # evaluating its AST alone; do not import bpy or execute other code.
            src=original_root.parent/"current/native_animation.py"
            tree=ast.parse(src.read_text())
            nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="exposures"]
            patterns=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="PATTERNS" for t in n.targets))
            ns=dict(json=json,ROOT=src.parent,FPS=24,PATTERNS=patterns)
            exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),"exec"),ns)
            self.assertEqual(ns['exposures'](),[(f,p) for f,p in enumerate(poses) if f==0 or p!=poses[f-1]])
            registry=config["historical_drawn_art"]
            registry["source_files"]["native_animation.py"]["sha256"]="changed"
            with self.assertRaisesRegex(ValueError,"checksum changed"):
                editor.historical_pose_track(registry)
            shot=next(s for s in config['shots'] if s['id']=='S023')
            registry['drawings']['P01_Mouth_Round.png']['sha256']='changed'
            with self.assertRaisesRegex(ValueError,"checksum changed"):
                editor.drawn_segments(config,shot,poses)
            shot['drawn_art_segments'][0]['start_frame']+=1
            with self.assertRaisesRegex(ValueError,"cover their shot"):
                editor.drawn_segments(config,shot,poses)

    def test_lead_source_and_endpoint_keep_all_121_changing_frames_once(self):
        # Exact production layout, with a distinct luminance on every source
        # frame: a repeated/dropped action frame or one-frame timing shift fails.
        editor.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                    "color=c=black:s=64x36:r=24,geq=lum=16+N:cb=128:cr=128",
                    "-frames:v", "121", "-c:v", "libx264", "-crf", "0", "-threads", "1",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                    "-color_range", "tv", self.clip])
        self.edit["shots"][0]["end_frame_exclusive"] = 291
        self.edit["shots"][1]["start_frame"] = 291
        self.approve(duration_seconds=121 / 24, lead_in_frames=92)
        shots, _ = editor.assemble_plan(self.edit)
        motion = shots[0]["motion"]
        self.assertEqual(motion["used_frames"], 121)
        self.assertEqual(motion["endpoint_hold_frames"], 78)
        self.assertEqual(motion["source_start_timeline_frame"], 92)
        self.assertEqual(motion["source_end_timeline_frame_exclusive"], 213)
        output = editor.render_shot(shots[0], SimpleNamespace(width=64, height=36, crf=0,
                                                             threads=1, force=True), self.root)
        def decoded(path):
            return editor.run(["ffmpeg", "-v", "error", "-i", path, "-pix_fmt", "gray",
                               "-f", "rawvideo", "-"], True)
        size = 64 * 36
        source = decoded(self.clip)
        self.assertEqual(len(source), 121 * size)
        expected = source[:size] * 92 + source + source[-size:] * 78
        self.assertEqual(decoded(output), expected)

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
