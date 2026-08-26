---
name: scene-req-to-demo
description: "场景需求分析→结构化需求文档+业务系统原型。Scene description → structured requirements + interactive prototype. Trigger when user describes a system feature/module/page, or says 场景需求/需求分析/场景描述/分析以下场景/交接班/看板/填报/查询/原型生成. Uses Python scripts in assets/scripts/."
license: MIT
compatibility: "Claude Code (~/.claude/skills, ~/.agents/skills), OpenCode (~/.config/opencode/skills, ~/.agents/skills), Amp (~/.config/amp/skills). Requires Python 3+."
metadata:
  author: scene-req-to-demo
  version: "0.0.3"
  domain: requirements-engineering
---

# Scene Requirements to Demo

Natural-language scene description → JSON analysis → Markdown requirement doc + interactive business system HTML prototype.

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

## Pipeline

### Step 1 — Generate JSON

Create `./output/<需求名称>.json` with this structure. Each FR requires 5 anchors: `uiLocation`, `dataSource`, `configurable` (bool), `defaultState`, `example`.

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
        {"id": "FR-1", "name": "...", "description": "...", "priority": "high|medium|low", "uiLocation": "...", "dataSource": "...", "configurable": true, "defaultState": "...", "example": "..."}
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

### Step 2 — Validate

```bash
mkdir -p ./output
python3 $SKILL_DIR/assets/scripts/analyze.py < ./output/<需求名称>.json
```

If `status` is `needs_correction`, fix the JSON and re-run.

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

### Step 5 — Validate merged

```bash
python3 $SKILL_DIR/assets/scripts/validate-anchors.py < ./output/merged.json
```

### Step 6 — Render (双轨 Demo)

#### 6a — Markdown + 约束版 Demo（脚本生成）

```bash
python3 $SKILL_DIR/assets/scripts/render-markdown.py --output-dir ./output < ./output/merged.json
python3 $SKILL_DIR/assets/scripts/render-demo.py --output-dir ./output < ./output/merged.json
```

约束版特点：单一页面承载所有 FR，按 `analyze_fr_roles` 自动布局（中央视图区 + 工具栏 + 侧边栏），暗蓝工业风，FR 协作关系体现在界面结构中。

> 如 Step 4 有参考页面 CSS：追加 `--css-file ./output/ref-styles.css` 参数覆盖默认主题。

#### 6b — 创意版 Demo（LLM 自由生成）

约束版生成后，LLM 再生成一个创意版 `./output/<标题>-creative.html`：

1. **检索同类参考**：根据 `title` 和 FR 关键词，联想 2-3 个同类业务系统的典型界面模式（如"综合看板"可参考 Grafana/电力调度大屏/铁路 CTC 界面）
2. **自由设计**：不受 `prototype-template-detail.md` 布局约束，可自选以下维度做差异化：
   - 布局：分栏/全屏/卡片网格/仪表盘拼贴
   - 视觉：配色、卡片形态、数据可视化选型
   - 交互：筛选联动、钻取、悬浮详情、时间轴
3. **约束**：
   - 必须是**业务系统界面**，不是需求分析展示
   - 必须覆盖所有 FR 的业务能力（`example` 字段提供模拟数据）
   - 必须可交互（Vue 响应式，参考 `vendor/vue.global.prod.js` 内联方式）
   - 自包含单 HTML 文件，可 `file://` 直接打开
4. **保存**：`./output/<标题>-creative.html`

两个版本供用户对比，启发设计讨论。

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