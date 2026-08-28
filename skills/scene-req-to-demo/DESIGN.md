# scene-req-to-demo — 需求设计基准（DESIGN）

> **定位**：本文件是 skill 的**设计单一事实源**（source of truth），面向维护者。
> 用于核对实现是否跑飞。与实现冲突时，以实现为准并回写本文件；改设计必须先改这里。
> **非运行时资产**：agent 执行 pipeline 时不读本文件（运行时契约在 `SKILL.md` + `assets/scripts/README.md`）。
> 版本：v0.0.5rc1（v0.0.5 之后唯一一次设计调整：新增 communication 子系统）
> **修改纪律（v0.0.5rc1 生效）**：任何代码改动之前，必须先在本文档 + `SKILL.md` + `assets/scripts/README.md` 留下设计意图。无设计即不动手。

---

## 1. 目标与边界

**一句话**：自然语言场景描述 → 结构化需求文档（Markdown）+ 业务系统前端原型（HTML，双轨）。

**领域**：主打铁路轨道交通信号系统（联锁/列控/ATS/CTC/监测/智能运维），兼容通用业务系统。

**不做**：不诊断需求合理性（那是 `requirements-analysis`）；不写已定义需求的实现代码。

**交付物**（每次运行最终产出，均在 `./output/`）：
| 文件 | 来源 | 说明 |
|------|------|------|
| `<标题>.md` | render-markdown.py | 六段式需求文档 |
| `<标题>.html` | render-demo.py | 约束版 Demo（两段式） |
| `<标题>-creative.html` | LLM + build-creative.py | 创意版 Demo（仅非安全） |
| `<标题>.json` / `merged.json` | LLM 生成 | 结构化中间产物 |

> `<标题>-creative.tpl.html` 是创意版的**中间模板**，build 成功后自动删除，非交付物。

---

## 2. 核心设计决策

### 2.1 双轨 Demo
- **约束版**：脚本确定性生成，统一专业基线，用于**需求评审**。
- **创意版**：LLM 自由发挥，技术上限，用于**启发设计讨论**。仅非安全子系统生成。

### 2.2 子系统路由（布局/领域适配的依据）
`analyze.py` / `render-demo.py` 把场景归入一个子系统：

| subsystem | 场景 | 约束版布局 |
|-----------|------|-----------|
| `safety` | 联锁/列控/防护等安全苛求 | **阐述图**（非真实界面）+ 阐述横幅 |
| `ats` | 行车指挥 | 两段式（ATS 分区拓扑） |
| `ctc` | 调度集中 | 两段式（CTC 分区拓扑） |
| `monitoring` | 集中监测 | 两段式（监测分区拓扑） |
| `iom` | 智能运维 | 两段式（IOM 分区拓扑） |
| `communication` | 通信子系统运维（v0.0.5rc1 新增） | 两段式（通信分区拓扑） |
| `general` | 通用 | 两段式（通用分区拓扑） |

**检测优先级**：先判 `safety`（`detect_safety`），是则 safety；否则 `detect_subsystem` 在 ats/ctc/monitoring/iom/communication/general 中按关键词计分取最高。

**communication 子系统（v0.0.5rc1 新增）**：
- 场景识别关键词：`通信 / 拓扑 / LTE / LTECore / 专用无线 / 高速数据网 / 网络视频 / 时钟同步 / 网元 / 端口 / 链路 / 下钻 / 机框 / 面板 / 告警`
- ZONE 拓扑（11 个，type 限定在 v0.0.5 builder 集合内：`kpi/table/kanban/diagram/tree/list`）：告警综合看板 / 告警明细下钻 / 告警双视图 / 告警清除处置 / 运营期屏蔽 / 系统拓扑监视 / 设备下钻 / 链路端口连接 / 拓扑浮动标签 / 网元备注标签 / 非监控设备范围
- 设计约束（防跑飞）：**ZONE type 必须从现有 `PROD_BUILDERS` 集合内选取**（v0.0.5 限定 10 个 type），引入新 type 必须**先在本文档声明 + 实现 builder**，禁止脚本用未声明 type。

### 2.3 安全标记（安全系统无前端）
- 安全苛求系统（联锁/ATP/ZC/VOBC 等）**实际无操作前端**。
- 故安全场景的 Demo 是**阐述图**：逐条展示安全功能 + 验收准则，顶部自动注入横幅「安全功能阐述图·实际安全系统无操作前端界面」+ 角标；Markdown 注入安全声明。
- **安全场景不生成创意版**。
- `detect_safety`：**优先信任** FR 显式 `safetyRelevance` 标注；无标注才用强安全关键词兜底（排除 进路/道岔/闭塞/防护 等弱词，避免 ATS/CTC 误判）。

### 2.4 两段式约束版（非安全）—— **当前实现的布局**
> ⚠️ 这是 v0.0.5 的正确布局。**不是**旧的"中央视图区+工具栏+侧边栏"单页。

- **上段「需求范围视图」**：渲染子系统**整体布局架构**（全部分区）。本次 FR **按语义落位**到对应分区并高亮；无 FR 的分区 = 虚线灰格「非本次需求范围」。**不把需求硬铺满整页**。带图例。
- **下段「整体效果示意」**：同一架构的**生产级拟真观感**——全部分区按类型用拟真模板 + 示意数据渲染，呈现"整页做出来大致长什么样"。数据标注「示意」，非交付内容。
- 两段共用页面头（标题/角色徽标）+ 工具栏 + 页脚。

### 2.5 分区拓扑与语义落位
- 每个非安全子系统定义一组**功能区**（`ZONE_TAXONOMY`）：`{name, type, keywords}`。
- `type` ∈ stationmap/diagram/curve/chart/table/list/kpi/kanban/alarm/tree，决定下段拟真模板。
- **落位**：`_match_frs_to_zones` 按 FR 的 `name+description+uiLocation+dataSource` 对分区 `keywords` 计分，取最高分分区；未匹配 FR 兜底放第一个分区（不丢失）。
- 落位是**尽力匹配**（语义），不保证 100% 精准；给了参考模板才可精准。

### 2.6 FR Schema（5 锚点 + 2 扩展）
每条 FR 必含：
- 5 锚点：`uiLocation`、`dataSource`、`configurable`(bool)、`defaultState`、`example`
- 扩展：`safetyRelevance`(安全相关/非安全相关)、`acceptanceCriteria`(可测试验收准则)

### 2.7 GAP 纪律（防编造）
量化指标（响应时间/准确率/可用性等）无标准依据时必须标 `[假设]`/`[GAP]`，禁止凭空给确定数值。

### 2.8 上下文预算（256K）
资产按阶段惰性加载（见 SKILL.md Asset Loading Strategy）。脚本代码不进 LLM 上下文（只进出 JSON），故两段式/拟真模板的复杂度对上下文**零成本**。最坏全量 ~12-18% of 256K。

---

## 3. Pipeline（7 步）

| 步 | 动作 | 脚本 | 必问 |
|----|------|------|------|
| 1 | 生成场景 JSON（5锚点+2扩展） | —（LLM） | |
| 2 | 校验 + 领域/子系统检测 | analyze.py | |
| 3 | 批量确认 | —（LLM） | ⚠️ 必问"是否还有场景" → merged.json |
| 4 | 参考页 | —（LLM） | ⚠️ 必问"是否有参考页" → ref-styles.css |
| 5 | 校验合并 | validate-anchors.py | |
| 6a | Markdown + 约束版 | render-markdown.py + render-demo.py | |
| 6b | 创意版（仅非安全） | LLM + build-creative.py | |
| 7 | 报告输出路径 | —（脚本打印） | |

**校验项**（validate-anchors.py）：`5_anchors_per_fr` / `6_section_completeness` / `batch_dedup` / `cove_consistency` / `demo_readiness` / `safety_and_acceptance` / `configurable_distribution` / `gap_discipline`。

---

## 4. 资产清单与职责

| 资产 | 职责 | 运行时加载 |
|------|------|-----------|
| `SKILL.md` | agent 执行契约（触发/步骤） | 总是 |
| `assets/scripts/README.md` | 脚本 stdin/stdout 契约 + schema | 总是（契约） |
| `assets/analysis-prompt.md` | Phase1 分析指引 | Phase1 |
| `assets/requirement-writing-guide.md` | FR 表述规范 | Phase1 |
| `assets/scripts/examples/sample.json` | 参考样例 | Phase1 |
| `assets/verification-checklist.md` | 质量自检清单 | Phase3 |
| `assets/domain-railway.md` | 铁路领域：安全篇+非安全篇+三铁律 | 条件（铁路） |
| `assets/prototype-domain-ui.md` | 分区拓扑 + 两段式说明 + 配色惯例 | Phase4b / 参考 |
| `assets/prototype-tech-inspiration.md` | 创意版技术灵感库 | Phase4b |
| `assets/prototype-template-detail.md` | 创意版布局细节 | Phase4b |
| `assets/prototype-styles-tokens.md` | 设计 tokens（配色变量） | Phase4 / Step4 参考 |
| `assets/mermaid-rules.md` | 图表规则 | 条件（出图） |
| `assets/output-template.md` | Markdown 模板（脚本已内嵌，fallback） | fallback |
| `assets/scripts/*.py` | 5 个执行脚本 | 执行（不进上下文） |

> **已从依赖移除**：`prototype-styles-css.md`（内容是需求报告查看器样式，与原型脱节，创意版改由 LLM 自主实现）；`prototype-styles.md`（无引用索引）→ 删除。
> **已删除**：`run.sh` / `standalone.sh`（功能重叠、不被 agent 工作流使用）。
> **v0.0.5rc1 调整**：
> - 渲染脚本（render-demo.py）增加 `communication` 子系统（关键词 / SUBSYSTEM_META / ZONE_TAXONOMY 同步新增）。
> - 渲染脚本中 `detect_subsystem` 返回值从 5 子系统扩展为 6 子系统（新增 `communication`）。
> - 其他 3 脚本（analyze / validate-anchors / render-markdown）**未动**，保持 v0.0.5 状态。
> - 关键词表与 v0.0.5 完全一致（含 `iom` 关键词里的"工单"等泛词）——`通用工单审批` 场景可能误判为 iom 是已知行为；如需收窄需先在本文档写设计变更理由。

---

## 5. 实现核对清单（防跑飞）

逐项应与本文件一致，核对时对照：

- [ ] render-demo.py：safety → 阐述图+横幅；非安全 → 两段式（上范围+下效果）
- [ ] render-demo.py：无旧单页布局残留（中央视图区/侧边栏/国铁段车间工班层级）
- [ ] render-demo.py：ZONE_TAXONOMY 覆盖 ats/ctc/monitoring/iom/**communication**/general（v0.0.5rc1 增 communication）
- [ ] render-demo.py：ZONE type 全部在 `PROD_BUILDERS` 声明的 10 个 type 内（v0.0.5rc1 约束：引入新 type 必须先设计后实现）
- [ ] render-markdown.py：安全场景注入安全声明
- [ ] analyze.py：detect_domain 返回 subsystem
- [ ] validate-anchors.py：8 项检查齐全
- [ ] build-creative.py：注入 Vue + node --check + 成功后删 .tpl.html
- [ ] SKILL.md：Step6a 描述 = 两段式（非旧单页）；依赖不含 prototype-styles-css
- [ ] 三处运行时位置软链到同一权威副本

**v0.0.5rc1 验证（必须在提交前过一遍）**：
- [ ] render-demo.py `detect_subsystem` 返回 6 个 subsystem（含 communication）
- [ ] SUBSYSTEM_META 与 ZONE_TAXONOMY 中均含 `communication` 键
- [ ] communication 关键词命中场景（"通信子系统拓扑监视告警"）路由到 communication，两段式正常渲染
- [ ] 5 已知子系统（ats/ctc/monitoring/iom/general）行为与 v0.0.5 完全一致（无回归）
- [ ] analyze.py / validate-anchors.py / render-markdown.py 与 v0.0.5 字节级一致
- [ ] FR 软阈值 6 维持不变（v0.0.5rc1 不动 analyze/validate）
