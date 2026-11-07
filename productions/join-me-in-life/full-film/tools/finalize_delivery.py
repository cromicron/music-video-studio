#!/usr/bin/env python3
"""Finalize a reviewed render without changing video/audio packet payloads.

The explicit, hash-bound acceptance record is editorial evidence supplied by the
studio owner/agent after outside reviews; this tool does not judge motion.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def packets(path):
    raw = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_packets', '-show_data_hash', 'sha256',
        '-show_entries', 'packet=stream_index,pts_time,dts_time,duration_time,data_hash',
        '-of', 'json', str(path)], text=True)
    # Container interleaving may change during remux; per-stream timing/payloads may not.
    return sorted(json.loads(raw)['packets'],
                  key=lambda p: (p['stream_index'], float(p['dts_time'])))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', required=True, type=Path)
    ap.add_argument('--render-manifest', required=True, type=Path)
    ap.add_argument('--acceptance', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    source, output = args.input.resolve(), args.output.resolve()
    if source == output or output.exists() or output.with_suffix('.manifest.json').exists():
        raise ValueError('Use a new output; existing files are preserved')
    candidate = json.loads(args.render_manifest.read_text())
    accepted = json.loads(args.acceptance.read_text())
    source_hash = digest(source)
    if source_hash != candidate['output_sha256'] or source_hash != accepted['candidate_sha256']:
        raise ValueError('Review/render/source hash mismatch')
    if accepted['status'] != 'accepted_for_delivery' or accepted['blocking_findings']:
        raise ValueError('Delivery requires an explicit acceptance with no unresolved blocking finding')
    if not candidate['coverage']['full_song'] or candidate['frames'] != 6667:
        raise ValueError('This delivery requires the complete Join Me in Life picture')
    expected_tools = ['ChatGPT image generation', 'Owned LTX system', 'FFmpeg']
    # The S003 crop is an LTX source processed with the same selected FFmpeg tool.
    # Normalize only this known compound provenance label; unknown tools still fail.
    labels = candidate['actual_picture_production_tools']
    aliases = {'Owned LTX system; fixed derivative crop through FFmpeg': 'Owned LTX system'}
    actual_tools = list(dict.fromkeys(aliases.get(label, label) for label in labels))
    if actual_tools != expected_tools:
        raise ValueError('The free delivery must use the selected three creative tools')
    for review in accepted['reviews']:
        path = ROOT / review['path']
        if digest(path) != review['sha256']:
            raise ValueError(f'Changed review: {review["path"]}')
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        'ffmpeg', '-v', 'error', '-n', '-i', str(source), '-map', '0:v:0', '-map', '0:a:0',
        '-c', 'copy', '-movflags', '+faststart', '-metadata', 'title=Join Me in Life',
        '-metadata', 'artist=Mercy in Minor', '-metadata',
        'comment=Complete hybrid music video. Original song; reviewed generated motion, supplied footage, drawing exposures and deliberate camera passages.',
        str(output)], check=True)
    source_packets, output_packets = packets(source), packets(output)
    if source_packets != output_packets:
        raise ValueError('Final remux changed packet payloads or timing; do not deliver')
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(output), '-f', 'null', '-'], check=True)
    result = dict(candidate)
    result.update(status='COMPLETED HYBRID MUSIC VIDEO — studio delivery acceptance',
                  output=str(output), output_sha256=digest(output),
                  production_tools_status='All three selected creative tools contributed to the accepted full picture; supplied historical material retains its separate provenance.',
                  three_tool_completed_video_requirement_met=True,
                  actual_picture_production_tools=actual_tools,
                  renderer_provenance_labels=labels,
                  tool_label_normalization=aliases,
                  reviewed_candidate_sha256=source_hash,
                  acceptance={'path': str(args.acceptance.resolve()), 'sha256': digest(args.acceptance)},
                  finalization={'method': 'Metadata-only stream-copy remux',
                                'packet_payloads_and_timestamps_identical': True,
                                'compared_packets': len(output_packets), 'full_decode': 'passed'},
                  review=accepted['verification_scope'])
    output.with_suffix('.manifest.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'output': str(output), 'sha256': result['output_sha256'],
                      'bytes': output.stat().st_size, 'packet_identity': True}, indent=2))


if __name__ == '__main__':
    main()
