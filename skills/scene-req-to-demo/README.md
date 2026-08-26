# Scene Requirements to Demo

自然语言场景描述 → 结构化需求文档 + 业务系统前端原型

## 快速安装

### Claude Code

```bash
# 全局安装（所有项目可用）
cp -r scene-req-to-demo ~/.claude/skills/

# 或项目级安装
cp -r scene-req-to-demo .claude/skills/
```

### OpenCode

```bash
# 全局安装
ln -sf $(pwd)/scene-req-to-demo ~/.agents/skills/scene-req-to-demo

# 或 OpenCode 原生目录
ln -sf $(pwd)/scene-req-to-demo ~/.config/opencode/skills/scene-req-to-demo
```

### Amp

```bash
ln -sf $(pwd)/scene-req-to-demo ~/.config/amp/skills/scene-req-to-demo
```

### 手动安装（任何 agent）

将整个 `scene-req-to-demo` 目录复制到 agent 的 skill 目录即可。

## 使用方式

### 方式 A：Agent 自动触发（推荐）

在对话中直接描述场景，agent 会自动加载 skill 并执行 pipeline：

```
帮我分析场景：综合看板中央区域显示管辖图&数据分析图，管辖图根据用户确定显示内容，数据分析图显示用户层级所辖设备的运用次数统计。
```

### 方式 B：手动执行

如果 agent 不自动触发，手动运行：

```bash
# 1. 准备 JSON（参考 SKILL.md 中的 schema，保存为 ./output/merged.json）
# 2. 运行 pipeline
python3 assets/scripts/analyze.py < ./output/merged.json
python3 assets/scripts/validate-anchors.py < ./output/merged.json
python3 assets/scripts/render-markdown.py --output-dir ./output < ./output/merged.json
python3 assets/scripts/render-demo.py --output-dir ./output < ./output/merged.json
# 创意版由 LLM 自由生成 → ./output/<标题>-creative.html
```

## 产物

| 产物 | 路径 | 说明 |
|------|------|------|
| Markdown 需求文档 | `./output/<标题>.md` | 6 段式结构化需求 |
| 约束版 Demo | `./output/<标题>.html` | 脚本生成，暗蓝工业风 |
| 创意版 Demo | `./output/<标题>-creative.html` | LLM 自由生成，双轨对比 |

## 目录结构

```
scene-req-to-demo/
├── SKILL.md              # Agent 指令（自包含，4.6KB）
├── run.sh                # 一键执行脚本
├── assets/
│   ├── scripts/
│   │   ├── analyze.py          # Phase 1 验证
│   │   ├── validate-anchors.py # Phase 3 锚点验证
│   │   ├── render-markdown.py  # Phase 4 Markdown 渲染
│   │   ├── render-demo.py      # Phase 4 Demo HTML 渲染
│   │   ├── README.md           # 完整 JSON schema 参考
│   │   ├── examples/sample.json # 参考样例
│   │   └── vendor/vue.global.prod.js
│   ├── mermaid-rules.md        # Mermaid 图表规则
│   ├── domain-railway.md       # 铁路领域知识
│   └── prototype-styles-*.md   # 前端样式参考
└── README.md              # 本文件
```

## 依赖

- Python 3+（仅标准库：json, sys, re, datetime, pathlib）
- 无 npm/pip 依赖

## 适配状态

| Agent | 状态 | 说明 |
|-------|------|------|
| Claude Code | ✅ | 原生 skill 支持，自动触发 |
| OpenCode | ⚠️ | skill 内容可加载，但 agent 可能不自动执行 Bash |
| Amp | ⚠️ | 待验证 |
| 其他 | 📋 | 参考 SKILL.md 手动执行 |

## 版本

- 当前版本：v0.0.3
- 更新日志见 git log
