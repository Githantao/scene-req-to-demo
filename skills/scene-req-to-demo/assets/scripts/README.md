# scene-req-to-demo Pipeline Guide

> **Read this FIRST** when this skill is triggered. This is the canonical execution path.

## TL;DR

```
Input:  scene text (Chinese natural language)
Output: JSON analysis → Markdown .md + self-contained Demo .html
```

The LLM does **semantic work** (understands scene, proposes structure). The 4 scripts below do **mechanical work** (validate, format, render). Script code is **NOT** loaded into LLM context — only their JSON I/O is.

## The 4 Scripts (call order)

### 1. `analyze.py` — Phase 1 validation

**When**: After LLM produces `analysis` JSON for one scene.

```bash
cat input.json | python3 analyze.py
```

**Input**:
```json
{
  "scene": "...",
  "analysis": { ... }   // LLM-produced, must match schema below
}
```

**Output** (stdout JSON):
- `status: "ok"` — ready for next phase
- `status: "needs_correction"` — LLM must fix errors listed
- `status: "duplicate_detected"` — overlaps with previous scenes, LLM should rename or merge
- `domain_info.matched` — bool, if true load `assets/domain-railway.md` next

Also reads stdin without `analysis` field → returns `needs_llm_analysis` with domain detection.

---

### 2. `validate-anchors.py` — Phase 3 post-merge

**When**: After merging all scene analyses (Phase 3 complete).

```bash
cat merged.json | python3 validate-anchors.py
```

**Input**:
```json
{
  "analysis": { ... full merged analysis ... },
  "previous_scenes": [optional, for dedup]
}
```

**Output**: Per-check `ok`/`error` status + warnings list. Fix all `errors` before Phase 4. Warnings can be acknowledged.

---

### 3. `render-markdown.py` — Phase 4 doc

**When**: After Phase 3 passes (no errors).

```bash
cat merged.json | python3 render-markdown.py > output.md
```

Renders 6-section Markdown per `assets/output-template.md` schema. No errors possible (LLM-controlled input).

---

### 4. `render-demo.py` — Phase 4 business system Demo

**When**: Same as render-markdown (Phase 4).

```bash
cat merged.json | python3 render-demo.py > demo.html
```

Generates self-contained Vue-inlined HTML. Open in Chrome (file:// OK).

---

## JSON Schema (single source of truth)

```json
{
  "businessContext": {
    "proposer": "string — who requested",
    "problemLevel": "string — 工班/车间/段/部/职能",
    "currentState": "string — current pain",
    "targetLevel": "string — 信息化/自动化/智能化",
    "expectedBenefit": "string — at least 1 quantified metric"
  },
  "requirements": {
    "title": "string — system name",
    "diagramType": "flowchart | sequenceDiagram | classDiagram | stateDiagram-v2 | erDiagram | requirementDiagram",
    "layers": {
      "business": { "goal": "...", "value": "..." },
      "user": { "scenario": "...", "painPoints": ["..."] },
      "system": { "summary": "..." }
    },
    "mainRequirement": { "name": "...", "description": "..." },
    "systemBoundary": "string",
    "stakeholders": ["..."],
    "functionalRequirements": [
      {
        "id": "FR-1",
        "name": "...",
        "description": "...",
        "priority": "high | medium | low",
        "uiLocation": "...",          // maps to Demo card location
        "dataSource": "...",           // maps to Demo data source
        "configurable": true | false,
        "defaultState": "默认开启 | 默认关闭",
        "example": "..."              // maps to Demo mock data
      }
      // 2-6 FRs
    ],
    "dataFlows": [
      { "from": "...", "to": "...", "data": "...", "type": "input|output|storage" }
    ],
    "interfaces": [],                // empty array OK, marked "无"
    "dataRequirements": [],
    "nonFunctionalRequirements": ["..."]  // label 【硬性约束】 vs 【假设】
  },
  "mermaidCode": "string"
}
```

**Constraints**:
- `businessContext` — all 5 fields required
- `mainRequirement` — exactly 1
- `functionalRequirements` — 2-6 items, each with all 5 anchors + priority
- `diagramType` — must be one of 6 enum values
- `interfaces`/`dataRequirements` — empty arrays OK

---

## 5 Anchor Rules (every FR must include ALL)

| # | Anchor | Field | Meaning |
|---|---|---|---|
| 1 | 页面位置 | `uiLocation` | Which page/module/area |
| 2 | 数据来源 | `dataSource` | What data feeds it |
| 3 | 配置方式 | `configurable` | bool — project-level configurable? |
| 4 | 默认状态 | `defaultState` | 默认开启/关闭 |
| 5 | 示例 | `example` | Real scenario example |

Missing any anchor = validation fails.

---

## FR粒度控制 (粒度粒度控制)

✅ Correct粒度: "用户登录认证" / "工单列表" / "统计看板"
❌ Too细: "显示登录页" / "点击按钮" / "输入用户名"
❌ Too粗: "报警管理系统" / "客服系统"

**判断标准**: one FR = one Demo card = one development task.

---

## Sample input/output

See `examples/sample.json` (3-FR complete example).

---

## Reference docs (load on demand, not all upfront)

| Doc | When to read |
|---|---|
| `assets/prototype-styles-tokens.md` | Phase 4 design reference |
| `assets/domain-railway.md` | Scene matches railway/signal keywords |
| `assets/mermaid-rules.md` | Phase 4 diagram generation |
| `assets/output-template.md` | Markdown template details (fallback) |

---

## Self-checks before calling each script

Before `analyze.py`:
- [ ] All 5 `businessContext` fields present
- [ ] `mainRequirement` is exactly 1
- [ ] 2-6 FRs, each with all 5 anchors
- [ ] `diagramType` valid enum
- [ ] `interfaces` and `dataRequirements` are arrays (even if empty)

Before `validate-anchors.py`:
- [ ] Merged result has ≥3 FRs for meaningful Demo
- [ ] No duplicate FR names across scenes

Before `render-markdown.py` / `render-demo.py`:
- [ ] All previous `validate-anchors.py` errors resolved
- [ ] Business is in Phase 4 (user confirmed no more scenes)