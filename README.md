# Scene Requirements to Demo

自然语言场景描述 → 结构化需求文档 + 业务系统前端原型（双轨 Demo）

主要面向**铁路轨道交通信号系统**（联锁/列控/ATS/CTC/监测/运维），也适用通用业务系统。

## 核心特性（v0.0.5）

- **子系统识别**：`analyze.py` 自动判定 `safety / ats / ctc / monitoring / iom / general`，驱动领域规则与 Demo 布局
- **安全标记**：安全苛求功能（联锁/防护类）**自动**在 Demo 注入"安全功能阐述图·实际安全系统无操作前端界面"横幅，Markdown 注入安全声明
- **双轨 Demo**：约束版（两段式：需求范围视图+整体效果示意，评审用）+ 创意版（按子系统界面骨架 + 信息化技术灵感，启发用；`build-creative.py` 注入 Vue 并 `node --check` 冒烟测试）
- **GAP 纪律**：量化指标无依据必须标 `[假设]/[GAP]`，防编造
- **FR 扩展**：5 锚点 + `safetyRelevance` + `acceptanceCriteria`

## 快速安装（推荐：git clone，无缝升级）

```bash
# 安装（文件夹名稳定为 scene-req-to-demo）
git clone https://github.com/Githantao/scene-req-to-demo.git ~/.agents/skills/scene-req-to-demo
ln -sf ~/.agents/skills/scene-req-to-demo ~/.config/opencode/skills/scene-req-to-demo

# 升级到新版本（原地，不产生新文件夹）
git -C ~/.agents/skills/scene-req-to-demo pull
```

> 其他 agent：把 `~/.agents/skills/scene-req-to-demo` **软链**（推荐，勿用复制）到对应 skill 目录：
> ```bash
> ln -sf ~/.agents/skills/scene-req-to-demo ~/.workbuddy/skills/scene-req-to-demo   # WorkBuddy
> ln -sf ~/.agents/skills/scene-req-to-demo ~/.claude/skills/scene-req-to-demo       # Claude Code
> ln -sf ~/.agents/skills/scene-req-to-demo ~/.config/amp/skills/scene-req-to-demo   # Amp
> ```
> ⚠️ **务必用软链、保持单一权威副本**。若某处是独立的实体副本，升级时会漂移成旧版——而 SKILL.md 的 find helper 会优先命中第一个找到的副本，导致跑到旧脚本、出旧布局（这是 v0.0.5 修复过的坑）。

### 不用 git？下载 Release 资产

从 Release 页下载 **`scene-req-to-demo.zip`**（Assets），解压即稳定的 `scene-req-to-demo/` 目录，覆盖旧安装即可。

> ⚠️ 不要下载 GitHub 自动生成的 "Source code (zip)"——它带 `-版本号` 后缀，每次升级产生新文件夹，无法无缝覆盖。

## 使用方式

### 方式 A：Agent 自动触发（推荐）

直接描述场景，agent 自动加载并执行（含两次必问：批量确认 + 参考页面）：

```
分析以下场景需求：综合看板中央区域显示管辖图&数据分析图，管辖图根据用户确定显示内容。
```

### 方式 B：手动执行

```bash
python3 assets/scripts/analyze.py < ./output/merged.json            # 校验+子系统检测
python3 assets/scripts/validate-anchors.py < ./output/merged.json   # 锚点/安全/GAP 校验
python3 assets/scripts/render-markdown.py --output-dir ./output < ./output/merged.json
python3 assets/scripts/render-demo.py --output-dir ./output < ./output/merged.json
# 创意版（非安全子系统）：
python3 assets/scripts/build-creative.py \
  --input ./output/<标题>-creative.tpl.html --output ./output/<标题>-creative.html
```

## 产物

| 产物 | 路径 | 说明 |
|------|------|------|
| Markdown 需求文档 | `./output/<标题>.md` | 6 段式；安全场景自动加安全声明 |
| 约束版 Demo | `./output/<标题>.html` | 脚本生成；安全场景自动加阐述横幅 |
| 创意版 Demo | `./output/<标题>-creative.html` | 非安全子系统；build-creative 组装+冒烟 |

## 目录结构

```
scene-req-to-demo/
├── SKILL.md                        # Agent 指令（主入口，含 Asset Loading Strategy）
├── DESIGN.md                       # 需求设计基准（维护者用，防跑飞；非运行时资产）
├── assets/
│   ├── scripts/
│   │   ├── analyze.py              # Phase 1 校验 + 子系统检测
│   │   ├── validate-anchors.py     # Phase 3 锚点/安全/GAP 校验
│   │   ├── render-markdown.py      # Phase 4 Markdown 渲染（+安全声明）
│   │   ├── render-demo.py          # Phase 4 约束版渲染（两段式 + 安全横幅，CSS 内置）
│   │   ├── build-creative.py       # Phase 4b 创意版组装 + node --check + 清理 tpl
│   │   ├── README.md               # 脚本契约 + JSON schema 单一事实源
│   │   ├── examples/sample.json
│   │   └── vendor/vue.global.prod.js
│   ├── analysis-prompt.md          # 核心分析指令
│   ├── requirement-writing-guide.md# FR 表述规范
│   ├── output-template.md          # Markdown 模板（fallback）
│   ├── verification-checklist.md   # 质量检查清单
│   ├── domain-railway.md           # 铁路领域：安全篇 + 非安全篇 + 三条铁律
│   ├── prototype-domain-ui.md      # 四子系统分区拓扑 + 两段式说明 + 配色惯例
│   ├── prototype-tech-inspiration.md# 信息化技术灵感库（创意版）
│   ├── prototype-template.md       # Demo 模板索引
│   ├── prototype-template-detail.md# 创意版布局细节
│   ├── prototype-styles-tokens.md  # 设计 tokens（配色/组件变量）
│   └── mermaid-rules.md            # 图表规则
└── README.md                       # 本文件
```

## 依赖

- Python 3+（仅标准库）
- 创意版冒烟测试需 `node`（无 node 时降级跳过并告警）

## 适配状态

| Agent | 状态 | 说明 |
|-------|------|------|
| Claude Code | ✅ | 原生 skill 支持，自动触发 |
| OpenCode | ✅ | skill 自动加载（`skills.paths`），命令 `/scene-req-to-demo` 可用 |
| Amp | ⚠️ | 待验证 |
| 其他 | 📋 | 参考 SKILL.md 手动执行 |

## 版本

- 当前版本：**v0.0.5**
- v0.0.5：子系统识别 / 安全标记自动注入 / build-creative 冒烟 / FR 扩展字段 / GAP 纪律 / 领域拆分安全篇+非安全篇 / 创意版灵感库
- 更新日志见 git log
