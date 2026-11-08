#!/usr/bin/env python3
"""Run the retained strict renderer; all original source gates remain enforced."""
from pathlib import Path
import runpy

ENGINE = Path(__file__).resolve().parents[2] / 'revision-2/tools/editor/strict_edit.py'
if __name__ == '__main__':
    runpy.run_path(str(ENGINE), run_name='__main__')
