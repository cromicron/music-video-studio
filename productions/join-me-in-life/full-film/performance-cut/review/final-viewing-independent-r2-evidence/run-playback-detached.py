from pathlib import Path
import runpy,json,traceback,datetime,sys
D=Path(__file__).resolve().parent
try:
 runpy.run_path(str(D/'playback.py'),run_name='__main__')
except BaseException as exc:
 (D/'playback-error-v1.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'type':type(exc).__name__,'error':str(exc),'traceback':traceback.format_exc()},indent=2)+'\n')
 raise
