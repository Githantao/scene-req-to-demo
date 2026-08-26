---
name: scene-req-to-demo
description: "场景需求分析→结构化需求文档+业务系统原型。Scene description → structured requirements + interactive prototype. Trigger when user describes a system feature/module/page, or says 场景需求/需求分析/场景描述/分析以下场景/交接班/看板/填报/查询/原型生成. Uses Python scripts in assets/scripts/."
license: MIT
compatibility: "Claude Code (~/.claude/skills, ~/.agents/skills), OpenCode (~/.config/opencode/skills, ~/.agents/skills), Amp (~/.config/amp/skills). Requires Python 3+."
metadata:
  author: scene-req-to-demo
  version: "0.0.4"
  domain: requirements-engineering
---

# Scene Requirements to Demo

Natural-language scene description → JSON analysis → Markdown requirement doc + interactive business system HTML prototype (双轨: 约束版 + 创意版).

## When to Use

Trigger when the user says (or implies) any of:

- 场景描述 / 需求分析 / 需求文档 / 原型 / Demo / 帮我分析这个场景
- 自然语言转需求 / 场景转需求 / 把这个想法整理成需求
- "我想做一个..." / "需要一个系统..." / "能不能帮我把...整理一下"
- "分析以下场景需求" / "交接班" / "看板" / "填报" / "查询" / 任何业务功能/模块/页面的场景描述
- 任何包含"把一段话/一个想法变成可评审的需求"意图的请求

**Do NOT trigger** when the user is asking to diagnose whether a requirement is valid (use `requirements-analysis` instead) or to write code for an already-defined requirement.

## Setup: find scripts

Run this Bash command first to locate the scripts:

```bash
SKILL_DIR=$(find ~/.agents/skills ~/.config/opencode/skills ~/.claude/skills -name "SKILL.md" -path "*/scene-req-to-demo/*" 2>/dev/null | head -1 | xargs dirname)
```

## ⭐ Read first: `assets/scripts/README.md`

动手前必读 `$SKILL_DIR/assets/scripts/README.md` — 4 个脚本的 stdin/stdout 契约、JSON schema 单一事实源、各阶段自检清单。**只读它即可正确调用全部脚本，无需打开脚本源码。**

## Asset Loading Strategy — 上下文优化

为适配本地模型 256K 上下文，按阶段**惰性加载**资产，勿一次性全读：

| 阶段 | 需加载 | 增量 | 累计 |
|------|--------|------|------|
| 契约 | `SKILL.md` + `scripts/README.md` | ~13 KB | ~13 KB |
| Phase 1（生成 JSON） | + `analysis-prompt.md` + `requirement-writing-guide.md` + `scripts/examples/sample.json` | ~18 KB | ~31 KB |
| Phase 3（校验合并） | + `verification-checklist.md` | ~6 KB | ~37 KB |
| Phase 4（渲染） | + `prototype-template.md` + `prototype-styles-tokens.md` | ~7 KB | ~44 KB |
| Phase 4b（创意版） | + `prototype-template-detail.md` + `prototype-styles-css.md` + `prototype-domain-ui.md` + `prototype-tech-inspiration.md` | ~33 KB | ~77 KB |
| 条件：铁路领域 | + `domain-railway.md`（`domain_info.matched=true` 时，按 `subsystem` 选章节） | ~7 KB | +7 KB |
| 条件：图表生成 | + `mermaid-rules.md` | ~6 KB | +6 KB |

**原则**：`output-template.md` 与样式细节已内嵌于 `render-*.py`，仅在脚本不可用或需手工微调时作为 fallback 读取；Phase 1-3 勿加载 Phase 4b 的大文件。

## Pipeline

### Step 1 — Generate JSON

用 `assets/analysis-prompt.md` 作为分析指引、`assets/requirement-writing-guide.md` 作为 FR 表述规范，参考 `assets/scripts/examples/sample.json`。创建 `./output/<需求名称>.json`。

每条 FR 必须有 5 锚点：`uiLocation`、`dataSource`、`configurable`(bool)、`defaultState`、`example`；并标注 `safetyRelevance`（安全相关/非安全相关）与 `acceptanceCriteria`（可测试验收准则）。

```json
{
  "scene": "<user text>",
  "analysis": {
    "businessContext": {"proposer": "...", "problemLevel": "...", "currentState": "...", "targetLevel": "...", "expectedBenefit": "..."},
    "requirements": {
      "title": "...",
      "diagramType": "flowchart|sequenceDiagram|stateDiagram-v2|classDiagram|erDiagram",
      "layers": {"business": {"goal": "...", "value": "..."}, "user": {"scenario": "...", "painPoints": ["..."]}, "system": {"summary": "..."}},
      "mainRequirement": {"name": "...", "description": "..."},
      "systemBoundary": "...",
      "stakeholders": ["..."],
      "functionalRequirements": [
        {"id": "FR-1", "name": "...", "description": "...", "priority": "high|medium|low", "safetyRelevance": "安全相关|非安全相关", "acceptanceCriteria": "...", "uiLocation": "...", "dataSource": "...", "configurable": true, "defaultState": "...", "example": "..."}
      ],
      "dataFlows": [{"from":"...", "to":"...", "data":"...", "type":"input|output|storage"}],
      "interfaces": [],
      "dataRequirements": [],
      "nonFunctionalRequirements": []
    },
    "mermaidCode": "flowchart TD\n  A --> B"
  }
}
```

**GAP 纪律（防编造）**：量化指标（响应时间/准确率/可用性等）无标准依据时，必须标 `[假设]` 或 `[GAP]`，禁止凭空给出确定数值。安全系统相关遵循 `domain-railway.md` 铁律。

### Step 2 — Validate（领域/子系统检测）

```bash
mkdir -p ./output
python3 $SKILL_DIR/assets/scripts/analyze.py < ./output/<需求名称>.json
```

- `status=needs_correction` → 修复 JSON 重跑。
- `domain_info.matched=true` → 加载 `assets/domain-railway.md`，按 `domain_info.subsystem` 选章节（safety / ats / ctc / monitoring / iom）。
- 记住 `domain_info.subsystem` — 它驱动 Step 6 的安全标记与布局选择。

### Step 3 — Batch confirmation ⚠️ MUST ASK

> ⛔ STOP — 你必须在此停下，向用户提问，未获答复前不得继续。

向用户展示当前场景的确认信息：需求名称 + 总体需求 + 功能需求列表。

然后**必须提问**：

> "是否还有其他需求场景需要补充？如有请直接描述，无则回复「没有」或「继续」。"

- **用户有补充** → 回到 Step 1 为新场景生成 JSON，重复 Step 2-3，直至用户说没有
- **用户说没有/继续** → 将所有已收集场景合并（去重 FR、重编号 ID）为 `./output/merged.json`；**仅一个场景时直接复制** `./output/<需求名称>.json` → `./output/merged.json`

```bash
# 仅一个场景时：
cp ./output/<需求名称>.json ./output/merged.json
```

⚠️ 无论单场景还是多场景，都必须执行本步（提问 + 生成 merged.json）。禁止跳过。

### Step 4 — Reference page ⚠️ MUST ASK

> ⛔ STOP — 你必须在此停下，向用户提问，未获答复前不得继续。

**必须提问**：

> "是否有基础页面/参考页面（截图/HTML/文字描述）可供参考？如有请提供，无则回复「没有」或「跳过」。"

- **有参考** → 提取样式特征，生成 `./output/ref-styles.css`（覆盖 `:root` 变量，参考 `assets/prototype-styles-tokens.md` 变量名）
- **无参考** → 使用默认暗蓝工业风，无需额外操作

⚠️ 本步必须提问，禁止跳过。即使无参考页面也需用户明确确认。

### Step 5 — Validate merged（含质量检查清单）

对照 `assets/verification-checklist.md` 自检后运行：

```bash
python3 $SKILL_DIR/assets/scripts/validate-anchors.py < ./output/merged.json
```

关注新增检查：`safety_and_acceptance`（安全标注+验收准则）、`configurable_distribution`（configurable 防摆设）、`gap_discipline`（量化指标防编造）。修复所有 `errors`，`warnings` 逐条确认。

### Step 6 — Render (双轨 Demo)

#### 6a — Markdown + 约束版 Demo（脚本生成）

```bash
python3 $SKILL_DIR/assets/scripts/render-markdown.py --output-dir ./output < ./output/merged.json
python3 $SKILL_DIR/assets/scripts/render-demo.py --output-dir ./output < ./output/merged.json
```

- 约束版：单页面承载所有 FR，按 FR 角色自动布局（中央视图区+工具栏+侧边栏），暗蓝工业风。
- **安全标记自动注入**：检测到安全苛求功能时，脚本自动在 Demo 顶部加"安全功能阐述图·实际安全系统无操作前端界面"横幅+角标，并在 Markdown 加安全声明。无需手动处理。
- 如 Step 4 有参考 CSS：追加 `--css-file ./output/ref-styles.css`。

#### 6b — 创意版 Demo（仅非安全子系统）

> ⚠️ `subsystem=safety` 时**跳过创意版**（安全系统无前端，只有约束版+阐述横幅）。

对 ats / ctc / monitoring / iom / general，生成 `./output/<标题>-creative.html`：

1. **专业下限**：按 `assets/prototype-domain-ui.md` 取对应子系统的界面骨架（布局/配色惯例）
2. **技术灵感**：从 `assets/prototype-tech-inspiration.md` 挑 2-3 个契合的信息化趋势模式叠加（大屏/实时流/数字孪生/钻取/AI/可配置）
3. **约束**：
   - 必须是**业务系统界面**，不是需求分析展示
   - 覆盖所有 FR 业务能力（`example` 字段提供模拟数据）
   - 遵守 `prototype-tech-inspiration.md` 的可行性约束（无构建、需网络要标注+降级）
4. **组装（勿手写 Vue 内联）**：LLM 写带 `<!--__INJECT_VUE__-->` 占位符的 HTML 存为 `./output/<标题>-creative.tpl.html`，再交给脚本注入 Vue 并自动冒烟测试：
   ```bash
   python3 $SKILL_DIR/assets/scripts/build-creative.py \
     --input ./output/<标题>-creative.tpl.html \
     --output ./output/<标题>-creative.html
   ```
   冒烟测试（`node --check`）失败会报错且不产出文件——修复内联 JS 后重跑，**禁止静默出货**。

约束版（专业下限）+ 创意版（技术上限）供对比，启发设计讨论。

Output path and filename are controlled by the scripts — agent cannot偏离。

### Step 7 — Done

The scripts print the actual output paths. Tell user.

## Diagram type rules

- Multi-party interaction / API / messaging → `sequenceDiagram`
- State flow / approval / lifecycle → `stateDiagram-v2`
- Data entities / table structure → `erDiagram`
- Class / module / interface → `classDiagram`
- Step-by-step process → `flowchart`

## Mermaid rules

- Fixed node naming: `[verbNoun]`
- Flow order: input → process → decision → output
- Subgraphs grouped by phase (input/process/output)
- Max 3 branches per decision diamond
