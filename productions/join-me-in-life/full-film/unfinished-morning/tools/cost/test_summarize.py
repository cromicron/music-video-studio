"""Failure-oriented tests use real temporary job bytes, hashes and current bindings."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

MODULE = Path(__file__).with_name('summarize.py')
spec = importlib.util.spec_from_file_location('cost_summary', MODULE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


class RuntimeEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'full-film/unfinished-morning'
        self.research = self.root / 'research'
        shots = []
        for sid, method, frames, raw in [('C01', 'reviewed_endpoints_I2V', 12, 25),
                                         ('C29', 'original_song_A2V', 10, 17),
                                         ('C16', 'existing_reviewed_motion_candidate', 5, None)]:
            shots.append({'id': sid, 'planned_generation': {'method': method, 'editorial_frames': frames,
                                                           'model_frames_8n_plus_1': raw}})
        write(self.root / 'story/shot-plan-v1.json', {'fps': 24, 'shot_count': 3, 'total_frames': 27, 'shots': shots})
        self.bindings = {'schema': 'jml-c-motion-bindings/v1', 'sources': {}, 'shot_sources': {}}
        self.add_job('narrative', 'C01', 25, 10, 'a' * 64)
        self.add_job('performance', 'C29', 17, 20, 'b' * 64)
        self.bind('C01', 'narrative', 12)
        self.bind('C29', 'performance', 10)
        existing = self.root / 'existing.mp4'
        existing.write_bytes(b'existing')
        self.bind('C16', None, 5, existing)
        self.save_bindings()

    def add_job(self, name, sid, frames, elapsed, lock):
        results = self.root / 'assets/motion' / name
        render = {'status': 'complete', 'technical_valid': True, 'generation_seconds': 3,
                  'elapsed_seconds': 8, 'manifest': {'frames': frames, 'fps': 24}}
        write(results / sid / 'render.json', render)
        video = results / sid / 'video-silent.mp4'
        video.write_bytes(name.encode())
        job = {'status': 'bounded_job_complete', 'elapsed_seconds': elapsed, 'execution': name,
               'shots': [{'shot_id': sid, 'status': 'child_complete_unreviewed', 'attempts': 1}]}
        write(results / 'job.json', job)
        write(self.research / (name + '-deployment.json'), {'package_lock_sha256': lock})
        report = {'schema': 'jml-v2-a2v-downloaded-verification/v1' if sid == 'C29' else 'jml-v2-downloaded-batch-verification/v1',
                  'package_lock_sha256': lock, 'job_record_sha256': m.sha(results / 'job.json'),
                  'job_status': 'bounded_job_complete', 'whole_job_seconds': elapsed,
                  'all_takes_technically_verified': True,
                  'takes': [{'shot_id': sid, 'technical_verification': 'pass', 'full_decode_passed': True,
                             'frames': frames, 'fps': 24, 'video_sha256': m.sha(video),
                             'render_sha256': m.sha(results / sid / 'render.json'),
                             'generation_seconds': 3, 'child_seconds': 8}]}
        path = self.research / (name + '-output-verification.json')
        write(path, report)
        return path

    def bind(self, sid, batch, frames, path=None):
        path = path or self.root / 'assets/motion' / batch / sid / 'video-silent.mp4'
        review = self.root / 'review' / (sid + '.md')
        review.parent.mkdir(exist_ok=True)
        review.write_text('Scoped independent source acceptance')
        self.bindings['sources'][sid] = {'kind': 'video', 'path': str(path.relative_to(self.root.parent)),
            'sha256': m.sha(path), 'review': {'status': 'accepted', 'path': str(review.relative_to(self.root.parent)),
            'sha256': m.sha(review), 'accepted_ranges': [[0, frames]]}}
        self.bindings['shot_sources'][sid] = {'id': sid, 'in_frame': 0, 'out_frame_exclusive': frames}

    def save_bindings(self):
        write(self.root / 'tools/editor/motion-bindings.json', self.bindings)
        self.save_current_edit()

    def save_current_edit(self, durations=None):
        plan = json.loads((self.root / 'story/shot-plan-v1.json').read_text())
        cursor = 0
        shots = []
        for shot in plan['shots']:
            sid = shot['id']
            n = (durations or {}).get(sid, shot['planned_generation']['editorial_frames'])
            shots.append({'id': sid, 'start_frame': cursor, 'end_frame_exclusive': cursor + n,
                          'source': self.bindings['shot_sources'].get(sid)})
            cursor += n
        path = self.root / 'tools/editor/edit-current.json'
        write(path, {'fps': 24, 'total_frames': plan['total_frames'], 'shots': shots})
        write(self.root / 'tools/editor/current-edit.json', {'schema': 'jml-c-current-edit/v1',
              'edit': str(path), 'sha256': m.sha(path), 'bound_shots': list(self.bindings['shot_sources'])})

    def test_counts_rejected_work_without_claiming_billing_or_final_film(self):
        self.add_job('narrative-retry', 'C01', 25, 15, 'a' * 64)
        # Same package, genuinely distinct actual job: cost must be counted even though unused.
        before = {str(p): m.sha(p) for p in self.root.rglob('*') if p.is_file()}
        result = m.summarize(self.root)
        self.assertEqual(result['completed_notebook_wall_seconds_sum'], 45)
        self.assertEqual(result['generated_takes'], 3)
        self.assertEqual(result['bindings']['accepted_distinct_new_video_sources'], 2)
        self.assertEqual(result['bindings']['accepted_existing_shots'], 1)
        self.assertIsNone(result['provider_billed_gpu_hours'])
        self.assertIsNone(result['cost']['total_personal_spending_eur'])
        self.assertEqual(result['cost']['existing_included_resources_incremental_cost_eur'], 0)
        self.assertEqual(result['cost']['purchased_Runway_credits_consumed_for_selected_C'], 0)
        self.assertEqual(result['cost']['paid_video_option_ten_complete_films_actual_checkout_cap_eur'], 20)
        self.assertFalse(result['cost']['chat_replenishment_in_paid_video_budget'])
        self.assertFalse(result['bindings']['whole_film_acceptance_established_by_this_tool'])
        self.assertEqual(before, {str(p): m.sha(p) for p in self.root.rglob('*') if p.is_file()})

    def test_duplicate_report_alias_fails_cli_without_printing_total(self):
        shutil.copyfile(self.research / 'narrative-output-verification.json', self.research / 'alias-output-verification.json')
        process = subprocess.run([sys.executable, str(MODULE), '--root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stdout, '')
        self.assertIn('duplicate completion record', process.stderr)

    def test_malformed_or_unfinished_report_is_rejected(self):
        path = self.research / 'narrative-output-verification.json'
        original = json.loads(path.read_text())
        for key, bad in [('whole_job_seconds', float('nan')), ('whole_job_seconds', -1),
                         ('job_status', 'running'), ('all_takes_technically_verified', False)]:
            with self.subTest(key=key, value=bad):
                changed = copy.deepcopy(original)
                changed[key] = bad
                write(path, changed)
                with self.assertRaises(m.EvidenceError):
                    m.summarize(self.root)
        write(path, original)
        changed = copy.deepcopy(original)
        changed['takes'].append(copy.deepcopy(changed['takes'][0]))
        write(path, changed)
        with self.assertRaisesRegex(m.EvidenceError, 'duplicate, missing or reordered'):
            m.summarize(self.root)

    def test_changed_actual_job_and_invented_frame_count_fail(self):
        path = self.research / 'narrative-output-verification.json'
        report = json.loads(path.read_text())
        report['takes'][0]['frames'] = 1000
        write(path, report)
        with self.assertRaisesRegex(m.EvidenceError, 'actual render manifest'):
            m.summarize(self.root)
        report['takes'][0]['frames'] = 25
        write(path, report)
        job = self.root / 'assets/motion/narrative/job.json'
        job.write_text(job.read_text() + ' ')
        with self.assertRaisesRegex(m.EvidenceError, 'actual job bytes missing'):
            m.summarize(self.root)

    def test_unverified_new_binding_and_unreviewed_range_fail(self):
        untracked = self.root / 'untracked.mp4'
        untracked.write_bytes(b'not generated by a counted job')
        self.bind('C01', None, 12, untracked)
        self.save_bindings()
        with self.assertRaisesRegex(m.EvidenceError, 'lacks exact completed take'):
            m.summarize(self.root)
        self.bind('C01', 'narrative', 12)
        self.bindings['sources']['C01']['review']['accepted_ranges'] = [[0, 11]]
        self.save_bindings()
        with self.assertRaisesRegex(m.EvidenceError, 'range not reviewed'):
            m.summarize(self.root)

    def test_running_job_is_not_costed_and_duplicate_json_keys_fail(self):
        write(self.root / 'assets/motion/running/job.json', {'status': 'running', 'elapsed_seconds': 500})
        result = m.summarize(self.root)
        self.assertEqual(result['completed_jobs'], 2)
        self.assertEqual(result['completed_notebook_wall_seconds_sum'], 30)
        path = self.research / 'narrative-output-verification.json'
        path.write_text(path.read_text()[:-1] + ', "whole_job_seconds": 999}')
        with self.assertRaisesRegex(m.EvidenceError, 'duplicate JSON key'):
            m.summarize(self.root)

    def test_adopted_editorial_reallocation_preserves_generation_cost(self):
        before = m.summarize(self.root)
        self.bind('C01', 'narrative', 14)
        self.bind('C29', 'performance', 8)
        self.save_bindings()  # The old current edit still allocates 12/10 frames.
        with self.assertRaisesRegex(m.EvidenceError, 'adopted current edit'):
            m.summarize(self.root)
        self.save_current_edit({'C01': 14, 'C29': 8})
        after = m.summarize(self.root)
        self.assertEqual(after['completed_notebook_wall_seconds_sum'], before['completed_notebook_wall_seconds_sum'])
        self.assertEqual(after['generated_takes'], before['generated_takes'])
        self.assertEqual(after['ten_film_scenarios'], before['ten_film_scenarios'])
        self.assertEqual(after['bindings']['accepted_retained_frames'], 27)
        self.assertEqual(after['editorial_accounting']['changed_editorial_durations']['C01']['adopted_edit_frames'], 14)

    def test_tampered_current_edit_or_gap_cannot_authorize_cost_coverage(self):
        path = self.root / 'tools/editor/edit-current.json'
        value = json.loads(path.read_text())
        value['shots'][1]['start_frame'] += 1
        write(path, value)
        with self.assertRaisesRegex(m.EvidenceError, 'current edit bytes changed'):
            m.summarize(self.root)
        pointer = self.root / 'tools/editor/current-edit.json'
        current = json.loads(pointer.read_text())
        current['sha256'] = m.sha(path)
        write(pointer, current)
        with self.assertRaisesRegex(m.EvidenceError, 'noncontiguous'):
            m.summarize(self.root)


if __name__ == '__main__':
    unittest.main()
