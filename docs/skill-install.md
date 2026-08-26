# Scene Requirements Generator — 本地安装与使用说明

> Skill 名称：`scene-req-to-demo`
> 版本：v0.0.5 | 协议：MIT

> **v0.0.5 要点**：① 子系统识别（safety/ats/ctc/monitoring/iom/general）；② 安全苛求功能自动注入"安全功能阐述图"横幅/声明（安全系统无操作前端）；③ 双轨 Demo——约束版（两段式：上段需求范围视图+下段整体效果示意）+ 创意版（`build-creative.py` 组装并 `node --check` 冒烟）；④ FR 扩展字段 `safetyRelevance`/`acceptanceCriteria`；⑤ GAP 纪律（量化指标无依据标 `[假设]/[GAP]`）。详见 `skills/scene-req-to-demo/SKILL.md`。

---

## 一、安装

### 1.1 自动安装（推荐）

```bash
# 在项目根目录执行
./scripts/install-skill.sh
```

该脚本会将 skill 安装到所有兼容的 agent 目录：

| 目录 | 对应 Agent |
|------|-----------|
| `~/.agents/skills/scene-req-to-demo/` | Amp / 通用 |
| `~/.config/opencode/skills/scene-req-to-demo/` | Opencode |
| `~/.claude/skills/scene-req-to-demo/` | Claude Code |

> 三处通过 symlink 指向同一份文件，更新只需改一处。

### 1.2 手动安装

```bash
# 克隆或复制 skill 目录到任意一个兼容位置
cp -r scene-req-to-demo ~/.agents/skills/

# 如需多 agent 兼容，创建 symlink
ln -s ~/.agents/skills/scene-req-to-demo ~/.config/opencode/skills/scene-req-to-demo
ln -s ~/.agents/skills/scene-req-to-demo ~/.claude/skills/scene-req-to-demo
```

### 1.3 验证安装

```bash
# 检查主文件是否存在
ls ~/.agents/skills/scene-req-to-demo/SKILL.md
ls ~/.agents/skills/scene-req-to-demo/DESIGN.md  # 设计基准

# 检查多位置（应为 symlink，指向同一权威副本）
ls -la ~/.config/opencode/skills/scene-req-to-demo  # 软链 → ~/.agents/skills/scene-req-to-demo
ls -la ~/.workbuddy/skills/scene-req-to-demo        # 软链 → 同上
ls -la ~/.claude/skills/scene-req-to-demo           # 软链 → 同上
```

---

## 二、目录结构

```
scene-req-to-demo/
├── SKILL.md                              # 主文件：触发、7 步工作流、双轨输出
├── DESIGN.md                             # 设计基准（维护者用，防跑飞；非运行时）
├── README.md                             # 快速安装 + 产物说明 + 目录结构
└── assets/
    ├── analysis-prompt.md                 # 核心分析指令（LLM system prompt）
    ├── requirement-writing-guide.md       # 需求表述规范（5锚点 + 6段式）
    ├── output-template.md                 # Markdown 六段式输出模板（fallback）
    ├── verification-checklist.md          # 质量检查清单
    ├── domain-railway.md                  # 铁路信号领域：安全篇+非安全篇+三铁律（可选注入）
    ├── mermaid-rules.md                   # 图表类型选择 + 生成规则
    ├── prototype-domain-ui.md             # 四子系统分区拓扑 + 两段式说明 + 配色惯例
    ├── prototype-tech-inspiration.md      # 创意版技术灵感库（信息化）
    ├── prototype-template.md              # Demo 模板索引（Phase 4 入口）
    ├── prototype-template-detail.md       # 创意版布局细节（Phase 4b）
    ├── prototype-styles-tokens.md         # 设计 tokens（配色/组件变量）
    └── scripts/
        ├── README.md                      # 脚本契约 + JSON schema 单一事实源
        ├── analyze.py                     # Phase1 校验 + 子系统检测
        ├── validate-anchors.py            # Phase3 锚点/安全/GAP 校验
        ├── render-markdown.py             # Phase4 Markdown 渲染（+安全声明）
        ├── render-demo.py                 # Phase4 约束版渲染（两段式 + 安全横幅，CSS 内置）
        ├── build-creative.py              # Phase4b 创意版组装 + node --check
        ├── examples/sample.json
        └── vendor/vue.global.prod.js
```

---

## 三、使用

### 3.1 触发方式

在任意支持 skills 的 agent 对话中，输入包含以下关键词的请求即可自动触发：

```
场景描述 / 需求分析 / 需求文档 / 原型 / Demo
自然语言转需求 / 场景转需求 / 帮我分析这个场景
```

**示例**：

> "帮我分析这个场景：学生通过手机扫码解锁校园共享单车，骑行结束后上锁结算，管理员可以在后台管理单车和查看使用统计"

> "我需要一个需求文档：郑州地铁4号线需要在报警摘要处增加故障响应等级，按报警code配置显示内容"

### 3.2 能力范围

| 输入 | 输出 |
|------|------|
| 一段自然语言场景描述（中文，任意长度） | ① Markdown 六段式需求文档（安全场景自动加安全声明） |
| | ② 约束版 Demo HTML（两段式：需求范围视图+整体效果示意；安全场景为阐述图） |
| | ③ 创意版 Demo HTML（非安全子系统；子系统骨架+技术灵感，build-creative 组装+冒烟） |
| | ④ 结构化 JSON（含 Mermaid 代码） |

### 3.3 领域自动检测

当场景描述包含以下关键词时，自动注入铁路信号领域知识：

```
铁路 / 信号 / 联锁 / 进路 / 道岔 / 闭塞 / 轨道电路
CBTC / TACS / ZC / VOBC / DCS / OC / MA / 移动闭塞
地铁 / 城轨 / 调度 / 行车 / 列控 / SIL / T2T
```

注入后，分析会自动应用：术语表、联锁/列控规则、CBTC/TACS 规则、SIL 约束等。

### 3.4 LLM 后端

本 skill 定义"输入→输出"契约，不绑定具体 LLM。Agent 使用其可用的 LLM 调用 `assets/analysis-prompt.md` 中的 prompt：

| 后端 | 调用方式 |
|------|---------|
| Claude API | `analysis-prompt.md` 作为 system prompt + 场景作为 user message |
| OpenAI API | 同上，`temperature: 0.2, max_tokens: 4096, seed: 42` |
| Ollama | 同上，`http://localhost:11434/v1/chat/completions` |
| WebLLM | 同上，`engine.chat.completions.create()` |

推荐参数：`temperature: 0.2, top_p: 0.9, max_tokens: 4096, seed: 42`

---

## 四、输出说明

### 4.1 Markdown 需求文档（六段式）

```markdown
一、业务背景及目标（提出方/问题层级/现状/解决层级/预期成效）
二、总体需求（1 条 mainRequirement + 系统边界 + 干系人 + 三层需求）
三、功能需求（2–6 条 FR，每条含 5 锚点：位置/数据/配置/默认/示例 + safetyRelevance/acceptanceCriteria 扩展）
四、接口需求（有则列出，无则标"无"）
五、数据需求（有则列出，无则标"无"）
六、非功能性需求（标注硬性约束 vs 假设）
附录 A：Mermaid 流程图
附录 B：结构化 JSON
```

- **GAP 纪律**：量化指标无依据必须标 `[假设]/[GAP]`，禁止编造。
- 安全场景自动注入安全声明（Markdown）与阐述横幅（Demo）。

### 4.2 Demo HTML 原型（双轨）

**约束版**（`{标题}.html`，脚本确定性生成，两段式）：

- 单页面按子系统自动适配布局（safety→阐述图；非安全→上段需求范围视图 + 下段整体效果示意，不把需求硬铺满整页）
- 打开：双击用 Chrome/Edge 打开即可，无需任何构建（Vue 已内联，`file://` 双击即用）
- 主题：暗蓝工业风（`#0a1e3c` 基底 + 霓虹五色状态徽标）；响应式
- 交互：筛选联动、上段落位高亮/非范围标记、下段拟真模板（示意数据）

**创意版**（`{标题}-creative.html`，仅非安全子系统，LLM 自由发挥）：

- 专业下限按 `prototype-domain-ui.md` 子系统骨架；叠加 `prototype-tech-inspiration.md` 技术灵感
- 通过 `build-creative.py` 注入 Vue（占位符 `<!--__INJECT_VUE__-->`）并 `node --check` 冒烟测试（失败不产出）；中间 `*.tpl.html` 自动删除

### 4.3 结构化 JSON

标准的 JSON 对象，包含 `businessContext` + `requirements` + `mermaidCode`，可直接被程序消费或导入其他工具。详见 `SKILL.md` 的 Output Contract 章节。

---

## 五、卸载

```bash
# 删除主目录（symlink 会自动失效）
rm -rf ~/.agents/skills/scene-req-to-demo

# 如需彻底清理 symlink
rm ~/.config/opencode/skills/scene-req-to-demo
rm ~/.claude/skills/scene-req-to-demo
```

---

## 六、更新

```bash
# 覆盖安装（重新执行安装脚本）
./scripts/install-skill.sh

# 或手动覆盖
cp -r scene-req-to-demo/* ~/.agents/skills/scene-req-to-demo/
```

---

## 七、与 `requirements-analysis` 的配合

```
Step 1: requirements-analysis  → 诊断问题是否清晰（RA0–RA5）
Step 2: scene-req-to-demo → 生成需求文档 + Demo
```

如果场景描述非常模糊或以解决方案开头（"我想做一个..."），建议先用 `requirements-analysis` 澄清问题，再用本 skill 生成交付物。

---

## 八、常见问题

**Q: 为什么 agent 没有自动触发 skill？**
A: 确保你的描述包含触发关键词（场景描述/需求分析/需求文档等）。或显式说"使用 scene-req-to-demo 分析这个场景"。

**Q: 铁路领域知识没有生效？**
A: 确保场景描述中包含领域关键词（铁路/信号/CBTC/地铁等）。通用场景不会加载领域知识，这是正常的。

**Q: Demo HTML 打开是白屏？**
A: 需要 Chrome 113+ 且联网（CDN 加载 Vue+Mermaid）。检查浏览器控制台是否有 CDN 加载错误。

**Q: 输出的 FR 只有标题没有 5 锚点？**
A: 可能是 LLM 没有严格遵循 prompt。尝试换一个更大的模型（如 `claude-sonnet-4` 或 `gpt-4o`）或重试。

**Q: 支持英文场景吗？**
A: 当前 skill 的输出固定为中文。如需英文，可在场景描述后追加"请用英文输出"。
