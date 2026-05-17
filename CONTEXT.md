# 场景需求分析器 — 项目记忆文档

> 此文件记录项目的需求设计、参考资料、架构决策和 Bug 修复历史。
> 用于 AI agent 跨会话恢复上下文。每次重大变更后更新。

---

## 一、项目概述

**一句话：** 自然语言场景描述 → 结构化系统需求 + Mermaid 流程图

**核心价值：** 纯浏览器本地运行，数据不离机，无需后端服务。支持跨平台（Mac/Windows），单 HTML 文件打开即用。

**用户场景：**
- 产品经理快速将想法落地为结构化需求文档
- 架构师将业务场景转化为系统设计输入
- 开发者理解业务需求并生成流程图

---

## 二、需求规格

### 2.1 核心功能

| ID | 功能 | 优先级 | 状态 |
|----|------|--------|------|
| FR-1 | 自然语言 → 结构化需求提取 | P0 | ✅ v0.1.0 |
| FR-2 | Mermaid 多图表类型生成（流程图/时序图/类图/状态图/ERD） | P0 | ✅ v2.0.0 |
| FR-3 | 三层需求展示 (BR→UR→SR) | P1 | ✅ v1.0.0 |
| FR-4 | Mermaid 代码编辑器 + 实时预览 | P1 | ✅ v1.0.0 |
| FR-5 | 导出 Markdown | P1 | ✅ v1.0.0 |
| FR-6 | 国内镜像下载源 | P1 | ✅ v1.1.0 |
| FR-7 | 多轮追问细化需求 | P2 | 📋 待开发 |
| FR-8 | Ollama 后端支持（绕过 WebGPU） | P2 | 📋 待开发 |
| FR-9 | 对比模式（两个场景并排对比）| P2 | 📋 待开发 |
| FR-10 | 导出 PNG | P2 | 📋 待开发 |

### 2.2 非功能需求

| NFR | 说明 | 状态 |
|-----|------|------|
| NFR-1 | 纯前端，无后端依赖 | ✅ |
| NFR-2 | WebGPU 浏览器本地推理 | ✅ |
| NFR-3 | 模型离线缓存（IndexedDB） | ✅ |
| NFR-4 | 跨平台（Chrome Mac/Win） | ✅ |
| NFR-5 | 单 HTML 文件分发（无需构建） | ✅ |
| NFR-6 | 国内网络可用（镜像源） | ✅ v1.1.0 |

### 2.3 输出 JSON 结构

```json
{
  "requirements": {
    "title": "系统名称",
    "layers": {
      "business": { "goal": "业务目标", "value": "业务价值" },
      "user": { "scenario": "用户场景", "painPoints": ["痛点"] },
      "system": { "summary": "系统职责" }
    },
    "mainRequirement": {
      "name": "总体需求名称",
      "description": "对该需求的概括描述"
    },
    "systemBoundary": "系统边界",
    "stakeholders": ["干系人"],
    "functionalRequirements": [
      { "id": "FR-1", "name": "子功能名", "description": "描述（必须可测试）", "priority": "high|medium|low" }
    ],
    "dataFlows": [
      { "from": "来源", "to": "目标", "data": "数据描述", "type": "input|output|storage" }
    ],
    "nonFunctionalRequirements": ["硬性约束 / 假设"]
  },
  "mermaidCode": "flowchart TD\n  ..."
}
```

### 2.4 System Prompt 设计

提示词结构（`analyzer.html` / `src/utils/prompt.ts`）：
1. JSON 输出格式定义（含三层需求字段 + `mainRequirement` 总体需求）
2. 需求分析规则：
   - 先识别 1 条核心/总体需求（mainRequirement），再拆解为子 FR
   - 区分"需要什么"（outcome）vs "怎么做"（implementation）
   - 每条需求必须可测试（隐式验收条件）
   - mainRequirement 恰 1 条，functionalRequirements 2-6 条
3. Mermaid 生成规则：
   - 节点命名固定格式 [动词+名词]，每次相同概念复用相同命名
   - 流程图结构固定顺序：输入 → 核心处理 → 分支决策 → 输出
   - subgraph 按阶段分组（输入阶段/处理阶段/输出阶段）
   - 决策菱形最多 3 个分支
   - 根据场景自动选择最佳图表类型（flowchart/sequenceDiagram/classDiagram/stateDiagram-v2/erDiagram）
   - `%%` 注释说明复杂逻辑
4. FR 粒度规则（v2.1.0）：
   - 每个 FR 代表一个**完整的业务能力**（如"用户登录认证"），而非 UI 操作步骤（如"显示登录页"）
   - 粒度控制在**系统分析层面**，实现阶段的细化拆分留给后续迭代
5. 生成质量增强：
   - **RaR 语义对齐** — 用户 prompt 要求"深入理解场景"后再分析
   - **CoVe 条件验证** — 复杂场景自动触发二次验证
   - **seed=42** — API 请求体传入 `seed:42` 使输出更稳定确定
   - ⚠️ `response_format: {type:'json_object'}` 已验证不兼容 Qwen2.5-1.5B，已移除

---

## 三、技术架构

### 3.1 架构图

```
用户输入场景 → WebLLM 浏览器推理（System Prompt）
  ├─ JSON 解析器（容错：code block / brace extraction）
  ├─ 渲染器
  │   ├─ 左栏：需求报告（三层卡片 + FR/DF/NFR）
  │   ├─ 右栏：Mermaid SVG（mermaid.js 渲染）
  │   └─ 代码编辑器（暗色文本框 + 600ms debounce 重渲染）
  └─ 持久化
      ├─ 历史记录（localStorage，上限 50 条）
      └─ 模型缓存（Cache API + IndexedDB）
```

### 3.2 推理参数配置

`engine.chat.completions.create()` 传入以下参数控制生成行为：

| 参数 | 值 | 理由 |
|------|-----|------|
| temperature | 0.2 | 结构化需求提取需要确定性输出；Qwen 官方推荐 0.1-0.3 结构化任务 |
| top_p | 0.9 | 保持适度多样性但不发散 |
| max_tokens | 4096 | Mermaid 代码 + 中文描述容易超 2048 |

### 3.3 技术栈

| 组件 | 技术 | 版本 |
|------|------|------|
| 前端框架 | Vue 3 (Composition API) | 3.x |
| 构建工具 | Vite | 8.x |
| 类型系统 | TypeScript | 6.x |
| AI 推理引擎 | @mlc-ai/web-llm | 0.2.83 |
| 图表渲染 | mermaid.js | 11.x |
| CDN（纯净版） | jsdelivr | — |

### 3.4 两种交付形态

1. **单 HTML 文件** `analyzer.html` — CDN 加载 Vue + Mermaid + WebLLM，双击 Chrome 打开即用
2. **Vue + Vite 工程** — `npm run dev` / `npm run build`，适合二次开发

### 3.5 模型支持

| 模型 ID（v0.2.83） | 标签 | 大小 | 说明 |
|---------------------|------|------|------|
| `Qwen2.5-1.5B-Instruct-q4f16_1-MLC` | Qwen2.5-1.5B | ~1GB | 中文能力最强，推荐 |
| `gemma-2-2b-it-q4f16_1-MLC` | Gemma-2-2B | ~1.5GB | 结构化输出稳定 |
| `Phi-3-mini-4k-instruct-q4f16_1-MLC` | Phi-3-mini-3.8B | ~2.5GB | 能力最强，加载慢 |

> ⚠️ 模型 ID 没有 `-1` 后缀（v0.2.83）。
> 镜像源使用 `hf-mirror.com`（经测试 CORS 正确）。

#### 镜像模型记录（硬编码）

```javascript
const MODEL_LIBS = {
  'Qwen2.5-1.5B-Instruct-q4f16_1-MLC':
    'https://raw.githubusercontent.com/mlc-ai/binary-mlc-llm-libs/main/web-llm-models/v0_2_83/base/Qwen2-1.5B-Instruct-q4f16_1_cs1k-webgpu.wasm',
  // ... 其他模型类似
};
```

> 镜像模式下`model_lib`（WASM，~5MB）走 GitHub raw（已确认 CORS 正确），
> `model`（权重，~1-2.5GB）走 hf-mirror.com。

---

## 四、参考材料

### 4.1 已安装的 Agent Skills

| Skill | 安装量 | 用途 |
|-------|--------|------|
| `jwynia/agent-skills@requirements-analysis` | 1.9K | 需求质量诊断框架（5 种问题状态） |
| `softaworks/agent-toolkit@mermaid-diagrams` | 4.0K | Mermaid 图表语法深度参考 |
| `davila7/claude-code-templates@mermaid-diagram-specialist` | 501 | Mermaid 图表类型选择与创建工作流 |

路径：`~/.agents/skills/requirements-analysis/` 和 `~/mermaid-diagrams/`

### 4.2 参考资料

- **三层需求模型** BR→UR→SR（业务/用户/系统），来自知乎文章（403 无法直接访问，搜索结果可见内容）
- **FFAB 分析框架** (Feature, Function, Advantage, Benefit)
- **Jobs-to-be-Done** 需求发现方法
- **SkillsBot mermaid-generator** — Mermaid 图表生成的提示工程最佳实践
- **Mermaid.js 官方文档** — https://mermaid.js.org/

---

## 五、开发历史 & Bug 记录

### v0.1.0 — 项目初始化

**新增：**
- Vue 3 + Vite + TS 工程脚手架
- `analyzer.html` 单文件版本
- WebLLM 浏览器本地推理
- 基础 System Prompt（单层需求输出）
- Mermaid 流程图生成
- 模型下载进度 + 缓存管理
- 历史记录（localStorage）
- WebGPU 检测 + 首次引导

### v0.2.0 — Prompt 升级 + Skills 安装

**新增：**
- System Prompt 融入需求分析规则 + Mermaid 最佳实践
- 安装 `requirements-analysis` + `mermaid-diagrams` skills

**参考：**
- SkillsBot mermaid-generator 页面（skillsbot.cn/skill/12496）

### Bug #1: Mermaid 渲染错误（\n 解析失败）

**症状：** `Parse error on line 1: flowchart TD\n  A[节点A]... — Expecting 'NEWLINE'`

**原因：** 模型输出的 Mermaid 代码中 `\n` 是字面字符串而非换行符。JS 单引号字符串中的 `\\\\n` 产生了 `\\n`（3 字符）→ LLM 收到后混淆。应为 `\\n`（2 字符）产生 `\n` 作为 JSON 换行转义。

**修复：**
1. System Prompt 中的 Mermaid 示例改用正确的 `\\n`（JS 中 = `\n` 2 字符）
2. `renderMermaid()` 加入 `code.replace(/\\n/g, '\n')` 容错

**关联文件：** `analyzer.html`、`src/components/MermaidDiagram.vue`、`src/utils/prompt.ts`

---

### Bug #2: WebGPU 闪退（file:// 不可用）

**症状：** Chrome 直接打开 `file://` 时，点击"开始下载"弹窗立即关闭，无实际下载

**原因：** Chrome 在 `file://` 协议下禁用 WebGPU（需要安全上下文）

**修复：**
1. 检测 `navigator.gpu`，不存在时显示黄色警告横幅
2. 提供两个解决方案：`python3 -m http.server 8080` 或 `chrome://flags/#enable-unsafe-webgpu`

**关联文件：** `analyzer.html`

---

### v1.0.0 — 编辑器 + 三层展示 + 导出

**新增：**
- Mermaid 代码编辑器（暗色 textarea + 600ms debounce 自动重渲染）
- 三层需求展示（🏢 业务层 → 👤 用户层 → ⚙️ 系统层）
- 导出 Markdown（Blob download）

**Prompt 改进：**
- 输出加入 `layers` 字段

**关联文件：** `analyzer.html`、`src/components/MermaidDiagram.vue`、`src/components/RequirementsReport.vue`、`src/utils/parser.ts`

---

### Bug #3: 模型下载弹窗闪退（WebGPU 检测先于按钮点击发生）

**症状：**（间接修复随 #2 一起）

---

### v2.0.0 — 多图表类型支持

**改进：**
- System Prompt 全面升级：加入 5 种图表类型选择规则，根据场景内容自动选择最合适的图表类型
- 输出 schema 新增 `diagramType` 字段
- 移除 flowchart-only 限制，`validateMermaid` 接受所有合法 mermaid 语法
- 新增 `generateFallbackMermaid(title, type)` 根据类型生成降级图表
- UI 新增图表类型徽标（蓝色标签显示当前类型）
- 版本信息展示：标题栏 v2.0.0 版本号 + 更新说明弹窗
- 安装 `davila7/claude-code-templates@mermaid-diagram-specialist` (501 安装量)

**图表选择规则：**
- 多方交互/API/消息传递 → sequenceDiagram
- 状态流转/审批/生命周期 → stateDiagram-v2
- 数据实体/表结构 → erDiagram
- 类/模块/接口/继承 → classDiagram
- 纯步骤流程 → flowchart

**关联文件：** `analyzer.html`、`src/utils/prompt.ts`、`src/utils/parser.ts`、`src/types/index.ts`、`src/components/RequirementsReport.vue`

---

### Bug #7: response_format 导致引擎挂起（10+ 分钟无结果）

---

### v2.2.0 — 主需求 + Mermaid 稳定性 + 实时计时 + 历史用时

**新增：**
- `mainRequirement` 字段：先提炼 1 条总体需求，再拆解为子 FRs
- 蓝色边框卡片在 FR 区域顶部展示总体需求
- Markdown 导出包含总体需求章节
- 实时分析计时器：分析中 header 显示累计用时（每秒更新）
- WebLLM 分析时显示"分析中... (用时)"
- 历史记录条目追加分析用时徽标

**Prompt 改进：**
- System Prompt 添加 `mainRequirement` JSON 格式定义
- 分析规则重排：先识别总体需求再拆解为子 FR
- Mermaid 生成规则重写：固定节点命名格式 [动词+名词]、流程图固定顺序（输入→处理→决策→输出）、subgraph 按阶段分组、决策分支上限 3 条

**API 稳定性：**
- `seed: 42` 添加到所有 API 请求体（`analyzer.html` apiCompletion + Vue `useApiLLM.ts` chat/chatRaw）
- `ApiLLMConfig` 类型新增 `seed?: number`

**Bug 修复：**
- WebLLM 分析时 header 无状态提示 → 现在显示"模型名 分析中... (累计用时)"
- 历史记录不显示分析用时 → 现在显示

**关联文件：**
- `analyzer.html` — SYSTEM_PROMPT, parseOutput, apiCompletion 添加 seed, 模板 mainRequirement 卡片 + 历史用时 + 实时计时 setInterval, CSS main-req-card + hist-tm, modelStatusText 支持 analyzing 状态
- `src/utils/prompt.ts` — 更新规则
- `src/utils/parser.ts` — 解析 mainRequirement
- `src/types/index.ts` — 新增 MainRequirement 接口, HistoryEntry 添加 analysisTime, ApiLLMConfig 添加 seed
- `src/composables/useApiLLM.ts` — chat/chatRaw 添加 seed:42
- `src/composables/useAnalysis.ts` — 实时计时 setInterval/clearInterval, reset 清理计时器
- `src/components/RequirementsReport.vue` — 模板+样式 mainRequirement 卡片
- `src/components/HistoryPanel.vue` — 分析用时徽标
- `src/App.vue` — modelStatusText 支持 analyzing 状态, 历史保存传入 analysisTime, 导出 MD 含总体需求

---

### v2.1.0 — (嵌入式在 2.4 System Prompt 中) FR 粒度 + RaR/CoVe

---

## 六、已知限制

| 限制 | 说明 | 计划 |
|------|------|------|
| WebGPU 依赖 | 需要 Chrome/Edge 113+ | 考虑 Ollama 后端支持 (P2) |
| CDN 网络依赖 | `analyzer.html` 首次需从 jsdelivr 加载 6MB | 不可消除（WebLLM 必须） |
| 模型下载大 | 首次需下载 1-2.5GB | 提供缓存复制指引 |
| Safari 不支持 | WebGPU 不可用 | 跟进 Safari WebGPU 支持 |
| 单轮对话 | 无法追问细化需求 | 多轮对话 (P2) |

---

## 七、环境与工具链

- Node.js 25.9.0, npm 11.12.1, Bun 1.3.14
- macOS (开发)/Windows (目标)
- Chrome 113+ (目标浏览器)

### 关键命令

```bash
npm run dev        # 开发服务器 :5173
npm run build      # 生产构建到 dist/
npm run build && npx serve dist  # 构建并本地预览
npx skills find    # 搜索 agent skills
```

### git 历史摘要

```
2ac7ccb feat: v2.0.0 多图表类型支持
01a240b fix: 模型加载失败问题修复 (v1.1.x)
dcd916f feat: v1.1.0 国内镜像下载源 + 打包使用文档
2a4bc92 docs: 完整项目文档 v1.0.0
44c7b35 feat: v1.0.0 Mermaid 编辑器、三层需求展示、导出 Markdown
f61177e feat: v0.2.0 升级 System Prompt
b9d2d06 feat: 场景需求分析器 v0.1.0
```

---

## 八、AI 工作指引

### 下一个开发方向（按优先级）

1. **多轮追问** — 对已生成的需求结果进一步追问细化
   - 需要维护对话历史（chat completions messages 数组）
   - UI：追加输入框 + "追问"按钮
2. **Ollama 后端支持** — 绕过 WebGPU 限制，支持更多平台
   - 增加 API 配置页面，支持自定义 endpoint
   - 复用现有 prompt/parser/UI 逻辑
3. **导出 PNG** — 使用 html2canvas 将流程图导出为图片
4. **对比模式** — 两个场景分析结果并排对比

### 常见文件修改模式

- **修改 prompt** → `analyzer.html` 中 `SYSTEM_PROMPT` 常量 + `src/utils/prompt.ts`
- **修改解析逻辑** → `analyzer.html` 中 `parseOutput()` + `src/utils/parser.ts`
- **修改 UI** → `analyzer.html` 中 Vue template + 对应 Vue 组件 (`src/components/`)
- **修改 WebLLM 集成** → `analyzer.html` 中 `loadModel/chat` 函数 + `src/composables/useWebLLM.ts`
- **修改分析流程（analyzer.html）** → `analyze()` 函数含 RaR + CoVe 逻辑；`isComplexScene()` / `coveVerify()` 辅助函数
- **修改分析流程（Vue）** → `src/composables/useAnalysis.ts` 含 `isComplexScene()` / 条件 CoVe；`src/App.vue` 传入 `chatRawFn`
- **修改镜像/模型配置** → `analyzer.html` 中 `MODEL_OPTIONS` + `MODEL_LIBS`
- **测试数据集** → `docs/test-dataset-railway-signal.md`

### 修改后必须验证

1. `npm run build` — TypeScript 检查 + Vite 构建通过
2. `analyzer.html` — 浏览器打开，欢迎页正常，模型加载/分析流程可用
