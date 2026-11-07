#!/usr/bin/env python3
"""Create a local upload directory/ZIP; never upload or create an account."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[1]
PRODUCTION = FILM.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    destination = args.output.resolve()
    if destination.exists():
        raise SystemExit('Choose a new output directory; existing bundles are preserved')
    destination.mkdir(parents=True)
    for name in ['ltx_kaggle.py', 'bootstrap.py', 'requirements.txt', 'model-lock.json', 'NOTICE.md', 'LICENSE.creator.txt']:
        shutil.copy2(HERE / name, destination / name)
    # Flat files avoid ambiguous automatic unpacking of nested Kaggle folders.
    assets = destination
    sources = {
        'window.png': FILM / 'assets/her_window_refined_candidate.png',
        'bridge_start.png': FILM / 'assets/bridge_plea_start_candidate.png',
        'bridge_end.png': PRODUCTION / 'art/04_Performance/P03_Bridge_Plea.png',
    }
    hashes = {}
    for name, source in sources.items():
        shutil.copy2(source, assets / name)
        hashes[name] = hashlib.sha256(source.read_bytes()).hexdigest()
    common = {'width': 864, 'height': 480, 'frames': 121, 'fps': 30, 'seeds': [49, 73, 169]}
    manifest = {
        'schema': 'jml-ltx-kaggle/v1', 'privacy': 'private', 'mode': 'pilot',
        'notes': 'Six planned follow-up takes; separate pilot.json contains exactly one first take. All motion remains unreviewed.',
        'shots': [
            {**common, 'shot_id': 'S003_window_pilot', 'image': 'window.png',
             'image_sha256': hashes['window.png'],
             'prompt': 'A detailed hand-drawn anime close-up. The auburn-haired woman sits beside the dark window, her gaze lowered. One shallow breath gently lifts her shoulder, then settles. Her eyelids soften briefly. She remains quietly withdrawn in the same side profile. Her lips remain closed and her head stays supported above her shoulders. The reflected face follows her exactly. Locked camera, consistent drawn lines, blue evening light.',
             'review_focus': ['head direction', 'reflection agreement', 'identity', 'shoulder continuity', 'intentional breathing', 'no comforting expression']},
            {**common, 'shot_id': 'S044_bridge_pilot', 'image': 'bridge_start.png',
             'image_sha256': hashes['bridge_start.png'], 'end_image': 'bridge_end.png',
             'end_image_sha256': hashes['bridge_end.png'],
             'prompt': 'A detailed hand-drawn anime performance shot. The frightened singer keeps his microphone against his open mouth. His free forearm extends once from beside his abdomen into the pleading final pose. His elbow opens smoothly and his palm rotates upward, with five coherent fingers and unchanged rings. His shoulders remain grounded, his eyes distressed. He holds the finished reach. Locked camera, consistent stage lighting and clothing.',
             'review_focus': ['all five digits', 'ring continuity', 'wrist rotation', 'supported shoulder', 'microphone contact', 'screamed plea throughout', 'start/end identity'],
             'source_risk': 'Independent still review could not certify all occluded starting fingers; intermediate frames must resolve them coherently.'}
        ]}
    (destination / 'pilot-suite.json').write_text(json.dumps(manifest, indent=2) + '\n')
    first = {**manifest, 'notes': 'Exactly one representative start/end bridge gesture; stop for playback review.',
             'shots': [{**manifest['shots'][1], 'seeds': [49]}]}
    (destination / 'pilot.json').write_text(json.dumps(first, indent=2) + '\n')
    (destination / 'dataset-metadata.json').write_text(json.dumps({
        'title': 'Join Me in Life private LTX pilot inputs',
        'id': 'darionalis/jml-ltx-private-pilot-inputs',
        'licenses': [{'name': 'other'}],
        'description': 'Private project artwork and owned pilot code. Do not publish or enable public sharing.'
    }, indent=2) + '\n')
    kernel = destination.with_name(destination.name + '-kernel')
    if kernel.exists():
        raise SystemExit('Choose a new output directory; companion kernel directory already exists')
    kernel.mkdir()
    for name in ['private-pilot.ipynb', 'kernel-metadata.json']:
        shutil.copy2(HERE / name, kernel / name)
    archive = destination.with_suffix('.zip')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as file:
        for path in sorted(destination.rglob('*')):
            if path.is_file():
                file.write(path, path.relative_to(destination))
    print(json.dumps({'directory': str(destination), 'kernel_directory': str(kernel), 'zip': str(archive),
                      'zip_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                      'privacy': 'LOCAL ONLY; upload as a private dataset and verify visibility',
                      'song_included': False, 'source_images': len(sources)}, indent=2))


if __name__ == '__main__':
    main()
