# 原型样式参考 — Style Tokens Reference

> Demo 设计时使用：理解可用的视觉变量（Design Tokens）与组件样式清单。
> **约束版**：完整 CSS 已内置于 `assets/scripts/render-demo.py`（`DESIGN_TOKENS_CSS`），无需手动内联。
> **创意版**：LLM 以本文件的 tokens 为设计基准，自主编写样式。

## 一、Design Tokens

### 色板

```css
:root {
  /* === 背景 === */
  --bg-primary: #0a1e3c;          /* 主背景 — 深海蓝 */
  --bg-card: #132a4a;             /* 卡片背景 */
  --bg-card-hover: #1a3658;       /* 卡片悬停 */
  --bg-header: #0d2445;           /* 顶栏背景 */
  --bg-sidebar: #0e2a4e;          /* 侧边栏背景 */
  --bg-input: #1a3658;            /* 输入框背景 */

  /* === 边框 === */
  --border: #1e4a7a;              /* 常规边框 */
  --border-glow: 0 0 8px rgba(0, 212, 255, 0.3);  /* 发光边框 */
  --border-glow-strong: 0 0 16px rgba(0, 212, 255, 0.5);
  --border-card: 1px solid #1e4a7a;
  --border-card-glow: 1px solid rgba(0, 212, 255, 0.4);

  /* === 文字 === */
  --text-primary: #e0f0ff;        /* 主文字 — 淡蓝白 */
  --text-secondary: #7a9ab8;      /* 次要文字 — 灰蓝 */
  --text-muted: #4a6a8a;          /* 弱化文字 */
  --text-accent: #00d4ff;         /* 强调文字 — 霓虹青 */

  /* === 强调 === */
  --accent-cyan: #00d4ff;         /* 主强调 — 霓虹青 */
  --accent-blue: #007aff;         /* 辅助强调 — 亮蓝 */
  --accent-glow: 0 0 12px rgba(0, 212, 255, 0.4);

  /* === 状态色（五色徽标体系） === */
  --status-red: #ff3b30;          /* 故障 / 高优 */
  --status-red-bg: rgba(255, 59, 48, 0.15);
  --status-orange: #ff9500;       /* 风险 / 中优 */
  --status-orange-bg: rgba(255, 149, 0, 0.15);
  --status-yellow: #ffcc00;       /* 异常 */
  --status-yellow-bg: rgba(255, 204, 0, 0.15);
  --status-purple: #af52de;       /* 卡控 */
  --status-purple-bg: rgba(175, 82, 222, 0.15);
  --status-blue: #007aff;         /* 监督 / 低优 */
  --status-blue-bg: rgba(0, 122, 255, 0.15);
  --status-green: #34c759;        /* 正常 / 完成 */
  --status-green-bg: rgba(52, 199, 89, 0.15);

  /* === 功能色 === */
  --primary: #00d4ff;
  --primary-alpha: rgba(0, 212, 255, 0.1);
  --success: #34c759;
  --warning: #ff9500;
  --danger: #ff3b30;

  /* === 圆角 / 间距 / 阴影 === */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --gap-xs: 4px;
  --gap-sm: 8px;
  --gap-md: 16px;
  --gap-lg: 24px;
  --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.4);
  --shadow-glow: 0 0 20px rgba(0, 212, 255, 0.15);
}

/* === 亮色主题覆盖 === */
body.theme-light-blue {
  --bg-primary: #e8eef6;
  --bg-card: #ffffff;
  --bg-card-hover: #f0f5ff;
  --bg-header: #1a3a5c;
  --bg-sidebar: #1e4a6e;
  --border: #c5d9f0;
  --text-primary: #1a3248;
  --text-secondary: #5a7a96;
  --text-muted: #8a9ab0;
  --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.08);
}
```

---

---

## 组件样式清单

| 组件 | CSS 类 | 用途 |
|------|-------|------|
| Header | `.proto-header` / `.header-left` / `.header-right` | 顶栏标题与控件 |
| 12 列布局 | `.proto-main` / `.proto-sidebar` / `.proto-center` / `.proto-right` | Dashboard 三栏布局 |
| 卡片通用 | `.card` / `.card-title` | 通用内容卡片 |
| 三层需求 | `.layers-row` / `.layer-card` / `.layer-biz` / `.layer-user` / `.layer-sys` | BR/UR/SR 三层 |
| 总体需求 | `.main-req-card` / `.main-req-label` / `.main-req-name` / `.main-req-desc` | 蓝色发光边框主需求 |
| FR 卡片 | `.req-card` / `.req-h` / `.req-id` / `.priority-badge` / `.req-n` / `.req-d` / `.req-anchors` | 功能需求（带5锚点） |
| 统计卡片 | `.stat-card` / `.stat-card-label` / `.stat-card-value` | 数据卡片 |
| 图表 | `.diagram-box` / `.mermaid-svg` | 图表容器 |
| 代码编辑器 | `.editor-textarea` / `.editor-toolbar` | 内联代码编辑器 |
| 数据流/NFR | `.df-item` / `.nfr` | 列表 |
| 侧边导航 | `.nav-item` | 左栏导航 |
| 状态色 | `.status-red` / `.status-orange` / `.status-yellow` / `.status-purple` / `.status-blue` / `.status-green` | 五色状态徽标 |
| 主题 | `body.theme-dark-blue` / `body.theme-light-blue` | 暗色/亮色主题切换 |

---

## 引用方式

**约束版**：CSS 已内置于 `render-demo.py`，直接运行脚本即可，无需读本文件。
**创意版（Phase 4b）**：以本文件的 Design Tokens 为视觉基准，LLM 自主编写样式。
**Step 4（参考页）**：生成 `ref-styles.css` 覆盖 `:root` 变量时，参考本文件的变量名。
