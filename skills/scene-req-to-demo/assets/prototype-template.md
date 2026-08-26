# Demo 原型模板 — Index

> **Phase 4（Demo 生成）时**：完整读取 [`prototype-template-detail.md`](./prototype-template-detail.md)。
> **Phase 1-3（需求分析）时**：仅读本文档定位即可，避免上下文占用（约 17KB → ~2KB）。

## 一、定位澄清

| | 需求文档（Markdown） | 业务系统原型（Demo HTML） |
|---|---|---|
| 内容 | 6 段 + 5 锚点 FR + Mermaid 流程图 | 按 FR 实现的真实业务界面 |
| 受众 | 评审、归档、开发任务输入 | 业务方/甲方 — "做出来长什么样" |
| 形态 | 静态文档 | 可交互界面，带模拟数据 |
| 示例 | 之前给的截图（郑州地铁/沈阳铁路局大屏）即为此类原型 | — |

**FR 到 Demo 的映射**：每条 FR 对应 Demo 中的一个可交互功能区，`example` 字段提供该区的模拟数据。

```
FR-1 "浏览车站数统计" → Demo 中的统计卡片（显示 "9/13  69%"）
FR-2 "系统发现异常数统计" → Demo 中的异常计数卡片（可点击下钻）
FR-3 "人工处理闭环数统计" → Demo 中的闭环率卡片（三态区分）
FR-4 "统计维度与可视化" → Demo 中的筛选控件 + 趋势图
```

---


## 二、技术选型

| 项 | 选择 | 理由 |
|----|------|------|
| 框架 | Vue 3（内联） | 响应式+组件化；内联 `vue.global.prod.js`（~160KB）确保 `file://` 双击即用，无需网络 |
| 图表 | 原生 SVG / Canvas 或 Chart.js（按需 CDN + 降级） | 业务图表（柱状/环形/折线）用轻量方案；Mermaid 仅随 Markdown 文档交付，不在 Demo 中 |
| 文件形态 | 自包含单 HTML | 双击即用，无需 `npm install` / `vite build`，跨操作系统 |

```html
<!-- Vue 已内联，不依赖 CDN -->
<script>/* vue.global.prod.js 内联内容约 160KB */</script>
<style>
  /* 样式以 prototype-styles-tokens.md 的 Design Tokens 为准；约束版 CSS 已内置于 render-demo.py */
</style>
```

> **为什么 Vue 必须内联**：`file://` 协议下 `type="module"` 受 CORS 限制，且 CDN 可能不可达。内联 Vue 可保证 Demo 在 `file://` 双击时立即可见。

---


## 详细指南引用

| 阶段 | 读取文件 |
|------|---------|
| Phase 1-3（需求分析） | 本文件（定位澄清 + 技术选型） |
| Phase 4（Demo 生成） | [`prototype-template-detail.md`](./prototype-template-detail.md)（布局/组件/交互/构建/防坑） |

## 详细指南大纲（Phase 4 加载）

- 三、Demo 设计原则（FR→功能区映射、界面类型判断、模拟数据）
- 四、整体布局 — 12 列网格拼装（Dashboard 形态为例）
- 五、组件规范（Header / 统计卡片 / 中央主视区 / 筛选 / 明细）
- 六、交互行为（筛选联动、卡片下钻、Tab 切换、主题）
- 七、参考页面处理（截图/HTML/文字描述 → 叠加/风格复制/全新三种模式）
- 八、构建步骤（Agent 执行 7 步）
- 九、单 HTML 文件模板骨架
- 十、代码生成防坑规则（5 类：script 转义 / module CORS / Vue 绑定 / f-string 冲突 / CDN 依赖）
- 十一、与 Markdown 文档的一致性

---

> 完整内容见 `prototype-template-detail.md`。
