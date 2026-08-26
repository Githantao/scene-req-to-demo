# Scene Requirements Generator — 本地安装与使用说明

> Skill 名称：`scene-req-to-demo`
> 版本：v0.0.3 | 协议：MIT

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
ls ~/.agents/skills/scene-req-to-demo/assets/ | wc -l
# 应输出 8（7 个资产文件 + 可能的额外文件）

# 检查多位置
ls -la ~/.config/opencode/skills/scene-req-to-demo  # 应为 symlink
ls -la ~/.claude/skills/scene-req-to-demo            # 应为 symlink
```

---

## 二、目录结构

```
scene-req-to-demo/
├── SKILL.md                              # 主文件：触发、工作流、三重输出
└── assets/
    ├── analysis-prompt.md                 # 核心分析指令（LLM system prompt）
    ├── domain-railway.md                  # 铁路信号领域知识（可选，需关键词触发）
    ├── mermaid-rules.md                   # 图表类型选择 + 生成规则
    ├── output-template.md                 # Markdown 六段式输出模板
    ├── requirement-writing-guide.md       # 需求表述规范（5锚点 + 6段式）
    ├── prototype-template.md              # Demo HTML 原型模板 + 构建指南
    ├── prototype-styles.md               # 暗蓝工业风样式规范
    └── verification-checklist.md          # 质量验证清单
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
| 一段自然语言场景描述（中文，任意长度） | ① Markdown 六段式需求文档 |
| | ② 可交互 Demo HTML（暗蓝工业风，单文件） |
| | ③ 结构化 JSON（含 Mermaid 代码） |

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
三、功能需求（2–6 条 FR，每条含 5 锚点：位置/数据/配置/默认/示例）
四、接口需求（有则列出，无则标"无"）
五、数据需求（有则列出，无则标"无"）
六、非功能性需求（标注硬性约束 vs 假设）
附录 A：Mermaid 流程图
附录 B：结构化 JSON
```

### 4.2 Demo HTML 原型

- **文件**：`{系统名称}-demo.html`（单文件，~50KB）
- **打开**：双击用 Chrome/Edge 打开即可，无需任何构建
- **依赖**：CDN 加载 `vue@3` + `mermaid@11`（jsdelivr）
- **主题**：暗蓝工业风（`#0a1e3c` 基底 + 霓虹五色状态徽标）
- **交互**：卡片折叠、FR 锚点展开、图表类型切换、Mermaid 实时编辑、主题切换、导出 Markdown
- **布局**：12 列网格，响应式（大屏三栏 → 平板两栏 → 手机单栏）

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
