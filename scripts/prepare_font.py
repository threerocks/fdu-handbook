"""Prepare offline fonts from the official Noto Sans CJK SC Regular OTF."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset
import argparse
ROOT=Path(__file__).resolve().parents[1]
args=argparse.ArgumentParser();args.add_argument('font',type=Path,help='Official NotoSansCJKsc-Regular.otf');source=args.parse_args().font
font=TTFont(source)
# CJK radical aliases share glyph IDs with ordinary Han characters. Removing the
# unused aliases prevents Chromium's PDF reverse map from exporting radical codepoints.
for table in font['cmap'].tables:
    if table.isUnicode():
        for code in list(table.cmap):
            if 0x2e80<=code<=0x2fdf or 0xf900<=code<=0xfaff:del table.cmap[code]
font.flavor='woff2';font.save(ROOT/'assets/fonts/noto-sans-sc.woff2')
text=''.join(p.read_text() for p in (ROOT/'chapters').glob('*.md'))
text+=(ROOT/'scripts/create_diagrams.py').read_text()
options=subset.Options();options.flavor='woff2';options.name_IDs=['*'];options.name_languages=['*'];options.notdef_glyph=True
subset_font=subset.load_font(str(source),options)
subsetter=subset.Subsetter(options=options);subsetter.populate(text=text,unicodes=range(32,127));subsetter.subset(subset_font)
subset.save_font(subset_font,str(ROOT/'assets/fonts/fdu-sans.woff2'),options)
print('Prepared full print font and embedded diagram subset')
