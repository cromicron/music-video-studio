#!/usr/bin/env python3
"""Exact unused C05 tail native keeper/song aids, not story acceptance."""
from pathlib import Path
import importlib.util
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('retained_pilot_source_aids',HERE.parent/'motion-pilot01-evidence/prepare_review.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.HERE=HERE/'inspection';m.HERE.mkdir(exist_ok=True)
m.SETTINGS={'C05TAIL':{'raw':225,'first':118,'last':218,'master':[3424,3524],'regions':{'girl-face':[520,45,240,245],'girl-hand-table':[470,345,320,160]}}}
if __name__=='__main__':m.main()
