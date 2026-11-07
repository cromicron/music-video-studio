#!/usr/bin/env python3
"""Prepare private hardware-test input/notebook files locally; never upload or run."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
from zipfile import ZipFile, ZIP_DEFLATED

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[2]
REPO = FILM.parents[2]
spec = importlib.util.spec_from_file_location('v2_prepare', HERE.parent/'production/prepare_batch.py')
production = importlib.util.module_from_spec(spec); spec.loader.exec_module(production)


def read(path): return json.loads(Path(path).read_text())
def save(path, data): Path(path).write_text(json.dumps(data, indent=2)+'\n')
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stage(destination):
    originals = [
        {'role': 'A', 'old': 'V2H01', 'new': 'V2WH01', 'frames': 169,
         'bundle': 'build/jml-story-v2-handoff-a-private-v1', 'plan': 'handoff-a-v1.json',
         'lock': '8b964d858e2a9ada24214430c320afaf1d223c8c4a9533a1c915e468c119b445'},
        {'role': 'B', 'old': 'V2C01', 'new': 'V2WC01', 'frames': 193,
         'bundle': 'build/jml-story-v2-chair-rise-a-private-v1', 'plan': 'chair-rise-a-v1.json',
         'lock': 'b5370c051537237abc1d73aea33ab40f2199d50e12291c444567723269087c06'}]
    takes, bindings = [], []
    for item in originals:
        original_bundle = REPO/item['bundle']
        if sha(original_bundle/'package-lock.json') != item['lock']:
            raise ValueError('Original frozen bundle changed: '+item['old'])
        frozen = read(original_bundle/(item['old']+'.json'))
        plan = read(HERE.parent/'production/plans'/item['plan'])
        take = copy.deepcopy(next(t for t in plan['takes'] if t['take_id'] == item['old']))
        if take['frames'] != frozen['frames'] or frozen['frames'] != item['frames'] or take['prompt'] != frozen['prompt']:
            raise ValueError('Selected original motion parameters changed')
        for side in ('start_image', 'end_image'):
            if take[side]['sha256'] != frozen[side+'_sha256'] or sha(original_bundle/frozen[side]) != take[side]['sha256']:
                raise ValueError('Selected exact endpoint changed')
        take['take_id'] = item['new']; takes.append(take)
        bindings.append({**item, 'original_manifest_sha256': sha(original_bundle/(item['old']+'.json')),
                         'prompt_sha256': hashlib.sha256(frozen['prompt'].encode()).hexdigest(),
                         'start_image_sha256': frozen['start_image_sha256'], 'end_image_sha256': frozen['end_image_sha256'],
                         'neural_changes': [], 'bookkeeping_change': 'New experiment take/queue IDs and matching provenance paths only'})
    plan = {'schema': 'jml-v2-action-batch/v1', 'state': 'ready_for_local_staging', 'privacy': 'private',
            'queue_id': 'V2WARMAB', 'dataset_id': 'darionalis/jml-story-v2-warm-ab-inputs',
            'dataset_title': 'JML Story V2 Warm AB Inputs', 'kernel_id': 'darionalis/jml-story-v2-warm-ab',
            'kernel_title': 'JML Story V2 Warm AB', 'takes': takes}
    plan_path = HERE/'experiment-plan.json'
    if plan_path.exists() and read(plan_path) != plan:
        raise ValueError('Frozen experiment plan differs; review before replacing it')
    if not plan_path.exists(): save(plan_path, plan)
    result = production.prepare(plan_path, destination)
    bundle, kernel, archive = Path(result['bundle']), Path(result['kernel']), Path(result['zip'])
    for name in ('warm_batch.py', 'binding-lock.json', 'experiment_child.py', 'experiment_driver.py', 'compare_experiment.py'):
        shutil.copy2(HERE/name, bundle/name)
    experiment = {'schema': 'jml-warm-hardware-experiment/v1', 'privacy': 'private', 'whole_job_seconds': 5400,
        'automatic_retries': 0, 'production_promotion': False, 'takes': ['V2WH01', 'V2WC01'],
        'cold_order': [{'label': 'cold-A', 'take_id': 'V2WH01'}, {'label': 'cold-B', 'take_id': 'V2WC01'}],
        'warm_order': [{'label': 'A1', 'take_id': 'V2WH01'}, {'label': 'B', 'take_id': 'V2WC01'},
                       {'label': 'A2', 'take_id': 'V2WH01'}], 'planned_generations': 5,
        'equality': 'exact_context_and_raw_rgb_hashes', 'maximum_warm_to_cold_time_ratio': 0.8,
        'permitted_repeated_A_allocated_memory_growth_bytes': [0, 0],
        'original_frozen_sources': bindings,
        'scheduling': 'Root/ops only, after initial motion results. Chair action test has priority; preserve unrelated queued work and at most two account GPU batch jobs.'}
    save(bundle/'experiment.json', experiment)
    for item in bindings:
        frozen = read(REPO/item['bundle']/(item['old']+'.json'))
        candidate = read(bundle/(item['new']+'.json'))
        for key in ('seed', 'width', 'height', 'fps', 'frames', 'start_frame_index', 'end_frame_index', 'prompt',
                    'start_image_sha256', 'end_image_sha256', 'start_image_dimensions', 'end_image_dimensions',
                    'supplied_audio', 'model_audio_output'):
            if candidate[key] != frozen[key]: raise ValueError('Neural input changed: '+key)
    lock = read(bundle/'package-lock.json')
    lock['files'] = {str(p.relative_to(bundle)): sha(p) for p in sorted(bundle.rglob('*'))
                     if p.is_file() and p.name not in ('dataset-metadata.json', 'package-lock.json') and '__pycache__' not in p.parts}
    lock['experimental_addition'] = 'Fixed cold-A/cold-B/warm-A-B-A driver and sealed conditioning cache. Runtime/model pins unchanged; no production promotion.'
    save(bundle/'package-lock.json', lock)
    notebook = read(kernel/'private-diagnostic.ipynb')
    notebook['cells'][0]['source'] = [
        '# Join Me in Life — private warm-cache equivalence experiment\n',
        'Fixed reviewed H01(169frames) and C01(193frames). Cache setup; fresh cold A/B; warm A→B→A. '
        'Exact context/raw-RGB comparison, no retry or automatic promotion. One90-minute cap including setup.\n']
    notebook['cells'][1]['source'] = [
        'from pathlib import Path\n', 'import subprocess\n', 'import sys\n',
        "candidates = [Path('/kaggle/input/jml-story-v2-warm-ab-inputs'), Path('/kaggle/input/datasets/darionalis/jml-story-v2-warm-ab-inputs')]\n",
        "found = [p for p in candidates if (p / 'package-lock.json').is_file()]\n",
        "if len(found) != 1: raise RuntimeError('Attach the exact PRIVATE warm-AB inputs once')\n",
        "subprocess.run([sys.executable, str(found[0] / 'experiment_driver.py'), '--bundle', str(found[0]), '--seconds', '5400'], check=True, timeout=5460)\n",
        "print('Experiment ended. Preserve all results; no production promotion or automatic retry.')\n"]
    save(kernel/'private-diagnostic.ipynb', notebook)
    subprocess.run([sys.executable, str(bundle/'experiment_driver.py'), '--bundle', str(bundle), '--validate-only'], check=True)
    for pycache in bundle.rglob('__pycache__'): shutil.rmtree(pycache)
    # The initial archive was local staging only; preserve it as the pre-experiment
    # base, then produce the complete experiment archive under a distinct name.
    base_archive = archive.with_name(archive.stem+'-base.zip')
    archive.rename(base_archive)
    with ZipFile(archive, 'x', ZIP_DEFLATED) as zipped:
        for path in sorted(bundle.rglob('*')):
            if path.is_file(): zipped.write(path, str(path.relative_to(bundle)))
    result.update(state='prepared_locally_not_uploaded_or_submitted', package_lock_sha256=sha(bundle/'package-lock.json'),
        zip_sha256=sha(archive), experiment_sha256=sha(bundle/'experiment.json'),
        planned_generations=5, root_scheduling_required=True, original_sources=bindings,
        verification_command='python3 tools/kaggle_verify_bundle.py --bundle '+str(bundle)+
            ' --evidence EVIDENCE_DIR --expected-lock '+sha(bundle/'package-lock.json')+' --notebook-version 1',
        hardware_validation_performed=False)
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--report', required=True, type=Path)
    args = p.parse_args()
    result = stage(args.output)
    save(args.report, result)
    print(json.dumps(result, indent=2))
