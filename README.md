# Scene Requirements to Demo

自然语言场景描述 → 结构化需求文档 + 业务系统前端原型（双轨 Demo）

主要面向**铁路轨道交通信号系统**（联锁/列控/ATS/CTC/监测/运维），也适用通用业务系统。

## 核心特性（v0.0.4）

- **子系统识别**：`analyze.py` 自动判定 `safety / ats / ctc / monitoring / iom / general`，驱动领域规则与 Demo 布局
- **安全标记**：安全苛求功能（联锁/防护类）**自动**在 Demo 注入"安全功能阐述图·实际安全系统无操作前端界面"横幅，Markdown 注入安全声明
- **双轨 Demo**：约束版（脚本统一布局，评审用）+ 创意版（按子系统界面骨架 + 信息化技术灵感，启发用；`build-creative.py` 注入 Vue 并 `node --check` 冒烟测试）
- **GAP 纪律**：量化指标无依据必须标 `[假设]/[GAP]`，防编造
- **FR 扩展**：5 锚点 + `safetyRelevance` + `acceptanceCriteria`

## 快速安装

### Claude Code

```bash
cp -r scene-req-to-demo ~/.claude/skills/        # 全局
cp -r scene-req-to-demo .claude/skills/          # 或项目级
```

### OpenCode

```bash
ln -sf $(pwd)/scene-req-to-demo ~/.agents/skills/scene-req-to-demo
ln -sf $(pwd)/scene-req-to-demo ~/.config/opencode/skills/scene-req-to-demo
```

### Amp / 其他

```bash
ln -sf $(pwd)/scene-req-to-demo ~/.config/amp/skills/scene-req-to-demo
```

将整个目录复制到 agent 的 skill 目录即可。

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
├── run.sh / standalone.sh          # 一键/独立执行
├── assets/
│   ├── scripts/
│   │   ├── analyze.py              # Phase 1 校验 + 子系统检测
│   │   ├── validate-anchors.py     # Phase 3 锚点/安全/GAP 校验
│   │   ├── render-markdown.py      # Phase 4 Markdown 渲染（+安全声明）
│   │   ├── render-demo.py          # Phase 4 约束版渲染（+安全横幅）
│   │   ├── build-creative.py       # Phase 4b 创意版组装 + node --check
│   │   ├── README.md               # 脚本契约 + JSON schema 单一事实源
│   │   ├── examples/sample.json
│   │   └── vendor/vue.global.prod.js
│   ├── analysis-prompt.md          # 核心分析指令
│   ├── requirement-writing-guide.md# FR 表述规范
│   ├── output-template.md          # Markdown 模板（fallback）
│   ├── verification-checklist.md   # 质量检查清单
│   ├── domain-railway.md           # 铁路领域：安全篇 + 非安全篇 + 三条铁律
│   ├── prototype-domain-ui.md      # 四子系统界面传统（创意版骨架）
│   ├── prototype-tech-inspiration.md# 信息化技术灵感库（创意版）
│   ├── prototype-template*.md      # Demo 布局（slim + detail）
│   ├── prototype-styles-*.md       # 样式（tokens + css）
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

- 当前版本：**v0.0.4**
- v0.0.4：子系统识别 / 安全标记自动注入 / build-creative 冒烟 / FR 扩展字段 / GAP 纪律 / 领域拆分安全篇+非安全篇 / 创意版灵感库
- 更新日志见 git log
