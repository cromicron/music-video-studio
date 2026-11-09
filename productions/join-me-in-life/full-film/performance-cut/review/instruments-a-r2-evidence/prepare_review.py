#!/usr/bin/env python3
"""Prepare source-bound instrument selections, including both disjoint B06 uses."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent
provider = BASE / 'story/shot-plan-v1.json'
editorial = BASE / 'story/editorial-plan-v2.json'
assert hashlib.sha256(provider.read_bytes()).hexdigest() == '420d9e7c086b028f716eff2e90fc0bad093de36c8da508560febb89aeace3b6e'
assert hashlib.sha256(editorial.read_bytes()).hexdigest() == 'f76d8065d1970a22652910f667267d7b5d5c26c809f445dea4a36459f6524075'
retained = HERE.parent / 'motion-pilot01-evidence/prepare_review.py'
spec = importlib.util.spec_from_file_location('retained_instrument_inspection', retained)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.HERE = HERE
regions = {
    'B02': {'right-picking': [370, 200, 130, 120],
            'left-fretting': [475, 130, 125, 125]},
    'B06_A': {'right-picking': [300, 370, 160, 135],
              'left-fretting': [550, 230, 155, 170]},
    'B06_B': {'right-picking': [300, 370, 160, 135],
              'left-fretting': [550, 230, 155, 170]},
    'B07': {'right-plucking': [355, 200, 135, 120],
            'left-fretting': [475, 120, 125, 135]},
    'B11': {'right-plucking': [265, 335, 150, 165],
            'left-fretting': [525, 205, 155, 160]},
}
generation = {s['id']: s for s in json.loads(provider.read_text())['shots']}
shots = {s['id']: s for s in json.loads(editorial.read_text())['shots']}
module.SETTINGS = {}
for sid, value in regions.items():
    shot = shots[sid]
    recipe = shot['planned_source']
    raw = generation[recipe['generation_id']]['planned_generation']['model_frames_8n_plus_1']
    module.SETTINGS[sid] = {
        'raw': raw, 'first': recipe['in_frame'], 'last': recipe['out_frame_exclusive'],
        'master': [shot['start_frame'], shot['end_frame_exclusive']], 'regions': value,
    }

if __name__ == '__main__':
    module.main()
