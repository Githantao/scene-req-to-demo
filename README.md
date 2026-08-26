# Scene-Req-to-Demo

> **自然语言场景描述 → 结构化需求文档 + 业务系统前端原型**

[![Version](https://img.shields.io/badge/version-v0.0.3-blue)](./VERSION)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Skill](https://img.shields.io/badge/skill-scene--req--to--demo-orange)](./skills/scene-req-to-demo/SKILL.md)

面向**铁路轨道交通信号系统**的场景需求分析与原型生成工具。输入一段自然语言描述的业务场景，自动生成可评审、可开发、可测试的结构化需求文档和可交互的业务系统前端原型。

---

## 适用领域

| 领域 | 典型场景 | 领域知识 |
|------|----------|----------|
| 🚃 轨道交通信号 | 联锁/进路/道岔、CBTC/TACS、调度集中 | `domain-railway.md` 自动注入 |
| 📊 运营监测 | 设备健康、故障分级、大屏看板 | 通用 + 铁路运营补充 |
| 🔧 通用业务系统 | 任意 CRUD/看板/流程类系统 | 通用分析（不加载领域知识） |

> 命中关键词`铁路/信号/CBTC/TACS/联锁/进路`等时，自动注入铁路信号领域知识（术语、SIL 约束、降级模式等）；未命中时保持通用分析的简洁性。

---

## 核心能力：Agent Skill `scene-req-to-demo`

### 一句话

自然语言场景描述 → 六段式需求文档 + 暗蓝工业风可交互 Demo + 结构化 JSON（含 Mermaid 图）

### Pipeline

```
场景描述 → JSON 分析(5 锚点 + 安全标注) → 子系统检测 → 批量确认 → 参考页面(可选) → 校验 → 双轨 Demo
                                                                                    ├─ 约束版(脚本生成)
                                                                                    └─ 创意版(骨架+灵感, build-creative 组装)
```

- 每条 FR 含 5 锚点（`uiLocation`/`dataSource`/`configurable`/`defaultState`/`example`）+ `safetyRelevance` + `acceptanceCriteria`
- **子系统识别**：`analyze.py` 判定 `safety/ats/ctc/monitoring/iom/general`，驱动领域规则与 Demo 布局
- **安全标记**：安全苛求功能自动在 Demo 注入"安全功能阐述图"横幅、Markdown 注入安全声明（安全系统无操作前端）
- 双轨 Demo：约束版（两段式：需求范围视图 + 整体效果示意，评审用）+ 创意版（子系统界面骨架 + 信息化技术灵感，启发用）
- 单页面承载所有 FR（非每 FR 一 Tab）；Tab 仅用于视图切换（如管辖图↔数据分析图）
- **GAP 纪律**：量化指标无依据必须标 `[假设]/[GAP]`，防编造

### 安装

```bash
./scripts/install-skill.sh          # 安装到所有兼容的 agent 目录
./scripts/install-skill.sh --force  # 覆盖已安装版本
```

详见 [本地安装与使用说明](docs/skill-install.md)。

### 触发

在任意支持 skills 的 agent 对话中输入以下任一关键词即可自动触发：

`场景描述` / `需求分析` / `分析以下场景` / `交接班` / `看板` / `填报` / `查询` / `原型生成`

详见 [`skills/scene-req-to-demo/SKILL.md`](skills/scene-req-to-demo/SKILL.md)。

### 输出

| 产物 | 路径 | 说明 |
|------|------|------|
| Markdown 需求文档 | `./output/<标题>.md` | 六段式；安全场景自动加安全声明 |
| 约束版 Demo | `./output/<标题>.html` | 脚本生成，暗蓝工业风；安全场景自动加阐述横幅 |
| 创意版 Demo | `./output/<标题>-creative.html` | 非安全子系统；子系统骨架+技术灵感，build-creative 组装+冒烟 |
| 结构化 JSON | `./output/<标题>.json` + `merged.json` | 含 Mermaid 代码，可编程消费 |

---

## 浏览器本地推理：`analyzer.html`

> Skill 之外的独立能力：纯浏览器本地运行，无需后端服务。

`analyzer.html` — 单 HTML 文件，用 Chrome 打开即可使用。基于 WebLLM（Qwen2.5-1.5B / Gemma-2B / Phi-3-mini）在浏览器内完成需求分析和 Mermaid 图生成，数据不离机。

```
下载 analyzer.html → 双击用 Chrome 打开 → 加载模型 → 使用
```

无需安装任何运行时环境，模型首次下载后自动缓存到 IndexedDB，后续可离线使用。

### Vue 3 + Vite 工程

完整的 Vue 3 + TypeScript 项目，适合二次开发：

```bash
npm install        # 安装依赖
npm run dev        # 启动开发服务器（默认 :5173）
npm run build      # 构建到 dist/
```

### 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 前端框架 | Vue 3 (Composition API) | 3.x |
| 构建工具 | Vite | 8.x |
| 类型系统 | TypeScript | 5.x |
| AI 推理引擎 | @mlc-ai/web-llm | 0.2.83 |
| 图表渲染 | mermaid.js | 11.x |
| CDN（纯净版） | jsdelivr | — |

### 支持的 LLM 模型

| 模型 | 大小 | 说明 |
|------|------|------|
| Qwen2.5-1.5B | ~1GB | 中文能力强，速度较快，推荐 |
| Gemma-2-2B | ~1.5GB | 结构化输出稳定 |
| Phi-3-mini-3.8B | ~2.5GB | 能力最强，但加载慢 |

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v0.0.5 | 2026-08-26 | 约束版 Demo 两段式：**上段需求范围视图**（子系统整体架构，FR 语义落位高亮，空区标"非本次需求范围"）+ **下段整体效果示意**（全分区生产级拟真，数据标"示意"）；分区拓扑按 ATS/CTC/集中监测/智能运维标准化系统调研；去除国铁"段/车间/工班"硬编码层级；安全检测信任显式标注防误判；find helper 补 WorkBuddy 路径 |
| v0.0.4 | 2026-08-26 | 子系统识别 / 安全标记自动注入 / build-creative 冒烟 / FR 扩展字段 / GAP 纪律 / 领域拆分安全篇+非安全篇 / 创意版灵感库 |
| v0.0.3 | 2026-08-26 | Skill 双轨 Demo / MUST ASK 流程 / 铁路领域知识 / 业务系统原型重构 |
| v0.0.1 | 2026-06-04 | Skill 初版：场景→需求→Demo 基础链路 |
| v2.x | 2026-06 | analyzer.html 多图表类型 / 铁路信号增强 / 布局优化 |

---

## 参考材料

- **Three-Layer Requirements Model (BR/UR/SR)** — 业务需求、用户需求、系统需求三层方法论
- **FFAB Analysis Framework** (Feature, Function, Advantage, Benefit)
- **Jobs-to-be-Done** 需求发现方法
- **CBTC/TACS 信号系统** — 铁路轨道交通信号领域知识

## 浏览器要求

- 需要 **Chrome 113+** 或 **Edge 113+**（WebGPU 支持）
- `file://` 打开需启用 `chrome://flags/#enable-unsafe-webgpu` 或通过 `python3 -m http.server 8080` 启动

## 国内镜像支持

模型文件默认从 HuggingFace 下载。国内用户可在模型选择器下方将下载源切换为**国内镜像**（hf-mirror.com）。

## 打包与跨电脑使用

详见 [CONTEXT.md](CONTEXT.md) 及 `analyzer.html` 内的使用指引。
