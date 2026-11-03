"""Bundle the portable native project and six finished camera-edition exports."""
from pathlib import Path
import json
import zipfile

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'Revision_4'

def main():
    assets={'A01_Approved_Character_Pair.jpg','A02_Approved_Anime_Window.png','Band_Logo_Original.png',
            'S02_Blink.png','P01_Mouth_Closed.png','P01_Open_Vowel.png','P01_Mouth_Round.png',
            'P02_Mouth_Closed.png','P02_Mouth_Narrow.png','P02_Mouth_Round.png'}
    for cut in ['simple','experimental']:
        for sh in json.loads((ROOT/f'camera_shots_{cut}.json').read_text()):
            assets.add(sh['art'])
            if sh.get('vert_art'):assets.add(sh['vert_art'])
    files=[p for p in ROOT.iterdir() if p.suffix in {'.py','.txt','.json','.srt','.ass','.blend'}]
    files += [ROOT/'audio.mp4']+[ROOT/'assets'/name for name in sorted(assets)]
    exports=sorted(OUT.glob('*_Camera.mp4'))
    assert len(exports)==6,len(exports)
    archive=OUT/'Join_Me_in_Life_Camera_Blender.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files:
            assert p.is_file(),p
            compression=zipfile.ZIP_STORED if p.suffix in {'.mp4','.png','.jpg','.jpeg'} else zipfile.ZIP_DEFLATED
            z.write(p,Path('Join_Me_in_Life_Camera_Project')/p.relative_to(ROOT),compress_type=compression)
        for p in exports:z.write(p,Path('Join_Me_in_Life_Camera_Project/exports')/p.name,compress_type=zipfile.ZIP_STORED)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        print('ARCHIVE_VALID',len(z.namelist()),archive.stat().st_size,flush=True)

if __name__=='__main__':main()
