"""One-time import of the supplied manuscript; chapter Markdown is maintained thereafter."""
from pathlib import Path
import hashlib, json, re
ROOT=Path(__file__).resolve().parents[1]
if any((ROOT/'chapters').glob('*.md')):
    raise SystemExit('章节已存在；首次导入脚本禁止覆盖维护中的 Markdown。')
source=ROOT/'source/完整原稿.md'
lines=source.read_text().splitlines()
# These spans are interrupted duplicates or chat scaffolding, not missing prose.
excluded=[(286,316,'5.2 截断版本及续写说明；采用第 317 行起的完整版本'),(592,606,'7.2 截断版本及续写说明；采用第 608 行起的完整版本'),(780,783,'附录的编辑提示，补充正文从第 784 行保留')]
spans=[('00-guide',1,28),('01-bottlenecks',29,90),('02-fde-limits',91,135),('03-paradigm',136,177),('04-fdu-anatomy',178,255),('05-operation',256,512),('06-cases',513,561),('07-china',562,747),('08-next-frontier',748,779),('09-supplement',784,len(lines))]
manifest=[]; source_fragments=[]

def format_tsv(block):
    header=block[0].split('\t'); rows=[]; row=[]
    if header[0]=='客户名称与所属行业':
        for index in range(1,len(block),2):
            cells=block[index+1].split('\t'); assert len(cells)==len(header)
            cells[0]=block[index]+'<br>'+cells[0]; rows.append(cells)
        return '\n'.join(['| '+' | '.join(header)+' |','| '+' | '.join(['---']*len(header))+' |']+['| '+' | '.join(cells)+' |' for cells in rows])
    for text in block[1:]:
        first=text.split('\t')[0].strip()
        starts_row='\t' in text and (not row or len('\n'.join(row).split('\t')) == len(header))
        if starts_row and row:
            rows.append('\n'.join(row).split('\t')); row=[]
        row.append(text)
    if row: rows.append('\n'.join(row).split('\t'))
    for cells in rows:
        assert len(cells)==len(header),(header,cells)
    def cell(t):return t.replace('|','&#124;').replace('\n','<br>')
    return '\n'.join(['| '+' | '.join(map(cell,header))+' |','| '+' | '.join(['---']*len(header))+' |']+['| '+' | '.join(map(cell,row))+' |' for row in rows])

for slug,start,end in spans:
    selected=[(n,lines[n-1]) for n in range(start,end+1) if not any(a<=n<=b for a,b,_ in excluded)]
    title=selected[0][1] if slug!='09-supplement' else '补充材料：生产级系统的生成与治理'
    output=['# '+title,'']
    if slug[:2] in [f'{i:02}' for i in range(1,9)]:output += [f'![第 {int(slug[:2])} 章封面](../assets/covers/{slug[:2]}.png)','']
    if slug=='09-supplement':output+=['> 编排说明：原稿末尾提供的 5.2 修订补丁，保留为补充阅读；与第五章正文存在内容重叠。','']
    pos=0 if slug=='09-supplement' else 1
    while pos<len(selected):
        number,text=selected[pos]; stripped=text.strip()
        if not stripped: output.append(''); pos+=1;continue
        if '\t' in text:
            block=[]
            while pos<len(selected) and selected[pos][1].strip():
                block.append(selected[pos][1]);source_fragments.append([selected[pos][0],selected[pos][1]]);pos+=1
            output += [format_tsv(block),''];continue
        if re.match(r'^[+┌=][─=\-]{5,}',stripped):
            block=[]
            while pos<len(selected) and (selected[pos][1].strip() or (number==188 and selected[pos][0]<=212)):
                block.append(selected[pos][1]);pos+=1
            output+=['<details class="source-diagram">','<summary>原稿示意图（文字版）</summary>','','```text','\n'.join(block),'```','','</details>',''];continue
        source_fragments.append([number,text])
        if re.match(r'^\d+\.\d+\s',stripped) or stripped.startswith(('序言：','导读与手册指南')):
            output += ['','## '+stripped,'']
        elif re.match(r'^(第[一二三四五六七八九十]+[关步]：|[一二三四五六七八九十]+、)',stripped):output += ['','### '+stripped,'']
        elif stripped.startswith('【') and stripped.endswith('】'):output+=['','### '+stripped,'']
        elif stripped.startswith('⚬'):
            indent=len(text)-len(text.lstrip()); output += [' '*(2 if indent>=4 else 0)+'- '+stripped[1:].strip()]
        elif stripped.startswith('•'):output+=['- '+stripped[1:].strip()]
        elif stripped.startswith('$$'):
            labels=re.findall(r'\\text\{([^}]+)\}',stripped)
            output+=[' → '.join(labels) if labels else stripped]
        else:output.append(text.replace('\\rightarrow','→'))
        pos+=1
    if slug=='07-china':
        body='\n'.join(output).replace('在欧美市场，正如 IBM 咨询高级副总裁','### 第一关：采购招投标与审计体制的刚性约束\n\n在欧美市场，正如 IBM 咨询高级副总裁')
    else:body='\n'.join(output)
    (ROOT/'chapters'/f'{slug}.md').write_text(body.rstrip()+'\n')
    manifest.append({'slug':slug,'title':title,'source_lines':[start,end],'characters':len(body)})
(ROOT/'book.json').write_text(json.dumps({'title':'从 FDE 到 FDU：重新定义 AI 交付','date':'2026-10-14','chapters':manifest},ensure_ascii=False,indent=2)+'\n')
(ROOT/'source/import-ledger.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'excluded_spans':excluded,'retained_spans':spans,'normalizations':['标题层级与列表标记','制表符表格转 Markdown 表格；单元格原文保留','原稿字符示意图收进可展开文字版；配图另行解释机制','\\rightarrow 转可见箭头','封面使用简短章名；正文章名完整保留'],'source_fragments':source_fragments},ensure_ascii=False,indent=2)+'\n')
print('Imported',len(manifest),'Markdown chapters and editorial ledger')
