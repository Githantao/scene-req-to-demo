# Changelog

## v1.0.0 (2026-05-16)

### 新增
- Mermaid 代码编辑器 + 实时预览：分析结果下方显示可编辑的 Mermaid 源码框，修改后 600ms 自动重渲染
- 需求分层展示（BR→UR→SR）：输出包含业务层（🏢 目标与价值）、用户层（👤 场景与痛点）、系统层（⚙️ 职责概述）三层架构
- 导出 Markdown：一键导出包含完整需求分层、功能列表、数据流、Mermaid 图标的 Markdown 文档
- Mermaid 代码复制按钮

### 改进
- System Prompt 全面升级：融入三层需求模型（BR/UR/SR）

## v0.2.0 (2026-05-16)

### 改进
- System Prompt 全面升级：
  - 需求分析规则：区分"需要什么" vs "怎么做"，检查每条需求的可测试性
  - 非功能性需求区分硬性约束与假设
  - Mermaid 生成规则：subgraph 分组、emoji 节点、%% 注释
- 引用 SkillsBot mermaid-generator、jwynia/requirements-analysis、softaworks/mermaid-diagrams 三个 skill 的最佳实践

### 安装的 Agent Skills
- `jwynia/agent-skills@requirements-analysis` — 需求质量诊断框架
- `softaworks/agent-toolkit@mermaid-diagrams` — mermaid 图表生成最佳实践

## v0.1.0 (2026-05-16)

### 新增
- 初始化项目：场景需求分析器
- Vue 3 + Vite + TypeScript 工程（`npm run dev` / `npm run build`）
- 单 HTML 文件版本 `analyzer.html`（可直接用 Chrome 打开）
- WebLLM 浏览器本地推理（支持 Qwen2.5-1.5B / Gemma-2-2B / Phi-3-mini）
- 自然语言 → 结构化系统需求（JSON + Markdown）
- Mermaid 流程图自动生成
- 模型下载进度展示 + 缓存管理（清除/查看）
- 历史记录（localStorage 持久化）
- WebGPU 不可用时自动检测并提示解决方案
- 首次使用欢迎引导页
- 跨系统模型缓存复制指引

### 技术栈
- 前端：Vue 3 + Vite + TypeScript
- WebLLM：@mlc-ai/web-llm (v0.2.83)
- 图表：mermaid.js (v11)
- CDN（纯净版）：jsdelivr
