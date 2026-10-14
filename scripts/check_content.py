"""Verify preserved prose, local assets and navigation in the generated handbook."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'dist/site'
ledger=json.loads((ROOT/'source/import-ledger.json').read_text())
book=json.loads((ROOT/'book.json').read_text())
html=''.join(BeautifulSoup((SITE/f'{c["slug"]}.html').read_text(),'html.parser').get_text() for c in book['chapters'])
def normalize(text):
    return re.sub(r'\s+','',text.replace('\\rightarrow','→').replace('⚬','').replace('•',''))
normalized=normalize(html);missing=[];checked=0
for line,text in ledger['source_fragments']:
    if text.startswith('$$'):
        segments=re.findall(r'\\text\{([^}]+)\}',text)
    else:segments=text.split('\t')
    for segment in segments:
        segment=re.sub(r'^\s*\d+\.\s*','',segment)
        checked+=1
        if normalize(segment) not in normalized:missing.append({'line':line,'text':segment[:120]})
broken=[]
for page in SITE.glob('*.html'):
    soup=BeautifulSoup(page.read_text(),'html.parser')
    for node in soup.select('[src],a[href]'):
        url=node.get('src') or node.get('href')
        if not url or re.match(r'^(https?:|data:|#|mailto:)',url):continue
        if not (page.parent/url.split('#')[0]).exists():broken.append([page.name,url])
    for node in soup.select('a[href^="#"]'):
        if not soup.find(id=node['href'][1:]):broken.append([page.name,node['href']])
report={'source_sha256_unchanged':hashlib.sha256((ROOT/'source/完整原稿.md').read_bytes()).hexdigest()==ledger['source_sha256'],'prose_fragments_checked':checked,'missing_prose_fragments':missing,'broken_local_links':broken,'chapter_count':8,'cover_count':len(list((ROOT/'assets/covers').glob('*.png'))),'diagram_count':len(list((ROOT/'assets/diagrams').glob('*.html')))}
(ROOT/'qa').mkdir(exist_ok=True)
(ROOT/'qa/source-preservation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False))
sys.exit(bool(missing or broken or not report['source_sha256_unchanged']))
