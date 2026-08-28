# scene-req-to-demo Pipeline Guide

> **Read this FIRST** when this skill is triggered. This is the canonical execution path.
> 脚本的 stdin/stdout 契约 + JSON schema 单一事实源 + 各阶段自检清单。**只读本文件即可正确调用全部脚本，无需打开脚本源码。**
> v0.0.5rc1 调整：仅 `render-demo.py` 增 `communication` 子系统（关键词 / SUBSYSTEM_META / ZONE_TAXONOMY 三处同步），其他 4 脚本与 v0.0.5 字节级一致。

## TL;DR

```
Input:  scene text (Chinese natural language)
Output: JSON analysis → Markdown .md + 约束版 Demo .html (+ 创意版 .html, LLM 生成)
```

The LLM does **semantic work** (understands scene, proposes structure). The 4 scripts below do **mechanical work** (validate, format, render). Script code is **NOT** loaded into LLM context — only their JSON I/O is.

所有脚本支持 `--output-dir ./output`（按 `title` 自动命名，**推荐**）；不带该参数则输出到 stdout。

## The 4 Scripts (call order)

### 1. `analyze.py` — Phase 1 验证 + 领域/子系统检测

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
- `domain_info.subsystem` — `safety | ats | ctc | monitoring | iom | communication | general`（v0.0.5rc1 增 communication），驱动安全标记与 Demo 布局
- `domain_info.subsystem_confidence` — `high | medium | none`

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

**Output**: Per-check `ok`/`error` status + warnings list. Fix all `errors` before Phase 4. Checks include:
- `5_anchors_per_fr` / `6_section_completeness` / `batch_dedup` / `demo_readiness` / `cove_consistency`
- `safety_and_acceptance` — FR 是否标注 `safetyRelevance`/`acceptanceCriteria`；安全 FR 的 uiLocation 不得指向界面
- `configurable_distribution` — 全 true 时提示复核（防摆设）
- `gap_discipline` — 量化指标未标 `[假设]/[GAP]` 时提示（防编造）

---

### 3. `render-markdown.py` — Phase 4 doc

**When**: After Phase 3 passes (no errors).

```bash
python3 render-markdown.py --output-dir ./output < merged.json
```

Renders 6-section Markdown per `assets/output-template.md` schema（已内嵌，模板文件仅作 fallback）。检测到安全苛求功能时**自动注入安全声明**。

---

### 4. `render-demo.py` — Phase 4 约束版 Demo

**When**: Same as render-markdown (Phase 4).

```bash
python3 render-demo.py --output-dir ./output < merged.json
# 参考页面样式覆盖：
python3 render-demo.py --output-dir ./output --css-file ./output/ref-styles.css < merged.json
# 文件名后缀（防撞）：
python3 render-demo.py --output-dir ./output --suffix=-v2 < merged.json
```

Generates self-contained Vue-inlined HTML. Open in Chrome (file:// OK). 单页面承载所有 FR，按 FR 角色自动布局。检测到安全苛求功能时**自动注入"安全功能阐述图"横幅+角标**。

> **创意版**（`<标题>-creative.html`）由 LLM 在 Phase 4b 生成，参考 `prototype-domain-ui.md` + `prototype-tech-inspiration.md`，**不经由脚本**（`subsystem=safety` 时跳过）。

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
    "diagramType": "flowchart | sequenceDiagram | classDiagram | stateDiagram-v2 | erDiagram",
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
        "safetyRelevance": "安全相关 | 非安全相关",   // drives Demo safety banner
        "acceptanceCriteria": "...",               // testable acceptance criteria
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
- `functionalRequirements` — 2-6 items, each with all 5 anchors + priority + safetyRelevance + acceptanceCriteria
- `diagramType` — must be one of the enum values
- `interfaces`/`dataRequirements` — empty arrays OK
- **GAP 纪律** — 量化指标无依据必须标 `[假设]/[GAP]`，禁止编造

---

## 5 Anchor Rules (every FR must include ALL)

| # | Anchor | Field | Meaning |
|---|---|---|---|
| 1 | 页面位置 | `uiLocation` | Which page/module/area（安全 FR 指向逻辑层，非界面） |
| 2 | 数据来源 | `dataSource` | What data feeds it |
| 3 | 配置方式 | `configurable` | bool — project-level configurable? |
| 4 | 默认状态 | `defaultState` | 默认开启/关闭 |
| 5 | 示例 | `example` | Real scenario example |

Missing any anchor = validation fails.

---

## FR粒度控制

✅ Correct粒度: "用户登录认证" / "工单列表" / "统计看板"
❌ Too细: "显示登录页" / "点击按钮" / "输入用户名"
❌ Too粗: "报警管理系统" / "客服系统"

**判断标准**: one FR = one Demo card = one development task.

---

## Sample input/output

See `examples/sample.json` (complete example).

---

## Reference docs (load on demand, not all upfront)

| Doc | When to read |
|---|---|
| `assets/prototype-styles-tokens.md` | Phase 4 design reference |
| `assets/domain-railway.md` | Scene matches railway/signal keywords（按 subsystem 选章节） |
| `assets/mermaid-rules.md` | Phase 4 diagram generation |
| `assets/output-template.md` | Markdown template details (fallback) |
| `assets/prototype-domain-ui.md` | Phase 4b 创意版 — 子系统界面骨架 |
| `assets/prototype-tech-inspiration.md` | Phase 4b 创意版 — 信息化技术灵感 |

---

## Self-checks before calling each script

Before `analyze.py`:
- [ ] All 5 `businessContext` fields present
- [ ] `mainRequirement` is exactly 1
- [ ] 2-6 FRs, each with all 5 anchors + safetyRelevance + acceptanceCriteria
- [ ] `diagramType` valid enum
- [ ] `interfaces` and `dataRequirements` are arrays (even if empty)
- [ ] 量化指标已标 `[假设]/[GAP]` 或有标准依据

Before `validate-anchors.py`:
- [ ] Merged result has ≥3 FRs for meaningful Demo
- [ ] No duplicate FR names across scenes

Before `render-markdown.py` / `render-demo.py`:
- [ ] All previous `validate-anchors.py` errors resolved
- [ ] Business is in Phase 4 (user confirmed no more scenes)
