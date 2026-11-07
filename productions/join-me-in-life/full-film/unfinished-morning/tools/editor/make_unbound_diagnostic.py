#!/usr/bin/env python3
"""Make an explicitly unbound exact-song review clip; never modify the edit ledger."""
import argparse
from array import array
import math
import sys
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

FULL_FILM = Path(__file__).resolve().parents[3]
REPO = FULL_FILM.parents[2]
C_ROOT = FULL_FILM / 'unfinished-morning'
engine_spec = importlib.util.spec_from_file_location('c_strict_editor', FULL_FILM / 'revision-2/tools/editor/strict_edit.py')
ed = importlib.util.module_from_spec(engine_spec)
engine_spec.loader.exec_module(ed)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def exact_trim_waveform(song, output, start_sample, end_sample):
    """Compare to fully decoded original samples, avoiding input MP3 seek rounding."""
    def pcm(path, trim=None):
        cmd = ['ffmpeg', '-v', 'error', '-i', str(path)]
        if trim:
            cmd += ['-af', trim]
        raw = subprocess.check_output(cmd + ['-vn', '-ac', '1', '-ar', '4000', '-f', 'f32le', '-'])
        values = array('f'); values.frombytes(raw)
        if sys.byteorder != 'little':
            values.byteswap()
        return values
    a = pcm(song, f'atrim=start_sample={start_sample}:end_sample={end_sample},asetpts=PTS-STARTPTS')
    b = pcm(output)
    def corr(lag, stride=1):
        a0, b0 = max(0, -lag), max(0, lag)
        n = min(len(a)-a0, len(b)-b0)
        xs, ys = a[a0:a0+n:stride], b[b0:b0+n:stride]
        den = math.sqrt(sum(x*x for x in xs)*sum(y*y for y in ys))
        return sum(x*y for x,y in zip(xs,ys))/den if den else 0
    lag = max(range(-400,401,10), key=lambda v: corr(v,40))
    lag = max(range(lag-10,lag+11), key=lambda v: corr(v,10))
    return {'sample_rate':4000, 'correlation':corr(lag), 'offset_seconds':lag/4000,
            'source_samples':len(a), 'output_samples':len(b),
            'reference_method':'Full MP3 decode, exact 48kHz sample trim, then 4kHz float mono conversion; no input seek.',
            'note':'Technical waveform alignment only, lossy AAC allowed; no subjective listening or phoneme-sync claim.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--shot', required=True)
    ap.add_argument('--story', type=Path, default=C_ROOT / 'story/shot-plan-v1.json')
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--expected-sha', required=True)
    ap.add_argument('--source-in', type=int, required=True)
    ap.add_argument('--source-out', type=int, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    source, output = a.source.resolve(), a.output.resolve()
    ed.require(source.is_relative_to(REPO) and source.is_file(), 'Source must be a local repository video')
    ed.require(output.is_relative_to(REPO), 'Diagnostic output must stay within the repository workspace')
    ed.require(not output.exists() and not output.with_suffix('.json').exists(), 'Preserve existing diagnostics')
    ed.require(sha(source) == a.expected_sha, 'Source SHA differs from requested actual take')
    story = json.loads(a.story.read_text())
    ed.require(story['fps'] == 24 and story['total_frames'] == 6667, 'Original song timeline required')
    shots = [s for s in story['shots'] if s['id'] == a.shot]
    ed.require(len(shots) == 1, 'Unknown or duplicated shot ID')
    shot = shots[0]
    lo, hi = shot['start_frame'], shot['end_frame_exclusive']
    count = hi - lo
    timing = ed.source_timing(source)
    ed.require(0 <= a.source_in < a.source_out <= timing['frames'], 'Keeper exceeds decoded natural-24fps source')
    ed.require(a.source_out - a.source_in == count, 'Keeper does not fill exact story slot')
    song = FULL_FILM.parent / 'full-song/track-49.mp3'
    ed.require(sha(song) == ed.SONG_SHA256, 'Original song changed')
    audio_stream = next(s for s in ed.legacy.probe(song)['streams'] if s['codec_type'] == 'audio')
    ed.require(int(audio_stream['sample_rate']) == 48000 and int(audio_stream['channels']) == 2, 'Diagnostic expects original 48kHz stereo source')
    output.parent.mkdir(parents=True, exist_ok=True)
    video = (f'[0:v]trim=start_frame={a.source_in}:end_frame={a.source_out},settb=1/24000,setpts=N*1000,'
             'scale=1920:1080:force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos,'
             'pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,setsar=1,format=yuv420p[v];')
    audio = f'[1:a]atrim=start_sample={lo*2000}:end_sample={hi*2000},asetpts=PTS-STARTPTS[a]'
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-n','-i',str(source),'-i',str(song),
           '-filter_complex_threads','1','-filter_complex',video+audio,'-map','[v]','-map','[a]',
           '-c:v','libx264','-preset','veryfast','-crf','18','-threads','3','-r','24','-fps_mode','cfr',
           '-video_track_timescale','24000','-c:a','aac','-b:a','256k','-movflags','+faststart',
           '-metadata',f'title=Unfinished Morning — {a.shot} unbound diagnostic',str(output)]
    subprocess.run(cmd,check=True)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True)
    decoded = ed.source_timing(output)
    ed.require(decoded['frames'] == count, 'Output lost or added frames')
    legacy_waveform = ed.legacy.waveform_check(song,output,lo/24,count/24)
    waveform = exact_trim_waveform(song,output,lo*2000,hi*2000)
    ed.require(waveform['correlation'] >= .995 and abs(waveform['offset_seconds']) <= .03, 'Original-song alignment failed')
    record = {'schema':'jml-c-unbound-diagnostic/v1','state':'UNBOUND_CANDIDATE_FOR_INDEPENDENT_REVIEW',
              'shot':a.shot,'file':str(output.relative_to(REPO)),'sha256':sha(output),
              'source':{'file':str(source.relative_to(REPO)),'sha256':a.expected_sha,'range':[a.source_in,a.source_out]},
              'master_range':[lo,hi],'fps':24,'story_sha256':sha(a.story),'decode':decoded,'waveform':waveform,'legacy_seek_waveform':legacy_waveform,
              'original_audio':{'sha256':ed.SONG_SHA256,'sample_range':[lo*2000,hi*2000],'sample_rate':48000},
              'motion_accepted':False,'binding_ledger_modified':False,
              'scope':'Technical complete clip for independent motion/acting review, not source/cut acceptance. No stills, holds, repeats, retiming or generated audio.',
              'reproduction':cmd}
    output.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'shot':a.shot,'file':record['file'],'sha256':record['sha256'],'frames':count,'waveform':waveform}))


if __name__ == '__main__':
    main()
