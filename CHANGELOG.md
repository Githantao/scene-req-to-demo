# Changelog

## v2.6.0 (2026-06-04)

### 改进
- **输入区自动压缩** — 分析完成后场景描述 `.card` 自动折叠为一条窄栏，释放垂直空间给需求报告和流程图区域
- **一键展开** — 压缩态显示场景文本预览（前 80 字符）+「展开」按钮，点击恢复完整编辑器，可重新编辑后再次分析
- **历史恢复同步压缩** — 从历史记录恢复结果时同样自动压缩输入区

### 关联文件
- `analyzer.html` — 新增 collapseInput ref、模板折叠/展开态切换、CSS 压缩态样式（`.card-collapsed`/`.input-compact`），analyze()/restoreEntry() 自动折叠逻辑

## v2.5.0 (2026-05-28)

### 改进
- **设置面板支持 WebLLM 模型管理** — 设置中选择 WebLLM 后端后，可直接选择模型、切换下载源（自动/国内镜像）、下载/加载/卸载模型、查看进度和缓存
- **国内镜像下载优化** — 模型权重（1-2.5GB）走 `hf-mirror.com` 镜像加速；WASM 库（~5MB）直连 GitHub raw 无需代理
- **loadModel 镜像源适配** — 根据 `mirrorSource` 自动切换模型权重源（auto→huggingface.co / china→hf-mirror.com）
- **设置面板 UI 改进** — 状态徽标（圆点颜色指示 idle/ready/error）、迷你进度条、缓存大小显示、操作按钮

### 修复
- **[FIX] raw.gitmirror.com DNS 不可用** — 移除不可达的镜像域名，WASM 库改为始终直连 `raw.githubusercontent.com`
- **[FIX] loadModel auto 模式不传 appConfig** — 避免自定义 model_list 覆盖 WebLLM 内置默认配置导致下载失败

### 关联文件
- `analyzer.html` — 设置面板新增 WebLLM 管理区（模型选择、下载源、下载按钮、进度条、缓存管理），MODEL_LIBS 恢复单一直链，loadModel 只对 china 模式传 appConfig，CSS 新增 as-radio-sm/as-pb/as-spinner-xs 等样式

## v2.4.0 (2026-05-27)

### 修复
- **WebGPU 不可用时用户被阻挡** — 当浏览器不支持 WebGPU（如 file:// 协议、Safari 等），WebGPU 警告栏和欢迎页均被隐藏导致用户处于空状态
- **WebLLM CDN 加载失败导致白屏** — 顶层 import catch 块用 `document.body.innerHTML` 覆盖页面，用户丢失 API 后端入口

### 改进
- **一键跳过 WebLLM** — WebGPU 警告栏新增「跳过 WebLLM，使用第三方 API」按钮，点击后自动切换至 API 后端并弹出设置面板
- **欢迎页直通 API** — 欢迎页底部新增相同跳转入口，CDN 加载失败时同样可跳过
- **saveSettings 自动绕过欢迎页** — 在设置中保存 API 后端配置时自动关闭欢迎页/警告
- **CDN 加载失败优雅处理** — 不再硬覆盖页面，保持 `CreateMLCEngine` 为 undefined，后续 `loadModel()` 友好提示切换后端

### 关联文件
- `analyzer.html` — WebGPU 警告栏/欢迎页新增 skipToApi 按钮，新增 skipToApi/skipToApiSettings 函数，saveSettings 增加欢迎页绕过逻辑，loadModel 增加 CDN 缺失检测，移除 CDN import catch 的 `document.body.innerHTML`

## v2.0.0 (2026-05-16)

### 新增
- **多图表类型支持** — 根据场景内容自动选择最佳图表类型：流程图（默认）、时序图（sequenceDiagram）、类图（classDiagram）、状态图（stateDiagram-v2）、ER 图（erDiagram）
- **图表类型徽标** — 结果页面流程图标题旁显示蓝色类型标签
- **版本信息展示** — 页面标题栏显示当前版本号，右侧"更新说明"按钮查看版本历史

### 改进
- **System Prompt** 全面升级：加入 5 种图表类型选择规则，根据场景语义自动匹配
- **输出 schema** 新增 `diagramType` 字段
- **parser.ts** 移除 flowchart-only 限制，`validateMermaid` 接受所有合法 mermaid 语法
- **analyzer.html** 与 Vue 组件同步更新

### 已安装的 Agent Skills
- `davila7/claude-code-templates@mermaid-diagram-specialist` — Mermaid 图表类型选择与创建工作流 (501 安装量)

## v1.1.0 (2026-05-16)

### 新增
- **国内镜像下载源** — 模型选择器增加"自动 / 国内镜像"切换，国内用户选择"国内镜像"后模型权重从 hf-mirror.com、WASM 库从 raw.gitmirror.com 下载

### 改进
- **README 文档** — 新增打包与跨电脑使用章节（3 种方式）、国内镜像支持说明
- **Vue 工程** — useWebLLM 支持镜像源配置，ModelSelector.vue 镜像切换

## v1.0.0 (2026-05-16)

### 新增
- **Mermaid 代码编辑器 + 实时预览** — 流程图下方显示可编辑源码框，修改代码后 600ms 自动重渲染，所见即所得
- **三层需求展示（BR→UR→SR）** — 输出现在包含业务层（🏢 业务目标与价值）、用户层（👤 使用场景与痛点）、系统层（⚙️ 系统职责概述），需求脉络一目了然
- **导出 Markdown** — 一键导出包含完整需求分层、功能列表、数据流、Mermaid 图标的 Markdown 文档
- **复制 Mermaid 代码** — 一键复制流程图源码

### 改进
- System Prompt 融入三层需求模型（BR/UR/SR）

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
