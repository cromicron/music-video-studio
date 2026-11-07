"""Offline transport/integrity checks. These do not prove neural action quality."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('v2_prepare_batch', HERE / 'prepare_batch.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def png(path, color):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)
    data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB',16,9,8,2,0,0,0))
    data += chunk(b'IDAT', zlib.compress((b'\0' + bytes(color) * 16) * 9)) + chunk(b'IEND', b'')
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


class StagingChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.film = self.root / 'film'; self.film.mkdir()
        first = png(self.film / 'first.png', (0, 0, 0)); last = png(self.film / 'last.png', (20, 40, 60))
        (self.film / 'review.md').write_text('Synthetic input-integrity fixture, not an artistic acceptance.\n')
        self.plan = json.loads((HERE / 'batch-template.json').read_text())
        self.plan['state'] = 'ready_for_local_staging'
        take = self.plan['takes'][0]
        take['start_image'] = {'path':'first.png','sha256':first}
        take['end_image'] = {'path':'last.png','sha256':last}
        take['source_review'] = {'path':'review.md','sha256':builder.sha256(self.film/'review.md'),'status':'pass'}
        take['prompt'] = 'A synthetic test action.'
        take['editorial']['segments'][0].update(shot_id='CA01', timeline_frames=[0,156])
        story={'test_fixture_only':True,'shots':[{'id':'CA01','start_frame':0,'end_frame_exclusive':156,'planned_generation':{'method':'reviewed_endpoints_I2V','fps':24,'model_frames_8n_plus_1':169,'source_keeper_range':[6,162],'head_handle_frames':6,'tail_handle_frames':7}}]}
        self.story=self.film/'unfinished-morning/story/shot-plan-v1.json';self.story.parent.mkdir(parents=True);self.story.write_text(json.dumps(story))
        self.plan['story_plan_sha256']=builder.sha256(self.story)


    def tearDown(self):
        self.tmp.cleanup()

    def stage(self, plan=None, name='bundle'):
        plan_path = self.root / (name + '-plan.json')
        plan_path.write_text(json.dumps(plan or self.plan))
        return builder.prepare(plan_path, self.root/name, film=self.film)

    def test_distinct_endpoints_reach_unchanged_runner_and_private_notebook(self):
        result = self.stage(); bundle=Path(result['bundle'])
        manifest = json.loads((bundle/'CA01.json').read_text())
        self.assertNotEqual(manifest['start_image_sha256'],manifest['end_image_sha256'])
        for name in ('runtime.py','run.py','bootstrap.py','model-lock.json','source-lock.json','patches.json'):
            self.assertEqual((bundle/name).read_bytes(),(builder.BASE/name).read_bytes())
        metadata=json.loads((Path(result['kernel'])/'kernel-metadata.json').read_text())
        self.assertIs(metadata['is_private'],True)
        self.assertEqual(metadata['dataset_sources'],[self.plan['dataset_id']])
        self.assertFalse(list(bundle.rglob('__pycache__')))
        self.assertFalse((bundle/'vendor/wangp-source.zip').exists())
        self.assertTrue((bundle/'vendor/wangp-source.zip.b64').exists())
        with self.assertRaises(ValueError): self.stage()

    def test_draft_and_unreviewed_sources_cannot_stage(self):
        draft=copy.deepcopy(self.plan);draft['state']='draft'
        with self.assertRaises(ValueError):self.stage(draft)
        draft=copy.deepcopy(self.plan);draft['takes'][0]['source_review']['status']='pending'
        with self.assertRaises(ValueError):self.stage(draft)
        self.assertFalse((self.root/'bundle').exists())

    def test_changed_source_bytes_fail_before_bundle_exists(self):
        (self.film/'last.png').write_bytes(b'changed')
        with self.assertRaises(ValueError):self.stage()
        self.assertFalse((self.root/'bundle').exists())

    def test_same_endpoint_and_duplicate_source_interval_are_rejected(self):
        same=copy.deepcopy(self.plan);same['takes'][0]['end_image']=same['takes'][0]['start_image']
        with self.assertRaises(subprocess.CalledProcessError):self.stage(same,'same')
        repeated=copy.deepcopy(self.plan)
        repeated['takes'][0]['editorial']['segments'].append({'shot_id':'repeat','source_frames':[6,40],'timeline_frames':None})
        with self.assertRaises(ValueError):self.stage(repeated,'repeat')

    def test_post_staging_tamper_fails_actual_child(self):
        result=self.stage();bundle=Path(result['bundle'])
        (bundle/'inputs/CA01-end_image.png').write_bytes(b'changed')
        run=subprocess.run([sys.executable,str(bundle/'run.py'),'--manifest',str(bundle/'CA01.json'),'--validate-only'],capture_output=True,text=True)
        self.assertNotEqual(run.returncode,0)
        self.assertIn('integrity mismatch',run.stderr)

    def test_stale_story_and_shifted_keeper_rejected_before_output(self):
        stale=copy.deepcopy(self.plan);stale['story_plan_sha256']='0'*64
        keeper=copy.deepcopy(self.plan);keeper['takes'][0]['editorial']['segments'][0]['source_frames']=[7,163]
        for index,plan in enumerate([stale,keeper]):
            name='stale-'+str(index)
            with self.assertRaisesRegex(ValueError,'story plan|adopted shot'):self.stage(plan,name)
            self.assertFalse((self.root/name).exists())
        self.story.write_text(self.story.read_text()+'\n')
        with self.assertRaisesRegex(ValueError,'stale adopted'):self.stage(name='mutated-story')
        self.assertFalse((self.root/'mutated-story').exists())

    def test_long_or_retimed_take_fails_actual_child(self):
        longer=copy.deepcopy(self.plan);longer['takes'][0]['frames']=233
        with self.assertRaises(ValueError):self.stage(longer,'longer')
        retimed=copy.deepcopy(self.plan);retimed['takes'][0]['editorial']['segments'][0]['timeline_frames']=[0,200]
        with self.assertRaises(ValueError):self.stage(retimed,'retimed')


if __name__=='__main__':
    unittest.main(verbosity=2)
