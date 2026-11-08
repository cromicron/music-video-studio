#!/usr/bin/env python3
"""Build a portable reference book from the hash-bound original image assets."""
import hashlib
import json
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

PACK = Path(__file__).resolve().parent
ROOT = PACK.parents[1]


def main():
    manifest = json.loads((PACK / 'manifest.json').read_text())
    pages = manifest['pages']
    for page in pages:
        source = ROOT / page['file']
        with source.open('rb') as stream:
            actual = hashlib.file_digest(stream, 'sha256').hexdigest()
        if actual != page['sha256'] or source.stat().st_size != page['bytes']:
            raise ValueError(f"Source changed; reconcile its review first: {page['file']}")
    output = PACK / 'Mercy_in_Minor_Anime_Band_Reference_Book.pdf'
    width, height = landscape(A4)
    canvas = Canvas(str(output), pagesize=(width, height), pageCompression=1)
    canvas.setTitle('Mercy in Minor - Anime Band Reference Book')
    canvas.setAuthor('Mercy in Minor studio')
    canvas.setSubject('Character, costume, instrument and stage consistency references')
    for number, page in enumerate(pages, 1):
        canvas.setFillColor(HexColor('#f6f3ec'))
        canvas.rect(0, 0, width, height, fill=1, stroke=0)
        canvas.setFillColor(HexColor('#162330'))
        canvas.rect(0, height - 75, width, 75, fill=1, stroke=0)
        canvas.setFillColor(HexColor('#a6c6cb'))
        canvas.setFont('Helvetica', 9)
        canvas.drawString(28, height - 23, 'MERCY IN MINOR  /  ANIME BAND REFERENCE PACK  /  V1')
        canvas.setFillColor(HexColor('#ffffff'))
        canvas.setFont('Helvetica-Bold', 18)
        canvas.drawString(28, height - 51, page['title'])
        source_width, source_height = page['dimensions']
        box_width, box_height = width - 56, height - 130
        scale = min(box_width / source_width, box_height / source_height)
        image_width, image_height = source_width * scale, source_height * scale
        x = (width - image_width) / 2
        y = 44 + (box_height - image_height) / 2
        assert x >= 28 and y >= 44 and y + image_height <= height - 86
        canvas.drawImage(ImageReader(str(ROOT / page['file'])), x, y,
                         width=image_width, height=image_height, mask='auto')
        canvas.setFillColor(HexColor('#344752'))
        canvas.setFont('Helvetica', 8)
        canvas.drawString(28, 26, page['caption'])
        canvas.setFillColor(HexColor('#66747b'))
        canvas.setFont('Helvetica', 7)
        canvas.drawString(28, 12, 'Static reference collection. Shot-specific playing contact and timing are checked during animation.')
        canvas.drawRightString(width - 28, 12, f'{number:02d} / {len(pages):02d}')
        canvas.bookmarkPage(page['id'])
        canvas.addOutlineEntry(page['title'], page['id'], level=0)
        canvas.showPage()
    canvas.save()
    record = {
        'pages': len(pages), 'output': str(output.relative_to(ROOT)),
        'bytes': output.stat().st_size,
        'sha256': hashlib.file_digest(output.open('rb'), 'sha256').hexdigest(),
        'manifest_sha256': hashlib.file_digest((PACK / 'manifest.json').open('rb'), 'sha256').hexdigest(),
        'method': 'Whole original images embedded with aspect preserved; no source-image editing or cropping',
        'all_source_hashes_verified': True, 'all_image_bounds_inside_page': True,
    }
    (PACK / 'book-build.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record))


if __name__ == '__main__':
    main()
