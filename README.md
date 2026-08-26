# scene-req-to-demo

> **自然语言场景描述 → 结构化需求文档 + 业务系统前端原型**

[![Version](https://img.shields.io/badge/version-v0.0.3-blue)](./SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green)](#license)

面向**铁路轨道交通信号系统**的场景需求分析与原型生成工具。输入一段自然语言描述的业务场景，自动生成可评审、可开发、可测试的结构化需求文档和可交互的业务系统前端原型。

---

## 适用领域

| 领域 | 典型场景 | 领域知识 |
|------|----------|----------|
| 🚃 轨道交通信号 | 联锁/进路/道岔、CBTC/TACS、调度集中 | `domain-railway.md` 自动注入 |
| 📊 运营监测 | 设备健康、故障分级、大屏看板 | 通用 + 铁路运营补充 |
| 🔧 通用业务系统 | 任意 CRUD/看板/流程类系统 | 通用分析 |

> 命中关键词`铁路/信号/CBTC/TACS/联锁/进路`等时，自动注入铁路信号领域知识；未命中时保持通用分析的简洁性。

---

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
ln -sf $(pwd)/scene-req-to-demo ~/.agents/skills/scene-req-to-demo
ln -sf $(pwd)/scene-req-to-demo ~/.config/opencode/skills/scene-req-to-demo
```

### Amp

```bash
ln -sf $(pwd)/scene-req-to-demo ~/.config/amp/skills/scene-req-to-demo
```

## 使用方式

### 方式 A：Agent 自动触发（推荐）

在对话中直接描述场景，agent 会自动加载 skill 并执行 pipeline：

```
帮我分析场景：综合看板中央区域显示管辖图&数据分析图，管辖图根据用户确定显示内容，数据分析图显示用户层级所辖设备的运用次数统计。
```

触发关键词：`场景描述` / `需求分析` / `分析以下场景` / `交接班` / `看板` / `填报` / `查询` / `原型生成`

### 方式 B：手动执行

```bash
python3 assets/scripts/analyze.py < ./output/merged.json
python3 assets/scripts/validate-anchors.py < ./output/merged.json
python3 assets/scripts/render-markdown.py --output-dir ./output < ./output/merged.json
python3 assets/scripts/render-demo.py --output-dir ./output < ./output/merged.json
```

## 产物

| 产物 | 路径 | 说明 |
|------|------|------|
| Markdown 需求文档 | `./output/<标题>.md` | 六段式结构化需求 |
| 约束版 Demo | `./output/<标题>.html` | 脚本生成，暗蓝工业风 |
| 创意版 Demo | `./output/<标题>-creative.html` | LLM 自由生成，双轨对比 |

详见 [SKILL.md](./SKILL.md) 完整 pipeline（含批量确认、参考页面、双轨 Demo）。

## Pipeline

```
场景描述 → JSON 分析(含 5 锚点 FR) → 批量确认 → 参考页面(可选) → 校验 → 双轨 Demo
                                                                    ├─ 约束版(脚本生成)
                                                                    └─ 创意版(LLM 自由生成)
```

## 目录结构

```
scene-req-to-demo/
├── SKILL.md              # Agent 指令（164 行，自包含）
├── README.md             # 本文件
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
```

## 版本

| 版本 | 日期 | 说明 |
|------|------|------|
| v0.0.3 | 2026-08-26 | 双轨 Demo / MUST ASK 流程 / 铁路领域定向 / 业务系统原型重构 |
| v0.0.2 | 2026-08-25 | 拆分大文件，55% 上下文节省 |
| v0.0.1 | 2026-08-25 | 初版发布 |

## License

MIT
