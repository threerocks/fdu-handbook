"""Diagram Design HTML sources, following its architecture, flowchart and layer grammars."""
from pathlib import Path
from html import escape
import json,base64
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/diagrams'
INK='#102451'; BLUE='#003fff'; MUTED='#526178'; RULE='#cbd4e2'

def label(x,y,text,kind='name',anchor='start'):
    return f'<text x="{x}" y="{y}" class="{kind}" text-anchor="{anchor}">{escape(text)}</text>'
def box(x,y,w,h,title,details=(),focal=False):
    stroke=BLUE if focal else RULE; fill='#edf2ff' if focal else '#fff'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}"/>'+label(x+16,y+28,title)+''.join(label(x+16,y+52+i*20,t,'sub') for i,t in enumerate(details))
def arrow(path,dashed=False):
    return f'<path d="{path}" fill="none" stroke="{MUTED}" stroke-width="1.5" '+('stroke-dasharray="5 4" ' if dashed else '')+'marker-end="url(#arrow)"/>'
def save(slug,title,desc,body,height=440):
    svg=f'<svg viewBox="0 0 720 {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc"><title id="{slug}-title">{escape(title)}</title><desc id="{slug}-desc">{escape(desc)}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="{MUTED}"/></marker></defs><rect width="720" height="{height}" fill="#fff"/>'+label(40,48,title,'title')+body+f'<line x1="40" y1="{height-48}" x2="680" y2="{height-48}" stroke="{RULE}"/>'+label(40,height-24,'依据本书相应章节绘制 · 实线：主流程 / 支撑 · 虚线：反馈','sub')+'</svg>'
    html=f'''<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>body{{margin:0;padding:24px;background:#fff;color:{INK};font-family:system-ui,'PingFang SC',sans-serif}}.frame{{max-width:960px;min-width:0;margin:auto}}.diagram-container{{width:100%;overflow-x:auto}}svg{{display:block;width:100%;min-width:720px}}text{{fill:{INK};font-family:system-ui,'PingFang SC','Microsoft YaHei',sans-serif}}.title{{font-size:28px;font-family:Georgia,'Songti SC',serif;font-weight:400}}.name{{font-size:12px;font-weight:600}}.sub{{font-size:12px;font-weight:400;fill:{MUTED}}}@media print{{body{{padding:0}}.diagram-container{{overflow:visible}}svg{{min-width:0}}}}</style></head><body><main class="frame"><div class="diagram-container">{svg}</div></main></body></html>'''
    (OUT/f'{slug}.html').write_text(html)

save('01-inner-outer','局部提速如何变成企业结果','内挽具提高个人生产，外挽具负责跨流程的评审、治理、部署与反馈。',
    '<rect x="272" y="92" width="408" height="232" rx="8" fill="#f4f7fc" stroke="#cbd4e2"/>'+label(292,116,'外挽具：跨生命周期的协调与治理')+
    arrow('M 236 212 H 292')+arrow('M 448 212 H 496')+arrow('M 588 272 V 344 Q 588 352 580 352 H 144 Q 136 352 136 344 V 272',True)+
    box(40,152,196,120,'内挽具：个人任务加速',['IDE / 编码助手 / 单点智能体','更快地产生代码与文档'],True)+box(292,152,156,120,'组织交付系统',['审查、测试与集成','上下文、安全与治理'])+box(496,152,164,120,'企业业务结果',['投产、使用与持续运营','质量、周期与商业回报']))

save('04-team','人类在两端，智能体在中间','客户成果负责人对结果负责，前端定义上下文，数字员工执行，后端验证并反馈。',
    arrow('M 236 128 H 148 Q 140 128 140 136 V 192')+arrow('M 484 128 H 568 Q 576 128 576 136 V 192')+arrow('M 228 256 H 272')+arrow('M 448 256 H 492')+arrow('M 584 328 V 368 Q 584 376 576 376 H 140 Q 132 376 132 368 V 328',True)+
    box(236,88,248,80,'客户成果负责人',['端到端业务结果 / ROI / QBR'],True)+box(40,192,188,136,'前端人类专家',['领域专家 + 前线架构师','框定问题、重构流程','策划上下文、定义合格标准'])+box(272,192,176,136,'专业数字员工',['需求、代码与测试','扫描缺陷、挖掘流程','按项目配置智能体队伍'])+box(492,192,188,136,'后端人类专家',['FDE + 数据设计师','应用 AI 专家','验证质量、治理与调优']),height=456)

save('05-engineering','工程平面：从现场资料到生产系统','Process Studio 解构流程，Context Studio 编码上下文，Product Workbench 生成应用及测试。',
    arrow('M 360 152 V 176')+arrow('M 360 252 V 276')+arrow('M 360 352 V 376')+
    box(100,88,520,64,'客户原始输入',['SOP、历史文档、系统日志、业务术语表'])+box(100,176,520,76,'01  Procedure Eater + Process Studio',['拆分原子流程；区分代码、智能体与人；输出 TOM 与 Specs'])+box(100,276,520,76,'02  Context Studio',['编码企业术语、架构标准与历史决策；形成持久上下文'])+box(100,376,520,76,'03  Product Workbench + 编码智能体',['根据规范与上下文生成应用、接口、测试、护栏和治理配置'],True),height=536)

names=['1  自动安全扫描','2  自动执行','3  自动学习','4  经验捕获 / EEP','5  自动认证','6  自动度量','7  自动验证','8  自动晋升','9  资产复用']
coords=[(40,100),(276,100),(512,100),(512,208),(276,208),(40,208),(40,316),(276,316),(512,316)]
paths=['M 208 136 H 276','M 444 136 H 512','M 596 172 V 208','M 512 244 H 444','M 276 244 H 208','M 124 280 V 316','M 208 352 H 276','M 444 352 H 512']
body=''.join(arrow(p) for p in paths)+arrow('M 596 388 V 416 Q 596 424 588 424 H 24 Q 16 424 16 416 V 92 Q 16 84 24 84 H 116 Q 124 84 124 92 V 100',True)
body+=''.join(box(x,y,168,72,name,[],i==6) for i,((x,y),name) in enumerate(zip(coords,names)))
body+=label(40,456,'EEP 捕获真实执行经验；LRP 持续重探测，结果经测试与 UAT 后晋升。','sub')
save('05-harness','执行不是终点：九步受控复用','九步按序连接，资产复用反馈到下一次扫描；验证是晋升生产环境的前提。',body,height=536)

body=''
levels=[('L1','AI 辅助','人类负责决策与执行'),('L2','工作流嵌入','执行界定清晰的单一任务'),('L3','受控委派','人类处理权限边界与异常'),('L4','多智能体协同','跨多步骤流程规划与协作'),('L5','自编排与自优化','按异常管理，持续治理结果')]
for i,(level,name,desc) in enumerate(levels):
    y=88+i*64
    body+=f'<rect x="72" y="{y}" width="608" height="56" fill="'+('#edf2ff' if i==2 else '#f7f9fc')+f'" stroke="{RULE}"/>'+label(88,y+32,level)+label(144,y+32,name)+label(368,y+32,desc,'sub')
body+=arrow('M 48 108 V 380')
save('05-autonomy','自治需要分级演进','从辅助到自编排，逐步扩大自主范围；依据流程风险和数据就绪度推进。',body,height=472)

body=''.join(arrow(f'M 132 {y+64} V {y+88}') for y in [88,176,264,352])
steps=[('内部先行','把自己作为 Client Zero，先验证业务效果'),('底座筑基','建立工程平台、上下文、评测与护栏'),('小队重组','组成常设 Pod，把绩效对齐业务成果'),('渐进演进','分级自治，每次交付沉淀双价值流'),('生态扩展','共建、共验、复用，分摊行业验证成本')]
for i,(name,desc) in enumerate(steps):body+=box(76,88+i*88,580,64,f'{i+1:02}  {name}',[desc],i==0)
save('07-roadmap','中国落地：先验证，再扩展','五步顺序连接内部验证、平台、小队、渐进演进和行业生态。',body,height=584)
print('6 Diagram Design HTML sources created')
