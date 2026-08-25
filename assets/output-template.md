# Markdown 输出模板 — 6-Section Requirement Document

> 本模板定义 Markdown 需求文档的标准结构。
> Agent 在完成 JSON 中间产物后，按此模板渲染 Markdown。
> 所有 6 段必须出现，空段标注"无"而非省略。

---

## 模板全文

```markdown
# {title} 需求文档

> 生成时间：{YYYY-MM-DD HH:mm} | 耗时：{analysisTime} | 图表类型：{diagramType}

---

## 一、业务背景及目标

### 提出方

{businessContext.proposer}

### 问题层级

{businessContext.problemLevel}

### 现状痛点

{businessContext.currentState}

### 解决层级

{businessContext.targetLevel}

### 预期成效

{businessContext.expectedBenefit}

---

## 二、总体需求

> **{mainRequirement.name}**
>
> {mainRequirement.description}

**系统边界**：{systemBoundary}

**干系人**：{stakeholders.join("、")}

### 三层需求

| 层级 | 内容 |
|------|------|
| 🏢 业务层 | **目标**：{layers.business.goal} · **价值**：{layers.business.value} |
| 👤 用户层 | **场景**：{layers.user.scenario} · **痛点**：{layers.user.painPoints.join("；")} |
| ⚙️ 系统层 | **职责**：{layers.system.summary} |

---

## 三、功能需求

> 共 {functionalRequirements.length} 项功能，{highCount} 项高优 / {mediumCount} 项中优 / {lowCount} 项低优

### FR-1 {name} `{priority}`

{description}

| 锚点 | 内容 |
|------|------|
| 📍 页面位置 | {uiLocation} |
| 🔗 数据来源 | {dataSource} |
| ⚙️ 配置方式 | {configurable ? "支持按项目配置" : "固定逻辑"} |
| 🔘 默认状态 | {defaultState} |
| 💡 示例 | {example} |

---

### FR-2 {name} `{priority}`

{description}

| 锚点 | 内容 |
|------|------|
| 📍 页面位置 | {uiLocation} |
| 🔗 数据来源 | {dataSource} |
| ⚙️ 配置方式 | {configurable ? "支持按项目配置" : "固定逻辑"} |
| 🔘 默认状态 | {defaultState} |
| 💡 示例 | {example} |

---

> ... 重复至 FR-N

---

## 四、接口需求

{interfaces.length > 0 ? interfaces.map(i => `- ${i}`).join("\n") : "无。\n\n> 本系统暂无外部接口依赖。"}

---

## 五、数据需求

{dataRequirements.length > 0 ? dataRequirements.map(d => `- ${d}`).join("\n") : "无。\n\n> 本系统暂无特殊数据约束。"}

**数据流**：

| 来源 | 目标 | 数据 | 类型 |
|------|------|------|------|
| {from} | {to} | {data} | {type} |

> ... 每条 dataFlow 一行，type: input=输入 / output=输出 / storage=存储

---

## 六、非功能性需求

{nonFunctionalRequirements.length > 0 ? nonFunctionalRequirements.map(n => `- ${n}`).join("\n") : "无明确非功能约束。\n\n> 建议后续补充性能/安全/可用性要求。"}

> 标注说明：【硬性约束】为必须满足的条件，【假设】为待验证的前提

---

## 附录 A：流程图

> 图表类型：`{diagramType}`

​```mermaid
{mermaidCode}
​```

---

## 附录 B：结构化数据

<details>
<summary>点击展开 JSON</summary>

​```json
{完整 JSON 中间产物，格式化输出}
​```

</details>

---

*本文档由 scene-req-to-demo 自动生成 | 渲染：Mermaid {mermaidVersion}*
```

---

## 字段映射表

| 模板占位符 | JSON 路径 | 为空时处理 |
|-----------|-----------|-----------|
| `{title}` | `requirements.title` | "未命名系统" |
| `{businessContext.*}` | `businessContext.*` | "待明确" |
| `{mainRequirement.*}` | `requirements.mainRequirement.*` | 不可为空（必有1条） |
| `{systemBoundary}` | `requirements.systemBoundary` | "待明确" |
| `{stakeholders}` | `requirements.stakeholders` | "待明确" |
| `{layers.*}` | `requirements.layers.*` | 对应层显示"待明确" |
| `{functionalRequirements}` | `requirements.functionalRequirements` | 至少2条 |
| `{priority}` | `fr.priority` | 显示为徽标：`high=高优` `medium=中优` `low=低优` |
| `{uiLocation}` 等5锚点 | `fr.uiLocation` 等 | "待明确"（但验证时会告警） |
| `{interfaces}` | `requirements.interfaces` | 显示"无" |
| `{dataRequirements}` | `requirements.dataRequirements` | 显示"无" |
| `{dataFlows}` | `requirements.dataFlows` | 显示"暂无数据流" |
| `{nonFunctionalRequirements}` | `requirements.nonFunctionalRequirements` | 显示"无明确约束" |
| `{mermaidCode}` | `mermaidCode` | 显示 fallback 图表 |
| `{diagramType}` | `requirements.diagramType` | `flowchart`（默认） |

---

## 渲染规则

1. **6 段必须全部出现**，即使某段为空也显示标题 + "无"
2. 每条 FR 的 **5 锚点表格必须完整**，空锚点显示"待明确"并在验证清单中标记
3. 优先级徽标：`high` → 🔴 高优 / `medium` → 🟡 中优 / `low` → 🔵 低优
4. Mermaid 代码块使用 ````mermaid` 包裹，GitHub/Notion/Obsidian 可直接渲染
5. JSON 附录使用 `<details>` 折叠，避免过长影响阅读
6. 所有中文标点使用全角（，。：；），表格内除外
