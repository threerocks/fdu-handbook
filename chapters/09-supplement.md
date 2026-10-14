# 补充材料：生产级系统的生成与治理

> 编排说明：原稿末尾提供的 5.2 修订补丁，保留为补充阅读；与第五章正文存在内容重叠。


## 5.2 自动生成带测试套件、安全护栏与治理策略的生产级系统：Product Workbench、RAD 规范栈与 DRS 智能体挽具


在 Process Studio 完成了业务流程的原子级解构、Context Studio 完成了企业专属知识与记忆的编码之后，FDU 面临着最惊险的一跃：如何将这些蓝图和上下文，安全、确定、可重复地转化为客户生产环境中真正跑得起来的智能体与应用，而不会在生产库里酿成“删库跑路”或合规泄密的灾难？

这正是 IBM Consulting Advantage 工程平面（Engineering Plane）的第三大支柱——Product Workbench（产品工作台），配合 RAD（激进应用开发）规范栈与 DRS Agentic Harness（数据重塑套件智能体挽具） 所承担的核心使命：将设计蓝图直接构建为自带自动化测试套件、内置安全护栏（Guardrails）与全生命周期治理策略的生产级系统。


### 一、告别静态文档：用 RAD“机器可读规范栈”驱动 Product Workbench


在传统软件工程中，需求文档（PRD）、设计文档、Jira 工单与测试计划是为“人类阅读”编写的静态参考资料——一旦决策变更，文档往往滞后，不同开发人员对同一句话的不同理解更是造成了海量的返工（Rework）。

在 FDU 的工程体系中，IBM 引入了 Radical Application Development（激进应用开发，简称 RAD），在代码仓库与 CI/CD 流水线之上增加了一层结构化的“持久上下文层”，用规范文件夹（The Spec Folder）作为人类与智能体共同遵循的唯一事实来源：

**RAD（激进应用开发）十层机器可读交付技术栈**

| 项目 | 说明 |
| --- | --- |
| 1. Human Intent (人类意图) | 明确业务愿景、目标成果与优先级排序 |
| 2. Context Studio (上下文工作室) | 沉淀产品决策与企业术语的持久化记忆底座 |
| 3. research.md (调研与论证) | 记录“为什么要构建该系统”的底层逻辑与依据 |
| 4. quickstart.md (快速启动规范) | 定义技术路线、架构选型与环境约束条件 |
| 5. spec.md (需求与范围规范) | 消除一切歧义，精确定义“到底要构建什么” |
| 6. plan.md (交付规划) | 制定系统架构连接方式与“如何构建”的工程路径 |
| 7. tasks.md (原子执行步) | 拆解可直接供智能体领取执行的原子级任务清单 |
| 8. Agent Execution (智能体执行) | 智能体自动生成代码、测试与配置，人类验证把关 |
| 9. workflow-state.md (实时状态流) | 实时追踪已完成项、进行中项与阻塞点（Blockers） |
| 10. Continuous Learning (持续学习) | 捕获每次执行洞察，反哺下一次迭代实现复利提升 |



当这套规范文件准备就绪后，Mohamad Ali 描述的自动化场景便开始上演：Process Studio 与 Product Workbench 自动输出构建智能体所需的全部规格说明书（Specs），包括连接器（Connectors）与 MCP（Model Context Protocol，模型上下文协议）服务器规范；随后将这些规范一键推入集成好的编码引擎（如 OpenAI Codex、Anthropic Claude Code 或 IBM 自研的 Project Bob），在底层编码挽具（Coding Harness）的约束下，直接批量生成智能体代码、集成接口与配套测试套件。


### 二、超越聊天机器人：用 DRS Agentic Harness 的“四大声明式支柱”与“九步复利闭环”锁死执行确定性


为什么普通的对话式 AI（Conversational AI）不能直接放进客户的生产环境？正如 IBM 咨询 CTO 兼端到端智能体 AI 负责人 Vishal Anand 所指出的：聊天机器人可以回答问题、写一段代码建议，但它无法走进客户真实的云账户、真实的网络和生产系统里，在零容忍静默失败（Zero tolerance for a silent failure）的严苛约束下，日复一日地给出确定性、可重复的执行结果。

为此，FDU 在底层架构中装备了 DRS Agentic Harness（智能体执行挽具），将“执行 AI（Execution AI）”建立在四大声明式支柱（Four Declarative Pillars）之上：

1. 声明式编写（AUTHOR declaratively）：提供一站式 UI-CLI 体验与内置 GitOps 推拉管控；在任何智能体触碰真实生产系统之前，团队必须通过门禁式编写（Gated authoring）明确声明“允许智能体做什么、绝不允许做什么”。
2. 声明式路由（ROUTE declaratively）：挽具根据当前执行任务的复杂程度，自动选择最匹配的底层模型（原生支持跨 ICA、AWS、Azure 的 Claude Code、IBM Bob 以及 OpenAI Codex，且模型层完全可插拔替换），无需在每次更换模型或任务变更时重写业务逻辑。
3. 声明式治理（GOVERN declaratively）：将自动化门禁（Automated gates）、安全评分（Security scoring）与全量审计追踪（Audit trail）内生嵌入每一次编写动作与运行过程中，而非事后补救。
4. 声明式复利（COMPOUND declaratively）：每一次安全扫描、运行、学习与认证都会向前馈送，将执行历史从“用完即丢的日志文件”转化为“越用越快、越用越省 Token 的增值资产”。

在具体运行中，每一个智能体任务都必须穿过一条严密受控的“九步自动化复利闭环（Nine-Stage Automated Compounding Loop）”：

自动安全扫描 (Auto-security scan) → 自动运行 (Auto-run) → 自动学习 (Auto-learn) → 自动经验捕获 (Auto-experience / EEP) → 自动认证 (Auto-certify) → 自动度量 (Auto-measure) → 自动验证 (Auto-verify) → 自动晋升 (Auto-promote) → 复用 (Reuse)

在这条闭环中，系统通过执行经验协议（Execution Experience Protocol, EEP）捕获智能体在真实环境中的行为表现，并通过实时重探测协议（Live Re-Probe Protocol, LRP）持续重新验证确定性自动化结果，确保任何智能体输出必须先通过开发环境（Dev）、测试环境（Test）与用户验收测试（UAT）的层层认证关卡，才能晋升进入生产环境（Production）。


### 三、独立的控制平面护栏、ADLC 全生命周期管理与“数字员工持证上岗”


当智能体真正进入生产环境后，FDU 还会通过 IBM watsonx Orchestrate 控制平面与 IBM Operate for AI 体系，为其套上三层动态安全护栏与治理策略：

- 与智能体本体解耦的独立安全护栏（Guardrails）：在 IBM Consulting Advantage 与 watsonx Orchestrate 中，安全护栏是独立于智能体本体之外进行实现与集中管理的。当提示词中出现个人身份信息（PII）时，系统会实时向顾问发出警报；同时内置护栏会实时检测输出偏见（Output bias），拦截提示词注入（Prompt injection）等恶意攻击，并确保智能体严格运行在客户现有的安全边界与访问控制权限之内——没有任何特殊特权、没有任何例外，客户的 CISO（首席信息安全官）甚至不需要为此额外审批一套新的控制平面。
- 遵循 ADLC（智能体开发生命周期）的持续观测与评测：IBM 联合 Anthropic 提出了 AI 智能体开发生命周期（Agent Development Lifecycle, ADLC） 标准。通过统一仪表盘，团队可以跨多个运行环境追踪智能体的处理流、LLM 调用历史、Token 消耗成本（FinOps）与响应延迟，并利用 LLM 自动生成多轮对话序列对智能体的工具调用准确率、RAG 回答精度进行定量与定性评估（AgentOps）。
- 联合培生（Pearson）推出“数字员工技能认证体系”：最具开创性的是，IBM 与全球教育与认证巨头 Pearson 达成深度合作，将原本用于认证人类专业技能的体系引入到了数字员工身上。在智能体触碰客户真实生产数据之前，IBM Consulting Advantage 中的数字员工会定期自动连接 Pearson 的认证验证工具进行技能考核并获取“数字徽章（Badges）”，确保持证上岗的每一个智能体都经过了严格的技术与可信度验证。
