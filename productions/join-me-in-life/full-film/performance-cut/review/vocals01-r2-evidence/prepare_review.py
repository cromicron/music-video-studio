#!/usr/bin/env python3
"""Reuse the retained pilot's streamed, source-bound inspection-aid generator."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
PLAN = BASE / 'story/shot-plan-v1.json'
EXPECTED_PLAN_SHA = '420d9e7c086b028f716eff2e90fc0bad093de36c8da508560febb89aeace3b6e'
assert hashlib.sha256(PLAN.read_bytes()).hexdigest() == EXPECTED_PLAN_SHA
retained = HERE.parent / 'motion-pilot01-evidence/prepare_review.py'
spec = importlib.util.spec_from_file_location('retained_pilot_inspection', retained)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.HERE = HERE
regions = {
    'B05A': {'face-mouth': [280, 0, 350, 320],
              'mic-contact': [250, 120, 270, 300],
              'free-hand': [400, 325, 270, 180]},
    'B05B': {'face-mouth': [235, 0, 450, 370],
              'mic-contact': [160, 180, 360, 330]},
    'B08A': {'face-mouth': [220, 0, 340, 310],
              'mic-contact': [170, 95, 300, 330],
              'free-hand': [485, 290, 355, 215]},
    'B08B': {'face-mouth': [230, 0, 460, 380],
              'mic-contact': [275, 180, 300, 330]},
}
shots = {s['id']: s for s in json.loads(PLAN.read_text())['shots']}
module.SETTINGS = {
    sid: {'raw': shots[sid]['planned_generation']['model_frames_8n_plus_1'],
          'first': shots[sid]['planned_generation']['source_keeper_range'][0],
          'last': shots[sid]['planned_generation']['source_keeper_range'][1],
          'master': [shots[sid]['start_frame'], shots[sid]['end_frame_exclusive']],
          'regions': value}
    for sid, value in regions.items()
}

if __name__ == '__main__':
    module.main()
