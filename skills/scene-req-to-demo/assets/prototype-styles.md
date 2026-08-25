# 原型样式规范 — Industrial Dark-Blue Design Tokens

> 本文件定义 Demo HTML 的全部视觉规范。
> 基于 CASCO 大屏（3 张截图 + 2 份 HTML）的工业级暗蓝设计语言提炼。
> 在 `prototype-template.md` 的单 HTML 中以内联 `<style>` 形式使用。

---

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

## 二、全局样式

```css
* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
               'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
  font-size: 14px;
}

a { color: var(--accent-cyan); text-decoration: none; }
a:hover { text-decoration: underline; }

/* 滚动条 — 暗色主题 */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
```

---

## 三、Header — 标题栏

```css
.proto-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: var(--bg-header);
  border-bottom: 1px solid var(--border);
  box-shadow: var(--shadow-glow);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.header-left h1 {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
}

.ver-badge {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  background: var(--bg-card);
  padding: 1px 6px;
  border-radius: 3px;
  border: 1px solid var(--border);
}

.diagram-badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  background: var(--accent-cyan);
  color: #001a2e;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-right button {
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-secondary);
  transition: all 0.15s;
}

.header-right button:hover {
  background: var(--bg-card-hover);
  color: var(--text-primary);
  border-color: var(--accent-cyan);
  box-shadow: var(--border-glow);
}

.header-right button.btn-primary {
  background: var(--accent-cyan);
  color: #001a2e;
  border-color: var(--accent-cyan);
  font-weight: 600;
}

.header-right button.btn-primary:hover {
  filter: brightness(1.1);
  box-shadow: var(--accent-glow);
}
```

---

## 四、主布局 — 12 列网格

```css
.proto-main {
  display: grid;
  grid-template-columns: 200px 1fr 280px;
  gap: 16px;
  padding: 16px;
  max-width: 1600px;
  margin: 0 auto;
}

@media (max-width: 1199px) {
  .proto-main { grid-template-columns: 1fr 260px; }
  .proto-sidebar { display: none; }
}

@media (max-width: 768px) {
  .proto-main { grid-template-columns: 1fr; }
  .proto-sidebar, .proto-right { display: none; }
}

.proto-center { min-width: 0; }
.proto-sidebar { /* 侧边导航 */ }
.proto-right { /* 右侧面板 */ }
```

---

## 五、卡片 — 通用

```css
.card {
  background: var(--bg-card);
  border: var(--border-card);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: var(--shadow-card);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.card:hover {
  border-color: rgba(0, 212, 255, 0.3);
  box-shadow: var(--shadow-glow);
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.card-title::before {
  content: "▦";
  color: var(--accent-cyan);
  font-size: 12px;
}

/* 折叠卡片 */
.card-collapsible .card-title {
  cursor: pointer;
  user-select: none;
}

.card-collapsible .card-title:hover {
  color: var(--text-primary);
}

.collapse-icon {
  font-size: 10px;
  width: 12px;
  text-align: center;
}
```

---

## 六、三层需求卡片

```css
.layers-row {
  display: flex;
  align-items: stretch;
  gap: 8px;
  margin-bottom: 20px;
}

@media (max-width: 600px) {
  .layers-row { flex-direction: column; }
  .layer-arrow { transform: rotate(90deg); justify-content: center; }
}

.layer-card {
  flex: 1;
  border-radius: var(--radius-md);
  padding: 12px;
  display: flex;
  gap: 10px;
  align-items: flex-start;
}

.layer-biz {
  background: rgba(0, 122, 255, 0.12);
  border: 1px solid rgba(0, 122, 255, 0.3);
}

.layer-user {
  background: rgba(52, 199, 89, 0.1);
  border: 1px solid rgba(52, 199, 89, 0.3);
}

.layer-sys {
  background: rgba(255, 204, 0, 0.08);
  border: 1px solid rgba(255, 204, 0, 0.3);
}

.layer-icon { font-size: 20px; line-height: 1; }

.layer-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  opacity: 0.6;
  margin-bottom: 2px;
}

.layer-title {
  font-size: 13px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.layer-desc {
  font-size: 11px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.layer-arrow {
  display: flex;
  align-items: center;
  color: var(--text-muted);
  font-size: 18px;
  padding: 0 2px;
}
```

---

## 七、总体需求卡片（发光边框）

```css
.main-req-card {
  border: 1px solid var(--accent-cyan);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 16px;
  background: rgba(0, 212, 255, 0.06);
  box-shadow: var(--border-glow);
}

.main-req-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--accent-cyan);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.main-req-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 6px;
}

.main-req-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}
```

---

## 八、功能需求卡片（含 5 锚点）

```css
.req-card {
  border: var(--border-card);
  border-radius: var(--radius-md);
  padding: 14px;
  margin-bottom: 10px;
  background: var(--bg-card);
  cursor: pointer;
  transition: all 0.15s;
}

.req-card:hover {
  border-color: rgba(0, 212, 255, 0.4);
  background: var(--bg-card-hover);
}

.req-h {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.req-id {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent-cyan);
  font-family: 'SF Mono', Menlo, Monaco, monospace;
}

.priority-badge {
  font-size: 10px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 3px;
}

.priority-badge.high {
  background: var(--status-red-bg);
  color: var(--status-red);
  border: 1px solid rgba(255, 59, 48, 0.3);
}

.priority-badge.medium {
  background: var(--status-orange-bg);
  color: var(--status-orange);
  border: 1px solid rgba(255, 149, 0, 0.3);
}

.priority-badge.low {
  background: var(--status-blue-bg);
  color: var(--status-blue);
  border: 1px solid rgba(0, 122, 255, 0.3);
}

.req-n {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
}

.req-d {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
}

.btn-fr-copy {
  font-size: 11px;
  padding: 2px 8px;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
}

.btn-fr-copy:hover {
  background: var(--bg-card-hover);
  color: var(--text-primary);
}

/* 5 锚点展开区 */
.req-anchors {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.anchor-row {
  display: flex;
  gap: 10px;
  font-size: 12px;
  line-height: 1.5;
}

.anchor-label {
  font-weight: 600;
  color: var(--text-secondary);
  white-space: nowrap;
  min-width: 90px;
}

.anchor-value {
  color: var(--text-primary);
  flex: 1;
}
```

---

## 九、Mermaid 图表区

```css
.diagram-box {
  background: #ffffff;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  padding: 16px;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  overflow: auto;
}

.diagram-box svg {
  max-width: 100%;
  height: auto;
  display: block;
}

.diagram-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e8eef6;
}

.dia-select {
  font-size: 12px;
  padding: 4px 8px;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--bg-card);
  color: var(--text-primary);
  cursor: pointer;
}

/* Mermaid 错误 */
.merr {
  border: 1px solid rgba(255, 59, 48, 0.3);
  background: var(--status-red-bg);
  border-radius: var(--radius-md);
  padding: 12px;
  width: 100%;
}

.merr-t {
  font-size: 13px;
  font-weight: 600;
  color: var(--status-red);
  margin: 0 0 6px;
}

.merr-d {
  font-size: 12px;
  color: var(--status-red);
  white-space: pre-wrap;
  margin: 0;
}
```

---

## 十、代码编辑器

```css
.code-editor { margin-top: 12px; }

.editor-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.editor-label {
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.editor-hint {
  font-size: 11px;
  color: var(--accent-cyan);
  font-style: italic;
}

.editor-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: #0d1a2e;
  color: #c0d8f0;
  font-family: 'SF Mono', Menlo, Monaco, 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.6;
  resize: vertical;
  min-height: 100px;
  tab-size: 2;
}

.editor-textarea:focus {
  outline: none;
  border-color: var(--accent-cyan);
  box-shadow: var(--border-glow);
}
```

---

## 十一、数据流 / NFR 列表

```css
.df-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}

.df-item:last-child { border-bottom: none; }
.df-s, .df-t { font-weight: 500; color: var(--text-primary); }
.df-a { color: var(--accent-cyan); }
.df-d { color: var(--text-secondary); flex: 1; }

.nfr { margin: 0; padding-left: 20px; }
.nfr li {
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin-bottom: 4px;
}
```

---

## 十二、侧边导航

```css
.proto-sidebar {
  position: sticky;
  top: 60px;
  align-self: start;
}

.nav-item {
  padding: 8px 12px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 6px;
  border-left: 2px solid transparent;
  transition: all 0.15s;
}

.nav-item:hover {
  color: var(--text-primary);
  background: var(--bg-card);
}

.nav-item.active {
  color: var(--accent-cyan);
  background: var(--primary-alpha);
  border-left-color: var(--accent-cyan);
}
```

---

## 十三、空状态 / 提示

```css
.empty-msg {
  font-size: 13px;
  color: var(--text-muted);
  font-style: italic;
  text-align: center;
  padding: 20px;
}
```

---

## 十四、Footer

```css
.proto-footer {
  text-align: center;
  padding: 16px;
  font-size: 11px;
  color: var(--text-muted);
  border-top: 1px solid var(--border);
  margin-top: 16px;
}
```
