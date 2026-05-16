# Changelog

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
