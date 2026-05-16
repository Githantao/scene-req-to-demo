# 场景需求分析器

自然语言场景描述 → 结构化系统需求 + Mermaid 流程图

一个完全在浏览器本地运行的 AI 工具。输入自然语言描述的业务场景，自动提取结构化的系统需求（功能需求、数据流、约束条件），并生成可视化的 Mermaid 流程图。所有数据处理都在本地完成，数据不会离开你的电脑。

## 核心架构

```
┌─────────────────────────────────────────────────────────────┐
│                     用户输入场景描述                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    WebLLM 浏览器本地推理                      │
│  (Qwen2.5-1.5B / Gemma-2-2B / Phi-3-mini)                  │
│                                                             │
│  [System Prompt: 需求分析 + Mermaid 生成规则]                  │
│      ┌──────────────────────────────────────┐                │
│      │ JSON 输出：                              │                │
│      │  layers: { business, user, system }   │                │
│      │  systemBoundary                        │                │
│      │  functionalRequirements[]               │                │
│      │  dataFlows[]                            │                │
│      │  mermaidCode                            │                │
│      └──────────────────────────────────────┘                │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
           ┌─────────────┴─────────────┐
           ▼                           ▼
┌─────────────────────┐   ┌─────────────────────────┐
│  需求报告（左栏）      │   │  Mermaid 流程图（右栏）    │
│  ┌─────────────────┐│   │  ┌─────────────────────┐│
│  │ 🏢 业务层        ││   │  │  rendered SVG       ││
│  │ 👤 用户层        ││   │  ├─────────────────────┤│
│  │ ⚙️ 系统层        ││   │  │ 代码编辑器 textarea  ││
│  │ 系统边界         ││   │  │ (600ms 自动重渲染)    ││
│  │ 功能需求 FR-*    ││   │  └─────────────────────┘│
│  │ 数据流           ││   └─────────────────────────┘
│  │ 非功能需求       ││
│  └─────────────────┘│
└─────────────────────┘
```

## 版本形式

本项目提供两种使用方式：

### 1. 单 HTML 文件（推荐跨平台使用）

`analyzer.html` — 一个完整的 HTML 文件，用 Chrome 打开即可使用。

```
下载 analyzer.html → 双击用 Chrome 打开 → 加载模型 → 使用
```

无需安装任何运行时环境，模型首次下载后自动缓存到 IndexedDB，后续可离线使用。

### 2. Vue 3 + Vite 工程

完整的 Vue 3 + TypeScript 项目，适合二次开发和定制。

```bash
npm install        # 安装依赖
npm run dev        # 启动开发服务器（默认 :5173）
npm run build      # 构建到 dist/
```

## 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 前端框架 | Vue 3 (Composition API) | 3.x |
| 构建工具 | Vite | 8.x |
| 类型系统 | TypeScript | 5.x |
| AI 推理引擎 | @mlc-ai/web-llm | 0.2.83 |
| 图表渲染 | mermaid.js | 11.x |
| CDN（纯净版） | jsdelivr | — |

## 支持的 LLM 模型

| 模型 | 大小 | 说明 |
|------|------|------|
| Qwen2.5-1.5B | ~1GB | 中文能力强，速度较快，推荐 |
| Gemma-2-2B | ~1.5GB | 结构化输出稳定 |
| Phi-3-mini-3.8B | ~2.5GB | 能力最强，但加载慢 |

## V1 功能清单

- **自然语言 → 结构化需求** — 输入场景描述，自动提取系统需求
- **三层需求展示（BR→UR→SR）** — 业务层（🏢 目标与价值）、用户层（👤 场景与痛点）、系统层（⚙️ 职责概述）
- **Mermaid 流程图自动生成** — 用 subgraph、emoji、决策菱形等最佳实践
- **Mermaid 代码编辑器** — 实时编辑 + 600ms 防抖自动重渲染
- **导出 Markdown** — 一键导出完整需求文档
- **模型管理** — 下拉切换模型、下载进度、缓存查看/清除
- **历史记录** — localStorage 持久化，上限 50 条
- **WebGPU 检测** — 自动检测环境并给出解决方案
- **首次引导** — 首次使用欢迎页 + 模型下载指引
- **缓存复制指引** — 提供跨机器复制模型缓存的方法

## 参考材料

本项目参考了以下资料的设计理念和实践：

- **Three-Layer Requirements Model (BR/UR/SR)** — 业务需求、用户需求、系统需求三层方法论
- **FFAB Analysis Framework** (Feature, Function, Advantage, Benefit)
- **Jobs-to-be-Done** 需求发现方法
- **SkillsBot mermaid-generator** — Mermaid 图表生成的提示工程最佳实践
- **jwynia/requirements-analysis** (1.9K installs) — 需求质量诊断框架（已安装到 `~/.agents/skills/requirements-analysis/`）
- **softaworks/mermaid-diagrams** (4K installs) — Mermaid 图表语法参考（已安装到 `~/.agents/skills/mermaid-diagrams/`）
- **Mermaid.js 官方文档** — https://mermaid.js.org/

## System Prompt

核心提示词位于：

- `analyzer.html` — 内联在 HTML 中的 `SYSTEM_PROMPT` 常量
- `src/utils/prompt.ts` — Vue 工程中的 TypeScript 版本

Prompt 结构：
```
1. JSON 输出格式定义（含三层需求字段）
2. 需求分析规则（可测试性、区分"需要什么"vs"怎么做"）
3. Mermaid 生成规则（subgraph、emoji 节点、决策菱形）
```

## 浏览器要求

- 需要 **Chrome 113+** 或 **Edge 113+**（WebGPU 支持）
- 从 `file://` 打开需要启用 `chrome://flags/#enable-unsafe-webgpu` 或通过 HTTP 服务
- 推荐：`python3 -m http.server 8080` → `http://localhost:8080/analyzer.html`
