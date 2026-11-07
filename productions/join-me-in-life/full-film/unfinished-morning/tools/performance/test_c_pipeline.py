"""C wrapper integrity tests. Synthetic review fixtures never authorize production."""
import ast,copy,hashlib,importlib.util,json,pathlib,subprocess,sys,tempfile,types,unittest,wave
from unittest.mock import patch
import prepare_bundle as builder

HERE=pathlib.Path(__file__).resolve().parent
class CPerformance(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory(prefix='c-a2v-test-only-',dir=builder.REPO/'build');cls.root=pathlib.Path(cls.tmp.name)
  old=json.loads((builder.FILM/'revision-2/tools/performance/plan-v1.json').read_text())
  cls.plan=copy.deepcopy(old);cls.plan.update(schema='jml-c-performance-plan/v1',queue_id='CTEST',dataset_id='darionalis/jml-c-test-only-inputs',kernel_id='darionalis/jml-c-test-only',dataset_title='C TEST ONLY',kernel_title='C TEST ONLY')
  for take,sid,frames in zip(cls.plan['takes'],['CTEST1','CTEST2'],[97,129]):
   take['shot_id']=sid;take['frames']=frames
   # Fixtures exercise exact mechanics only; these are not creative-review evidence.
   review={'test_fixture_only':True,'pairs':[{'shot':sid,'verdict':'PASS_STATIC_SOURCE_FOR_BOUNDED_MOTION_TEST','panels':['fixture']}], 'inspection':{'native_review_crops':[{'panel':'fixture','native_pixels_viewed':True,'sha256':take['image']['sha256']}]}}
   path=cls.root/(sid+'-synthetic-review.json');path.write_text(json.dumps(review))
   take['source_review']={'path':str(path.relative_to(builder.REPO)),'sha256':builder.sha(path),'panel':'fixture'}
   take['timeline_frames']=[4989,5070] if sid=='CTEST1' else [5070,5183]
  cls.original_adopted=builder.ADOPTED_STORY
  fixture=[]
  for take in cls.plan['takes']:
   first,last=take['timeline_frames']; frames=take['frames']; start=first-6
   fixture.append({'id':take['shot_id'],'start_frame':first,'end_frame_exclusive':last,'planned_generation':{'method':'original_song_A2V','fps':24,'model_frames_8n_plus_1':frames,'source_keeper_range':[6,6+last-first],'head_handle_frames':6,'tail_handle_frames':frames-(6+last-first),'original_audio':{'sample_rate':48000,'source_frame_start':start,'source_samples':[start*2000,(start+frames)*2000]}}})
  builder.ADOPTED_STORY=cls.root/'synthetic-story.json';builder.ADOPTED_STORY.write_text(json.dumps({'test_fixture_only':True,'shots':fixture}))
  cls.plan['story_plan_sha256']=builder.sha(builder.ADOPTED_STORY)
  cls.plan_path=cls.root/'plan.json';cls.plan_path.write_text(json.dumps(cls.plan))
  cls.report=builder.prepare(cls.root/'bundle',cls.plan_path);cls.bundle=pathlib.Path(cls.report['bundle'])
  spec=importlib.util.spec_from_file_location('c_validation_fixture',HERE/'validation_v2.py');cls.validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.validator)
  cls.manifests=[json.loads((cls.bundle/(sid+'.json')).read_text()) for sid in ['CTEST1','CTEST2']]
 @classmethod
 def tearDownClass(cls):
  builder.ADOPTED_STORY=cls.original_adopted;cls.tmp.cleanup()
 def test_original_pcm_every_sample_and_extent(self):
  pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(builder.MASTER),'-f','s16le','-acodec','pcm_s16le','-'])
  for m in self.manifests:
   with wave.open(str(self.bundle/m['audio']),'rb') as w:actual=w.readframes(w.getnframes())
   start=(m['editorial']['timeline_frames'][0]-6)*2000;end=start+m['frames']*2000
   self.assertEqual(actual,pcm[start*4:end*4]);self.assertEqual(len(actual),m['frames']*2000*4)
   self.validator.validate_manifest(m,self.bundle)
 def test_exact_frozen_manifest_and_queue_reject_tampering(self):
  for m in self.manifests:
   for delta in [{'frames':121},{'audio_sha256':'0'*64},{'prompt':m['prompt']+' altered'},{'end_image':'x.png'},{'seed':50}]:
    bad=dict(m,**delta)
    with self.assertRaises(ValueError):self.validator.validate_manifest(bad,self.bundle)
  q=json.loads((self.bundle/'queue.json').read_text());self.validator.validate_queue(q,self.bundle)
  for manifests in [['V2-36.json'],list(reversed(q['manifests'])),q['manifests']*2]:
   with self.assertRaises(ValueError):self.validator.validate_queue(dict(q,manifests=manifests),self.bundle)
 def test_runtime_neural_code_pins_and_process_methods_unchanged(self):
  for name in ['runtime.py','model-lock.json','source-lock.json','patches.json','requirements.txt']:
   self.assertEqual((self.bundle/name).read_bytes(),(builder.BASE/name).read_bytes())
  def funcs(p):return {n.name:ast.dump(n) for n in ast.parse(p.read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
  for name,names in [('run.py',['preflight']),('bootstrap.py',['run_bounded','torch_constraints','install_environment'])]:
   before,after=funcs(builder.BASE/name),funcs(self.bundle/name)
   for n in names:self.assertEqual(before[n],after[n])
 def test_true_backend_audio_shape_and_short_coverage_guard(self):
  import torch
  # Use retained real backend with its published coverage patch; no inference/download.
  common_spec=importlib.util.spec_from_file_location('c_fixture_common',builder.BASE/'common.py');common=importlib.util.module_from_spec(common_spec);common_spec.loader.exec_module(common)
  backend=self.root/'backend';common.prepare_backend(self.bundle,backend)
  tree=ast.parse((backend/'models/ltx2/ltx2.py').read_text());statements=None
  for node in ast.walk(tree):
   if isinstance(node,ast.If):
    for i,item in enumerate(node.orelse):
     if isinstance(item,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='target_frames' for t in item.targets):statements=node.orelse[i:]
  self.assertIsNotNone(statements);code=compile(ast.fix_missing_locations(ast.Module(body=statements,type_ignores=[])),'<real-coverage>','exec')
  m=types.ModuleType('isolated_c_types')
  with patch.dict(sys.modules,{m.__name__:m}):exec(compile((backend/'models/ltx2/ltx_core/types.py').read_text(),'<real-shapes>','exec'),m.__dict__)
  class Full:
   def __init__(self,latent,strength):self.shape=tuple(latent.shape);self.strength=strength
  for frames,expected in [(97,101),(113,118),(129,134)]:
   target=m.AudioLatentShape.from_video_pixel_shape(m.VideoPixelShape(batch=1,frames=frames,height=512,width=896,fps=24));self.assertEqual(target.frames,expected)
   for count in [expected-1,expected,expected+1]:
    ns={'target_shape':target,'audio_latent':torch.zeros(1,8,count,16),'audio_strength':1.,'self':types.SimpleNamespace(),'json':json,'AudioConditionByLatent':Full}
    if count<expected:
     with self.assertRaisesRegex(ValueError,'prefix fallback forbidden'):exec(code,ns)
    else:exec(code,ns);self.assertTrue(ns['self']._jml_audio_coverage['full_coverage']);self.assertEqual(ns['audio_conditionings'][0].shape[2],expected)
 def test_old_destination_and_unbounded_lengths_rejected_before_staging(self):
  for change in [{'kernel_id':'darionalis/jml-story-v2-old'},{'queue_id':'V2OLD'}]:
   plan=dict(self.plan,**change);path=self.root/'bad-plan.json';path.write_text(json.dumps(plan))
   with self.assertRaises(ValueError):builder.prepare(self.root/'never-created',path)
  for frames in [True,137,225]:
   plan=copy.deepcopy(self.plan);plan['takes'][0]['frames']=frames;path=self.root/'bad-plan.json';path.write_text(json.dumps(plan))
   with self.assertRaises(ValueError):builder.prepare(self.root/'never-created',path)
  self.assertFalse((self.root/'never-created').exists())
 def test_stale_story_and_shifted_timing_fail_before_output(self):
  stale=copy.deepcopy(self.plan);stale['story_plan_sha256']='0'*64
  shifted=copy.deepcopy(self.plan);shifted['takes'][0]['timeline_frames']=[4990,5071]
  wrong_length=copy.deepcopy(self.plan);wrong_length['takes'][0]['frames']=105
  for index,plan in enumerate([stale,shifted,wrong_length]):
   path=self.root/('bad-story-'+str(index)+'.json');path.write_text(json.dumps(plan));out=self.root/('story-reject-'+str(index))
   with self.assertRaisesRegex(ValueError,'story plan|adopted shot'):builder.prepare(out,path)
   self.assertFalse(out.exists())
 def test_private_mount_and_no_retry_and_all_locked_files(self):
  meta=json.loads((pathlib.Path(self.report['kernel'])/'kernel-metadata.json').read_text());self.assertTrue(meta['is_private']);self.assertEqual(meta['dataset_sources'],[self.plan['dataset_id']])
  queue=json.loads((self.bundle/'queue.json').read_text());self.assertEqual(queue['automatic_retries'],0);self.assertEqual(queue['provider_cap_seconds'],5400)
  for name,expected in json.loads((self.bundle/'package-lock.json').read_text())['files'].items():self.assertEqual(builder.sha(self.bundle/name),expected)
  self.assertFalse(list(self.bundle.rglob('__pycache__')))

if __name__=='__main__':unittest.main(verbosity=2)
