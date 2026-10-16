#!/usr/bin/env python3
"""胖东来专供版站点文案改写：index.html + 0ccz6j2vqtl32.js 同步替换。
内容对齐《胖东来专供版简历》(lyl-v10-AIGC中台版.pen, x=11200 三页)。
用法: python3 pdl_content.py   (在 site-mirror-pdl/ 目录下运行)
"""
import re, sys

HTML = 'index.html'
CHUNK = '_next/static/chunks/0ccz6j2vqtl32.js'

html = open(HTML, encoding='utf-8').read()
chunk = open(CHUNK, encoding='utf-8').read()

report = []

# ---------- 1) 中英成对数据 (zh/en 对象) ----------
# (旧zh, 旧en, 新zh, 新en)
PAIRS = [
    # ABOUT ME 六卡
    ('独立操盘「孙武 Fleet」虚拟员工平台从规划到上线验收,交付厨电客户方太,10+ 虚拟员工在线承接岗位工作。',
     'Sole owner of the Sunwu Fleet virtual-employee platform from planning to launch: delivered to kitchen-appliance client Fotile, with 10+ virtual employees now on the job.',
     '独立操盘 Personal Agent 平台(原孙武 Fleet)从 0 到 1 的规划与落地,主导 Agent 工作台、Skill 技能工坊、企业知识库三大板块;平台累计服务活跃企业 20 余家、在岗 AI 虚拟员工 2000 余个。',
     'Sole owner of the Personal Agent platform (formerly Sunwu Fleet) from 0 to 1: led the Agent workspace, Skill workshop, and knowledge base; the platform now serves 20+ active enterprises with 2,000+ virtual employees on the job.'),
    ('多 Agent 并行加 20+ 自研 Skills 体系,原型、验证、交付一个人跑通全链路。',
     'Multi-agent parallel runs plus 20+ self-built Skills let me ship hi-fi prototypes and validate solutions solo.',
     '用 Claude Code 与自研 Skill 体系快速完成产品 POC 验证,沉淀 20 余个可复用 Skill;独立完成 2.8 万条社媒数据 AI 打标的消费洞察报告,交付商务部司局级汇报;以 SQL 与 Python 做数据分析与自动化取数。',
     'Claude Code plus 20+ self-built Skills for rapid POC validation; solo-delivered a consumer-insight report with 28,000 social posts AI-tagged for a ministry-level briefing; SQL and Python for data analysis and automated pulls.'),
    ('Golden Case 评测集与数据飞轮,效果不靠感觉,靠可复盘的证据。',
     'Golden Case eval sets and data flywheels. Results rest on auditable evidence, not gut feel.',
     'Golden Case 评测集与语义、结构、归属、字典四类自动检查,抽取结果带置信度与反证条件,效果不靠感觉,靠可复盘的证据。',
     'Golden Case eval sets plus four automated checks (semantic, structural, attribution, dictionary), with confidence scores and counter-evidence on every extraction. Results rest on auditable evidence, not gut feel.'),
    ('把零散功能收拢成体系。',
     'Turn scattered features into a system.',
     '把非结构化数据收拢成体系。',
     'Turn unstructured data into a system.'),
    ('信息架构先行,以「虚拟员工 + 会话 + Skill」核心模型,把 Agent 工作台、技能工坊、企业知识库收进清晰的产品骨架。',
     'Architecture first: a virtual-employee + session + skill model folds the Agent workspace, Skill workshop, and knowledge base into one clear product skeleton.',
     '以「原信息判断 → 信息抽取」两级 AI 流水线为核心,atoms + atom_fields 主从结构落库,一条数据从输入到入库一行可见。',
     'A two-stage AI pipeline (source judgment, then extraction) with an atoms + atom_fields master-detail schema: every record stays traceable from input to database in one visible line.'),
    ('规划帅 / 将 / 兵三层组织级效能度量:人天系数、AI 节省人力成本自动统计、AI 成熟度矩阵,把工具做成组织的基础设施。',
     'A three-layer efficiency system with per-item coefficients, automated labor-cost savings, and an AI maturity matrix, turning tools into organizational infrastructure.',
     '规划组织级 AI 效能度量体系:工作项人天系数、AI 节省人力成本自动统计、AI 成熟度矩阵,让每一分 AI 投入的产出可见。',
     'An org-wide AI efficiency system: man-day coefficients per work item, automated labor-cost savings tracking, and an AI maturity matrix, making the return on every AI investment visible.'),
    ('「存用分离」「训练态 / 使用态解耦」「伪功能规避」产品范式与开源 PM 知识库,让一套能力复制到更多场景。',
     'Paradigms like storage-use separation, training-usage decoupling, and fake-feature avoidance, plus an open-sourced PM knowledge base, make one capability replicable across scenarios.',
     '「客户口述经验、结构化成 Skill」四步交付法与规范基线,沉淀为平台级 Skill 资产库,让一套能力跨客户复制到更多场景。',
     'A four-step method that turns client know-how into structured Skills, compounded into a platform-level asset library replicable across customers and scenarios.'),
    # WHAT I CAN DO 四卡
    ('Agent 产品设计',
     'Agent Product Design',
     '数据流水线设计',
     'Data Pipeline Design'),
    ('从信息架构到交互闭环,把虚拟员工、技能工坊、知识库做成能上线的企业级产品。',
     'From information architecture to interaction loops, I turn virtual employees, skill workshops, and knowledge bases into shippable enterprise products.',
     '设计「采集 → 原信息判断 → 画像抽取 → 结构化入库 → 洞察应用」两级 AI 处理流水线,跑通 7 类数据源从采集到 MySQL 入库全链路。',
     'A two-stage AI pipeline from collection through source judgment, profiling extraction, and structured storage to insight application, proven end-to-end across 7 data sources into MySQL.'),
    ('Golden Case 评测集加数据飞轮,让模型效果不是感受,而是可复盘的证据。',
     'Golden Case sets plus data flywheels turn model quality from a feeling into auditable evidence.',
     'Golden Case 评测集与四类自动质检,对多个主流大模型按抽取准确率、稳定性与成本完成选型,让效果不是感受,而是可复盘的证据。',
     'Golden Case eval sets with four automated quality checks; mainstream models benchmarked and selected on extraction accuracy, stability, and cost. Quality is auditable evidence, not a feeling.'),
    ('企业知识架构',
     'Knowledge Architecture',
     '数据分析与洞察',
     'Data Analysis & Insight'),
    ('三级知识库、存用分离、非结构化两层架构,打通「文件 → 知识 → 训练用例」的数据飞轮。',
     'Three-tier knowledge bases, storage-use separation, and a two-layer unstructured data architecture connect the file-to-knowledge-to-training flywheel.',
     '249 个画像字段与四层人群建档,以 SQL 与 Python 完成人群、SKU、路径三视角分析,直接支撑产品定义与经营决策。',
     'A 249-field profiling system with four-layer audience files; SQL and Python power three-perspective analysis across people, SKU, and decision paths, feeding product definition and business decisions.'),
    # WHAT I HAVE DONE 八项目
    ('「孙武 Fleet」虚拟员工平台',
     'Sunwu Fleet Virtual Employee Platform',
     '方太人群画像数据项目',
     'Fotile Audience Profiling'),
    ('思灵科技(浙大研究院)· 从 0 到 1 独立操盘 AI Agent 平台:以「虚拟员工 + 会话 + Skill」为核心模型,覆盖 Agent 工作台、Skill 技能工坊、企业知识库三大板块,交付厨电客户方太并上线运行,10+ 虚拟员工在线承接客服、品控、运营岗位工作。',
     'Siling Tech (ZJU Research Institute): sole 0-to-1 owner of an AI agent platform built on a virtual-employee + session + skill model, spanning the Agent workspace, Skill workshop, and knowledge base. Delivered to Fotile and running in production with 10+ virtual employees covering customer service, quality control, and operations.',
     '阿里云(杭州端点网络科技有限公司)· 设计 249 个字段的人群画像体系与「原信息判断 → 信息抽取」两级 AI 流水线,覆盖小红书、京东/天猫客服会话、电话录音、问卷、访谈、焦点小组 7 类数据源,8000 余条帖子、2.7 万余条评论纳入候选池,直接支撑产品定义与消费者决策路径分析。',
     'Alibaba Cloud (Hangzhou Duandian Network Technology): designed a 249-field audience profiling system with a two-stage AI pipeline (source judgment, then extraction), covering 7 data sources including Xiaohongshu posts, JD/Tmall customer-service chats, call recordings, surveys, interviews, and focus groups, with 8,000+ posts and 27,000+ comments pooled, directly feeding product definition and consumer decision-path analysis.'),
    ('Golden Case 评测与训练闭环',
     'Golden Case Evaluation Loop',
     'Personal Agent 平台(原孙武 Fleet)',
     'Personal Agent Platform (Sunwu Fleet)'),
    ('建立 Golden Case 评测集与测试集规范,会话一键沉淀、批量跑测;「训练态/使用态解耦」让调试噪音不污染质量分析,非技术员工也能完成训练闭环。',
     'Built Golden Case evaluation standards with one-click test-set capture and batch runs. Decoupled tuning from real usage so non-technical staff can close the training loop.',
     '从 0 到 1 规划落地,以「虚拟员工 + 会话 + Skill」为核心模型,覆盖 Agent 工作台、Skill 技能工坊、企业知识库及营销专家板块;平台累计服务 20 余家活跃企业、2000 余个在岗虚拟员工,方太单客户 300 余个 Skill 入库。',
     'Planned and shipped from 0 to 1 around a virtual-employee + session + skill model, spanning the Agent workspace, Skill workshop, enterprise knowledge base, and marketing-expert module. The platform serves 20+ active enterprises and 2,000+ virtual employees, with 300+ Skills in production for Fotile alone.'),
    ('企业知识库与数据飞轮',
     'Enterprise Knowledge Flywheel',
     'AI 合同审核平台',
     'AI Contract Review Platform'),
    ('组织、部门、个人三级知识库,「知识订阅 → 知识条目」索引层替代全文召回;非结构化数据两层架构打通「文件 → 知识 → 训练用例」,为 Skill 进化供给原料。',
     'A three-tier knowledge base with a subscription-to-entry index layer replacing full-text recall. A two-layer unstructured data architecture feeds the file-to-knowledge-to-training loop that supplies raw material for Skill evolution.',
     '设计条款抽取、合规规则匹配、历史案例检索、修改建议生成的多子 Agent 架构,确立「AI 初审 + 人工复审」分级机制,联合业务方共建 Golden Case 评测集,单份合同审核由小时级压缩至分钟级,POC 验收通过。',
     'Designed a multi-agent architecture spanning clause extraction, compliance-rule matching, historical-case retrieval, and revision suggestions, with an AI-first-review + human-recheck tiered mechanism. Co-built Golden Case eval sets with business teams; single-contract review compressed from hours to minutes, passing POC acceptance.'),
    ('以帅、将、兵三层重构信息架构,为工作项设置人天系数,自动统计 AI 节省的人力成本;AI 成熟度矩阵让组织看见每一分 AI 投入的产出。',
     'Rebuilt information architecture across three org levels, assigning man-day coefficients to work items and auto-tracking saved labor costs. An AI maturity matrix shows the return on every AI investment.',
     '以 FDE 前线部署模式进驻方太、箭牌、海底捞等 5 家客户一线:箭牌首批 43 个业务场景上线 26 个,覆盖天猫、京东、抖音、拼多多四大电商渠道,对账 Agent 自动化约 60%,交付方法沉淀为可跨客户复用的实施 SOP。',
     'Deployed on-site with 5 clients including Fotile, Arrow, and Haidilao under the FDE model: Arrow launched 26 of its first 43 business scenarios across Tmall, JD, Douyin, and Pinduoduo, with reconciliation automation around 60%. Delivery methods compounded into reusable implementation SOPs.'),
    ('东来 AI 运营平台',
     'Donglai AI Operations Platform',
     'Skill 技能工坊 · 自助训练体系',
     'Skill Workshop & Self-Service Training'),
    ('负责受理侧 4 模块,覆盖 7 门店、10 类客诉、4+1 渠道;以语义层落地智能问数,业务方自然语言秒级取数,临时取数工单下降约 65%,有效会话采纳率 50% → 80%。',
     'Owned 4 intake modules across 7 stores, 10 complaint categories, and 5 channels. Semantic-layer self-service analytics cut ad-hoc data tickets by about 65% and raised session adoption from 50% to 80%.',
     '让非技术员工无需研发介入即可自助完成 AI 能力的训练、测试与发布,训练过程、文件改动与检测报告全程可见;沉淀「客户口述经验、结构化成 Skill」四步交付法,形成平台级 Skill 资产库。',
     'Non-technical staff train, test, and publish AI capabilities without engineering involvement, with full visibility into the training process, file changes, and test reports. A four-step method turns spoken client expertise into structured Skills, forming a platform-level asset library.'),
    ('数字审核平台多 Agent 闭环',
     'Multi-Agent Compliance Review',
     '组织级 AI 效能度量',
     'Org-Level AI Efficiency Metrics'),
    ('独立设计多子 Agent 审核架构,建立「物料 - AI 初审 - 法条引用 - 人工复审」闭环:单条审核 2-3 天 → 4h,月处理 400 → 800 条,支撑重大舆情取证,被最高法评为 2025 年度十大案例。',
     'Designed a multi-agent review architecture with a material-to-AI-review-to-legal-citation-to-human-recheck loop. Review time dropped from 2-3 days to 4 hours and monthly volume doubled from 400 to 800, supporting evidence collection in major public-opinion cases, named a top-10 case of 2025 by the Supreme Court.',
     '规划组织级 AI 效能度量体系:工作项人天系数、AI 节省人力成本自动统计、AI 成熟度矩阵,让每一分 AI 投入的产出可见,把工具做成组织的基础设施。',
     'Designed an org-wide AI efficiency measurement system: man-day coefficients per work item, automated tracking of labor-cost savings, and an AI maturity matrix, making every AI investment visible and turning tools into organizational infrastructure.'),
    ('孙武 Fleet · 多 Agent 研发模式',
     'Sunwu Fleet: Multi-Agent Development',
     '智能剪辑功能 · LessCut',
     'LessCut AI Video Editing'),
    ('以 Claude Code + 多 Agent 并行驱动产品验证:线框图、高保真原型、交互动画全流程自研,方案评审一次通过;沉淀 Pencil + Figma 设计工作流,设计稿即产品文档,避免开发返工。',
     'Multi-agent parallel product validation with Claude Code: wireframes, hi-fi prototypes, and interaction demos all built in-house, passing solution reviews on the first try. Built a Pencil + Figma workflow where the design file is the product doc, avoiding development rework.',
     '主导智能剪辑功能从 0 到 1 上线:把专业剪辑门槛降到一句中文对话,Agent 直接改写多轨时间线、本地渲染导出,剪辑工具经 MCP 开放给外部 Agent 调用。',
     'Led the smart-editing feature from 0 to 1: professional video editing reduced to a single Chinese sentence, with the Agent rewriting multi-track timelines and rendering locally, exposed to external agents via MCP.'),
    ('华为 · AI 智能审核助手',
     'Huawei AI Review Assistant',
     '胖东来门店企划内容',
     'Pang Dong Lai Store Content'),
    ('华为技术有限公司 · AI 产品经理(实习):梳理广告/内容合规审核痛点、流程与竞品,参与 PRD 与「物料 - AI 初审 - 风险识别 - 法条 - 修改建议 - 人工复审」闭环设计,建立评测指标与视觉判例体系,支撑 AI 审核模块上线。',
     'AI PM intern at Huawei: mapped pain points, workflows, and competitors in ad/content compliance review; contributed to the PRD and the material - AI review - risk detection - legal citation - revision suggestion - human recheck loop; built evaluation metrics and a visual precedent system, supporting the AI review module launch.',
     '胖东来商贸集团 · 许昌企划 · 编导:负责门店企划内容的选题策划与脚本撰写,独立完成短视频与活动视频的编导与拍摄执行,策划并落地卖场互动活动、主题场景与打卡点。',
     'Pang Dong Lai Commercial Group, Xuchang planning and directing: owned topic planning and scriptwriting for store content, independently directed and shot short-form and event videos, and planned in-store interactive events, themed scenes, and photo spots.'),
]

for old_zh, old_en, new_zh, new_en in PAIRS:
    # chunk: zh:"...",en:"..." 成对
    pat = f'zh:"{old_zh}",en:"{old_en}"'
    rep = f'zh:"{new_zh}",en:"{new_en}"'
    n = chunk.count(pat)
    if n == 0:
        # 尝试宽松匹配(有些字符串可能带转义差异)
        pat_esc = 'zh:"' + re.escape(old_zh) + r'",en:"((?:[^"\\]|\\.)*)"'
        m = re.search(pat_esc, chunk)
        report.append(f'[CHUNK-PAIR-FUZZY] {old_zh[:30]}... found={bool(m)}')
        if m:
            chunk = re.sub(pat_esc, 'zh:"' + new_zh + '",en:"' + new_en + '"', chunk, count=1)
    else:
        chunk = chunk.replace(pat, rep)
        report.append(f'[chunk x{n}] {old_zh[:24]} -> {new_zh[:24]}')
    # html: 纯 zh
    nh = html.count(old_zh)
    html = html.replace(old_zh, new_zh)
    report.append(f'[html x{nh}] {old_zh[:24]} -> {new_zh[:24]}')

# ---------- 2) ternary 中英 inline ----------
TERN = [
    ('从 Agent 产品设计、评测体系到企业知识架构,提供 AI 产品全链路的能力储备。',
     'From agent product design and evaluation systems to enterprise knowledge architecture, I cover the full chain of AI product work.',
     '从数据流水线、人群画像分析到 AI 平台设计,提供「数据工程 · 数据分析与产品」全链路的能力储备。',
     'From data pipelines and audience profiling to AI platform design, I cover the full chain of data engineering, analysis, and product work.'),
]
for old_zh, old_en, new_zh, new_en in TERN:
    pat = f'"{old_zh}":"{old_en}"'
    n = chunk.count(pat)
    chunk = chunk.replace(pat, f'"{new_zh}":"{new_en}"')
    nh = html.count(old_zh)
    html = html.replace(old_zh, new_zh)
    report.append(f'[tern chunk x{n} html x{nh}] {old_zh[:20]}')

# ---------- 3) 硬编码串 ----------
HARDCODE = [
    ('AI Native Builder', 'AI Native 数据分析'),
    ('Agent × Product', 'Data × Product'),
    # 项目分类
    ('AI · Agent Platform', 'Data · User Insight'),
    ('AI · Evaluation System', 'AI · Agent Platform'),
    ('AI · Knowledge Architecture', 'AI · Compliance Agent'),
    ('AI · Org Efficiency', 'AI · Skill Ecosystem'),
    ('Retail · AI Operations', 'Retail · FDE Delivery'),
    ('Retail · Compliance Agent', 'AI · Org Efficiency'),
    ('AI · Agent Workflow', 'AI · Creative Tool'),
    ('Huawei · AI Review', 'Retail · Content Planning'),
    # WHAT I CAN DO 标签
    ('tags:["Agent","IA","0→1"]', 'tags:["Pipeline","ETL","MySQL"]'),
    ('tags:["GoldenCase","Rubric","Flywheel"]', 'tags:["GoldenCase","Eval","Rubric"]'),
    ('tags:["RAG","Knowledge","Pipeline"]', 'tags:["SQL","Python","Insight"]'),
    # WHAT I HAVE DONE 标签
    ('Agent · Skill Workshop · 0→1', '249 字段 · 7 类数据源 · 两级流水线'),
    ('GoldenCase · Eval · Decoupling', 'Agent · Skill Workshop · 0→1'),
    ('RAG · Knowledge · Flywheel', '20+ 企业 · 2000+ Agent · 300+ Skill'),
    ('Metrics · Maturity · Infra', 'Metrics · Maturity · Infra'),  # 占位防误配
    ('NL2SQL · FCR · Rollout', 'FDE · Rollout · SOP'),
    ('Multi-Agent · Compliance · SLA', 'Multi-Agent · Golden Case · SLA'),
    ('Multi-Agent · Claude Code · Prototype', 'Agent · MCP · 0→1'),
    ('Compliance · PRD · Evaluation', 'Content · Planning · Retail'),
]
for old, new in HARDCODE:
    if old == new:
        continue
    nc = chunk.count(old)
    chunk = chunk.replace(old, new)
    nh = html.count(old)
    html = html.replace(old, new)
    report.append(f'[hard chunk x{nc} html x{nh}] {old[:34]} -> {new[:34]}')

# ROLE 主标题(独立于跑马灯的纯文本节点)
pat = re.compile(r'children:"AI PRODUCT MANAGER"')
n = len(pat.findall(chunk)); chunk = pat.sub('children:"数据工程 · 数据分析与产品方向"', chunk)
pat2 = '>AI PRODUCT MANAGER</div>'
nh = html.count(pat2); html = html.replace(pat2, '>数据工程 · 数据分析与产品方向</div>')
report.append(f'[ROLE chunk x{n} html x{nh}]')

# ---------- 4) 跑马灯(用 \xa0 灵活的空白) ----------
def flex_re(display):
    parts = [p for p in re.split(r'(\s+)', display) if p]
    return ''.join(r'[\s\xa0]+' if p.isspace() else re.escape(p) for p in parts)

MARQUEE = [
    ('AI NATIVE · AI PRODUCT MANAGER · LI YANLONG ·', 'DATA ENGINEERING · DATA ANALYSIS · LI YANLONG ·'),
    ('AGENT × PRODUCT · DATA FLYWHEEL · AI NATIVE ·', 'USER INSIGHT · DATA PIPELINE · AI NATIVE ·'),
]
for old, new in MARQUEE:
    for name, s in (('chunk', chunk), ('html', html)):
        new_s, k = re.subn(flex_re(old), lambda m: new, s)
        if name == 'chunk':
            chunk = new_s
        else:
            html = new_s
        report.append(f'[marquee {name} x{k}] {old[:30]}')

# ---------- 5) title / meta / 头部 ----------
META = [
    ('<title>◤ LIYANLONG // AI PM ◢</title>', '<title>◤ LIYANLONG // DATA × PRODUCT ◢</title>'),
    ('<meta name="description" content="LI YANLONG · AI Product Manager Portfolio"/>',
     '<meta name="description" content="LI YANLONG · 数据工程 · 数据分析与产品方向"/>'),
    ('◤ LIYANLONG // AI PM ◢', '◤ LIYANLONG // DATA × PRODUCT ◢'),
]
for old, new in META:
    nh = html.count(old)
    html = html.replace(old, new)
    report.append(f'[meta html x{nh}] {old[:40]}')

# ---------- 6) 子路径部署:绝对路径改相对 ----------
PATHS = [
    ('"/_next/', '"./_next/'),
    ('"/videos/', '"./videos/'),
    ('href="/favicon.ico', 'href="./favicon.ico'),
    ('href="/icon.png', 'href="./icon.png'),
    ('href="/apple-icon.png', 'href="./apple-icon.png'),
    ('content="/icon.png', 'content="./icon.png'),
]
for old, new in PATHS:
    nh = html.count(old)
    html = html.replace(old, new)
    nc = chunk.count(old)
    chunk = chunk.replace(old, new)
    report.append(f'[path html x{nh} chunk x{nc}] {old}')

open(HTML, 'w', encoding='utf-8').write(html)
open(CHUNK, 'w', encoding='utf-8').write(chunk)

print('\n'.join(report))
print('DONE')
