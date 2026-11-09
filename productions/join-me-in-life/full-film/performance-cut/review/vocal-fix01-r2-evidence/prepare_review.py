#!/usr/bin/env python3
"""Reuse retained source-bound inspection for two actual supported-mic repairs."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
plan = BASE / 'story/shot-plan-v1.json'
assert hashlib.sha256(plan.read_bytes()).hexdigest() == '420d9e7c086b028f716eff2e90fc0bad093de36c8da508560febb89aeace3b6e'
spec = importlib.util.spec_from_file_location('retained_repair_inspection',
    HERE.parent / 'motion-pilot01-evidence/prepare_review.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.HERE = HERE
shots = {s['id']: s for s in json.loads(plan.read_text())['shots']}
regions = {
    'B05B': {'mouth-face': [350, 150, 200, 180],
              'mic-support': [150, 220, 300, 200]},
    'B08A': {'mouth-face': [375, 105, 200, 200],
              'mic-support': [160, 190, 300, 210]},
}
module.SETTINGS = {
    sid: {'raw': 113, 'first': 6,
          'last': shots[sid]['planned_generation']['source_keeper_range'][1],
          'master': [shots[sid]['start_frame'], shots[sid]['end_frame_exclusive']],
          'regions': region}
    for sid, region in regions.items()
}

if __name__ == '__main__':
    module.main()
