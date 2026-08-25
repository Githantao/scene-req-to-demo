# Demo HTML 原型模板 — Business System Frontend Prototype

> 本文件定义**业务系统前端原型** Demo HTML 的生成规范。
> **核心定位**：Demo 是业务系统本身的可交互界面（带模拟数据），不是需求文档的展示页。
> 样式细节见 `prototype-styles.md`，本文件聚焦**结构、组件与构建逻辑**。

---

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
  /* 内联 prototype-styles.md 的全部样式 */
</style>
```

> **为什么 Vue 必须内联**：`file://` 协议下 `type="module"` 受 CORS 限制，且 CDN 可能不可达。内联 Vue 可保证 Demo 在 `file://` 双击时立即可见。

---

## 三、Demo 设计原则

### 3.1 从 FR 推导界面

```
输入：JSON 中间产物（title + functionalRequirements + businessContext）
  │
  ├─ title → Demo 的系统/页面标题
  ├─ FR-1/F R-2/... → Demo 的功能区（卡片/表格/图表/表单）
  │    ├─ uiLocation → 该功能区在 Demo 中的位置
  │    ├─ example → 该功能区的模拟数据
  │    └─ priority → 视觉权重（高优更大/更醒目）
  ├─ businessContext → Demo 顶部的业务背景提示（可选）
  └─ dataFlows → Demo 中数据流转的交互逻辑（如：筛选→刷新）
```

### 3.2 界面类型判断

根据 `title` 和 FR 内容自动选择最合适的界面形态：

| 场景特征 | Demo 形态 | 参考 |
|---------|----------|------|
| 统计/看板/监测/大屏 | Dashboard 大屏（多宫格统计卡片 + 图表 + 地图） | 郑州地铁/沈阳/上海截图 |
| 工单/任务/工单管理 | 列表+详情页（表格 + 筛选 + 详情抽屉） | 传统管理系统 |
| 流程/审批/工单流转 | 流程图+状态机（步骤条 + 操作按钮） | 审批流 |
| 表单/配置/设置 | 表单页（输入控件 + 配置开关） | 后台配置 |
| 地图/管辖/线路 | 地图视图（SVG 地图 + 标记 + 悬浮详情） | 沈阳管辖图 |

### 3.3 模拟数据

- 每条 FR 的 `example` 字段即为该功能区的模拟数据来源
- 补充合理的假数据使界面饱满（如：表格 5–8 行，图表 5–7 个数据点）
- 数据需符合 FR 的 `dataSource` 描述（如：按线路分组、按等级分类）

---

## 四、整体布局 — 12 列网格拼装（Dashboard 形态为例）

> Dashboard 是最常见的形态（参考 3 张大屏截图），其他形态可简化。

```
┌──────────────────────────────────────────────────────────────┐
│  Header: [系统标题]                    [时间] [用户] [全屏]   │
├──────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌─────────────────────────────────┐ ┌───────┐ │
│  │ 侧边导航 │  │  顶部统计卡片区（FR-1/FR-2/FR-3） │ │ 右侧  │ │
│  │  (可选)  │  │  ┌─────┐ ┌─────┐ ┌─────┐        │ │ 面板  │ │
│  │  菜单    │  │  │FR-1 │ │FR-2 │ │FR-3 │  ...   │ │ (可选)│ │
│  │          │  │  │ 9/13│ │  5  │ │60%  │        │ │ 指标/ │ │
│  │          │  │  └─────┘ └─────┘ └─────┘        │ │ 预警  │ │
│  │          │  ├─────────────────────────────────┤ │       │ │
│  │          │  │  中央主视区                       │ │       │ │
│  │          │  │  (地图/图表/表格，按场景选择)      │ │       │ │
│  │          │  │  ┌─────────────────────────┐     │ │       │ │
│  │          │  │  │  地图 / 柱状图 / 表格    │     │ │       │ │
│  │          │  │  │  (FR-1~3 的数据可视化)   │     │ │       │ │
│  │          │  │  └─────────────────────────┘     │ │       │ │
│  │          │  ├─────────────────────────────────┤ │       │ │
│  │          │  │  底部功能区（FR-4 筛选/趋势等）   │ │       │ │
│  │          │  │  [日期▼] [线路▼] [车站▼] [搜索]  │ │       │ │
│  │          │  │  趋势图 / 明细表格                │ │       │ │
│  │          │  └─────────────────────────────────┘ │       │ │
│  └──────────┘  └─────────────────────────────────┘ └───────┘ │
├──────────────────────────────────────────────────────────────┤
│  Footer: 需求原型 · 生成时间                                  │
└──────────────────────────────────────────────────────────────┘
```

### 响应式断点

| 宽度 | 布局 |
|------|------|
| ≥ 1200px | 三栏：侧边(200px) + 中央(1fr) + 右侧(280px) |
| 768–1199px | 两栏：侧边隐藏为抽屉 + 中央(1fr) + 右侧(260px) |
| < 768px | 单栏：全部纵向堆叠 |

---

## 五、组件规范

### 5.1 Header — 标题栏

```html
<header class="proto-header">
  <div class="header-left">
    <h1>{{ title }}</h1>
    <span class="header-time">{{ currentTime }}</span>
  </div>
  <div class="header-right">
    <span class="user-info">admin</span>
    <button @click="toggleFullscreen">全屏</button>
    <button @click="toggleTheme">主题切换</button>
  </div>
</header>
```

### 5.2 统计卡片（对应 FR）

每个 FR 对应一张统计卡片，数据来自 `example`：

```html
<div class="stat-cards">
  <div v-for="fr in functionalRequirements" :key="fr.id"
       class="stat-card" :class="'priority-' + fr.priority"
       @click="onCardClick(fr)">
    <div class="stat-card-title">{{ fr.name }}</div>
    <div class="stat-card-value">{{ mockValue(fr) }}</div>
    <div class="stat-card-desc">{{ mockDesc(fr) }}</div>
  </div>
</div>
```

卡片样式参考 `prototype-styles.md` 的五色状态徽标体系：
- `high` → 红色发光边框
- `medium` → 橙色
- `low` → 蓝色

### 5.3 中央主视区

根据场景选择：

| 场景 | 组件 | 实现 |
|------|------|------|
| 统计/看板 | 柱状图/环形图/折线图 | 原生 SVG 或内联 Chart.js |
| 管辖/线路 | SVG 地图（站点/线路标记） | SVG + 悬浮详情 |
| 工单/列表 | 表格（带分页/排序） | HTML table + Vue 逻辑 |
| 流程/状态 | 步骤条/状态流转图 | CSS 步骤条 |

### 5.4 筛选控件

```html
<div class="filter-bar">
  <select v-model="filter.date"><option>今日</option><option>近7天</option><option>近30天</option></select>
  <select v-model="filter.line"><option>全部线路</option><option v-for="l in lines">{{ l }}</option></select>
  <button @click="onSearch">查询</button>
  <button @click="onReset">重置</button>
</div>
```

筛选联动：改变筛选条件 → 统计卡片数值和图表联动刷新（前端模拟，无需后端）。

### 5.5 明细表格/抽屉

点击统计卡片 → 弹出明细：

```html
<div v-if="showDetail" class="detail-drawer">
  <div class="drawer-header">
    <span>{{ currentFR.name }} — 明细</span>
    <button @click="showDetail = false">×</button>
  </div>
  <table class="detail-table">
    <tr v-for="row in mockDetailRows(currentFR)" :key="row.id">
      <td>{{ row.name }}</td><td>{{ row.value }}</td><td>{{ row.time }}</td>
    </tr>
  </table>
</div>
```

---

## 六、交互行为

| 交互 | 触发 | 行为 |
|------|------|------|
| 筛选 | 选择日期/线路/车站 | 统计卡片数值和图表联动刷新（模拟） |
| 卡片点击 | 点击统计卡片 | 弹出明细抽屉/表格，显示该 FR 的详细数据 |
| 图表交互 | 悬浮/点击图表元素 | 显示 tooltip 详情 |
| Tab 切换 | 点击 Tab（如管辖图↔数据分析图） | 中央主视区内容切换 |
| 主题切换 | 点击按钮 | `body` class 在 `theme-dark-blue` ↔ `theme-light-blue` 间切换 |
| 全屏 | 点击按钮 | `document.documentElement.requestFullscreen()` |

---

## 七、参考页面处理（Phase 2 产出）

> 对应 SKILL.md Phase 2 的"是否有基础页面/参考页面？"分支。

| 输入 | 识别 | 处理 |
|------|------|------|
| 截图（PNG/JPG） | 提取布局、配色、字体、组件样式、卡片/表格形态 | **风格复制**：新 Demo 复刻该视觉语言 |
| HTML 文件 | 提取 DOM 结构、CSS 变量、组件模式、交互逻辑 | **风格复制**或**功能叠加**（见下） |
| 文字描述 | 如"现有XX系统的XX页面" | 按描述推断风格/结构，结合默认样式 |

### 三种 Demo 模式

| 模式 | 条件 | 做法 | 适用场景 |
|------|------|------|----------|
| **A. 功能叠加** | 有基础页面 + 新增 FR | 保留原有布局/已实现的功能区，在其上新增 FR 对应的功能区/卡片；复用原有样式变量 | 迭代开发：已有系统新增模块 |
| **B. 风格复制** | 有参考页面，无需保留其功能 | 提取参考页的视觉特征（色板/字体/间距/卡片样式/导航形态），新 Demo 按此风格全新排布所有 FR | 全新系统但需与现有系统视觉一致 |
| **C. 全新生成** | 无参考页面 | 按本文件 §四 的默认布局 + `prototype-styles.md` 暗蓝工业风全新生成 | 从零开始的新系统 |

> **Agent 执行时**：收到参考材料后，先用一句话概括提取到的风格特征（如"深蓝大屏 + 12宫格 + 霓虹状态色"），再进入构建步骤。

---

## 八、构建步骤（Agent 执行）

```
1. 读取合并后的 JSON 中间产物（title + 全部 FRs + businessContext + dataFlows）
2. 确认 Demo 模式（A/B/C，见 §七）
   - A/B：先提取参考页的布局/样式特征
   - C：直接使用默认布局与样式
3. 判断界面形态（Dashboard / 列表+详情 / 流程 / 表单 / 地图）
4. 为每条 FR 设计对应的功能区：
   - 位置：按 uiLocation 确定在 Demo 中的区域
   - 数据：按 example 生成模拟数据（补充至饱满）
   - 交互：按 description 确定可交互行为
5. 组装单 HTML 文件：
   - <head> 中内联所有 CSS（参考页样式或 prototype-styles.md 默认样式）
   - <body> 中按"整体布局"组织业务界面 DOM
   - <script> 中（不用 type="module"，避免 file:// CORS）：
     a. Vue 已内联（全局 Vue）
     b. 注入 JSON 数据 + 模拟数据为 Vue 响应式数据
     c. 实现所有交互行为（筛选联动、卡片下钻、图表渲染）
     d. 图表用原生 SVG/Canvas 渲染，无需 Mermaid
6. 写入文件：{title}-demo.html（约 180–250KB，Vue 内联）
7. 验证：file:// 双击打开，确认各功能区正常显示、交互可用
```

---

## 九、单 HTML 文件模板骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<script>/* 内联 vue.global.prod.js 约 160KB，确保 file:// 双击即用 */</script>
<style>
  /* 内联 prototype-styles.md 的全部样式 */
</style>
</head>
<body class="theme-dark-blue">
<div id="app">
  <!-- 业务系统界面：Header + 统计卡片 + 中央主视区 + 筛选/明细 -->
</div>
<script>
  const DATA = {/* 注入的 JSON 中间产物 */};
  const MOCK = {/* 基于 example 生成的模拟数据 */};
  const { createApp, ref, computed } = Vue;
  createApp({
    setup() {
      // 将 FR 映射为业务功能区的响应式数据与交互逻辑
      return { /* ... */ };
    }
  }).mount('#app');
</script>
</body>
</html>
```

---

## 十、代码生成防坑规则

> 以下为 Demo 调试中暴露的"一次写对"问题，生成 Demo HTML 时必须逐项遵守。

| # | 坑 | 症状 | 规则 |
|---|----|------|------|
| 1 | `</script>` 转义 | `<\/script>` 导致浏览器把 `<style>` 和 `<body>` 当作 JS 解析，整页空白 | HTML 外层的 `</script>` 闭标签**必须写成 `</script>`**；仅 JS 字符串内的 `</script>` 才转义为 `<\/script>` |
| 2 | `type="module"` 在 `file://` 下被 CORS 拦截 | `file://` 双击打开时整页空白 | Demo 的应用脚本**必须用 `<script>`**（无 `type`），**禁止 `type="module"`** |
| 3 | `:class="{{ }}"` / `:style="{{ }}"` 错误绑定 | `Unexpected token '{'` → Vue 编译失败，整页空白蓝底 | `:` / `v-bind:` 绑定的属性**直接写 JS 表达式**：`:class="active ? 'a' : 'b'"` / `:style="{ width: val + '%' }"`，**禁止** `:class="{{ ... }}"` / `:style="{{ ... }}"`；`{{ }}` 仅用于文本插值 |
| 4 | Python f-string 与 Vue `{{ }}` 冲突 | `:style` 的 `{ }` 对象字面量被 f-string 误包进 `{{ }}`，导致同上 | **禁止用 Python f-string 直接生成含 Vue 模板的 HTML**；改用 `str.replace()` 占位符、`string.Template` 或独立模板文件；若必须用 f-string，`:style` / `:class` 的表达式部分用变量拼接而非内联 |
| 5 | CDN 依赖导致离线空白 | `file://` 或离线环境下整页空白 | Vue **必须内联**（~160KB）；图表用原生 SVG，不依赖 CDN |

### 生成后自检（写入文件前执行）

```python
# 1. script 标签匹配
assert html.count("<script") == html.count("</script>"), "script 开闭标签数量不一致"

# 2. 无 type="module"
assert 'type="module"' not in html, "禁止 type=module，file:// 下会被 CORS 拦截"

# 3. 无错误的 :class="{{"
import re
assert not re.search(r':\w+="\{\{', html), "存在 :class=\"{{  错误写法"

# 4. Vue 已内联
assert "<script>/*" in html or "vue.global" in html.lower(), "Vue 未内联"

# 5. 有业务内容（非需求展示页）
assert "stat-card" in html or "业务" in html, "Demo 应为业务系统界面，非需求卡片罗列"
```

---

## 十一、与 Markdown 文档的一致性

Demo HTML 和 Markdown 文档**同源渲染**（同一份 JSON 中间产物）：

```
JSON 中间产物
  ├──→ output-template.md 渲染 → {title}.md（需求文档：6段+5锚点+Mermaid）
  └──→ prototype-template.md + prototype-styles.md 渲染 → {title}-demo.html（业务系统前端原型）
```

**一致性保证**：

| 维度 | Markdown | Demo HTML |
|------|----------|-----------|
| FR 标题 | `### FR-1 浏览车站数统计` | 统计卡片标题"浏览车站数" |
| FR 描述 | `统计并展示...` | 卡片/表格/图表的功能行为 |
| FR example | `某日覆盖 9/13` | 卡片中的模拟数据"9/13  69%" |
| NFR | `首屏 ≤2秒` | Demo 首屏确实快速加载 |
| 优先级 | `high/medium/low` 徽标 | 卡片的视觉权重（高优更醒目） |

