"""Export Diagram Design HTML and embed a font in the portable SVG copies."""
from pathlib import Path
import argparse,base64,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--helper',type=Path,default=Path.home()/'.codex/skills/diagram-design/scripts/export_svg.py')
helper=parser.parse_args().helper
if not helper.exists():raise SystemExit('请先安装 Diagram Design，或使用 --helper 指定其 export_svg.py。')
font64=base64.b64encode((ROOT/'assets/fonts/fdu-sans.woff2').read_bytes()).decode()
font_css='@font-face{font-family:"FDU Sans";src:url(data:font/woff2;base64,'+font64+') format("woff2");font-weight:100 900;}text{font-family:"FDU Sans",sans-serif!important;font-variant-ligatures:none!important}'
for html in sorted((ROOT/'assets/diagrams').glob('*.html')):
    subprocess.run(['python3',str(helper),str(html),'--system-fonts'],check=True)
    svg=html.with_suffix('.svg');text=svg.read_text()
    # Add @font-face after upstream selector scoping; @-rules cannot be element-prefixed.
    text=text.replace('</style>',font_css+'</style>',1)
    svg.write_text(text)
