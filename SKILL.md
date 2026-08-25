---
name: scene-req-to-demo
description: "Transform natural-language scene descriptions into structured requirement documents (6-section Markdown), high-fidelity interactive frontend prototypes (industrial dark-blue dashboard), and Mermaid diagrams. Supports optional railway/CBTC domain knowledge injection. Use when the user wants to turn a vague idea or oral description into reviewable, developable, testable requirement deliverables."
license: MIT
compatibility: "Claude Code (~/.claude/skills), OpenCode/Amp (~/.agents/skills), Opencode (~/.config/opencode/skills). Pure Markdown + HTML + JSON, no build step required."
metadata:
  author: scene-req-to-demo
  version: "0.0.2"
  domain: requirements-engineering
  cluster: software
  type: generative
  mode: assistive
---

# Scene Requirements Generator — 场景需求生成器

> **一句话**：自然语言场景描述 → 六段式需求文档 + 业务系统前端原型 Demo + 结构化 JSON

## Purpose

You transform a vague natural-language scene description into three consistent, reviewable deliverables:

| # | Deliverable | Format | Audience | 内容 |
|---|-------------|--------|----------|------|
| 1 | 结构化需求文档 | Markdown（六段式） | 评审、归档、导入项目管理工具 | 6 段 + 5 锚点 FR + Mermaid |
| 2 | 业务系统前端原型 | 自包含单 HTML 文件 | 业务方/甲方/开发 — 直观感受"做出来长什么样" | 按 FR 实现的真实业务界面，带模拟数据与可交互功能 |
| 3 | 结构化数据 | JSON（含 Mermaid 代码） | 程序化消费、导入其他工具 | 完整中间产物 |

> **关键区分**：Demo 是**业务系统本身的前端原型**（如：统计看板、工单列表、管辖地图），不是需求文档的展示页。每条 FR 对应 Demo 中的一个可交互功能区，`example` 字段提供模拟数据。

All three are rendered from a single JSON intermediate result — the requirements drive both the document and the business system prototype.

---

## When to Use

Trigger when the user says (or implies) any of:

- 场景描述 / 需求分析 / 需求文档 / 原型 / Demo / 帮我分析这个场景
- 自然语言转需求 / 场景转需求 / 把这个想法整理成需求
- "我想做一个..." / "需要一个系统..." / "能不能帮我把...整理一下"
- 任何包含"把一段话/一个想法变成可评审的需求"意图的请求

**Do NOT trigger** when the user is asking to diagnose whether a requirement is valid (use `requirements-analysis` instead) or to write code for an already-defined requirement.

### Relationship with `requirements-analysis`

| Skill | Role | When |
|-------|------|------|
| `requirements-analysis` | 诊断：问题是否清晰、约束是否明确、范围是否合理（RA0–RA5） | 前置 — 先确认"要解决什么问题" |
| `scene-req-to-demo` (this skill) | 生成：把清晰的场景描述变成可交付的需求文档+原型 | 后置 — 再把"要做什么"落到文档和 Demo |

If the user's description is very vague or solution-first, consider running `requirements-analysis` first to clarify the problem, then use this skill to generate deliverables.

---

## Domain Auto-Detection

Before analysis, scan the scene description for railway/signal domain keywords. If matched, load `assets/domain-railway.md` and inject its terminology and rules into the analysis prompt.

**Detection keywords**:

```
铁路 / 信号 / 联锁 / 进路 / 道岔 / 闭塞 / 轨道电路 / 接近锁闭 / 敌对进路 / 故障导向安全
CBTC / TACS / ZC / VOBC / DCS / OC / MA / 移动闭塞 / 区域控制器 / 车载控制器
地铁 / 城轨 / 调度 / 行车 / 列控 / ATS / ATO / ATP / SIL / T2T / 信号机 / 轨道
```

---

## Workflow — Iterative Batch + Reference-Aware (4 Phases)

```
Phase 1 — Iterative Requirement Collection (repeatable)
  │
  │  Scene 1 → Domain Detection → Background Analysis → Structured Analysis → Text requirement (简版：需求名称+总体需求+功能需求，便于人工审核)
  │  Scene 2 → ...same...
  │  Scene N → ...same...
  │  Each scene produces 1 mainRequirement + 2–6 FRs (5 anchors each)
  │  Per-scene output format (text, no file):
  │    【需求名称】{title}
  │    【总体需求】{mainRequirement.name}：{description}
  │    【功能需求】FR-1..N（每条：名称+描述+5锚点压缩为一行）
  │  After each scene, ask: "是否还有需求？"
  │    有 → next scene
  │    无 → Phase 2
  │  Note: 全量的 6 段（业务背景/接口/数据/NFR 等）仅在 Phase 4 的 Markdown 中完整呈现
  │
  ▼
Phase 2 — Reference Page Check
  │  Ask: "是否有基础页面或参考页面？"
  │  Input options:
  │    - Screenshot (PNG/JPG) — extract layout, colors, component style
  │    - HTML file — extract structure, styles, component patterns
  │    - Text description — "现有XX系统的XX页面"
  │  Result:
  │    有 → Mode A: Overlay (add new FR zones onto existing layout) or
  │           Mode B: Style Copy (replicate reference page's visual language)
  │    无 → Mode C: Fresh (generate from scratch, default dark-blue industrial)
  │
  ▼
Phase 3 — Merge & Verify
  │  Merge all collected FRs: deduplicate, reassign IDs (FR-1..N), check priority balance
  │  Merge businessContext: combine proposers/stakeholders, unify problem statement
  │  Diagram generation per assets/mermaid-rules.md (one diagram covering merged scope)
  │  Quality verification per assets/verification-checklist.md:
  │    □ 5-anchor completeness per FR
  │    □ 6-section completeness (empty sections marked "无")
  │    □ Hallucination / omission / over-decomposition / logic consistency
  │    □ Batch deduplication (no overlapping FRs)
  │    □ Demo readiness (merged FRs ≥ 3, ideally 6–12 for a full dashboard)
  │
  ▼
Phase 4 — Triple Output (from merged result)
  │
  ├─→ Markdown 6-section requirement document (assets/output-template.md) — merged
  ├─→ Business System Demo HTML — single self-contained file
  │     Mode A: Overlay on base page layout + new feature zones
  │     Mode B: Reference style + all feature zones
  │     Mode C: Fresh dashboard per assets/prototype-template.md + prototype-styles.md
  └─→ Structured JSON (embedded in Markdown code block, for programmatic use)
```

### Single-Scene Shortcut

For a single scene that already has sufficient scope (≥ 3 FRs), Phases 1–2 can be done in one turn — collect the scene, optionally ask about reference page, then directly proceed to Phases 3–4.

---

## Output Contract

### JSON Intermediate Schema

The analysis in Step 3 must produce JSON conforming to this schema. This JSON is the single source of truth for all three outputs.

```json
{
  "businessContext": {
    "proposer": "string — 提出方",
    "problemLevel": "string — 问题层级（工班/车间/段/部/职能）",
    "currentState": "string — 现状痛点",
    "targetLevel": "string — 解决层级（信息化/自动化/智能化）",
    "expectedBenefit": "string — 预期成效（降成本/降人力/提效率/提质量，至少1项可量化）"
  },
  "requirements": {
    "title": "string — 系统名称（即业务系统名称，如：智能浏览统计看板）",
    "diagramType": "flowchart | sequenceDiagram | classDiagram | stateDiagram-v2 | erDiagram | requirementDiagram",
    "layers": {
      "business": { "goal": "业务目标", "value": "业务价值" },
      "user": { "scenario": "用户场景", "painPoints": ["痛点"] },
      "system": { "summary": "系统职责" }
    },
    "mainRequirement": { "name": "总体需求名称", "description": "概括描述" },
    "systemBoundary": "string — 系统边界",
    "stakeholders": ["干系人"],
    "functionalRequirements": [
      {
        "id": "FR-1",
        "name": "功能名称",
        "description": "可测试的描述",
        "priority": "high | medium | low",
        "uiLocation": "页面/模块位置（映射到 Demo 的功能区）",
        "dataSource": "数据来源/触发条件",
        "configurable": true,
        "defaultState": "默认开启 | 默认关闭",
        "example": "具体场景举例（映射到 Demo 的模拟数据）"
      }
    ],
    "dataFlows": [
      { "from": "来源", "to": "目标", "data": "数据", "type": "input | output | storage" }
    ],
    "interfaces": ["接口需求，无则为空数组"],
    "dataRequirements": ["数据需求，无则为空数组"],
    "nonFunctionalRequirements": ["非功能约束，标注硬性约束 vs 假设"]
  },
  "mermaidCode": "string — Mermaid diagram code（流程/时序/状态等，随 Markdown 文档交付）"
}
```

**Constraints**:

- `businessContext` — all 5 fields required, no omission
- `mainRequirement` — exactly 1
- `functionalRequirements` — 2–6 items, each with all 5 anchors + `priority`
- `diagramType` — must be one of the 6 enum values
- `interfaces` / `dataRequirements` — must be present even if empty (mark "无" in Markdown)
- All descriptions in Chinese
- JSON must be strictly valid

### Markdown Output

Render per `assets/output-template.md` — 6 sections + Mermaid code block. This is the **requirements document** for review and downstream handoff.

### Demo HTML Output — Business System Frontend Prototype

Render per `assets/prototype-template-detail.md` + `assets/prototype-styles-css.md`:

- Single self-contained HTML file, Vue inlined (~160KB) for `file://` compatibility
- **This is the business system itself** — e.g., a monitoring dashboard, work order list, or jurisdiction map — not a requirements viewer
- Each FR maps to an interactive feature zone in the Demo; `example` field provides mock data
- Reference-aware: if a base/reference page was provided in Phase 2, Demo overlays new features onto it or replicates its visual style; otherwise uses default dark-blue industrial theme
- Interactions: filter/search, tab switching, drill-down, data visualization — as the real system would behave
- Mock data derived from FR `example` fields; no backend required
- Zero build step — double-click to open in Chrome

---

## Asset Loading Strategy — Context Optimization

To fit within 256K context budgets (local models), this skill **lazy-loads** large assets:

| Phase | Stage | Required Assets | Approx. Size |
|-------|-------|-----------------|--------------|
| **Phase 1** | Per-scene requirement collection | `SKILL.md` + `analysis-prompt.md` + `requirement-writing-guide.md` + `prototype-styles-tokens.md` + `prototype-template.md` (slim) | ~30 KB |
| **Phase 2** | Reference page check | Same as Phase 1 | ~30 KB |
| **Phase 3** | Merge & verify | + `verification-checklist.md` | ~37 KB |
| **Phase 4** | Triple output | + `output-template.md` + `prototype-template-detail.md` + `prototype-styles-css.md` (only when building Demo) | ~67 KB |

**Key principle**: `prototype-styles.md` and `prototype-template.md` are split into a **slim index** (always-readable) and a **detail file** (Phase 4 only). Do NOT load detail files in Phase 1-3 — they contain only CSS/HTML skeleton code needed for Demo generation.

---

## LLM Backend — Backend-Agnostic

This skill defines **what** to generate (prompt + schema + templates), not **how** to call an LLM. The agent should use whatever LLM is available:

| Backend | How to use this skill's prompt |
|---------|-------------------------------|
| Claude API | Send `assets/analysis-prompt.md` as system prompt + scene as user message |
| OpenAI API | Same — system + user messages, `temperature: 0.2, max_tokens: 4096` |
| Ollama (local) | Same, via `http://localhost:11434/v1/chat/completions` |
| Any OpenAI-compatible (WebLLM / Ollama / LM Studio) | Same, via `chat.completions.create()` |

The skill does NOT bundle or require any specific LLM SDK. See `assets/analysis-prompt.md` for the full prompt text.

**Stability**: All API calls should include `seed: 42` where supported, `temperature: 0.2` for deterministic structured output.

---

## Assets Index

| Asset | Phase | Purpose |
|-------|-------|---------|
| `assets/analysis-prompt.md` | 1-4 | Core analysis prompt — rules, schema, FR granularity, RaR/CoVe |
| `assets/domain-railway.md` | 1-4 (conditional) | Railway/signal domain — glossary, interlocking + CBTC/TACS rules |
| `assets/requirement-writing-guide.md` | 1-4 | Requirement writing guide — 5 anchors, 6 sections, testability |
| `assets/verification-checklist.md` | 3 | Quality checklist — CoVe + anchor + section completeness |
| `assets/output-template.md` | 4 | Markdown 6-section template + field mapping |
| `assets/mermaid-rules.md` | 4 | Diagram type selection + generation rules (6 types) |
| `assets/prototype-styles.md` | 1-4 (slim index) | Style index — what styles/components exist |
| `assets/prototype-styles-tokens.md` | 1-4 (light) | Design tokens + component inventory reference |
| `assets/prototype-styles-css.md` | 4 only (heavy) | Full CSS code to inline into Demo HTML |
| `assets/prototype-template.md` | 1-4 (slim index) | Template index — positioning + tech choice |
| `assets/prototype-template-detail.md` | 4 only (heavy) | Full Demo guide — layout, components, build steps, pitfalls |

**Heavy files loaded only in Phase 4**: `prototype-styles-css.md` (11 KB) + `prototype-template-detail.md` (15 KB). Total Phase 4 footprint is ~67 KB. Phase 1-3 footprint is ~30 KB.

---

## References

- Word template paradigm: 6-section document (`报警新增功能.docx`) + 11-chapter functional panorama (`需求描述示例V1.doc`)
- Frontend design language: CASCO 12×24 grid, dark-blue industrial dashboard (3 screenshots + 2 HTML references)
- Prompt engineering: RaR (Rephrase and Respond) + CoVe (Chain-of-Verification) + seed stability
- Existing skills: `requirements-analysis` (diagnostic) + `mermaid-diagrams` (syntax) + `frontend-design` / `baoyu-design` (aesthetics)
- Similar projects researched: [franklinxkk/ai-delivery-spec](https://github.com/franklinxkk/ai-delivery-spec) (lifecycle entry diagnosis), [Paritck/prototype-spec-html](https://github.com/Paritck/prototype-spec-html) (element-level annotation), [qierkang/product-dev-skill](https://github.com/qierkang/product-dev-skill) (reverse direction: prototype → requirements)
