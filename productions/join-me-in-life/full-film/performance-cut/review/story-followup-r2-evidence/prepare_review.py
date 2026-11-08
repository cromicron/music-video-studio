#!/usr/bin/env python3
"""Actual O03/O04 source inspection using retained pilot streamed-frame workflow."""
import importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
old=HERE.parent/'motion-pilot01-evidence/prepare_review.py'
spec=importlib.util.spec_from_file_location('retained_pilot_source_aids',old)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.HERE=HERE/'inspection';m.HERE.mkdir(exist_ok=True)
m.SETTINGS={
'O03':{'raw':145,'first':6,'last':139,'master':[4856,4989], 'regions':{'face-eyes':[410,65,245,250],'hand-cup':[495,375,255,130]}},
'O04':{'raw':209,'first':6,'last':196,'master':[6477,6667], 'regions':{'face-eyes-tears':[400,65,255,265],'hand-cup':[490,375,300,130]}}
}
if __name__=='__main__':m.main()
